import click

from cheermonk.app import create_app
from cheermonk.extensions import db

from cheermonk.blueprints.user.models import User

app = create_app()
db.app = app


@click.group()
def cli():
    """ Populate your db with generated data. """
    pass


@click.command()
def user_addresses():
    """
    Read user addresses
    """
    for user in db.session.query(User).all():
        if user.address:
            click.echo(
                    'User {0} has address: {1},{2},{3},{4} at address_id: {5} matching address_id: {6}'.format(
                        user.email, user.address.street, user.address.city,
                        user.address.state, user.address.zipcode,
                        user.address_id, user.address.id
                    )
                )
        else:
            click.echo(
                    'User {0}: has no addresses.'.format(
                        user.email
                    )
                )


@click.command()
@click.pass_context
def all(ctx):
    """
    Read all relations at once.

    :param ctx:
    :return: None
    """
    ctx.invoke(user_addresses)
    return None


cli.add_command(user_addresses)
cli.add_command(all)
