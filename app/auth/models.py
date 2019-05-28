from datetime import datetime
from time import time
from flask import current_app
from app.database import Model, Column, relationship, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


groups_users = db.Table(
    'groups_users',
    db.Column('groups_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)


class User(Model):
    """User Model"""
    __tablename__ = 'users'
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(50), unique=True, nullable=False)
    username = Column(db.String(64), unique=True, index=True, nullable=False)
    email = Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = Column(db.String(128))
    nickname = Column(db.String(20), default='no name')
    created_on = Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

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
                'groups': [group.name for group in self.groups],
                'permissions': [permission.text for group in self.groups for permission in group.permissions],
                'exp': time() + expries_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

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
                algorithms=['HS256']
            )
        except Exception:
            return None
        return data


groups_permissions = db.Table(
    'groups_permissions',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)


class Group(Model):
    """User Group"""
    __tablename__ = 'groups'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), unique=True, nullable=False)
    users = relationship(
        'User', secondary=groups_users, lazy='subquery',
        backref=db.backref('groups', lazy=True))
    permissions = relationship(
        'Permission', secondary=groups_permissions, lazy='subquery',
        backref=db.backref('groups', lazy=True))

    def __repr__(self):
        return '<Group %r>' % self.name


class Permission(Model):
    """User Permission"""
    __tablename__ = 'permissions'
    id = Column(db.Integer, primary_key=True)
    text = Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Permission %r>' % self.text
