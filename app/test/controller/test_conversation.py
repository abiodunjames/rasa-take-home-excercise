import unittest

from app.main import db
from app.main.seed.user import seed_admin_user
from app.main.seed.conversation import seed_conversation, SEED_REQUEST, SEED_RESPONSE

from app.main.model.user import User
import json
from app.test.base import BaseTestCase
import sys


def get_conversation_list(self):
    seed_conversation()
    admin_user_id = 1
    token = User.encode_auth_token(admin_user_id)
    return self.client.get(
        "/conversation/", headers={"Authorization": token.decode('utf-8')}
    )

class TestConversationBlueprint(BaseTestCase):
    def test_admin_user_get_all_conversations(self):
        """ Test admin user can get a conversation list """
        get_conversation_list(self)
        with self.client:
            response = get_conversation_list(self)
            json_response = json.loads(response.data.decode())
            data = json_response['data']
            self.assertTrue(data[0]["request"] == SEED_REQUEST)
            self.assertTrue(data[0]["response"] == SEED_RESPONSE)
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 200)

    def test_non_admin_user_can_not_get_conversation(self):
        pass

    def test_un_authorized_user_can_not_get_conversation(self):
        pass


if __name__ == "__main__":
    unittest.main()
