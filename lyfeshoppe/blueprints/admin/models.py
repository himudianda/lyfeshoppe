from sqlalchemy import func

from lyfeshoppe.blueprints.user.models import db, User
from lyfeshoppe.blueprints.issue.models import Issue
from lyfeshoppe.blueprints.business.models.business import Business


class Dashboard(object):
    @classmethod
    def group_and_count_users(cls):
        """
        Perform a group by/count on all user types.

        :return: dict
        """
        return Dashboard._group_and_count(User, User.role)

    @classmethod
    def group_and_count_issues(cls):
        """
        Perform a group by/count on all issue types.

        :return: dict
        """
        return Dashboard._group_and_count(Issue, Issue.status)

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
        query = db.session.query(count, field).group_by(field).all()

        results = {
            'query': query,
            'total': model.query.count()
        }

        return results
