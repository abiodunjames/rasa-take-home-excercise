from app.main.controller.auth_controller import api as auth_namespace
from app.main.controller.conversation_controller import api as conversation_namespace
from app.main.controller.user_controller import api as user_namespace
from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Take Home Test",
    version="1.0",
    description="Rasa take-home exercise",
)

api.add_namespace(user_namespace, path="/users")
api.add_namespace(auth_namespace)
api.add_namespace(conversation_namespace, path="/conversations")
