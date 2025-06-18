from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.token_schema import Token
from database.database import db_dependency
from helper.hash_passwords import check_password
from models.user import User
from database.database import settings


oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")

form_data = Annotated[OAuth2PasswordRequestForm, Depends()]

def authenticate_user(username:str, password:str, db:db_dependency):
    """Authenticate a user by checking the username and password against the database.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.
        db (db_dependency): Dependency injection

    Raises:
        HTTPException: Incorrect credentials

    Returns:
        _type_: User object if authentication is greenlit, otherwise raise HTTPException
    """
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not check_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")    
    
    return user

def create_access_token(username: str, id: str) -> str:
    encode = {'sub': username, 'id': id, 'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)    
    
    
def get_current_user(db: db_dependency, token: str = Depends(oauth)) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    if username is None or user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user = db.query(User).filter(User.id == user_id).first() 
    return user   