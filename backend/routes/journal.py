from fastapi import APIRouter, Depends, HTTPException, status
from helper.journal_logic import get_journals, create_journal, get_journal_by_id, update_journal, delete_journal
from schemas.journal_schema import JournalEntryCreate, JournalEntryResponse
from database.database import db_dependency
from helper.token import get_current_user
from models.user import User


journal_router = APIRouter()

@journal_router.post("/create-journal")
async def create_journal_entry(db: db_dependency, 
                               journal: JournalEntryCreate, 
                               user: User = Depends(get_current_user)):
    journal = create_journal(journal, db, user)
    if not journal and not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create journal entry")
    
    return {"detail": "Journal entry created successfully!"}
    
@journal_router.get("/get-journals", response_model=list[JournalEntryResponse])
async def get_jounrnals(db: db_dependency, user: User = Depends(get_current_user)) -> list[JournalEntryResponse]:
    journals = get_journals(db, user)
    if not journals: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No jounrals found!")
    return journals        