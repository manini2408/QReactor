from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """
    Decorator for routes that should be accessible only by admins.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """
    Decorator for routes that should be accessible only by regular users.
    This is mainly for semantic clarity in routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash('This page is for regular users only.', 'warning')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function 