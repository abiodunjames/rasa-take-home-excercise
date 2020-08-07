from app.main.model.user import User
from app.main import db
import datetime

SEED_ADMIN_EMAIL = 'admin@test.com'
SEED_ADMIN_PASSWORD= '123456'

def seed_admin_user():
    """
    Seed initial admin user. This user will be use to create other non-admin user.
    """
    user = User(
            email=SEED_ADMIN_EMAIL,
            password=SEED_ADMIN_PASSWORD,
            registered_on=datetime.datetime.utcnow(),
            admin=True
        )
    db.session.add(user)
    db.session.commit()