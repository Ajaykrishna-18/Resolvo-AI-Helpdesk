import streamlit as st
import pandas as pd
import requests
import sqlite3

# Database connection
conn = sqlite3.connect("resolvo.db", check_same_thread=False)

def init_db():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            issue TEXT,
            resolution TEXT,
            status TEXT
        )
    """)
    conn.commit()

init_db()

st.title("🎧 Resolvo: AI Helpdesk")

# Sidebar for Navigation (User vs Admin)
app_mode = st.sidebar.selectbox("Choose Mode", ["User (Raise Ticket)", "Admin (View Database)"])

if app_mode == "User (Raise Ticket)":
    st.subheader("Submit your issue to our AI Assistant")
    
    with st.form("user_ticket_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        issue = st.text_area("Describe your problem")
        submitted = st.form_submit_button("Submit Ticket")
        
        if submitted:
            if name and email and issue:
                # Unga Render backend correct URL & route path
                backend_url = "https://resolvo-ai-helpdesk.onrender.com/tickets/"
                
                # Backend-kku anuppura data (TicketCreate schema-oda match aaganum)
                payload = {
                    "customer_name": name,
                    "customer_email": email,
                    "ticket_text": issue
                }
                
                try:
                    response = requests.post(backend_url, json=payload)
                    if response.status_code == 200:
                        res_data = response.json()
                        # Backend return panra AI resolution-ah eduthurom
                        resolution = res_data.get("resolution", "AI processed your request successfully.")
                        st.success("Ticket submitted successfully and processed by AI!")
                        st.info(f"**AI Solution:** {resolution}")
                    else:
                        st.error(f"Failed to submit ticket. Server returned status: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            else:
                st.warning("Please fill all the fields.")

elif app_mode == "Admin (View Database)":
    st.subheader("🔒 Admin Login (Restricted)")
    password = st.text_input("Enter Admin Password", type="password")
    
    # Neenga mattum use panra password (e.g., "admin123")
    if password == "admin123":
        st.success("Welcome Admin!")
        
        # Database-la irukkura ellaa tickets-ahyum read panni kaattum
        try:
            df = pd.read_sql_query("SELECT * FROM tickets", conn)
            if not df.empty:
                st.dataframe(df)
            else:
                st.warning("No tickets found in database yet.")
        except Exception as e:
            st.error(f"Error loading database: {e}")
    elif password != "":
        st.error("Incorrect Password!")