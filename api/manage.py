import os
import unittest

from app import blueprint
from app.main import create_app, db
from app.main.model import blacklist, conversation, user
from app.main.seed.user import seed_admin_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = create_app(os.getenv("APP_ENV") or "dev")
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)


@manager.command
def run():
    app.run(host="0.0.0.0")


@manager.command
def create_db():
    """
    This will drop database tables and recreate them.
    Run this command once.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed():
    """ Populate the db with admin credentials """
    seed_admin_user()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover("app/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
