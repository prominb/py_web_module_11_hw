from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.repo import ContactsRepository
from src.contacts.schemas import ContactsCreate, ContactsResponse

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


@router.get("/{id}", response_model=list[ContactsResponse])
async def search_contacts(id: int, db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    contact = await repo.get_by_id(id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} Not Found")
    return contact


@router.get("/search/", response_model=list[ContactsResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    return await repo.search_contacts(query)


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    repo = ContactsRepository(db)
    await repo.delete_contact(contact_id)
    return {"message": f"Contact {contact_id} deleted"}
