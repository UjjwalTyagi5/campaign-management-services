from db import models
from fastapi import HTTPException
from api.schemas.customer import CustomerCreate
from typing import List
from loguru import logger

def create_customer_helper(customer: CustomerCreate, db):
    """
    Create a new customer in the database.
    Args:
        customer (CustomerCreate): Customer data.
        db (Session): SQLAlchemy session.
    Returns:
        Customer: The created customer object.
    Raises:
        HTTPException: If creation fails.
    """
    try:
        db_customer = models.Customer(name=customer.name)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        logger.info(f"Created customer: customer_id={db_customer.id}")
        return db_customer
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create customer")


def get_customers_helper(db):
    """
    Retrieve all customers from the database.
    Args:
        db (Session): SQLAlchemy session.
    Returns:
        List[Customer]: List of customer objects.
    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        customers = db.query(models.Customer).all()
        logger.info(f"Fetched all customers, count={len(customers)}")
        return customers
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch customers")


def get_customer_helper(customer_id: int, db):
    """
    Retrieve a single customer by ID.
    Args:
        customer_id (int): Customer ID.
        db (Session): SQLAlchemy session.
    Returns:
        Customer: The customer object.
    Raises:
        HTTPException: If not found or retrieval fails.
    """
    try:
        customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not customer:
            logger.warning(f"Customer not found: customer_id={customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")
        logger.info(f"Fetched customer: customer_id={customer_id}")
        return customer
    except Exception as e:
        logger.error(f"Error fetching customer: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch customer")


def update_customer_helper(customer_id: int, customer: CustomerCreate, db):
    """
    Update an existing customer's name.
    Args:
        customer_id (int): Customer ID.
        customer (CustomerCreate): Updated customer data.
        db (Session): SQLAlchemy session.
    Returns:
        Customer: The updated customer object.
    Raises:
        HTTPException: If not found or update fails.
    """
    try:
        db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not db_customer:
            logger.warning(f"Customer not found for update: customer_id={customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")
        db_customer.name = customer.name
        db.commit()
        db.refresh(db_customer)
        logger.info(f"Updated customer: customer_id={customer_id}")
        return db_customer
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update customer")


def delete_customer_helper(customer_id: int, db):
    """
    Delete a customer by ID.
    Args:
        customer_id (int): Customer ID.
        db (Session): SQLAlchemy session.
    Returns:
        dict: Deletion confirmation message.
    Raises:
        HTTPException: If not found or deletion fails.
    """
    try:
        db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not db_customer:
            logger.warning(f"Customer not found for delete: customer_id={customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")
        db.delete(db_customer)
        db.commit()
        logger.info(f"Deleted customer: customer_id={customer_id}")
        return {"detail": "Customer deleted"}
    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete customer")