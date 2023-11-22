from datetime import date, timedelta, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])



@router.get("/", response_model=List[ContactResponse], name="Get all contacts")
async def get_contacts(limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_all_contacts(limit, offset, db)
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, name = "Create contact")
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.get("/id/{contact_id}", response_model=ContactResponse, name="Find contact")
async def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID={contact_id} not found")
    return contact


@router.get("/firstname/{contact_name}", response_model=list[ContactResponse], name="Find contact by firstname")
async def get_contact_by_firstname(contact_firstname: str, limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_firstname(contact_firstname, limit, offset, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contacts with name {contact_firstname} not found")
    return contacts

@router.get("/lastname/{contact_lastname}", response_model=list[ContactResponse], name="Find contact by lastname")
async def get_contact_by_lastname(contact_lastname: str, limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_lastname(contact_lastname, limit, offset, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contacts with lastname {contact_lastname} not found")
    return contacts

@router.get("/email/{contact_email}", response_model=ContactResponse, name="Find contact by email")
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with email {contact_email} not found")
    return contact


@router.get("/birthday/{contact_birthday}", response_model=list[ContactResponse], name="Find contact by birthday")
async def get_contacts_birthday(contact_birthday: str, limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_birthday(contact_birthday, limit, offset, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found contacts with birthday in {contact_birthday}")
    return contacts



@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if get_contact_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {contact_id} not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, name = 'Delete contact by ID')
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID={contact_id} not found")
    return contact


@router.get("/birthdays_in_next_week", response_model=list[ContactResponse], name="Find contact by birthday in next week")
async def get_birthdays_in_next_week(limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_birthdays_in_next_week(limit, offset, db)
    if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No contacts birthday in this period")
    return contact