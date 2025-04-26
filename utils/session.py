import secrets
import time

def generate_session_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def check_authentication(st):
    """Check if user is authenticated using session token"""
    if st.session_state.get('authenticated'):
        # Check if session token exists and is not expired
        if st.session_state.get('session_token') and st.session_state.get('session_expiry'):
            if time.time() < st.session_state.session_expiry:
                return True
        # Clear session if token is expired or missing
        st.session_state.clear()
    return False 