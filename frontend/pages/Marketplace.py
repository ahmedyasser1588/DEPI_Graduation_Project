import streamlit as st

st.set_page_config(page_title="AI Employees Marketplace | AgentSquad", layout="wide")

st.markdown("## AI Employees Marketplace")
st.caption("Browse, inspect, and hire specialized AI employees for your company.")

col_filters, col_catalog = st.columns([1, 3.2])

with col_filters:
    st.markdown("#### Role Categories")
    st.button("Reset Filters", use_container_width=True)
    
    st.markdown("**Core & Hireable**")
    st.checkbox("AI Cofounder / Orchestrator", value=True)
    st.checkbox("Marketing Specialist", value=True)
    st.checkbox("Sales Specialist", value=True)
    st.checkbox("Market & Customer Researcher", value=True)
    st.checkbox("Financial Analyst", value=True)
    st.checkbox("Pitch Advisor", value=True)
    
    st.markdown("---")
    st.markdown("**Commercial Role**")
    st.radio("Role Filter", ["All Roles", "Core (Included)", "Hireable ($5/mo)"], label_visibility="collapsed")

with col_catalog:
    st.markdown("#### Available Agent Team")
    
    # 1. AI Cofounder / Orchestrator
    with st.container(border=True):
        c_meta, c_actions = st.columns([4, 1.3])
        with c_meta:
            st.markdown("### Alex | AI Cofounder / Orchestrator")
            st.caption("Commercial Role: Always Available / Core • Rating: 5.0/5.0")
            st.write("**Primary Responsibility:** Company-wide reasoning, coordination, delegation, memory and synthesis.")
            st.markdown("`Company Reasoning` `Team Coordination` `Delegation` `Memory Synthesis`")
        with c_actions:
            st.markdown("**Included** in Platform")
            if st.button("Open Workspace", key="open_alex", type="primary", use_container_width=True):
                st.switch_page("pages/4_Agent_Chat.py")

    # 2. Marketing Specialist
    with st.container(border=True):
        c_meta, c_actions = st.columns([4, 1.3])
        with c_meta:
            st.markdown("### Nora | Marketing Specialist")
            st.caption("Commercial Role: Hireable • Rating: 5.0/5.0")
            st.write("**Primary Responsibility:** Marketing strategy, content, campaigns and approved social execution.")
            st.markdown("`Marketing Strategy` `Content Calendars` `Campaign Concepts` `Social Execution`")
        with c_actions:
            st.markdown("**$5.00** / month")
            st.button("Hire Nora", key="hire_nora", type="secondary", use_container_width=True)

    # 3. Sales Specialist
    with st.container(border=True):
        c_meta, c_actions = st.columns([4, 1.3])
        with c_meta:
            st.markdown("### Karim | Sales Specialist")
            st.caption("Commercial Role: Hireable • Rating: 4.9/5.0")
            st.write("**Primary Responsibility:** Sales strategy and, as an explored capability, approved AI sales calls.")
            st.markdown("`Sales Strategy` `Discovery Playbooks` `Objection Handling` `Outbound Scripts`")
        with c_actions:
            st.markdown("**$5.00** / month")
            st.button("Hire Karim", key="hire_karim", type="secondary", use_container_width=True)

    # 4. Market & Customer Researcher
    with st.container(border=True):
        c_meta, c_actions = st.columns([4, 1.3])
        with c_meta:
            st.markdown("### Tarek | Market & Customer Researcher")
            st.caption("Commercial Role: Hireable • Rating: 4.9/5.0")
            st.write("**Primary Responsibility:** Market, competitors, customers, ICPs, personas, pain points and validation.")
            st.markdown("`Market Sizing` `Competitor Benchmarking` `ICPs & Personas` `Customer Validation`")
        with c_actions:
            st.markdown("**$5.00** / month")
            st.button("Hire Tarek", key="hire_tarek", type="secondary", use_container_width=True)

    # 5. Financial Analyst
    with st.container(border=True):
        c_meta, c_actions = st.columns([4, 1.3])
        with c_meta:
            st.markdown("### Salma | Financial Analyst")
            st.caption("Commercial Role: Hireable • Rating: 4.8/5.0")
            st.write("**Primary Responsibility:** Advanced startup financial analysis, modeling and scenarios.")
            st.markdown("`Revenue Modeling` `Unit Economics (CAC/LTV)` `Runway Analysis` `Sensitivity`")
        with c_actions:
            st.markdown("**$5.00** / month")
            st.button("Hire Salma", key="hire_salma", type="secondary", use_container_width=True)

    # 6. Pitch Advisor
    with st.container(border=True):
        c_meta, c_actions = st.columns([4, 1.3])
        with c_meta:
            st.markdown("### Youssef | Pitch Advisor")
            st.caption("Commercial Role: Hireable • Rating: 5.0/5.0")
            st.write("**Primary Responsibility:** Pitch strategy, pitch-deck generation/review and investor preparation.")
            st.markdown("`Pitch Strategy` `Deck Generation` `Slide Review` `Investor Q&A`")
        with c_actions:
            st.markdown("**$5.00** / month")
            st.button("Hire Youssef", key="hire_youssef", type="secondary", use_container_width=True)
