tools = [

    {
        "type": "function",
        "function": {
            "name": "get_pending_approvals",
            "description": (
                "Get all pending approval requests"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_dashboard_summary",
            "description": (
                "Get dashboard analytics summary"
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_request_status",
            "description": (
                "Get status of an approval request"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "integer",
                        "description": (
                            "Approval request ID"
                        )
                    }
                },
                "required": ["request_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_request_history",
            "description": (
                "Get approval request history"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "integer"
                    }
                },
                "required": ["request_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "approve_request",
            "description": (
                "Approve an approval request"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "integer"
                    }
                },
                "required": ["request_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "reject_request",
            "description": (
                "Reject an approval request"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "integer"
                    }
                },
                "required": ["request_id"]
            }
        }
    },

    {
    "type": "function",
    "function": {
        "name": "run_select_query",
        "description": (
            "Run SQL SELECT queries "
            "on the approval database"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    }
}

]