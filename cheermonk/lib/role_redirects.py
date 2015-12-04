from flask import url_for
from flask_login import current_user


def get_dashboard_url():
    if current_user.role == "admin":
        return url_for('admin.dashboard')
    elif current_user.role == "member":
        return url_for('dashboard.index')
    else:
        return url_for('page.home')
