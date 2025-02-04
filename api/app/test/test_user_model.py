import datetime
import unittest

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_encode_auth_token(self):
        user = User(
            email="test@test.com",
            password="test",
            registered_on=datetime.datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email="test@test.com",
            password="test",
            registered_on=datetime.datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user)
        self.assertTrue(isinstance(auth_token, bytes))
        sub, scope = User.decode_auth_token(auth_token.decode("utf-8"))
        self.assertTrue(sub == user.id)
        self.assertTrue(scope == False)


if __name__ == "__main__":
    unittest.main()
