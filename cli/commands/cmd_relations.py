import click

from lyfeshoppe.app import create_app
from lyfeshoppe.extensions import db

from lyfeshoppe.blueprints.business.models.business import Business, Employee, Product


app = create_app()
db.app = app


@click.group()
def cli():
    """ Populate your db with generated data. """
    pass


@click.command()
def business_relations():
    """
    Read business relations
    """
    for business in db.session.query(Business).all():
        click.echo(" === Business with id {0} and email {1} === ".format(business.id, business.email))

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
                    'product {0} with price {1} & duration {2} mins'.format(
                        product.name, product.price, product.duration_mins
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
                    'product {0} with price {1} & duration {2} mins'.format(
                        product.name, product.price, product.duration_mins
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
                    'employee {0} handles product with name {1}'.format(
                        employee.user.email, product.name,
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
    ctx.invoke(business_relations)
    ctx.invoke(employee_relations)
    ctx.invoke(product_relations)

    return None


cli.add_command(business_relations)
cli.add_command(employee_relations)
cli.add_command(product_relations)
cli.add_command(all)
