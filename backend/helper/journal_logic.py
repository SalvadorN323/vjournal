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


def get_journals_all(db: db_dependency, user: User = Depends(get_current_user)) -> list[JournalEntryResponse]:
    return db.query(JournalEntry).filter(JournalEntry.user_id == user.id).all()
    
    

def get_journal_by_titles(title: str, db: db_dependency, user: User = Depends(get_current_user)) -> JournalEntryResponse:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    journal = db.query(JournalEntry).filter(JournalEntry.title == title).first()
    return journal


def update_journal(db: db_dependency, title: str, journal: JournalEntryCreate, user: User = Depends(get_current_user)) -> None:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    existing_journal = db.query(JournalEntry).filter(JournalEntry.title == title, JournalEntry.user_id == user.id).first()
    if not existing_journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
    
    existing_journal.title = journal.title
    existing_journal.content = journal.content
    db.commit()
    db.refresh(existing_journal)
    

def delete_journal(title: str, db: db_dependency, user: User = Depends(get_current_user)) -> dict:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    journal = db.query(JournalEntry).filter(JournalEntry.title == title).first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
    
    db.delete(journal)
    db.commit()
    return {"message": "Journal entry deleted successfully"}