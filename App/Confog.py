import os

from dotenv import load_dotenv

load_dotenv()

database_hostname = os.getenv("database_hostname")

database_port = os.getenv("database_port")

database_password = os.getenv("database_password")

database_name = os.getenv("database_name")

database_username = os.getenv("database_username")

secret_key = os.getenv("secret_key")

algorithm = os.getenv("algorithm")

access_token_expire_minutes = int(os.getenv("access_token_expire_minutes"))

