from flask import url_for
from flask_babel import ngettext as _n
from flask_babel import gettext as _

from lyfeshoppe.tests.lib.util import ViewTestMixin
from lyfeshoppe.tests.lib.assertions import assert_status_with_message
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.issue.models import Issue


class TestDashboard(ViewTestMixin):
    def test_dashboard_page(self):
        self.login()
        response = self.client.get(url_for('admin.dashboard'))

        assert 'Subscriptions' in response.data
        assert 'Coupons' in response.data
        assert 'User' in response.data
        assert 'Issue' in response.data


class TestUsers(ViewTestMixin):
    def test_index_page(self):
        """ Index renders successfully. """
        self.login()
        response = self.client.get(url_for('admin.users'))

        assert response.status_code == 200

    def test_edit_page(self):
        """ Edit page renders successfully. """
        self.login()
        response = self.client.get(url_for('admin.users_edit', id=1))

        assert_status_with_message(200, response, 'admin@localhost.com')

    def test_edit_resource(self):
        """ Edit this resource successfully. """
        params = {
            'role': 'admin',
            'username': 'foo',
            'active': True
        }

        self.login()
        response = self.client.post(url_for('admin.users_edit', id=1),
                                    data=params, follow_redirects=True)

        assert_status_with_message(200, response,
                                   _('User has been saved successfully.'))


class TestIssues(ViewTestMixin):
    def test_index_page(self):
        """ Index renders successfully. """
        self.login()
        response = self.client.get(url_for('admin.issues'))

        assert response.status_code == 200

    def test_edit_page(self, issues):
        """ Edit page renders successfully. """
        self.login()
        response = self.client.get(url_for('admin.issues_edit', id=1))

        assert_status_with_message(200, response, 'admin@localhost.com')

    def test_edit_resource(self):
        """ Edit this resource successfully. """
        params = {
            'label': 'signup',
            'email': 'foo@bar.com',
            'question': 'Cool.',
            'status': 'open',
        }

        issue = Issue(**params)
        issue.save()

        params_edit = {
            'label': 'other',
            'email': 'foo@bar.com',
            'question': 'Cool.',
            'status': 'closed',
        }

        self.login()
        response = self.client.post(url_for('admin.issues_edit', id=issue.id),
                                    data=params_edit, follow_redirects=True)

        assert_status_with_message(200, response,
                                   _('Issue has been saved successfully.'))

