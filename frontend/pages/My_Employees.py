import streamlit as st

st.set_page_config(page_title="Active Workforce | AgentSquad", layout="wide")

st.markdown("## Active AI Workforce")
st.caption("Review and manage specialized agents currently provisioned for workspace: **Daz Apparel**")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### Cole | Marketing & Growth Strategist")
        st.caption("Department: Marketing • Deployment Date: September 2026 • Status: Active")
        st.write("Responsible for growth sprint design, acquisition channels, and Notion document sync.")
        st.markdown("**Current Task Focus:** `30-Day Seasonal Growth Strategy`")
        st.button("Open Channel (dm-cole)", type="primary", key="open_cole", use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("### Lily | Content & Visual Designer")
        st.caption("Department: Design & Creative • Deployment Date: September 2026 • Status: Active")
        st.write("Produces social copy, creative asset specifications, and campaign visuals.")
        st.markdown("**Current Task Focus:** `Lookbook Social Media Campaign`")
        st.button("Open Channel (dm-lily)", type="secondary", key="open_lily", use_container_width=True)

st.markdown("---")
st.page_link("pages/3_Marketplace.py", label="Deploy Additional Agents from Marketplace")
