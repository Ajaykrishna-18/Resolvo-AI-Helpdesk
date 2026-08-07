import os
from groq import Groq
from dotenv import load_dotenv
import rag_engine # <-- Pudhusa create panna RAG file-ah ulla kondu varom

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Server start aagumbothe policies-ah database-la load pannidurom
rag_engine.load_policies_to_db()

def analyze_ticket(ticket_text: str):
    
    # 1. RAG: Ticket-ku thevayana policy-ah ChromaDB-la irunthu edukkurom
    relevant_policy = rag_engine.get_relevant_policy(ticket_text)

    # 2. AI-ku thevayana instruction + Policy rendu thiyum kudukurom
    system_prompt = f"""
    You are an AI customer support agent. 
    Here is the exact company policy: {relevant_policy}
    
    Read the user's ticket and do two things:
    1. Categorize it into one of these: Refund, Delivery, Technical, General.
    2. Draft a polite reply based STRICTLY on the provided company policy. Do not make up any rules.
    
    Format your response EXACTLY like this:
    Category: [Your Category]
    Reply: [Your Reply]
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ticket_text}
        ],
        model="llama-3.3-70b-versatile", 
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content