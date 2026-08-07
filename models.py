from sqlalchemy import Column, Integer, String, Text
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    customer_email = Column(String)
    ticket_text = Column(Text) # Customer type pandra problem
    category = Column(String, default="Uncategorized") # AI kandu pudikkum category
    status = Column(String, default="Open") # Resolved or Escalated
    ai_generated_reply = Column(Text, nullable=True) # AI ezhuthura reply