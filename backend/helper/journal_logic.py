from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from database.database import db_dependency
from schemas.token_schema import Token
from helper.token import oauth
from schemas.journal_schema import JournalEntryCreate, JournalEntryResponse
from helper.token import get_current_user
from models.user import User
from models.journal import JournalEntry

def create_journal(journal: JournalEntryCreate, db: db_dependency, user: User = Depends(get_current_user)) -> None:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    journal_data = JournalEntry(title=journal.title, content=journal.content, user_id=user.id, created_at=datetime.utcnow())
    db.add(journal_data)
    db.commit()
    db.refresh(journal_data)


def get_journals(db: db_dependency, user: User = Depends(get_current_user)) -> list[JournalEntryResponse]:
    return db.query(JournalEntry).filter(JournalEntry.user_id == user.id).all()
    
    

def get_journal_by_id():
    pass


def update_journal():
    pass

def delete_journal():
    pass