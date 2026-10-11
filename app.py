"""
AI Agents, Tools & Automation - Module 5
Streamlit Application - Main Entry Point
"""

import streamlit as st
from agent import AIAgent

# Page Configuration
st.set_page_config(
    page_title="AI Agent - Module 5",
    page_icon="🤖",
    layout="wide"
)

# Initialize Agent in Session State (State Management)
if "agent" not in st.session_state:
    st.session_state.agent = AIAgent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header
st.title("🤖 AI Agents, Tools & Automation")
st.markdown("### Module 5 | Day 21-25 | High Priority")
st.info("**Agent Workflow:** Understand Task → Decide Action → Use Tool → Process Result → Respond | This is how AI Agents differ from Chatbots.")

# Sidebar - Agent State & Memory Dashboard
with st.sidebar:
    st.header("🧠 Agent Memory & State")
    st.metric("Tasks Completed", st.session_state.agent.state["tasks_completed"])
    st.metric("Tools Used", len(st.session_state.agent.state["tools_used"]))
    
    if st.session_state.agent.state["tools_used"]:
        st.write("**Recent Tools:**")
        for tool in st.session_state.agent.state["tools_used"][-5:]:
            st.code(tool)

    st.divider()
    st.subheader("🛠️ Available Tools")
    st.markdown("""
    - **Calculator:** Function Calling
    - **Weather API:** External API Integration
    - **ToDo Manager:** State Management
    - **Email Drafter:** Workflow Automation
    """)

    st.divider()
    if st.button("🗑️ Clear Agent Memory", use_container_width=True):
        st.session_state.agent = AIAgent()
        st.session_state.chat_history = []
        st.rerun()

# Chat Interface
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

if user_prompt := st.chat_input("Ask your AI Agent to use a tool..."):
    # User message
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Agent processing
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent is thinking... Understanding task and deciding action..."):
            understanding = st.session_state.agent.understand_task(user_prompt)
            tool_name, params = st.session_state.agent.decide_action(understanding)
            tool_result = st.session_state.agent.execute_tool(tool_name, params)
            final_response = st.session_state.agent.generate_response(understanding, tool_result)
            
            st.markdown(final_response)
            st.session_state.chat_history.append({"role": "assistant", "content": final_response})

# Footer
st.divider()
st.caption("Module 5 Project | Demonstrates AI Agents, Tool Calling, State Management, and Multi-step Workflows | Built with Pure Python")