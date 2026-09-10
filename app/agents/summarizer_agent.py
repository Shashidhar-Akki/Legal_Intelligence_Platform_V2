from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


def summary(state):

    context = state["context"]
    
    prompt = f"""
    You are a legal document summarization assistant.

    Prepare a structured summary using only the legal document
    context provided below.

    Include, where available:

    1. Parties
    2. Important facts
    3. Legal issues
    4. Arguments
    5. Findings
    6. Decision
    7. Important amounts
    8. Important dates

    Rules:
    - Use only information present in the provided context.
    - Do not invent or assume facts that are not present.
    - Clearly distinguish between arguments made by parties and findings made by the court.
    - If an important detail is not available in the provided context, do not guess it.
    - Keep the summary factual and neutral.

    Document context:
    {context}
    """

    response = llm.invoke(prompt)

    return {
        "summary_result": response.content
    }