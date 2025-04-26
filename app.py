import streamlit as st
from pages.auth import auth_page
from pages.real_estate import real_estate_page
from pages.buyers import buyers_page
from pages.marketers import marketers_page
from database import init_db
import sqlite3

# Set page config globally
st.set_page_config(
    page_title="AqarDash",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'admin_id' not in st.session_state:
        st.session_state.admin_id = None
    
    # Sidebar navigation
    st.sidebar.title("القائمة الرئيسية")
    if st.session_state.authenticated:
        if st.sidebar.button("تسجيل الخروج"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.admin_id = None
            st.rerun()
        
        page = st.sidebar.radio(
            "اختر الصفحة",
            ["العقارات", "المشترين", "المسوقين"]
        )
        
        if page == "العقارات":
            real_estate_page()
        elif page == "المشترين":
            buyers_page()
        elif page == "المسوقين":
            marketers_page()
    else:
        auth_page()

if __name__ == "__main__":
    init_db()
    main()
