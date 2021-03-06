from flask import Blueprint, redirect, request, flash, url_for, render_template
from flask_login import login_required, current_user
from flask_babel import ngettext as _n
from flask_babel import gettext as _
from sqlalchemy import text

from lyfeshoppe.blueprints.admin.models import Dashboard
from lyfeshoppe.blueprints.user.decorators import role_required
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.business.models.business import Business
from lyfeshoppe.blueprints.issue.models import Issue
from lyfeshoppe.blueprints.admin.forms import SearchForm, BulkDeleteForm, \
    UserForm, IssueForm, IssueContactForm
from lyfeshoppe.extensions import db

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')


@admin.before_request
@login_required
@role_required('admin')
def before_request():
    """ We are protecting all of our admin endpoints. """
    pass


# Dashboard -------------------------------------------------------------------
@admin.route('')
def dashboard():
    group_and_count_users = Dashboard.group_and_count_users()
    group_and_count_issues = Dashboard.group_and_count_issues()
    group_and_count_businesses = Dashboard.group_and_count_businesses()

    return render_template('admin/page/dashboard.jinja2',
                           group_and_count_users=group_and_count_users,
                           group_and_count_issues=group_and_count_issues,
                           group_and_count_businesses=group_and_count_businesses)


# Businesses -----------------------------------------------------------------------
@admin.route('/businesses', defaults={'page': 1})
@admin.route('/businesses/page/<int:page>')
def businesses(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Business.sort_by(request.args.get('sort', 'name'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_businesses = Business.query \
        .filter(Business.search(request.args.get('q', ''))) \
        .order_by(Business.type.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('admin/business/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           businesses=paginated_businesses)


@admin.route('/businesses/bulk_deactivate', methods=['POST'])
def businesses_bulk_deactivate():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Business.get_bulk_action_ids(request.form.get('scope'),
                                           request.form.getlist('bulk_ids'),
                                           query=request.args.get('q', ''))

        # Cant use the query in comments below; coz businesses_relationships & not just Business
        # has stuff to be deleted.
        # Business.query.filter(Business.id.in_(ids)).delete()
        # Hence use the below work-around.

        for id in ids:
            business = Business.query.get(id)
            business.active = not business.active

        # map(db.session.delete, [Business.query.get(id) for id in ids])
        db.session.commit()

        flash(_n('%(num)d business was deactivated.',
                 '%(num)d businesses were deactivated.',
                 num=len(ids)), 'success')
    else:
        flash(_('No businesses were deactivated, something went wrong.'), 'error')

    return redirect(url_for('admin.businesses'))


# Users -----------------------------------------------------------------------
@admin.route('/users', defaults={'page': 1})
@admin.route('/users/page/<int:page>')
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = User.sort_by(request.args.get('sort', 'name'),
                           request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query \
        .filter(User.search(request.args.get('q', ''))) \
        .order_by(User.role.desc(),
                  text(order_values)) \
        .paginate(page, 20, True)

    return render_template('admin/user/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           users=paginated_users)


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.is_last_admin(user,
                              request.form.get('role'),
                              request.form.get('active')):
            flash(_('You are the last admin, you cannot do that.'), 'error')
            return redirect(url_for('admin.users'))

        form.populate_obj(user)

        if user.username == '':
            user.username = None
        user.save()

        flash(_('User has been saved successfully.'), 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user/edit.jinja2', form=form, user=user)


@admin.route('/users/bulk_deactivate', methods=['POST'])
def users_bulk_deactivate():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(request.form.get('scope'),
                                       request.form.getlist('bulk_ids'),
                                       omit_ids=[current_user.id],
                                       query=request.args.get('q', ''))

        # Cant use the query in comments below; coz businesses_relationships & not just Business
        # has stuff to be deleted.
        # Business.query.filter(Business.id.in_(ids)).delete()
        # Hence use the below work-around.

        for id in ids:
            user = User.query.get(id)
            user.active = not user.active

        # map(db.session.delete, [Business.query.get(id) for id in ids])
        db.session.commit()

        flash(_n('%(num)d user was deactivated.',
                 '%(num)d users were deactivated.',
                 num=len(ids)), 'success')
    else:
        flash(_('No users were deactivated, something went wrong.'), 'error')

    return redirect(url_for('admin.users'))


# Issues ----------------------------------------------------------------------
@admin.route('/issues', defaults={'page': 1})
@admin.route('/issues/page/<int:page>')
def issues(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Issue.sort_by(request.args.get('sort', 'status'),
                            request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_issues = Issue.query \
        .filter(Issue.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 20, True)

    return render_template('admin/issue/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           issues=paginated_issues, LABEL=Issue.LABEL)


@admin.route('/issues/edit/<int:id>', methods=['GET', 'POST'])
def issues_edit(id):
    issue = Issue.query.get(id)

    if request.method == 'GET' and issue and issue.status == 'unread':
        issue = Issue.unread_to_open(issue)

    form = IssueForm(obj=issue)

    subject = _('[LyfeShoppe issue] Re: %(issue_type)s', issue_type=issue.LABEL[issue.label])

    # Shenanigans to comply with PEP-8's formatting style.
    body_string = '\n\nYou opened an issue regarding:'
    issue_string = '\n\n---\n{0}\n---\n\n'.format(issue.question)
    message = _('Hello,%(body)s:%(issue)s\n\nThanks,\nLyfeShoppe support team', body=body_string, issue=issue_string)

    contact_form = IssueContactForm(email=issue.email,
                                    subject=subject, message=message)

    if form.validate_on_submit():
        form.populate_obj(issue)
        issue.save()

        flash(_('Issue has been saved successfully.'), 'success')
        return redirect(url_for('admin.issues'))

    return render_template('admin/issue/edit.jinja2', form=form, contact_form=contact_form, issue=issue)


@admin.route('/issues/bulk_delete', methods=['POST'])
def issues_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Issue.get_bulk_action_ids(request.form.get('scope'),
                                        request.form.getlist('bulk_ids'),
                                        query=request.args.get('q', ''))

        delete_count = Issue.bulk_delete(ids)

        flash(_n('%(num)d issue was deleted.',
                 '%(num)d issues were deleted.',
                 num=delete_count), 'success')
    else:
        flash(_('No issues were deleted, something went wrong.'), 'error')

    return redirect(url_for('admin.issues'))


@admin.route('/issues/contact/<int:id>', methods=['POST'])
def issues_contact(id):
    issue = Issue.query.get(id)

    if issue:
        from lyfeshoppe.blueprints.admin.tasks import deliver_support_email
        deliver_support_email.delay(id,
                                    request.form.get('subject'),
                                    request.form.get('message'))

        Issue.set_as_contacted(issue)

        flash(_('The person who sent the issue has been contacted.'), 'success')
    else:
        flash(_('Issue no longer exists, no e-mail was sent.'), 'error')

    return redirect(url_for('admin.issues'))
