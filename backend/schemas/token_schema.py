from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenValidation(BaseModel):
    detail: str
    current_user: str
    
    class Config:
        orm_mode = True