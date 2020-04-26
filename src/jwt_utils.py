import datetime
import jwt

def create_jwt(project_id: str, private_key_file: str, algorithm: str):
    token_config = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
        'aud': project_id
    }

    with open(private_key_file, 'rb') as jwt_file:
        private_key = jwt_file.read()

    return jwt.encode(token_config, private_key, algorithm=algorithm)
