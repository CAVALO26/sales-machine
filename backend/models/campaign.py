from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import DeclarativeBase
import datetime

class Base(DeclarativeBase):
    pass

class Campaign(Base):
    __tablename__ = "campaigns"

    id             = Column(Integer, primary_key=True, index=True)
    product_url    = Column(String)
    niche          = Column(String)
    country        = Column(String)
    price          = Column(String)
    target         = Column(String)
    status         = Column(String, default="queued")
    headline       = Column(String,  nullable=True)
    copy_json      = Column(Text,    nullable=True)
    wp_page_url    = Column(String,  nullable=True)
    meta_campaign_id = Column(String, nullable=True)
    meta_adset_id  = Column(String,  nullable=True)
    meta_ad_id     = Column(String,  nullable=True)
    headline_score = Column(Float,   nullable=True)
    bullet_score   = Column(Float,   nullable=True)
    ctr_real       = Column(Float,   nullable=True)
    cpa_real       = Column(Float,   nullable=True)
    created_at     = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at     = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
