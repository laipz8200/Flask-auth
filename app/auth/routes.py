import uuid
from flask import request, jsonify, make_response
from app import db
from app.auth import bp
from app.auth.models import User


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
    user = User.query.filter_by(username=data['username'].strip()).first()
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
    return response


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
    user = User.query.get(data['user_id'])

    return jsonify({
        'uuid': user.public_id,
        'username': user.username,
        'email': user.email,
        'created_on': user.created_on,
    })


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
    if User.query.filter_by(username=data['username'].strip()).first():
        return jsonify({'message': 'Username already exists.'}), 409
    # check if email existed
    if User.query.filter_by(email=data['email'].strip()).first():
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
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Created a new user.'}), 201
