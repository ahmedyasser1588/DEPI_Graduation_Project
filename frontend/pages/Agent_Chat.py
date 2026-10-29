import streamlit as st

st.set_page_config(page_title="Agent Workspace | AgentSquad", layout="wide")

# Workspace Channel Header
h_left, h_mid, h_right = st.columns([3, 1.5, 1.5])

with h_left:
    st.markdown("### Channel: dm-cole | Marketing Strategist")
    st.caption("Active Workspace: Daz Apparel • Dedicated Direct Session")

with h_mid:
    st.button("Integrate Communication Channel", help="Link channel to corporate messaging endpoint")

with h_right:
    st.button("Initialize New Task Thread", type="secondary")

st.markdown("---")

chat_main, meta_panel = st.columns([3.5, 1.5])

with chat_main:
    # Embedded Deliverable Card
    with st.container(border=True):
        st.caption("Deliverable Code: **STRAT-6** | Version: 1.0")
        st.markdown("#### Deliverable: 30-Day Growth Sprint Strategy")
        
        st.markdown("**Strategic Objective**")
        st.write(
            "Establish fit-first brand positioning, improve buyer purchase confidence, "
            "clear existing seasonal inventory at full margin, and develop the customer acquisition baseline for the upcoming drop."
        )
        
        with st.expander("Expand Deliverable Specifications"):
            st.markdown("""
            * **Phase 1 (Days 1-10)**: Publish UGC video testimonials highlighting sizing reliability.
            * **Phase 2 (Days 11-20)**: Execute targeted micro-influencer outreach with trackable promo attribution.
            * **Phase 3 (Days 21-30)**: Re-engage cart abandoners using dynamic size-assurance messaging.
            """)
            
        b1, b2, b3 = st.columns([1.5, 2, 3])
        with b1:
            if st.button("Request Revision", key="btn_rev"):
                st.info("Revision dialog opened. Specify requested edits in chat below.")
        with b2:
            if st.button("Sync to Notion Page", type="primary", key="btn_notion_sync"):
                st.success("Deliverable synced to Notion page: 'Daz Apparel Growth Strategy'.")

    # Chat Transcript
    with st.chat_message("user"):
        st.write("Please export this growth plan to the Notion strategic documents page.")

    with st.chat_message("assistant"):
        st.write(
            "The 30-Day Growth Sprint Strategy has been formatted into a structured document "
            "and synchronized to your connected Notion workspace under 'Daz Complete Marketing Strategy'."
        )

    user_query = st.chat_input("Enter command or prompt for the agent...")
    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            st.write(f"Processing instruction: '{user_query}'...")

with meta_panel:
    st.markdown("#### Session Overview")
    st.markdown("**Agent Assigned:** Cole")
    st.markdown("**Department:** Growth Marketing")
    st.markdown("**Status:** Online / Available")
    
    st.markdown("---")
    st.markdown("#### Connected Services")
    st.markdown("* Notion: **Synchronized**")
    st.markdown("* Google Drive: **Standby**")
    st.markdown("* Knowledge Base (RAG): **Indexed**")
    
    st.markdown("---")
    st.markdown("#### Deliverables Log")
    st.markdown("* `STRAT-6`: 30-Day Growth Sprint")
    st.markdown("* `COPY-3`: Drop Campaign Drafts")
    st.markdown("* `ICP-1`: Target Persona Profiles")
