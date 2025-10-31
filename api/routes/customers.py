from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import db_instance
from db import models
from api.schemas.customer import CustomerCreate, CustomerRead
from typing import List
from api.dependencies.customers import create_customer_helper, get_customers_helper, get_customer_helper, update_customer_helper, delete_customer_helper

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate, db: Session = Depends(db_instance.get_db)):
    return create_customer_helper(customer, db)

@router.get("/", response_model=List[CustomerRead])
def get_customers(db: Session = Depends(db_instance.get_db)):
    return get_customers_helper(db)

@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(db_instance.get_db)):
    return get_customer_helper(customer_id, db)

@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(db_instance.get_db)):
    return update_customer_helper(customer_id, customer, db)

@router.delete("/{customer_id}", response_model=dict)
def delete_customer(customer_id: int, db: Session = Depends(db_instance.get_db)):
    return delete_customer_helper(customer_id, db)
