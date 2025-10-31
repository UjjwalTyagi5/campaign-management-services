import datetime
from sqlalchemy.orm import Session
from db import models
from fastapi import HTTPException
from api.schemas.campaign import CampaignCreate, CampaignPatch
from loguru import logger

def update_campaign_fields(db_campaign: models.Campaign, patch_data: dict, db: Session):
    """
    Update fields of a campaign with patch data.
    Args:
        db_campaign (Campaign): The campaign object to update.
        patch_data (dict): Fields to update.
        db (Session): SQLAlchemy session.
    Returns:
        Campaign: The updated campaign object.
    Raises:
        HTTPException: If update fails.
    """
    try:
        for field, value in patch_data.items():
            if field == "customer_ids" and value is not None:
                db_campaign.customers = db.query(models.Customer).filter(models.Customer.id.in_(value)).all()
            elif field in ["start_date", "end_date"] and value is not None:
                db_campaign.__setattr__(field, datetime.date.fromisoformat(value))
            elif value is not None:
                db_campaign.__setattr__(field, value)
        db.commit()
        db.refresh(db_campaign)
        logger.info(f"Updated campaign fields for campaign_id={db_campaign.id}")
        return db_campaign
    except Exception as e:
        logger.error(f"Error updating campaign fields: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update campaign fields")

def get_available_campaigns_helper(discount_type: str, customer_id: int, db):
    """
    Fetch available campaigns for a customer and discount type.
    Args:
        discount_type (str): Type of discount ('cart' or 'delivery').
        customer_id (int): Customer ID.
        db (Session): SQLAlchemy session.
    Returns:
        List[Campaign]: List of available campaigns.
    Raises:
        HTTPException: If fetch fails.
    """
    try:
        today = datetime.date.today()
        campaigns = db.query(models.Campaign).filter(
            models.Campaign.discount_type == discount_type,
            models.Campaign.is_active == True,
            models.Campaign.start_date <= today,
            models.Campaign.end_date >= today,
            models.Campaign.customers.any(models.Customer.id == customer_id)
        ).all()
        logger.info(f"Fetched available campaigns for customer_id={customer_id}, discount_type={discount_type}")
        return campaigns
    except Exception as e:
        logger.error(f"Error fetching available campaigns: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch available campaigns")

def get_single_campaign_helper(campaign_id: int, db):
    """
    Retrieve a single campaign by ID.
    Args:
        campaign_id (int): Campaign ID.
        db (Session): SQLAlchemy session.
    Returns:
        Campaign: The campaign object.
    Raises:
        HTTPException: If not found or fetch fails.
    """
    try:
        campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
        if not campaign:
            logger.warning(f"Campaign not found: campaign_id={campaign_id}")
            raise HTTPException(status_code=404, detail="Campaign not found")
        logger.info(f"Fetched campaign: campaign_id={campaign_id}")
        return campaign
    except Exception as e:
        logger.error(f"Error fetching campaign: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch campaign")

def delete_campaign_helper(campaign_id: int, db):
    """
    Delete a campaign by ID.
    Args:
        campaign_id (int): Campaign ID.
        db (Session): SQLAlchemy session.
    Returns:
        dict: Deletion confirmation message.
    Raises:
        HTTPException: If not found or deletion fails.
    """
    try:
        db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
        if not db_campaign:
            logger.warning(f"Campaign not found for delete: campaign_id={campaign_id}")
            raise HTTPException(status_code=404, detail="Campaign not found")
        db.delete(db_campaign)
        db.commit()
        logger.info(f"Deleted campaign: campaign_id={campaign_id}")
        return {"detail": "Campaign deleted"}
    except Exception as e:
        logger.error(f"Error deleting campaign: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete campaign")

def create_campaign_helper(campaign: CampaignCreate, db):
    """
    Create a new campaign in the database.
    Args:
        campaign (CampaignCreate): Campaign data.
        db (Session): SQLAlchemy session.
    Returns:
        Campaign: The created campaign object.
    Raises:
        HTTPException: If creation fails.
    """
    try:
        db_campaign = models.Campaign(
            name=campaign.name,
            sponsor_type=campaign.sponsor_type,
            discount_type=campaign.discount_type,
            discount_value=campaign.discount_value,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            budget=campaign.budget,
            max_transactions_per_customer_per_day=campaign.max_transactions_per_customer_per_day,
            is_active=campaign.is_active
        )
        if campaign.customer_ids:
            db_campaign.customers = db.query(models.Customer).filter(models.Customer.id.in_(campaign.customer_ids)).all()
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        logger.info(f"Created campaign: campaign_id={db_campaign.id}")
        return db_campaign
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create campaign")

def patch_campaign_helper(campaign_id: int, patch: CampaignPatch, db: Session):
    """
    Patch (partially update) a campaign by ID.
    Args:
        campaign_id (int): Campaign ID.
        patch (CampaignPatch): Patch data.
        db (Session): SQLAlchemy session.
    Returns:
        Campaign: The updated campaign object.
    Raises:
        HTTPException: If not found or update fails.
    """
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not db_campaign:
        logger.warning(f"Campaign not found for patch: campaign_id={campaign_id}")
        raise HTTPException(status_code=404, detail="Campaign not found")
    patch_data = patch.dict(exclude_unset=True)
    return update_campaign_fields(db_campaign, patch_data, db)