# flake8: noqa
import os
import sys
import logging
import argparse
import subprocess
from epi2melabs.workflows.database import get_session, Instance, Statuses


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Execute a netflow workflow and update the database.",
        usage="nf_invoke -w epi2melabs/wf-alignment -p <file> -wd <dir> -o <file> -d <file>"
    )

    parser.add_argument(
        '-n',
        '--nextflow',
        required=True,
        default='nextflow',
        help='Path to the nextflow executable.'
    )

    parser.add_argument(
        '-i',
        '--id',
        required=True,
        help='ID of the database instance record to acquire and update.'
    )

    parser.add_argument(
        '-w',
        '--workflow',
        required=True,
        help='Path to or name of the workflow to be run.'
    )

    parser.add_argument(
        '-p',
        '--params',
        required=True,
        help='Path to the workflow params file.'
    )

    parser.add_argument(
        '-wd',
        '--work_dir',
        required=True,
        help='Path to what should become the working directory.'
    )

    parser.add_argument(
        '-l',
        '--log_file',
        required=True,
        help='Path to which the logs should be written.'
    )

    parser.add_argument(
        '-s',
        '--std_out',
        required=True,
        help='Path to which the stdout should be written.'
    )

    parser.add_argument(
        '-d',
        '--database',
        required=True,
        help='Path to the SQLITE database to update.'
    )

    start = 1
    if 'invoke' != sys.argv[0]:
        start = 0

    return parser.parse_args(sys.argv[start:])


def invoke(id: str, workflow: str, params: str, work_dir: str, 
    log_file:str, std_out: str, database: str, nextflow: str):
    logging.basicConfig(
        format='EPI2MELABS <%(asctime)s> [%(levelname)s]: %(message)s', 
        level=logging.DEBUG)

    logging.info('Initialising workflow.')

    # Get the command
    command = (
        f'{nextflow} -log {log_file} run {workflow} -params-file {params} '
        f'-w {work_dir} -ansi-log false')
    logging.info(f'Command: {command}.')

    # Modify if we're on windows
    if sys.platform in ["win32"]:
        logging.info("Detected OS as Windows.")
        command = 'wsl ' + command

    # Get the invocation instance by id
    db = get_session(database)
    invocation = db.query(Instance).get(id)

    # Update the invocation with the current pid
    pid = os.getpid()
    logging.info(f'The wrapper PID is {pid}.')
    invocation.pid = pid
    db.commit()

    # Invoke the command
    logging.info(f'Launching workflow.')
    cli_logfile = open(std_out, 'a')
    stdout = cli_logfile
    stderr = cli_logfile
    proc = subprocess.Popen(
        command.split(' '), stdout=stdout, stderr=stderr)
    logging.info(f'The workflow PID is {proc.pid}.')

    try:
        invocation.status = Statuses.LAUNCHED
        db.commit()

        # Wait for the exit status
        ret = proc.wait()
        sys.exit(ret)

    # If we receive sigint, assume the process was
    # terminated intentionally and exit gracefully
    except KeyboardInterrupt:
        logging.info(f'Interrupt detected: terminating workflow.')
        proc.kill()
        invocation.status = Statuses.TERMINATED
        db.commit()
        sys.exit(0)

    except SystemExit as e:
        # If we receive system exit of 0, assume the process
        # ended peacefully and exit gracefully.
        if not e.code:
            logging.info(f'Workflow completed.')
            invocation.status = Statuses.COMPLETED_SUCCESSFULLY
            db.commit()
            sys.exit(0)

        # If we receive a non-zero system exit update the
        # status to reflect an error. Exit with code 1.
        logging.info(f'Workflow encountered an error.')
        invocation.status = Statuses.ENCOUNTERED_ERROR
        db.commit()
        sys.exit(1)

    # Handle all other exception classes in the event of
    # unhandled exceptions occurring within the callable.
    # Set the status to error and exit with code 1.
    except Exception as e:
        logging.info(f'Workflow encountered an error.')
        invocation.status = Statuses.ENCOUNTERED_ERROR
        db.commit()
        sys.exit(1)


def main():
    args = parse_args()
    invoke(
        id=args.id,
        workflow=args.workflow,
        params=args.params,
        work_dir=args.work_dir,
        log_file=args.log_file,
        std_out=args.std_out,
        database=args.database,
        nextflow=args.nextflow
    )


if __name__ == '__main__':
    main()