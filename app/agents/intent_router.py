def classify_request(request: str) -> str:

    request = request.lower()

    analysis_keywords = [
        "analysis",
        "analyze",
        "analyse",
        "risk",
        "risky",
        "summarize",
        "summary",
        "detailed report",
        "report",
        "review",
        "review clauses",
        "analyze clauses",
        "analyse clauses",
        "clause",
        "clauses"
    ]

    for keyword in analysis_keywords:
        if keyword in request:
            return "analysis"

    return "qa"



#classifier 2 for langgraph

def classify_analysis_type(question: str) -> str:

    question = question.lower()

    if "risk" in question or "risky" in question:
        return "risk"

    if "clause" in question or "clauses" in question:
        return "reader"

    if "summary" in question or "summarize" in question:
        return "summary"

    return "summary"