from app.main import db
from app.main.seed.user import seed_admin_user
from flask_testing import TestCase
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        seed_admin_user()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
