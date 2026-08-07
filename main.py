from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database
from database import SessionLocal, engine
import ai_agent # <-- Namma AI file-ah inga ulla kondu varom

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resolvo Backend API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    ticket_text: str

@app.get("/")
def read_root():
    return {"message": "Resolvo Backend is Running Superbly!"}

@app.post("/tickets/")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    
    # 1. AI-kitta ticket-ah anuppi category & reply vaangurom
    ai_response = ai_agent.analyze_ticket(ticket.ticket_text)
    
    # 2. AI output-la irunthu 'Category' ayum 'Reply' ayum thaniya pirikurom
    try:
        parts = ai_response.split("Reply:")
        category_part = parts[0].replace("Category:", "").strip()
        reply_part = parts[1].strip()
    except:
        category_part = "General"
        reply_part = ai_response
        
    # 3. Database-la AI kudutha details-oda save pandrom
    new_ticket = models.Ticket(
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        ticket_text=ticket.ticket_text,
        category=category_part,           # AI kandupudicha category
        ai_generated_reply=reply_part,    # AI ezhuthuna reply
        status="Resolved" 
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    return {
        "message": "Ticket processed by AI!", 
        "ticket_id": new_ticket.id,
        "category": new_ticket.category,
        "ai_reply": new_ticket.ai_generated_reply
    }