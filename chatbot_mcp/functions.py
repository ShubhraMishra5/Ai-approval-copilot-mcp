import sys
from llm import client, deployment_name
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import requests
import os
from pathlib import Path
PROJECT_PATH = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "project"
)

sys.path.insert(
    0,
    str(PROJECT_PATH)
)

print(PROJECT_PATH)
from app.database import SessionLocal
from sqlalchemy import text

env_path = Path(__file__).parent / ".env"

load_dotenv(dotenv_path=env_path)

BASE_URL = "http://127.0.0.1:8080"

API_KEY = os.getenv("API_KEY")

headers = {
    "api-key": API_KEY
}


def summarize_text(text):

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize the following text "
                    "clearly and professionally."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
    )


def get_history():

    history = ""

    for msg in st.session_state.messages:

        if msg["role"] != "system":

            history += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

    return history


def get_pending_approvals():

    response = requests.get(
        f"{BASE_URL}/approval-requests"
        "?status=PENDING",
        headers=headers
    )

    if response.status_code != 200:
        return (
            "Could not fetch "
            "pending approvals."
        )

    data = response.json()

    if not data:
        return "No pending approvals."

    result = ""

    for item in data:

        result += (
            f"ID: {item['id']} | "
            f"Title: {item['title']} | "
            f"Priority: {item['priority']} | "
            f"Requester: "
            f"{item['requester_name']}\n"
        )

    return result


def get_dashboard_summary():

    response = requests.get(
        f"{BASE_URL}/dashboard/summary",
        headers=headers
    )

    if response.status_code != 200:
        return (
            "Could not fetch "
            "dashboard summary."
        )

    data = response.json()

    return (
        f"Total Requests: "
        f"{data['total_requests']}\n"
        f"Pending: "
        f"{data['pending_requests']}\n"
        f"Approved: "
        f"{data['approved_requests']}\n"
        f"Rejected: "
        f"{data['rejected_requests']}\n"
        f"Cancelled: "
        f"{data['cancelled_requests']}"
    )


def get_request_status(request_id):

    response = requests.get(
        f"{BASE_URL}/approval-requests/"
        f"{request_id}",
        headers=headers
    )

    if response.status_code != 200:
        return "Request not found."

    data = response.json()

    return (
        f"Request ID "
        f"{data['id']} "
        f"is currently "
        f"{data['status']}"
    )


def get_request_history(request_id):

    response = requests.get(
        f"{BASE_URL}/approval-requests/"
        f"{request_id}/history",
        headers=headers
    )

    if response.status_code != 200:
        return (
            "Could not fetch "
            "request history."
        )

    history = response.json()

    if not history:
        return "No history found."

    result = ""

    for item in history:

        result += (
            f"Action: {item['action']} | "
            f"{item['old_status']} → "
            f"{item['new_status']} | "
            f"Comment: "
            f"{item['comment']}\n"
        )

    return result


def approve_request(request_id):

    payload = {
        "decision_comment": (
            "Approved via chatbot"
        )
    }

    response = requests.put(
        f"{BASE_URL}/approval-requests/"
        f"{request_id}/approve",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return "Approval failed."

    return (
        f"Request {request_id} "
        f"approved successfully."
    )


def reject_request(request_id):

    payload = {
        "decision_comment": (
            "Rejected via chatbot"
        )
    }

    response = requests.put(
        f"{BASE_URL}/approval-requests/"
        f"{request_id}/reject",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return "Rejection failed."

    return (
        f"Request {request_id} "
        f"rejected successfully."
    )

def run_select_query(query):

    query_clean = query.strip().lower()

    blocked_words = [
        "drop",
        "delete",
        "update",
        "insert",
        "alter"
    ]

    if not query_clean.startswith("select"):
        return (
            "Only SELECT queries "
            "are allowed."
        )

    for word in blocked_words:

        if word in query_clean:
            return (
                "Unsafe query blocked."
            )

    db = SessionLocal()

    try:

        result = db.execute(text(query))

        rows = result.fetchall()

        columns = result.keys()

        if not rows:
            return "No results found."

        output = ""

        for row in rows:

            row_dict = dict(
                zip(columns, row)
            )

            output += (
                f"{row_dict}\n"
            )

        return output
    

    except Exception as e:

        return (
            f"Database error: {str(e)}"
        )

    finally:

        db.close() 

        
        