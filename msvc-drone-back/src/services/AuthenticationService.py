from sqlalchemy import and_
from src.database.declarative_base import open_session
from src.models.User import User
from src.models.Role import Role
from src.utils.SecurityUtils import SecurityUtils


class AuthenticationService:

    @classmethod
    def login_user(cls, username, password):
        session = open_session()

        authenticated_user = session.query(User).filter(
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
        session = open_session()

        role = session.query(Role).filter(Role.role_name == role).first()
        user = session.query(User).filter(User.email == email).first()

        if role and user is None:
            new_user = User(
                fullname=fullname,
                username=username,
                password=password,
                role=role,
                email=email
            )
            session.add(new_user)
            session.commit()
            session.close()
            return True

        session.close()
        return False

    @classmethod
    def verify_token(cls, headers):
        return SecurityUtils.verify_token(headers)

    @classmethod
    def get_id_from_token(cls, headers):

        data = SecurityUtils.decode_token(headers)
        return data['user_id']
