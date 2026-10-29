import streamlit as st

st.set_page_config(page_title="Subscription Plans | AgentSquad", layout="wide")

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="font-weight: 700; color: #0F172A;">Enterprise Pricing Structure</h2>
    <p style="color: #64748B; font-size: 1.1rem;">
        Workforce billing calibrated to output capacity rather than per-seat licensing.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("#### Starter Tier")
        st.markdown("# $0 <span style='font-size: 1rem; color: #64748B;'>/ month</span>", unsafe_allow_html=True)
        st.write("Baseline environment for small project teams.")
        st.markdown("---")
        st.markdown("* Provision up to 2 Concurrent Agents")
        st.markdown("* Standard Execution Latency")
        st.markdown("* Markdown & Text Deliverables")
        st.markdown("* Standard Knowledge Base (RAG) Index")
        st.button("Current Active Plan", disabled=True, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("#### Flexible Workforce")
        st.markdown("# $5 <span style='font-size: 1rem; color: #64748B;'>/ agent / month</span>", unsafe_allow_html=True)
        st.write("Scalable capacity for expanding businesses.")
        st.markdown("---")
        st.markdown("* 2 Baseline Agents Included Free")
        st.markdown("* $5.00/mo per additional deployed specialist")
        st.markdown("* Notion & Google Drive Connectors Included")
        st.markdown("* High Priority Processing Pipeline")
        st.button("Select Flexible Plan", type="primary", use_container_width=True)

with col3:
    with st.container(border=True):
        st.markdown("#### Unlimited Enterprise")
        st.markdown("# $50 <span style='font-size: 1rem; color: #64748B;'>/ month</span>", unsafe_allow_html=True)
        st.write("Comprehensive workforce deployment across all departments.")
        st.markdown("---")
        st.markdown("* Unlimited Agent Deployments")
        st.markdown("* Full Access to 30+ Role Catalog")
        st.markdown("* Multi-Workspace Centralized Administration")
        st.markdown("* Custom Agent Prompt Architect Tool")
        st.button("Upgrade to Enterprise", use_container_width=True)
