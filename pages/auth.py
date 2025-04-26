import streamlit as st
from database_utils import verify_admin, register_admin

def auth_page():
    # Initialize session state variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'admin_id' not in st.session_state:
        st.session_state.admin_id = None
    
    # Check if user is already authenticated
    if st.session_state.authenticated:
        st.sidebar.success(f"مرحباً {st.session_state.username}")
        if st.sidebar.button("تسجيل الخروج"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.admin_id = None
            st.rerun()
        return
    
    st.title("تسجيل الدخول")
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        
        if st.form_submit_button("تسجيل الدخول"):
            success, admin_id = verify_admin(username, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.admin_id = admin_id
                st.success("تم تسجيل الدخول بنجاح")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    
    # Registration form
    with st.expander("تسجيل مستخدم جديد"):
        with st.form("register_form"):
            new_username = st.text_input("اسم المستخدم الجديد")
            new_password = st.text_input("كلمة المرور الجديدة", type="password")
            confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
            
            if st.form_submit_button("تسجيل"):
                if new_password != confirm_password:
                    st.error("كلمات المرور غير متطابقة")
                else:
                    success, message = register_admin(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    return st.session_state.authenticated 