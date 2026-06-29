from fastmcp import FastMCP
import requests
import os
import sys

from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import text

PROJECT_PATH = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "project"
)

sys.path.insert(
    0,
    str(PROJECT_PATH)
)

from app.database import SessionLocal

mcp = FastMCP(
    "Approval Copilot"
)

env_path = (
    Path(__file__).parent
    / ".env"
)

load_dotenv(
    dotenv_path=env_path
)

BASE_URL = "http://127.0.0.1:8080"

API_KEY = os.getenv(
    "API_KEY"
)

headers = {
    "api-key": API_KEY
}


@mcp.tool()
def get_pending_approvals() -> str:
    """
    Get all pending approval requests.
    """

    response = requests.get(
        f"{BASE_URL}/approval-requests?status=PENDING",
        headers=headers
    )

    if response.status_code != 200:
        return "Could not fetch pending approvals."

    data = response.json()

    if not data:
        return "No pending approvals."

    result = ""

    for item in data:
        result += (
            f"ID: {item['id']} | "
            f"Title: {item['title']} | "
            f"Priority: {item['priority']} | "
            f"Requester: {item['requester_name']}\n"
        )

    return result


@mcp.tool()
def get_dashboard_summary() -> str:
    """
    Get dashboard summary.
    """

    response = requests.get(
        f"{BASE_URL}/dashboard/summary",
        headers=headers
    )

    if response.status_code != 200:
        return "Could not fetch dashboard summary."

    data = response.json()

    return (
        f"Total Requests: {data['total_requests']}\n"
        f"Pending: {data['pending_requests']}\n"
        f"Approved: {data['approved_requests']}\n"
        f"Rejected: {data['rejected_requests']}\n"
        f"Cancelled: {data['cancelled_requests']}"
    )


@mcp.tool()
def get_request_status(
    request_id: int
) -> str:
    """
    Get status of an approval request.
    """

    response = requests.get(
        f"{BASE_URL}/approval-requests/{request_id}",
        headers=headers
    )

    if response.status_code != 200:
        return "Request not found."

    data = response.json()

    return (
        f"Request ID {data['id']} "
        f"is currently {data['status']}"
    )


@mcp.tool()
def get_request_history(
    request_id: int
) -> str:
    """
    Get request history.
    """

    response = requests.get(
        f"{BASE_URL}/approval-requests/{request_id}/history",
        headers=headers
    )

    if response.status_code != 200:
        return "Could not fetch request history."

    history = response.json()

    if not history:
        return "No history found."

    result = ""

    for item in history:
        result += (
            f"Action: {item['action']} | "
            f"{item['old_status']} → "
            f"{item['new_status']} | "
            f"Comment: {item['comment']}\n"
        )

    return result


@mcp.tool()
def approve_request(
    request_id: int
) -> str:
    """
    Approve a request.
    """

    payload = {
        "decision_comment":
        "Approved via MCP"
    }

    response = requests.put(
        f"{BASE_URL}/approval-requests/{request_id}/approve",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return "Approval failed."

    return (
        f"Request {request_id} "
        f"approved successfully."
    )


@mcp.tool()
def reject_request(
    request_id: int
) -> str:
    """
    Reject a request.
    """

    payload = {
        "decision_comment":
        "Rejected via MCP"
    }

    response = requests.put(
        f"{BASE_URL}/approval-requests/{request_id}/reject",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return "Rejection failed."

    return (
        f"Request {request_id} "
        f"rejected successfully."
    )


@mcp.tool()
def run_select_query(
    query: str
) -> str:
    """
    Execute safe SELECT queries.
    """

    query_clean = (
        query
        .strip()
        .lower()
    )

    blocked_words = [
        "drop",
        "delete",
        "update",
        "insert",
        "alter"
    ]

    if not query_clean.startswith(
        "select"
    ):
        return (
            "Only SELECT queries are allowed."
        )

    for word in blocked_words:

        if word in query_clean:
            return (
                "Unsafe query blocked."
            )

    db = SessionLocal()

    try:

        result = db.execute(
            text(query)
        )

        rows = result.fetchall()

        columns = result.keys()

        if not rows:
            return "No results found."

        output = ""

        for row in rows:

            row_dict = dict(
                zip(
                    columns,
                    row
                )
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


if __name__ == "__main__":
    mcp.run()