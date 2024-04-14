from sqlalchemy import and_
from src.database.declarative_base import Session
from src.models.User import User, Role
from src.utils.SecurityUtils import SecurityUtils


class AuthenticationService:

    @classmethod
    def login_user(cls, username, password):
        authenticated_user = Session.query(User).filter(
            and_(
                User.username == username,
                User.password == password
            )
        ).first()

        if authenticated_user:
            return SecurityUtils.generate_token(authenticated_user)

        return None

    @classmethod
    def sign_up(cls, fullname, username, password, role, email):
        role = Session.query(Role).filter(Role.role_name == role).first()
        user = Session.query(User).filter(User.email == email).first()

        if role or user is None:
            new_user = User(
                fullname=fullname,
                username=username,
                password=password,
                role=role,
                email=email
            )
            Session.add(new_user)
            Session.commit()
            return True

        return False

    @classmethod
    def verify_token(cls, headers):
        return SecurityUtils.verify_token(headers)
