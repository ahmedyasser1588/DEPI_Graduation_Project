import streamlit as st

st.set_page_config(
    page_title="AgentSquad Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Formal Corporate Styling
st.markdown("""
<style>
    .formal-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .formal-subtitle {
        font-size: 1.15rem;
        color: #475569;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    .metric-panel {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1.25rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1.5rem;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### AgentSquad Enterprise")
st.sidebar.markdown("---")

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = "founder@enterprise.com"
if "active_workspace" not in st.session_state:
    st.session_state.active_workspace = "Daz Apparel"

# Workspace Selector in Sidebar
st.sidebar.markdown("**Active Workspace**")
workspaces = ["Daz Apparel", "Alpha Financial", "Create Workspace"]
st.session_state.active_workspace = st.sidebar.selectbox(
    "Select Workspace",
    options=workspaces,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.page_link("pages/1_Login.py", label="Authentication / Sign In")
st.sidebar.page_link("pages/2_Register.py", label="Create New Account")
st.sidebar.page_link("pages/3_Marketplace.py", label="Agent Marketplace")
st.sidebar.page_link("pages/4_Agent_Chat.py", label="Direct Agent Workspace")
st.sidebar.page_link("pages/5_My_Employees.py", label="Active Workforce")
st.sidebar.page_link("pages/6_Integrations.py", label="Connected Integrations")
st.sidebar.page_link("pages/7_Pricing_Plans.py", label="Subscription Plans")

# Main Page Header
st.markdown('<div class="formal-title">Autonomous AI Workforce Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="formal-subtitle">Deploy specialized AI agents for marketing, sales outreach, financial analysis, and operational coordination directly into your business workflows.</div>',
    unsafe_allow_html=True
)

col_cta1, col_cta2, col_spacer = st.columns([1.5, 1.5, 4])
with col_cta1:
    if st.button("Explore Marketplace", type="primary", use_container_width=True):
        st.switch_page("pages/3_Marketplace.py")
with col_cta2:
    if st.button("Manage Workforce", type="secondary", use_container_width=True):
        st.switch_page("pages/5_My_Employees.py")

st.markdown("<br>", unsafe_allow_html=True)

# Performance Metrics Row
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-panel"><div class="metric-value">32</div><div class="metric-label">Certified Agents</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-panel"><div class="metric-value">1,540+</div><div class="metric-label">Connected Tools</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-panel"><div class="metric-value">99.8%</div><div class="metric-label">Execution Uptime</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-panel"><div class="metric-value">0</div><div class="metric-label">Seat Fees Required</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Feature Highlights
st.subheader("Platform Architecture")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="section-card">
        <h4>1. Specialized Roles</h4>
        <p style="color: #475569; font-size: 0.95rem;">
            Rather than generic prompts, each agent functions with a strictly scoped domain model, toolset, and structured deliverable specifications.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="section-card">
        <h4>2. Verifiable Deliverables</h4>
        <p style="color: #475569; font-size: 0.95rem;">
            Agents return structured deliverables (growth sprints, financial projections, copy blocks) containing review checkpoints and status logging.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="section-card">
        <h4>3. Tool Synchronization</h4>
        <p style="color: #475569; font-size: 0.95rem;">
            Approved outputs sync automatically to connected external platforms including Notion, Google Drive, and communication channels.
        </p>
    </div>
    """, unsafe_allow_html=True)
