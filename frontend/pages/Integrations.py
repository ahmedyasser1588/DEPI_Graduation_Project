import streamlit as st

st.set_page_config(page_title="Integrations | AgentSquad", layout="wide")

st.markdown("## Connected Enterprise Integrations")
st.caption("Manage authentication tokens and service connectors for external workspace platforms.")

col_a, col_b = st.columns(2)

with col_a:
    with st.container(border=True):
        st.markdown("### Notion Workspace Integration")
        st.write("Allows agents to export deliverables, reports, and documentation directly into specified Notion team databases.")
        st.info("Status: Active Connection (Daz Strategic Documents)")
        st.button("Configure Notion Settings", key="cfg_notion")

    with st.container(border=True):
        st.markdown("### Corporate Messaging Gateway (WhatsApp)")
        st.write("Route deliverable approvals and summary notifications directly to authorized mobile endpoints.")
        st.warning("Status: Disconnected")
        st.button("Authorize Gateway Connection", type="primary", key="cfg_whatsapp")

with col_b:
    with st.container(border=True):
        st.markdown("### Google Workspace & Drive")
        st.write("Automatically store generated PDF presentations, spreadsheets, and source archives in designated Drive folders.")
        st.warning("Status: Disconnected")
        st.button("Authorize Google Drive Access", type="primary", key="cfg_drive")

    with st.container(border=True):
        st.markdown("### Slack Operations Channel")
        st.write("Post agent status updates and completion alerts into enterprise Slack channels.")
        st.warning("Status: Disconnected")
        st.button("Connect Slack Workspace", key="cfg_slack")
