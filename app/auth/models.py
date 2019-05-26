from datetime import datetime
from time import time
from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

user_permissions = db.Table(
    'user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)


class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.relationship(
        'Permission', secondary=user_permissions, back_populates='users'
    )

    def __repr__(self):
        return '<User (%r, %r, %r)>' % (self.id, self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self, expries_in=24*60**2):
        """Generate JSON Web Token

        :expries_in: Validaty period
        :returns: JSON Web Token string

        """
        return jwt.encode(
            {
                'user_id': self.id,
                'uuid': self.public_id,
                'exp': time() + expries_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        """Verify JSON Web Token

        :token: JSON Web Token
        :returns: data dict or None

        """
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except Exception:
            return None
        return data


class Permission(db.Model):
    """User Permission"""
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    permission = db.Column(db.String(50), unique=True)
    users = db.relationship(
        'User', secondary=user_permissions, back_populates='permissions'
    )

    def __repr__(self):
        return '<Permission %r>' % self.permission
