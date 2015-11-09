import subprocess
import click


@click.command()
def cli():
    """ Start all services """
    cmd = 'python run.py'
    return subprocess.call(cmd, shell=True)
