from flask import url_for
from flask_login import current_user


def get_dashboard_url():
    if current_user.role == "admin":
        return url_for('admin.dashboard')
    elif current_user.role == "member":
        if current_user.num_of_businesses == 0:
            return url_for('backend.shop')
        elif current_user.num_of_businesses == 1:
            return url_for('backend.business_dashboard', id=current_user.id_of_businesses[0])
        else:
            # If user has multiple businesses on lyfeshoppe
            return url_for('backend.businesses')
    else:
        return url_for('page.home')
