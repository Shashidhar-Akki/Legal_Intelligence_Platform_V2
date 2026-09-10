from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


def risk(state):

    context = state["context"]

    prompt = f"""
    You are a legal document analysis assistant.

    Analyze only the legal document context provided below.

    Identify potential legal risks, weaknesses, adverse findings,
    and other important legal concerns that are supported by the context.

    For each significant concern, explain:
    1. What the concern is
    2. What information in the context supports it
    3. Why it may be important

    Rules:
    - Use only information present in the provided context.
    - Do not invent facts, allegations, legal provisions, or risks.
    - Distinguish between an actual finding and a potential concern.
    - If no significant risk is identifiable from the provided context, say so.
    - Do not present your analysis as legal advice.

    Document context:
    {context}
    """

    response = llm.invoke(prompt)

    return {
        "risk_result": response.content
    }