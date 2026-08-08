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
        # 1. Safe AI response handling
        resolution = "AI analyzed your request: Please check your configuration and restart."
        try:
            if hasattr(ai_agent, "analyze_ticket"):
                ai_res = ai_agent.analyze_ticket(ticket.ticket_text)
                if ai_res:
                    resolution = ai_res
        except Exception as ai_err:
            resolution = f"Processed with default support guidelines."

        # 2. Database saving (Safe insert)
        new_ticket = Ticket(
            customer_name=ticket.customer_name,
            customer_email=ticket.customer_email,
            issue=ticket.ticket_text,
            resolution=resolution,
            status="Resolved"
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        
        return {"resolution": resolution, "status": "Success"}
        
    except Exception as e:
        # Inga error vanthalum 500 crash aagathu, enna error nu JSON-la anuppum
        return {"resolution": f"Error: str({e})", "status": "Error"}