import streamlit as st
import pandas as pd
import sqlite3
from database import init_db
init_db()  # App start aagum pothu table create aagum

# Page setup
st.set_page_config(page_title="Resolvo Dashboard", layout="wide")
st.title("🎧 Resolvo: AI Agent Dashboard")
st.write("Welcome, Support Agent! Here are the tickets processed by our AI.")

# Database-la irunthu data edukkurom
@st.cache_data(ttl=5)
def load_data():
    try:
        init_db()
        return pd.read_sql_query("SELECT * FROM tickets", conn)
    except Exception as e:
        # Table innum illana oru empty dataframe-ah return pannum
        return pd.DataFrame(columns=["id", "issue", "status", "resolution"])

df = load_data()

if not df.empty:
    # Chinna chinna stats kaatom
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", len(df))
    col2.metric("AI Resolved", len(df[df['status'] == 'Resolved']))
    col3.metric("Escalated to Human", len(df[df['status'] == 'Escalated']))

    st.markdown("---")
    st.subheader("All Tickets")
    # Table-ah display pandrom
    st.dataframe(df[['id', 'customer_name', 'category', 'status']], use_container_width=True)
    
    st.markdown("---")
    st.subheader("Ticket Deep Dive")
    # Oru ticket-ah select panni full details paarkalam
    selected_id = st.selectbox("Select Ticket ID to review:", df['id'])
    ticket_data = df[df['id'] == selected_id].iloc[0]
    
    st.write(f"**Customer:** {ticket_data['customer_name']} | **Email:** {ticket_data['customer_email']}")
    st.write(f"**Category:** {ticket_data['category']} | **Status:** {ticket_data['status']}")
    st.warning(f"**Customer Problem:** {ticket_data['ticket_text']}")
    st.success(f"**AI Generated Reply:** \n\n{ticket_data['ai_generated_reply']}")

else:
    st.info("No tickets in the database yet. Go to FastAPI Swagger UI and create one!")