 # 🤖 AI Agent with Tools & Automation

> **Module 5: Day 21 - 25 | High Priority**
> A production-ready implementation of an Autonomous AI Agent demonstrating Tool Calling, State Management, and Multi-step Workflows.

### 🔗 Live Links
- **GitHub Repository:** https://github.com/sivasankari-v/ai-agent-tools-automation
- **Live Demo:** (Add your Streamlit Cloud link after deployment)

---
### 📌 Project Overview
This project implements an autonomous AI Agent that goes beyond a chatbot. While a chatbot only generates text responses, this agent can **decide which tool to use, execute the tool, observe the result, and respond**.

This is the core architecture used in modern Agentic AI like OpenAI Function Calling.

### 🏗️ System Architecture
```mermaid
graph LR
    A[User Input] --> B[1. Understand Task]
    B --> C[2. Decide Action]
    C --> D[3. Use Tool]
    D --> E[4. Process Result]
    E --> F[5. Respond]
    F --> A