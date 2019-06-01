from functools import wraps
from flask import jsonify, request
from app.auth.models import User


def require_permission(permission):
    """Decorator for checking permissions."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            # get jwt
            token = request.cookies.get('jwt')
            if not token:
                return jsonify({
                    'message': 'Missing verification letter.'
                }), 401
            # verify jwt
            data = User.verify_jwt(token)
            if not data:
                return jsonify({'message': 'Token expired.'}), 401
            # check permissions
            if permission not in data['permissions']:
                return jsonify({'message': 'Permission denied.'}), 403
            return view_func(*args, **kwargs)
        return wrapper
    return decorator


def require_login(view_func):
    """Decorator for checking login."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # get jwt
        token = request.cookies.get('jwt')
        if not token:
            return jsonify({
                'message': 'Missing verification letter.'
            }), 401
        # verify jwt
        data = User.verify_jwt(token)
        if not data:
            return jsonify({'message': 'Token expired.'}), 401
        # get user
        current_user = User.get_by_id(data['user_id'])
        if current_user is None:
            jsonify({'message': 'Require login.'}), 401
        return view_func(current_user, *args, **kwargs)
    return wrapper
