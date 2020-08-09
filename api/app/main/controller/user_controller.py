from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users
from typing import Dict, Tuple

api = UserDto.api
user = UserDto.user


@api.route("/")
@api.doc(
    params={"Authorization": {"in": "header", "description": "An authorization token"}}
)
class UserList(Resource):
    @api.doc("list_of_registered_users")
    @admin_token_required
    @api.marshal_list_with(user, envelope="data")
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(user, validate=True)
    @api.response(201, "User successfully created.")
    @api.doc("create a new user")
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)
