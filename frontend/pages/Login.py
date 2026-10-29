import streamlit as st

st.set_page_config(page_title="Sign In | AgentSquad", layout="centered")

st.markdown("""
<style>
    .auth-container {
        max-width: 420px;
        margin: 2rem auto;
        padding: 2rem;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }
    .auth-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .auth-sub {
        font-size: 0.95rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="auth-title">Sign In</div>', unsafe_allow_html=True)
st.markdown('<div class="auth-sub">Enter your credentials to access your organization workspace</div>', unsafe_allow_html=True)

with st.form("login_form", clear_on_submit=False):
    email = st.text_input("Business Email Address", placeholder="name@company.com")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    remember_me = st.checkbox("Remember this session")
    
    submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)
    if submitted:
        if email and password:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.success("Authentication successful. Redirecting to workspace...")
            st.switch_page("pages/3_Marketplace.py")
        else:
            st.error("Please provide both valid email and password.")

st.markdown("---")
c_left, c_right = st.columns(2)
with c_left:
    st.page_link("pages/2_Register.py", label="Create an account")
with c_right:
    st.markdown("<div style='text-align: right;'><a href='#'>Forgot password?</a></div>", unsafe_allow_html=True)
