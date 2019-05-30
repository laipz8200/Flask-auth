import uuid
from flask import Blueprint, request, jsonify, make_response
from app.auth.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


def check_permission(permission):
    """Decorator for checking permissions."""
    def decorator(view_func):
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


@bp.route('/login', methods=['POST'])
def login():
    """Login
    :returns: TODO

    """
    # get form info
    data = request.form
    # check info
    error = []
    if 'username' not in data:
        error.append('username')
    if 'password' not in data:
        error.append('password')
    if len(error) > 0:
        return jsonify({
            'message': 'Require {}.'.format(' and '.join(error))
        }), 400
    # find username
    user = User.filter_by(username=data['username'].strip()).first()
    if user is None:
        return jsonify({'message': 'User does not exist.'}), 404
    # verify password
    if user.check_password(data['password'].strip()):
        response = make_response(jsonify({'message': 'login successful.'}))
        # issue token
        response.set_cookie(
            'jwt', user.generate_jwt(),
            httponly=True, max_age=24*60**2, samesite='Lax')
        return response, 200
    return jsonify({'message': 'Wrong username or password.'}), 401


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout
    :returns: TODO

    """
    response = make_response(jsonify({
        'message': 'You have already logged out.'
    }))
    # clear token
    response.set_cookie('jwt', '', httponly=True, max_age=1, samesite='Lax')
    return response, 200


@bp.route('/user/me', methods=['GET'])
def get_myself():
    """Get your own information
    :returns: TODO

    """
    # get token
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'message': 'Missing verification letter.'}), 401
    # verify token
    data = User.verify_jwt(token)
    if not data:
        return jsonify({'message': 'Token expired.'}), 401
    # find user
    user = User.get_by_id(data['user_id'])
    if user is None:
        return jsonify({'message': 'User does not exist.'}), 404

    return jsonify({
        'uuid': user.public_id,
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'groups': data['groups'],
        'permissions': data['permissions'],
        'created_on': user.created_on,
    }), 200


@bp.route('/user', methods=['POST'])
def create_user():
    """Create a new user
    :returns: TODO

    """
    # get form info
    data = request.form
    # check info
    error = []
    if 'username' not in data:
        error.append('username')
    if 'password' not in data:
        error.append('password')
    if 'email' not in data:
        error.append('email')
    if len(error) > 0:
        return jsonify({
            'message': 'Require {}.'.format(' and '.join(error))
        }), 400
    # check if user existed
    if User.filter_by(username=data['username'].strip()).first():
        return jsonify({'message': 'Username already exists.'}), 409
    # check if email existed
    if User.filter_by(email=data['email'].strip()).first():
        return jsonify({'message': 'Email has been registered.'}), 409
    # create User
    user = User(
        public_id=str(uuid.uuid1()),
        username=data['username'].strip(),
        email=data['email'].strip()
    )
    # password hash
    user.set_password(data['password'].strip())
    # db commit
    user.save()

    return jsonify({'message': 'Created a new user.'}), 201


@bp.route('/user/<uuid>', methods=['GET'])
def view_user(uuid):
    """View user information

    :uuid: User's public id
    :returns: TODO

    """
    # find user with uuid
    user = User.filter_by(public_id=uuid).first()
    if not user:
        return jsonify({'message': 'User does not exist.'}), 404
    # return user information
    return jsonify({
        'uuid': user.public_id,
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'created_on': user.created_on,
    }), 200


@bp.route('/user/<uuid>', methods=['PUT'])
def update_user(uuid):
    """Update user information

    :uuid: User's public id
    :returns: TODO

    """
    # get jwt
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'message': 'Missing verification letter.'}), 401
    # verify jwt
    data = User.verify_jwt(token)
    if not data:
        return jsonify({'message': 'Token expired.'}), 401
    # check uuid
    if uuid != data['uuid']:
        return jsonify({
            'message': 'Can only modify your own information.'
        }), 401
    # get user
    user = User.get_by_id(data['user_id'])
    if user is None:
        return jsonify({'message': 'User does not exist.'}), 404
    # get form data
    data = request.form
    # check form data
    error = []
    if 'nickname' not in data:
        error.append('nickname')
    if len(error) > 0:
        return jsonify({
            'message': 'Require {}.'.format(' and '.join(error))
        }), 400
    # update user information
    user.update(nickname=data['nickname'].strip())

    return jsonify({'message': 'Data update completed.'}), 200


@bp.route('/user/<uuid>', methods=['DELETE'])
@check_permission(permission='Can delete user')
def delete_user(uuid):
    """Delete user

    :uuid: User's public id
    :returns: TODO

    """
    # get user
    user = User.filter_by(public_id=uuid).first()
    if not user:
        return jsonify({'message': 'User does not exist.'}), 404
    # delete user
    user.delete()
    return jsonify({'message': 'User has been deleted.'}), 200
