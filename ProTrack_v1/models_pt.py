#Database Tables

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db_pt import DatabaseManager

class Project(DatabaseManager):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)

    p_name = Column(String)
    p_manager = Column(String)
    p_team = Column(String)
    p_segment = Column(String)
    p_type = Column(String)
    p_status = Column(String)
    p_s_date = Column(DateTime)
    p_e_date = Column(DateTime)
    job_id = Column(String)
    job_ol_id = Column(String)
    job_ra_id = Column(String)
    s_id = Column(String)
    ta_id = Column(Integer)
    pf_link = Column(String)
    b_unit = Column(String)
    b_country = Column(String)
    b_name = Column(String)
    b_name_id = Column(Integer)
    market = Column(String)
    ir = Column(Integer)
    loi = Column(Integer)
    f_deliverables = Column(Integer)
    f_currency = Column(String)
    f_revenue = Column(Integer)
    f_cost = Column(Integer)
    f_nprofit = Column(Integer)
    f_margin = Column(Integer)
    f_remarks = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class AIInsight(DatabaseManager):
    __tablename__ = "ai_reports"

    id = Column(Integer, primary_key=True, index=True)
    manager = Column(String, index=True)
    period = Column(String)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)