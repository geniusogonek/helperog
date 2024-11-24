import jwt

from config import JWT_SECRET


def generate_jwt(data):
    try:
        return jwt.encode(
            payload={"username": data.username, "password": data.password},
            key=JWT_SECRET,
            algorithm="HS256"
        )
    except:
        return None


def decode_jwt(jwt_token):
    try:
        return jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
    except:
        return None