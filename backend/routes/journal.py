from fastapi import APIRouter, Depends, HTTPException, status
from helper.journal_logic import get_journals_all, create_journal, get_journal_by_titles , update_journal, delete_journal
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
async def get_journals(db: db_dependency, user: User = Depends(get_current_user)) -> list[JournalEntryResponse]:
    journals = get_journals_all(db, user)
    if not journals: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No jounrals found!")
    return journals        

@journal_router.get("/get-journal/{journal_title}", response_model=JournalEntryResponse)
async def get_journal_by_title(journal_title: str, 
                                db: db_dependency, 
                                user: User = Depends(get_current_user)) -> JournalEntryResponse:
    journal = get_journal_by_titles(journal_title, db, user)
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
    return journal

@journal_router.put("/update-journal/{journal_title}")
async def update_journal_entry(journal_title: str,
                                 db: db_dependency, 
                                 journal: JournalEntryCreate, 
                                 user: User = Depends(get_current_user)):
     update_journal(db, journal_title, journal, user)
     return {"detail": "Journal entry updated successfully!"}
 
@journal_router.delete("/delete-journal/{journal_title}")
async def delete_journal_entry(journal_title: str,
                                    db: db_dependency, 
                                    user: User = Depends(get_current_user)):
        response = delete_journal(journal_title, db, user)
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
        return response