import jwt
from datetime import datetime, timedelta


def generate_session_token(user_id, name):
    payload = {
        "sub": user_id,
        "name": name,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=1),
    }

    token = jwt.encode(payload, "your_secret_key", algorithm="HS256")
    return token


def validate_session_token(session_token, secret_key):
    try:
        payload = jwt.decode(session_token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError as e:
        return str(e)


def decode_jwt(token: str):
    decoded_token = jwt.decode(token, algorithms=["RS256"])
    print(decoded_token)
    return decoded_token
