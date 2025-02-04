from typing import Dict, Tuple, Union

from app.main.model.user import User
from werkzeug.local import LocalProxy

from app.main.service.blacklist_service import save_token


class Auth:
    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get("email")).first()
            if user and user.check_password(data.get("password")):
                auth_token = User.encode_auth_token(user)
                if auth_token:
                    response_object = {
                        "status": "success",
                        "message": "Successfully logged in.",
                        "Authorization": auth_token.decode("utf-8"),
                    }
                    return response_object, 200
            else:
                response_object = {
                    "status": "fail",
                    "message": "email or password does not match.",
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {"status": "fail", "message": "Try again"}
            return response_object, 500

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as revoked
                return save_token(token=auth_token)
            else:
                response_object = {"status": "fail", "message": resp}
                return response_object, 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(
        new_request: LocalProxy
    ) -> Tuple[Dict[str, Union[str, Dict[str, Union[int, str, bool]]]], int]:
        # get the auth token
        auth_token = new_request.headers.get("Authorization")
        if auth_token:
            user_id, is_admin = User.decode_auth_token(auth_token)
            if user_id is not None:
                response_object = {
                    "status": "success",
                    "data": {"user_id": user_id, "admin": is_admin},
                }
                return response_object, 200
            return response_object, 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return response_object, 401
