from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# Association table for campaign-customer targeting
campaign_customers = Table(
    "campaign_customers", Base.metadata,
    Column("campaign_id", Integer, ForeignKey("campaigns.id")),
    Column("customer_id", Integer, ForeignKey("customers.id"))
)

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sponsor_type = Column(String, nullable=False)  # 'product_group' or 'vendor'
    discount_type = Column(String, nullable=False)  # 'cart' or 'delivery'
    discount_value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    max_transactions_per_customer_per_day = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    customers = relationship("Customer", secondary=campaign_customers, back_populates="campaigns")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    campaigns = relationship("Campaign", secondary=campaign_customers, back_populates="customers")

class DiscountUsage(Base):
    __tablename__ = "discount_usages"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    used_at = Column(DateTime, default=datetime.datetime.utcnow)
