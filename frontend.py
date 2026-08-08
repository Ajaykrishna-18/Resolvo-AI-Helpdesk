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
                # 1. AI moolama solution generate panrathu (oruvela backend API call pannanum-na inga pannanum)
                # Inga namma simple-a oru dummy AI response allathu backend API request-ah podalam
                resolution = "AI analyzed your issue: Please restart your system and check connection." # Or fetch from backend API
                
                # 2. Database-la save panrathu
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tickets (name, email, issue, resolution, status) VALUES (?, ?, ?, ?, ?)", 
                               (name, email, issue, resolution, "Resolved"))
                conn.commit()
                
                st.success("Ticket submitted successfully! AI has generated a solution.")
                st.info(f"**AI Solution:** {resolution}")
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