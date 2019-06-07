import uuid
from flask import Blueprint, request, jsonify, make_response, url_for
from app.auth.models import User
from app.auth.decorators import require_permission, require_login


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/', methods=['GET'])
def index():
    """Index page for interface."""
    return jsonify({'message': 'Welcome to the user interface.'}), 200


@bp.route('/login', methods=['POST'])
def login():
    """Login."""
    # get form info
    data = request.json or {}
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
    """Logout."""
    response = make_response(jsonify({
        'message': 'You have already logged out.'
    }))
    # clear token
    response.set_cookie('jwt', '', httponly=True, max_age=1, samesite='Lax')
    return response, 200


@bp.route('/users', methods=['GET'])
@require_permission(permission='Can view users')
def view_users():
    """View user list.

    This method has two hidden parameters:

    * ``page`` is current page number, default to 1.
    * ``per_page`` is number of users per page, default to 20.
    """
    # get user list
    page = User.paginate(max_per_page=50)
    # format user data
    data = []
    for current_user in page.items:
        data.append({
            'url': url_for(
                'auth.view_user', uuid=current_user.public_id, _external=True
            ),
            'uuid': current_user.public_id,
            'username': current_user.username,
            'email': current_user.email,
            'created_on': current_user.created_on
        })
    # return
    return jsonify({
        'count': User.count(),
        'prev': url_for(
            'auth.view_users', page=page.prev_num, _external=True
        ) if page.has_prev else None,
        'next': url_for(
            'auth.view_users', page=page.next_num, _external=True
        ) if page.has_next else None,
        'result': data
    }), 200


@bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    # get form info
    data = request.json or {}
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


@bp.route('/users/me', methods=['GET'])
@require_login
def get_myself(current_user):
    """Get your own information."""
    return jsonify({
        'uuid': current_user.public_id,
        'username': current_user.username,
        'email': current_user.email,
        'nickname': current_user.nickname,
        'groups': [group.name for group in current_user.groups],
        'permissions': [permission.text
                        for group in current_user.groups
                        for permission in group.permissions],
        'created_on': current_user.created_on,
    }), 200


@bp.route('/users/<uuid>', methods=['GET'])
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
        'groups': [group.name for group in user.groups],
        'created_on': user.created_on,
    }), 200


@bp.route('/users/<uuid>', methods=['PUT'])
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
    data = request.json or {}
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


@bp.route('/users/<uuid>', methods=['DELETE'])
@require_permission(permission='Can delete users')
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
    if 'administrator' in [group.name for group in user.groups]:
        return jsonify({'message': 'You cannot delete an admin user.'}), 403
    user.delete()
    return jsonify({'message': 'User has been deleted.'}), 200
