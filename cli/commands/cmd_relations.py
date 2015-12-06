import click

from cheermonk.app import create_app
from cheermonk.extensions import db

from cheermonk.blueprints.user.models import User
from cheermonk.blueprints.business.models.business import Business


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
def user_occupancies():
    """
    Read user occupancies
    """
    for user in db.session.query(User).all():
        if user.occupancies and len(user.occupancies):
            click.echo(
                    'User {0} has {1} occupancies'.format(
                        user.email, len(user.occupancies)
                    )
                )
        else:
            click.echo(
                    'User {0}: has no occupancies.'.format(
                        user.email
                    )
                )


@click.command()
def business_occupancies():
    """
    Read business occupancies
    """
    for business in db.session.query(Business).all():
        if business.occupancies and len(business.occupancies):
            click.echo(
                    'Business {0} has {1} occupancies'.format(
                        business.email, len(business.occupancies)
                    )
                )
        else:
            click.echo(
                    'Business {0}: has no occupancies.'.format(
                        business.email
                    )
                )


@click.command()
def business_addresses():
    """
    Read business addresses
    """
    for business in db.session.query(Business).all():
        if business.address:
            click.echo(
                    'Business {0} has address: {1},{2},{3},{4} at address_id: {5} matching address_id: {6}'.format(
                        business.email, business.address.street, business.address.city,
                        business.address.state, business.address.zipcode,
                        business.address_id, business.address.id
                    )
                )
        else:
            click.echo(
                    'Business {0}: has no addresses.'.format(
                        business.email
                    )
                )


@click.command()
def business_employees():
    """
    Read business employees
    """
    for business in db.session.query(Business).all():
        if business.employees:
            click.echo(
                    'Business {0} has {1} employees'.format(
                        business.email, len(business.employees)
                    )
                )
            for employee in business.employees:
                click.echo(
                    'employee {0} is a {1} at business {2}'.format(
                        employee.user.email, employee.role,
                        employee.business.email
                    )
                )

        else:
            click.echo(
                    'Business {0}: has no employees.'.format(
                        business.email
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
    ctx.invoke(business_addresses)
    ctx.invoke(user_occupancies)
    ctx.invoke(business_occupancies)
    ctx.invoke(business_employees)

    return None


cli.add_command(user_addresses)
cli.add_command(business_addresses)
cli.add_command(user_occupancies)
cli.add_command(business_occupancies)
cli.add_command(business_employees)
cli.add_command(all)
