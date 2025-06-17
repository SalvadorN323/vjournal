import bcrypt

def hash_password(password: str) -> str:
    """Converts a password into a hashed string with salt

    Args:
        password (str): user unhashed password

    Returns:
        str: hashed password with salting
    """
    
    return bcrypt.hashpw(password.encode("UTF-8", bcrypt.gensalt())).decode("UTF-8")


def check_password(password: str, hashed_password: str) -> bool:
    """Checks if user password matches the hashed password

    Args:
        password (str): unhashed password
        hash_password (str): hashed password_

    Returns:
        bool: True if password matches and False otherwise
    """
    
    return bcrypt.checkpw(password.encode("UTF-8"), hashed_password.encode("UTF-8"))