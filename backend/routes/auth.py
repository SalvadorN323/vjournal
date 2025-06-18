from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserCreate, UserResponse
from database.database import db_dependency
from helper.user_logic import get_user_by_usename, create_user

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: db_dependency):
    db_user = get_user_by_usename(user.username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="User exists")
    return create_user(user=user, db=db)
    