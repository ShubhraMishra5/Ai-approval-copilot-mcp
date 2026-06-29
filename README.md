# AI Approval Copilot (MCP Enabled)

AI Approval Copilot (MCP Enabled) is an advanced LLM-powered assistant that uses Model Context Protocol (MCP) to interact with backend services through structured tools.

It enables natural language interaction with an approval management system, allowing users to query requests, perform actions (approve/reject), and fetch analytics using tool-based execution.

---

## Features

- MCP-based tool execution layer
- LLM-powered conversational interface (Streamlit)
- Dynamic tool discovery and invocation
- Approval workflow actions:
  - Approve / Reject requests
- Fetch real-time data:
  - Pending approvals
  - Request status & history
  - Dashboard summary
- SQL query execution (safe SELECT only)
- Async MCP client-server communication

---

## Tech Stack

- Python
- FastAPI (backend API)
- Streamlit (chat UI)
- Azure OpenAI (LLM)
- FastMCP (Model Context Protocol)
- SQLAlchemy
- SQLite

