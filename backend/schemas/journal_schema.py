from pydantic import BaseModel
from datetime import datetime
import uuid

class JounralEntryBase(BaseModel):
    title: str
    content: str
    
class JournalEntryCreate(JounralEntryBase):
    pass

class JournalEntryResponse(JounralEntryBase):
    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID
    
    class Config:
        orm_mode = True