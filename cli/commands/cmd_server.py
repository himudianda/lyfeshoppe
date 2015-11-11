import subprocess
import click


@click.group()
def cli():
    """ Start all services """
    pass


@click.command()
def debug():
    """
    Run debug
    """
    cmd = 'python run.py'
    return subprocess.call(cmd, shell=True)


@click.command()
def gunicorn():
    """
    Run gunicorn
    """
    cmd = 'honcho start'
    return subprocess.call(cmd, shell=True)


cli.add_command(debug)
cli.add_command(gunicorn)

