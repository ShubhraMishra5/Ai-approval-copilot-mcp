def detect_intent(user_input):

    text = user_input.lower()

    if "pending approvals" in text:
        return "pending"

    elif "dashboard summary" in text:
        return "dashboard"

    elif "approve request" in text:
        return "approve"

    elif "reject request" in text:
        return "reject"

    elif "chat history" in text:
        return "history"

    elif "status of request" in text:
        return "status"

    elif "summarize" in text:
        return "summarize"

    else:
        return "chat"
