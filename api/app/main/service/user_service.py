import uuid
import datetime
from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        new_user = User(
            email=data["email"],
            username=data["username"],
            password=data["password"],
            registered_on=datetime.datetime.utcnow(),
        )
        save_changes(new_user)
        response_object = {"status": "success", "message": "Successfully registered."}
        return response_object, 201
    else:
        response_object = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()
