import streamlit as st
from pages.auth import auth_page
from pages.real_estate import real_estate_page
from pages.buyers import buyers_page
from pages.marketers import marketers_page
from database import init_db
from pages.home import home_page
from pages.automation import automation_page
import sqlite3
from utils.session import check_authentication

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
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None
    if 'session_expiry' not in st.session_state:
        st.session_state.session_expiry = None
    
    # Check authentication status
    is_authenticated = check_authentication(st)
    
    # Sidebar navigation
    st.sidebar.title("القائمة الرئيسية")
    if is_authenticated:
        if st.sidebar.button("تسجيل الخروج"):
            st.session_state.clear()
            st.rerun()
        
        page = st.sidebar.radio(
            "اختر الصفحة",
            ["الصفحة الرئيسية", "صفحة العقارات", "صفحة المشترين", "صفحة المعلنين", "صفحة الاتمتة"]
        )
        
        if page == "الصفحة الرئيسية":
            home_page()
        elif page == "صفحة العقارات":
            real_estate_page()
        elif page == "صفحة المشترين":
            buyers_page()
        elif page == "صفحة المعلنين":
            marketers_page()
        elif page == "صفحة الاتمتة":
            automation_page()
    else:
        auth_page()

if __name__ == "__main__":
    init_db()
    main()
