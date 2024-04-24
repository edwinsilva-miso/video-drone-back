from decouple import config

import datetime
import jwt
import pytz


class SecurityUtils:
    secret = config('JWT_KEY')
    tz = pytz.timezone('America/Bogota')

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=120),
            'username': authenticated_user.username,
            'fullname': authenticated_user.fullname,
            'user_id': authenticated_user.id,
            'roles': [authenticated_user.role.role_name]
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if len(encoded_token) > 0:
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    roles = list(payload['roles'])

                    if 'PARTICIPANT' in roles:
                        return True

                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

            return False

    @classmethod
    def decode_token(cls, headers):
        authorization = headers['Authorization']
        encoded_token = authorization.split(" ")[1]
        try:
            payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
            return payload

        except jwt.ExpiredSignatureError:
            print("El token ha expirado.")

        except jwt.InvalidTokenError:
            print("El token es inválido.")

