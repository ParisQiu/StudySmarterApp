# generate_secret.py
import os

def generate_secret_keys():
    """
    Generates two secure random keys:
    - A Flask SECRET_KEY
    - A JWT_SECRET_KEY

Returns:
tuple: (flask_secret_key, jwt_secret_key)
    """
    flask_secret_key = os.urandom(24).hex()
    jwt_secret_key = os.urandom(24).hex()
    return flask_secret_key, jwt_secret_key

if __name__ == '__main__':
    flask_key, jwt_key = generate_secret_keys()
    print("Generated Flask Secret Key:", flask_key)
    print("Generated JWT Secret Key:", jwt_key)
    