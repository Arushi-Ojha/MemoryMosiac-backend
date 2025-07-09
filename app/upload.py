from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas, models, ai
from app.database import get_db

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/journal")
def create_journal(journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    new_journal = models.Journal(
        title=journal.title,
        description=journal.description,
        user_id=journal.user_id
    )
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return {"message": "Journal created", "journal_id": new_journal.id}


@router.post("/entry")
async def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    last_entry = db.query(models.Entry)\
                   .filter(models.Entry.book_id == entry.book_id)\
                   .order_by(models.Entry.page_number.desc())\
                   .first()
    next_page = 1 if not last_entry else last_entry.page_number + 1
    story = await ai.generate_beautiful_story(entry.description)

    new_entry = models.Entry(
        book_id=entry.book_id,
        page_number=next_page,
        date=datetime.utcnow().date(),
        time=datetime.utcnow().time(),
        mood=entry.mood,
        story=story
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"message": "Entry created with AI-generated story", "page_number": new_entry.page_number}
@router.get("/user-journals")
def get_user_journals(user_id: int, db: Session = Depends(get_db)):
    journals = db.query(models.Journal).filter(models.Journal.user_id == user_id).all()
    return journals

@router.get("/entry-page")
def get_entry_by_page(book_id: int, page: int, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(
        models.Entry.book_id == book_id,
        models.Entry.page_number == page
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Page not found")
    return entry
