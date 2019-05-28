from app.app import create_app
from app.extensions import db
from app.auth.models import User, Permission, Group

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Permission': Permission, 'Group': Group}
