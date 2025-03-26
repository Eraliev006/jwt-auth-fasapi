from logging import getLogger

import bcrypt

from logging_config import setup_logging

setup_logging()
password_utils_logger = getLogger('project.password')

def hash_password(password: str) -> str:
    password_utils_logger.info('Hashing password')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()