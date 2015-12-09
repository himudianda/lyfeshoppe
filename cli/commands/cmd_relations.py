import click

from cheermonk.app import create_app
from cheermonk.extensions import db

from cheermonk.blueprints.user.models import User
from cheermonk.blueprints.business.models.business import Business, Employee, Product


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
def employee_relations():
    """
    Read employee relations
    """
    for employee in db.session.query(Employee).all():
        click.echo(" === Employee with id {0} and email {1} === ".format(employee.id, employee.user.email))

        # Employee User addresses
        if employee.user.address:
            click.echo(
                    'Address: {0},{1},{2},{3}'.format(
                        employee.user.address.street, employee.user.address.city,
                        employee.user.address.state, employee.user.address.zipcode
                    )
                )
        else:
            click.echo('No address listed.')

        # Employee User occupancies
        if employee.user.occupancies and len(employee.user.occupancies):
            click.echo(
                    'Occupancies: {0}'.format(
                        len(employee.user.occupancies)
                    )
                )

            for occupancy in employee.user.occupancies:
                click.echo(
                    'start_time: {0}  -  end_time: {1}  occupied for user {2}'.format(
                        occupancy.start_time, occupancy.end_time,
                        occupancy.user.email
                    )
                )

        else:
            click.echo('No occupancies listed.')

        # Employee reservations
        if employee.reservations:
            click.echo(
                    'Reservation: {0}'.format(
                        len(employee.reservations)
                    )
                )

            for reservation in employee.reservations:
                click.echo(
                    'reservation {0} with status {1} for customer {2} has product {3}'.format(
                        reservation.id, reservation.status,
                        reservation.customer.user.email, reservation.product.name
                    )
                )

        # Employee products
        if employee.products:
            click.echo(
                    'Products: {0}'.format(
                        len(employee.products)
                    )
                )

            for product in employee.products:
                click.echo(
                    'product {0} with capacity {1} has price {2} cents & duration {3} mins'.format(
                        product.name, product.capacity,
                        product.price_cents, product.duration_mins
                    )
                )

        else:
            click.echo('No products listed.')


@click.command()
def product_relations():
    """
    Read product relations
    """
    for product in db.session.query(Product).all():
        click.echo(
            " === Product with id {0} has {1} number of employees === ".format(
                product.id, len(product.employees)
            )
        )

        # Product Employees
        if product.employees:
            click.echo(
                    'Employees: {0}'.format(
                        len(product.employees)
                    )
                )

            for employee in product.employees:
                click.echo(
                    'employee {0} handles product with name {3}'.format(
                        employee.email, product.name,
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
    ctx.invoke(employee_relations)
    ctx.invoke(product_relations)

    return None


cli.add_command(user_relations)
cli.add_command(business_relations)
cli.add_command(employee_relations)
cli.add_command(product_relations)
cli.add_command(all)
