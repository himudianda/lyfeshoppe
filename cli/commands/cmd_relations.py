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
def user_relations():
    """
    Read user relations
    """
    for user in db.session.query(User).all():
        click.echo(" === User with id {0} and email {1} === ".format(user.id, user.email))

        # User addresses
        if user.address:
            click.echo(
                    'Address: {0},{1},{2},{3}'.format(
                        user.address.street, user.address.city,
                        user.address.state, user.address.zipcode
                    )
                )
        else:
            click.echo('No address listed.')

        # User occupancies
        if user.occupancies and len(user.occupancies):
            click.echo(
                    'Occupancies: {0}'.format(
                        len(user.occupancies)
                    )
                )

            for occupancy in user.occupancies:
                click.echo(
                    'start_time: {0}  -  end_time: {1}  occupied for user {2}'.format(
                        occupancy.start_time, occupancy.end_time,
                        occupancy.user.email
                    )
                )

        else:
            click.echo('No occupancies listed.')


@click.command()
def business_relations():
    """
    Read business relations
    """
    for business in db.session.query(Business).all():
        click.echo(" === Business with id {0} and email {1} === ".format(business.id, business.email))

        # Business addresses
        if business.address:
            click.echo(
                    'Address: {0},{1},{2},{3}'.format(
                        business.address.street, business.address.city,
                        business.address.state, business.address.zipcode
                    )
                )
        else:
            click.echo('No address listed.')

        # Business occupancies
        if business.occupancies and len(business.occupancies):
            click.echo(
                    'Occupancies: {0}'.format(
                        len(business.occupancies)
                    )
                )

            for occupancy in business.occupancies:
                click.echo(
                    'start_time: {0}  -  end_time: {1}  occupied for business {2}'.format(
                        occupancy.start_time, occupancy.end_time,
                        occupancy.business.email
                    )
                )

        else:
            click.echo('No occupancies listed.')

        # Business employees
        if business.employees:
            click.echo(
                    'Employees: {0}'.format(
                        len(business.employees)
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
            click.echo('No employees listed.')

        # Business products
        if business.products:
            click.echo(
                    'Products: {0}'.format(
                        len(business.products)
                    )
                )

            for product in business.products:
                click.echo(
                    'product {0} with capacity {1} has price {2} cents & duration {3} mins'.format(
                        product.name, product.capacity,
                        product.price_cents, product.duration_mins
                    )
                )

        else:
            click.echo('No products listed.')


@click.command()
@click.pass_context
def all(ctx):
    """
    Read all relations at once.

    :param ctx:
    :return: None
    """
    ctx.invoke(user_relations)
    ctx.invoke(business_relations)

    return None


cli.add_command(user_relations)
cli.add_command(business_relations)
cli.add_command(all)
