from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config:
        from_attributes = True

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    sponsor_type: str = Field(..., pattern="^(product_group|vendor)$")
    discount_type: str = Field(..., pattern="^(cart|delivery)$")
    discount_value: float = Field(..., gt=0)
    start_date: date
    end_date: date
    budget: float = Field(..., gt=0)
    max_transactions_per_customer_per_day: int = Field(..., gt=0)
    is_active: Optional[bool] = True
    customer_ids: Optional[List[int]] = []

    @validator('end_date')
    def end_date_after_start(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class CampaignCreate(CampaignBase):
    pass

class CampaignRead(CampaignBase):
    id: int
    customers: List[CustomerRead] = []
    class Config:
        from_attributes = True

class DiscountUsageBase(BaseModel):
    campaign_id: int
    customer_id: int

class DiscountUsageCreate(DiscountUsageBase):
    pass

class DiscountUsageRead(DiscountUsageBase):
    id: int
    used_at: str
    class Config:
        from_attributes = True


class CampaignPatch(BaseModel):
    name: Optional[str] = None
    sponsor_type: Optional[str] = Field(None, pattern="^(product_group|vendor)$")
    discount_type: Optional[str] = Field(None, pattern="^(cart|delivery)$")
    discount_value: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[float] = None
    max_transactions_per_customer_per_day: Optional[int] = None
    is_active: Optional[bool] = None
    customer_ids: Optional[List[int]] = None