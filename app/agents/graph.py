from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.reader_agent import reader
from app.agents.risk_agent import risk
from app.agents.summarizer_agent import summary


class State(TypedDict, total=False):

    context: str
    analysis_type: str

    reader_result: str
    risk_result: str
    summary_result: str


builder = StateGraph(State)

builder.add_node("reader", reader)
builder.add_node("risk", risk)
builder.add_node("summary", summary)


builder.add_conditional_edges(
    START,
    lambda state: state["analysis_type"], # replaced the route analysis function because there is already a rpoter in intent router
    {
        "reader": "reader",
        "summary": "summary",
        "risk": "risk"
    }
)


builder.add_edge("reader", END)
builder.add_edge("risk", END)
builder.add_edge("summary", END)


graph = builder.compile()