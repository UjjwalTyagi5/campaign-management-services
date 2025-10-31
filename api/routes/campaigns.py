from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import db_instance
from db import models
from api.schemas.campaign import CampaignCreate, CampaignRead,CampaignPatch
from typing import List
from api.dependencies.campaigns import create_campaign_helper, update_campaign_fields, get_available_campaigns_helper, get_single_campaign_helper, delete_campaign_helper, patch_campaign_helper

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

# Create campaign
@router.post("/", response_model=CampaignRead)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(db_instance.get_db)):
    return create_campaign_helper(campaign, db)

# Read all campaigns
@router.get("/", response_model=List[CampaignRead])
def get_campaigns(db: Session = Depends(db_instance.get_db)):
    return db.query(models.Campaign).all()

# GET endpoint to fetch available discount campaigns based on cart parameters
@router.get("/available", response_model=List[CampaignRead])
def get_available_campaigns(discount_type: str, customer_id: int, db: Session = Depends(db_instance.get_db)):
    return get_available_campaigns_helper(discount_type, customer_id, db)

# Read single campaign
@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(campaign_id: int, db: Session = Depends(db_instance.get_db)):
    return get_single_campaign_helper(campaign_id, db)

# Delete campaign
@router.delete("/{campaign_id}", response_model=dict)
def delete_campaign(campaign_id: int, db: Session = Depends(db_instance.get_db)):
    return delete_campaign_helper(campaign_id, db)

# update campaign
@router.patch("/{campaign_id}", response_model=CampaignRead)
def patch_campaign(campaign_id: int, patch: CampaignPatch, db: Session = Depends(db_instance.get_db)):
    return patch_campaign_helper(campaign_id, patch, db)
