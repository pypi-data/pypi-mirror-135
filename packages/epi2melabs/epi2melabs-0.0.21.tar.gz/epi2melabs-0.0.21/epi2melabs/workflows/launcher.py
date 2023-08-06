# flake8: noqa
import os
import json
import signal
import shutil
import requests
import shortuuid
import subprocess
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import quote_plus
from nf_core.schema import PipelineSchema
from jsonschema.validators import validator_for
from typing import Callable, Dict, TypedDict, Union, Tuple, List
from epi2melabs.workflows.database import Statuses, get_session, Instance


class LauncherException(Exception):

    def __init__(self, message):
        super(LauncherException, self).__init__(message)


class Path(TypedDict):
    name: str
    path: str
    updated: float
    dir: bool


@dataclass
class Workflow:
    url: str
    name: str
    desc: str
    path: str
    target: str
    schema: Dict
    defaults: Dict

    def to_dict(self):
        return {
            'url': self.url,
            'name': self.name,
            'desc': self.desc,
            'path': self.path,
            'target': self.target,
            'schema': self.schema,
            'defaults': self.defaults}


class WorkflowLauncher(object):
    MAINNF: str = 'main.nf'
    PARAMS: str = 'params.json'
    SCHEMA: str = 'nextflow_schema.json'
    
    def __init__(self, base_dir=None, workflows_dir=None,
        invoker='invoke_nextflow', nextflow='nextflow') -> None:

        self._workflows: Dict[str, Workflow] = {}

        self.orig_dir = base_dir or 'epi2melabs'
        self.base_dir = base_dir or os.path.join(os.getcwd(), 'epi2melabs')
        self.workflows_dir = workflows_dir or os.path.join(self.base_dir, 'workflows')
        self.instance_dir = os.path.join(self.base_dir, 'instances')
        self.database_uri = f'sqlite:///{self.base_dir}/db.sqlite'

        self.invoker = invoker
        self.nextflow = nextflow

        self.get_or_create_dir(self.base_dir)
        self.get_or_create_dir(self.instance_dir)
        self.get_or_create_dir(self.workflows_dir)
        self.db = get_session(self.database_uri)

    #
    # Workflows
    #
    @property
    def workflows(self) -> Dict:
        for item in os.listdir(self.workflows_dir):
            if self._workflows.get(item):
                continue
            path = os.path.join(self.workflows_dir, item)
            if not os.path.isdir(path):
                continue
            if not self.SCHEMA in os.listdir(path):
                continue
            try:
                self._workflows[item] = self.load_workflow(
                    item, path)
            except LauncherException:
                pass
        return {
            workflow.name: workflow.to_dict()
            for workflow in self._workflows.values()
        }

    def get_workflow(self, name: str) -> Dict:
        if workflow := self.workflows.get(name):
            return workflow
        return {}

    def _get_workflow(self, name: str) -> Union[Workflow, None]:
        if not self.workflows:
            pass
        if workflow := self._workflows.get(name):
            return workflow
        return None

    def load_workflow(self, name: str, path: str) -> Workflow:
        nfcore = PipelineSchema()
        nfcore.get_schema_path(path)
        nfcore.load_schema()
        nfcore.get_schema_defaults()

        if not nfcore.schema:
            raise LauncherException(
                f'Cannot reload {name}: missing schema')

        target = None
        main_nf = os.path.join(path, self.MAINNF)
        if os.path.exists(main_nf):
            target = main_nf
        
        if not target:
            target = nfcore.schema.get('title')

        if not target:
            raise LauncherException(
                'Cannot load {name}: no entrypoint')

        return Workflow(
            name = name,
            path = path,
            target = target,
            schema = nfcore.schema,
            defaults = nfcore.schema_defaults,
            url =  nfcore.schema.get('url', '#'),
            desc = nfcore.schema.get('description', ''))

    #
    # Instances
    #
    @property
    def instances(self) -> Dict:
        return {
            instance.id: instance.to_dict()
            for instance in self.db.query(Instance).all()
        }

    def get_instance(self, id: str) -> Dict:
        if instance := self._get_instance(id):
            return instance.to_dict()
        return {}

    def _get_instance(self, id: str) -> Union[Instance, None]:
        if instance := self.db.query(Instance).get(id):
            return instance
        return None

    def create_instance(
        self, workflow_name: str, params: Dict
    ) -> Tuple[bool, Dict]:
        workflow = self._get_workflow(workflow_name)

        if not workflow or not workflow.target:
            return False, {}

        return self._create_instance(workflow.name, workflow.target, params)

    def _create_instance(
        self, workflow_name: str, workflow_target: str, params: Dict
    ) -> Tuple[bool, Dict]:

        # Generate instance details
        _id = str(shortuuid.uuid())
        now = datetime.now().strftime("%Y-%m-%d-%H-%M")
        name = '_'.join([now, workflow_name, _id])
        path = os.path.join(self.instance_dir, name)

        # Create instance db record
        instance = Instance(_id, path, name, workflow_name)
        self.db.add(instance)
        self.db.commit()

        # Construct instance filepaths
        params_file = os.path.join(path, self.PARAMS)
        nf_logfile = os.path.join(path, 'nextflow.log')
        nf_std_out = os.path.join(path, 'nextflow.stdout')
        iv_std_out = os.path.join(path, 'invoke.stdout')
        out_dir = os.path.join(path, 'output')
        work_dir = os.path.join(path, 'work')

        # Touch instance files and directories
        self.get_or_create_dir(path)
        self.get_or_create_dir(out_dir)
        self.get_or_create_dir(work_dir)

        for targ in [nf_logfile, nf_std_out, iv_std_out]:
            with open(targ, 'a'):
                pass

        # Coerce params accordingly
        params = self._fix_parameters(workflow_name, **params)
        params['out_dir'] = out_dir # Todo: generalise to support 3rd party wfs

        with open(params_file, 'w') as json_file:
            json_file.write(json.dumps(params, indent=4))

        # Launch process
        self._start_instance(instance, workflow_target, params_file,
            work_dir, nf_logfile, nf_std_out, iv_std_out, self.database_uri)

        return True, instance.to_dict()

    def _start_instance(self, instance, target: str, params_file: str,
        work_dir: str, nf_logfile: str, nf_std_out: str,
        iv_std_out: str, database: str) -> None:

        logfile = open(iv_std_out, 'a')
        stdout = logfile
        stderr = logfile

        command = (
            f'{self.invoker} -i {instance.id} -w {target} -p {params_file} '
            f'-wd {work_dir} -l {nf_logfile} -s {nf_std_out} -d {database} '
            f'-n {self.nextflow}')

        # Ensure the default location for docker on MacOS is available
        env = os.environ.copy()
        env["PATH"] = "/usr/local/bin:" + env["PATH"]

        # Todo: May need to provide some different flags on windows
        # in lieu of start_new_session working
        proc = subprocess.Popen(command.split(' '), start_new_session=True,
            stdout=stdout, stderr=stderr, close_fds=True, cwd=self.base_dir,
            env=env)

        instance.pid = proc.pid
        self.db.commit()

    def delete_instance(self, id: str, delete: bool = False) -> bool:
        instance = self._get_instance(id)
        if not instance:
            return False

        # Stop any process
        self._stop_instance(instance)

        # Optionally delete the directory
        if delete:
            try:
                shutil.rmtree(instance.path)
            except FileNotFoundError:
                pass

            # Delete record
            self.db.delete(instance)
            self.db.commit()

        return True

    def _stop_instance(self, instance) -> bool:
        if instance.status != Statuses.LAUNCHED:
            return False

        try:
            os.kill(int(instance.pid), signal.SIGINT)
            return True
        except (OSError, KeyboardInterrupt, TypeError):
            pass

        return False

    #
    # Validation
    #
    def validate(self, workflow, params):
        nfcore = PipelineSchema()
        nfcore.get_schema_path(workflow.path)
        nfcore.load_schema()
        nfcore.input_params.update(params)
        valid, errors = self._validate(nfcore.input_params, nfcore.schema)
        return valid, errors

    def _validate(self, instance, schema, *args, **kwargs):
        errors = {}
        cls = validator_for(schema)
        cls.check_schema(schema)
        validator = cls(schema, *args, **kwargs)
        for error in validator.iter_errors(instance):
            split_message = error.message.split("'")
            errors[split_message[1]] = error.message
        return bool(errors), errors

    def validate_path(self, path: str) -> Tuple[bool, str]:
        is_file, error = self.validate_file_path(path)
        if is_file:
            return is_file, ''

        is_dir, error = self.validate_directory_path(path)
        if is_dir:
           return is_dir, ''

        return False, error

    def validate_file_path(self, path: str) -> Tuple[bool, str]:
        return self._validate_path(path, os.path.isfile, 'file')

    def validate_directory_path(self, path: str) -> Tuple[bool, str]:
        return self._validate_path(path, os.path.isdir, 'directory')

    def _validate_path(self, path: str, checker: Callable, 
        format: str) -> Tuple[bool, str]:

        def check(_path: str) -> Tuple[bool, str]:
            if os.path.exists(_path):
                if checker(_path):
                    return True, ''
                return False, f'Path is not a {format}.'
            return False, 'Path does not exist or host cannot see it.'

        if os.path.isabs(path):
            return check(path)
        
        # This behaviour is intended to support jupyterlab copy_path
        if abs_path := self._fix_relative_jupyterlab_path(path):
            return check(abs_path)

        return False, 'Path does not exist or host cannot see it.'

    #
    # Helpers
    #
    def get_or_create_dir(self, path: str) -> Tuple[bool, str]:
        if not os.path.exists(path):
            os.mkdir(path)
            return True, os.path.abspath(path)
        return False, os.path.abspath(path)

    #
    # Pathing
    #
    def list_dir(self, path: str) -> List[Path]:
        items = []
        abspath = os.path.abspath(path)
        for item in os.listdir(path):
            if item.startswith('.'):
                continue
            item_abspath = os.path.join(abspath, item)
            # modified = os.path.getmtime(item_abspath)
            is_dir = os.path.isdir(item_abspath)
            items.append(Path(
                name=item,
                path=item_abspath,
                updated=0.1,
                dir=is_dir))
        return items

    def _fix_parameters(self, workflow_name, **params):
        coerced = {}
        for param_key, param_value in params.items():
            schema = self._get_schema_for_param(workflow_name, param_key)
            fmt = schema.get('format')
            if fmt in ['path', 'file-path', 'directory-path']:
                path = param_value
                if not os.path.isabs(path):
                    if abs_path := self._fix_relative_jupyterlab_path(path):
                        path = abs_path
                coerced[param_key] = path
                continue
            coerced[param_key] = param_value
        return coerced

    def _fix_relative_jupyterlab_path(self, path: str) -> Union[str, None]:
        base_name = os.path.basename(self.base_dir)
        if path.startswith(base_name + '/'):
            _path = path.split(base_name  + '/')[1]
            return os.path.join(self.base_dir, _path)

    def _get_schema_for_param(self, workflow_name: str, param_name: str) -> Dict:
        if workflow := self._get_workflow(workflow_name):
            sections = workflow.schema.get('definitions', {})
            for section in sections.values():
                for k, v in section.get('properties', {}).items():
                    if k == param_name:
                        return v
        return {}


class RemoteWorkflowLauncher(WorkflowLauncher):

    def __init__(self, base_dir, workflows_dir,
        ip: str = '0.0.0.0', port: str = '8090'):
        self.ip = ip
        self.port = port

        super().__init__(base_dir, workflows_dir)

    def create_instance(
        self, workflow_name: str, params: Dict
    ) -> Tuple[bool, Dict]:
        workflow = self._get_workflow(workflow_name)

        if not workflow or not workflow.target:
            return False, {}

        response = requests.post(
            f'http://{self.ip}:{self.port}/invocation', 
            data=json.dumps({
                'workflow_name': workflow_name,
                'workflow_target': workflow.target,
                'params': params,
            }),
            headers={
                'Content-type': 'application/json', 
                'Accept': 'text/plain'
            })

        data = response.json()
        return data['created'], data['instance']

    def delete_instance(self, id: str, delete: bool = False) -> bool:
        response = requests.delete(
            f'http://{self.ip}:{self.port}/invocation/{id}')

        data = response.json()
        return data['deleted']

    def validate_path(self, path: str) -> Tuple[bool, str]:
        response = requests.get(
            f'http://{self.ip}:{self.port}/path/{quote_plus(quote_plus(path))}')

        data = response.json()
        return data.get('exists', False), data.get('error', 'Cannot see file')

    def validate_file_path(self, path: str) -> Tuple[bool, str]:
        response = requests.get(
            f'http://{self.ip}:{self.port}/file/{quote_plus(quote_plus(path))}')
        
        data = response.json()
        return data.get('exists', False), data.get('error', 'Cannot see file')

    def validate_directory_path(self, path: str) -> Tuple[bool, str]:
        response = requests.get(
            f'http://{self.ip}:{self.port}/directory/{quote_plus(quote_plus(path))}')
        
        data = response.json()
        return data.get('exists', False), data.get('error', 'Cannot see dir')

    def list_dir(self, path: str) -> List[Path]:
        path = quote_plus(quote_plus(path))
        uuid = shortuuid.uuid()
        response = requests.get(
            f'http://{self.ip}:{self.port}/directory/{path}?contents={uuid}')

        data = response.json()
        return data.get('contents', [])


def get_workflow_launcher(
    base_dir, workflows_dir, remote=False, ip=None, port=None):

    if remote:
        kwargs = {'ip': ip, 'port': port}
        for k, v in kwargs.items():
            if v is None:
                kwargs.pop(k)
        return RemoteWorkflowLauncher(base_dir, workflows_dir, **kwargs)

    return WorkflowLauncher(base_dir, workflows_dir)