from flask import current_app
from flask_login import current_user


def admin_level_required(admin_level=10):

    def decorator(func):
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            if current_user.admin_level < admin_level:
                return current_app.login_manager.unauthorized()

            return func(*args, **kwargs)

        return decorated_view

    return decorator

