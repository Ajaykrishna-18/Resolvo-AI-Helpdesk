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
    try:
        # AI call-ah try panrom
        ai_response = ai_agent.analyze_ticket(ticket.ticket_text)
        resolution = ai_response if ai_response else "Default resolution."
        
        # Database insert logic inga irukkum...
        new_ticket = Ticket(
            customer_name=ticket.customer_name,
            customer_email=ticket.customer_email,
            issue=ticket.ticket_text,
            resolution=resolution,
            status="Resolved"
        )
        db.add(new_ticket)
        db.commit()
        
        return {"resolution": resolution, "status": "Success"}
        
    except Exception as e:
        # Inga enna error nu print pannum, appo Render logs-la exact error theriyum
        print(f"CRASH ERROR: {str(e)}")
        return {"resolution": f"Error occurred: {str(e)}", "status": "Failed"}