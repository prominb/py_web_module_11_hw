from sqlalchemy import select

from src.contacts.models import Contact
from src.contacts.schemas import ContactsCreate, ContactsUpdate


class ContactsRepository:
    def __init__(self, session):
        self.session = session

    async def get_contacts(self, limit: int = 10, offset: int = 0):
        query = select(Contact).offset(offset).limit(limit)
        results = await self.session.execute(query)
        return results.scalars().all()

    async def create_contacts(self, contact: ContactsCreate):
        new_contact = Contact(**contact.model_dump())
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)  # To get the ID from the database
        return new_contact
    
    async def get_by_id(self, id: int):  # = 1):
        q = select(Contact).where(Contact.id == id)
        result = await self.session.execute(q)
        return result.one_or_none()

    async def search_contacts(self, query):
        q = select(Contact).filter(
            (Contact.first_name.ilike(query))
            | (Contact.last_name.ilike(query))
            | (Contact.email.ilike(query))
        )
        results = await self.session.execute(q)
        return results.scalars().all()
    
    async def update_contact(self, contact_id: int, body: ContactsUpdate):
        stmt = select(Contact).filter_by(id=contact_id)
        result = await self.session.execute(stmt)
        contact = result.scalar_one_or_none()
        if contact:
            contact.first_name = body.first_name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone_number = body.phone_number
            contact.birthday = body.birthday
            contact.additional_info = body.additional_info
            await self.session.commit()
            await self.session.refresh(contact)
        return contact

    async def delete_contact(self, contact_id):
        q = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(q)
        contact = result.scalar_one()
        await self.session.delete(contact)
        await self.session.commit()
