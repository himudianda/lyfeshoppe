from sqlalchemy import func
from flask_login import current_user

from cheermonk.blueprints.user.models import db
from cheermonk.blueprints.business.models.business import Business, Employee


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
        query = db.session.query(count, field).filter(
                        model.employees.any(Employee.id.in_([current_user.id]))
                    ).group_by(field).all()

        results = {
            'query': query,
            'total': db.session.query(model).filter(
                        model.employees.any(Employee.id.in_([current_user.id]))
                    ).count()
        }

        return results
