from pydantic import BaseModel
from datetime import datetime
import uuid

class JounralEntryBase(BaseModel):
    title: str
    content: str
    
class JournalEntryCreate(JounralEntryBase):
    pass

class JournalEntryResponse(JounralEntryBase):
    user_id: uuid.UUID
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        orm_mode = True