from flask_restx import Namespace, fields


class UserDto:
    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
        },
    )


class AuthDto:
    api = Namespace("auth", description="authentication related operations")
    user_auth = api.model(
        "auth_details",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password "),
        },
    )


class ConversationDto:
    api = Namespace("conversation", description="conversation related operations")
    response = api.model(
        "conversation_response",
        {
            "sender": fields.String(required=True, description="sender identifier"),
            "message": fields.String(required=True, description="sender message"),
            "response": fields.String(required=False, description="predicted response"),
        },
    )

    request = api.model(
        "conversation_request",
        {
            "sender": fields.String(required=True, description="sender identifier"),
            "message": fields.String(required=True, description="sender message"),
        },
    )
