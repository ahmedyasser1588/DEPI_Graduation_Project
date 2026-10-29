import streamlit as st

st.set_page_config(page_title="Create Account | AgentSquad", layout="centered")

st.markdown("""
<style>
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

st.markdown('<div class="auth-title">Create Account</div>', unsafe_allow_html=True)
st.markdown('<div class="auth-sub">Set up your enterprise profile and initial workspace</div>', unsafe_allow_html=True)

with st.form("register_form", clear_on_submit=False):
    full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
    email = st.text_input("Work Email", placeholder="name@company.com")
    workspace_name = st.text_input("Brand or Company Name", placeholder="e.g. Daz Apparel")
    password = st.text_input("Password", type="password", placeholder="Minimum 8 characters")
    terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
    
    submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)
    if submitted:
        if full_name and email and password and workspace_name and terms:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.active_workspace = workspace_name
            st.success("Account successfully created. Proceeding to Agent Marketplace...")
            st.switch_page("pages/3_Marketplace.py")
        else:
            st.error("Please fill in all required fields and accept the terms.")

st.markdown("---")
st.write("Already have an account?")
st.page_link("pages/1_Login.py", label="Sign in here")
