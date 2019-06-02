from app.app import create_app
from app.extensions import db
from app.auth.models import User, Permission, Group
from sqlalchemy import or_, and_

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Shell import."""
    return {
        'db': db,
        'User': User,
        'Permission': Permission,
        'Group': Group,
        'or_': or_,
        'and_': and_
    }
