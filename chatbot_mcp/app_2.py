import streamlit as st
import json
import asyncio
from fastmcp import Client

from llm import (
    client,
    deployment_name
)

from tools import tools


st.set_page_config(
    page_title="AI Approval Copilot",
    layout="centered"
)

st.title("AI Approval Copilot")
async def call_mcp_tool(
    tool_name,
    arguments
):

    async with Client(
        "mcp_server.py"
    ) as mcp_client:

        result = await mcp_client.call_tool(
            tool_name,
            arguments
        )

        return str(result.data)

DATABASE_SCHEMA = """

Table: approval_requests

Columns:
- id
- title
- status
- priority
- requester_name
- department
- created_at

"""

SYSTEM_PROMPT = f"""



You are an AI approval copilot.

For decision-making questions:

1. Consider approving.
2. Consider rejecting.
3. Consider escalating.
4. Evaluate pros and cons of each.
5. Recommend the best option.

Use tools whenever information is needed.

Database schema:

{DATABASE_SCHEMA}

"""

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

with st.sidebar:

    st.header("⚙️ Settings")

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7
    )

    if st.button("Clear Chat"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()

for msg in st.session_state.messages[1:]:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

prompt = st.chat_input(
    "Type your message"
)

if prompt:

    with st.chat_message(
        "user",
        avatar="👨"
    ):

        st.write(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Thinking..."):

            try:

                response = (
                    client.chat.completions.create(
                        model=deployment_name,
                        messages=(
                            st.session_state.messages
                        ),
                        tools=tools,
                        tool_choice="auto",
                        temperature=temperature
                    )
                )

                message = (
                    response
                    .choices[0]
                    .message
                )

                

                if message.tool_calls:

                    tool_call = (
                        message.tool_calls[0]
                    )

                    function_name = (
                        tool_call.function.name
                    )

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    st.sidebar.write(
                        f"Tool Used: "
                        f"{function_name}"
                    )

                    

                    reply = asyncio.run(
                      call_mcp_tool(
                          function_name,
                            arguments
)
)

                

                else:

                    reply = message.content

                st.write(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )