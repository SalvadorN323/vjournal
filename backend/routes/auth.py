from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserCreate, UserResponse
from database.database import db_dependency
from helper.user_logic import get_user_by_usename, create_user
from schemas.token_schema import Token
from helper.token import authenticate_user, form_data, create_access_token


auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: db_dependency):
    db_user = get_user_by_usename(user.username, db)
    if db_user:
        raise HTTPException(status_code=401, detail="User exists")
    return create_user(user=user, db=db)

@auth_router.post("/token", response_model=Token)
async def login_user(form_data: form_data, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    token = create_access_token(user.username, user.hashed_password)

    return {"access_token": token, "token_type": "Bearer"}
    