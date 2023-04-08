import bcrypt

def hash(password: str):

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def verify(plain_password, hashed_password):

    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

