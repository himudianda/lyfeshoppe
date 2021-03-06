from sqlalchemy import func
from flask_login import current_user

from lyfeshoppe.blueprints.user.models import db
from lyfeshoppe.blueprints.business.models.business import Business, Employee, Product, Reservation


class Dashboard(object):

    @classmethod
    def group_and_count_businesses(cls):
        """
        Perform a group by/count on all issue types.

        :return: dict
        """
        return Dashboard._group_and_count(Business, Business.type)

    @classmethod
    def _group_and_count(cls, model, field):
        """
        Group results for a specific model and field.

        :param model: Name of the model
        :type model: SQLAlchemy model
        :param field: Name of the field to group on
        :type field: SQLAlchemy field
        :return: dict
        """

        count = func.count(field)
        user_employee_ids = [employee.id for employee in Employee.query.filter(Employee.user == current_user)]

        query = db.session.query(count, field).filter(
                        model.employees.any(Employee.id.in_(user_employee_ids))
                    ).group_by(field).all()

        results = {
            'query': query,
            'total': db.session.query(model).filter(
                        model.employees.any(Employee.id.in_(user_employee_ids))
                    ).count()
        }

        return results


class BusinessDashboard(object):

    @classmethod
    def group_and_count_employees(cls, business):
        """
        Perform a group by/count on all issue types.

        :return: dict
        """
        return cls._group_and_count(business, Employee, Employee.role)

    @classmethod
    def group_and_count_products(cls, business):
        """
        Perform a group by/count on all issue types.

        :return: dict
        """
        return cls._group_and_count(business, Product, Product.category)

    @classmethod
    def group_and_count_reservations(cls, business):
        """
        Perform a group by/count on all issue types.

        :return: dict
        """
        return cls._group_and_count(business, Reservation, Reservation.status)

    @classmethod
    def _group_and_count(cls, business, model, field):
        """
        Group results for a specific model and field.

        :param model: Name of the model
        :type model: SQLAlchemy model
        :param field: Name of the field to group on
        :type field: SQLAlchemy field
        :return: dict
        """

        count = func.count(field)
        query = db.session.query(count, field).filter(
                model.business == business
            ).group_by(field).all()

        results = {
            'query': query,
            'total': db.session.query(model).filter(
                        model.business == business
                    ).count()
        }

        return results
