from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.repo import ContactsRepository
from src.contacts.schemas import ContactsCreate, ContactsResponse, ContactsUpdate

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": "pong"}


@router.get("/", response_model=list[ContactsResponse])
async def get_contacts(
    limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    repo = ContactsRepository(db)
    return await repo.get_contacts(limit, offset)


@router.post("/", response_model=ContactsResponse)
async def create_contacts(contact: ContactsCreate, db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    return await repo.create_contacts(contact)


@router.get("/birthdays", response_model=list[ContactsResponse])
async def get_birthdays(days: int = Query(default=7, ge=7), db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    # contacts = await repo.get_birthdays(days, db)
    # return contacts
    return await repo.get_birthdays(days)


@router.get("/{id}", response_model=ContactsResponse)
async def get_by_id(id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    contact = await repo.get_by_id(id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} Not Found")
    return contact


@router.get("/search/", response_model=list[ContactsResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    return await repo.search_contacts(query)


@router.put("/update_contact/{id}", response_model=ContactsResponse)
async def update_contact(body: ContactsUpdate, id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    upd_contact = await repo.update_contact(id, body)
    if upd_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} Not Found")
    return upd_contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    await repo.delete_contact(contact_id)
    return {"message": f"Contact {contact_id} deleted"}
