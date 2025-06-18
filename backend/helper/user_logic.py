from schemas.user_schema import UserCreate
from database.database import db_dependency
from models.user import User
from helper.hash_passwords import hash_password

def get_user_by_usename(usernname: str, db: db_dependency) -> User | None:
    """Queries User table by username

    Args:
        usernname (str): username string
        db (db_dependency): Dependency Injection
        
    Returns:
        User | None: Returns the user object found by the query parameter, or none if no user exists
    """
    
    return db.query(User).filter(User.username == usernname).first()

def create_user(user: UserCreate, db: db_dependency) -> User:
    """creates a new user into the db 

    Args:
        user (UserCreate): UserCreate schema object containing user data
        db (db_dependency): Dependency Injection

    Returns:
        User: new user object 
    """
    hashed = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user