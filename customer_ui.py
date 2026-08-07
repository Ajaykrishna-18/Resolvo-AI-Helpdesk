import streamlit as st
import requests

# Professional Page Config
st.set_page_config(page_title="Resolvo | Customer Support", page_icon="🏢", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #00466a;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #00334e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🏢 Resolvo Support Portal")
st.markdown("---")
st.markdown("Welcome to the **Resolvo** helpdesk. Please submit your request below, and our system will provide an immediate resolution based on our company policies.")

# Sidebar for extra company info
with st.sidebar:
    st.header("Resolvo Inc.")
    st.write("📍 123 Tech Park, Bangalore")
    st.write("📧 support@resolvo.com")
    st.info("Our automated system handles requests 24/7. Complex issues are automatically escalated to human agents.")

# Customer Form
with st.form("ticket_form"):
    st.subheader("Submit a New Ticket")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
    with col2:
        email = st.text_input("Email Address", placeholder="e.g. rahul@example.com")
    
    issue = st.text_area("Describe your issue in detail", placeholder="Please provide order numbers or specific details...", height=150)
    
    submitted = st.form_submit_button("Submit Request")

# Form Submission Logic
if submitted:
    if name and email and issue:
        with st.spinner("Processing your request..."):
            data = {"customer_name": name, "customer_email": email, "ticket_text": issue}
            try:
                response = requests.post("http://127.0.0.1:8000/tickets/", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Ticket Successfully Submitted!")
                    
                    # Professional Response Display
                    st.markdown("### 📩 Resolution Strategy")
                    st.info(result['ai_reply'])
                    
                    st.caption(f"Ticket Category: **{result['category']}** | Tracking ID: **#{result['ticket_id']}**")
                else:
                    st.error("Failed to submit ticket. Please try again later.")
            except Exception as e:
                st.error("Could not connect to the server. Please ensure the backend is running.")
    else:
        st.warning("⚠️ Please fill out all the fields before submitting.")