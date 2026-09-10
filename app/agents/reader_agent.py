from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


def reader(state):

    context = state["context"]

    prompt = f"""
    You are a legal document analysis assistant.
    
    Analyze only the legal document context provided below.

    Identify and organize the following information when available:

    1. Parties involved
    2. Important facts
    3. Legal issues
    4. Relevant clauses or provisions
    5. Important dates
    6. Amounts or financial details
    7. Important legal points, arguments, or findings

    Rules:
    - Use only information present in the provided context.
    - Do not invent or assume facts that are not present.
    - Clearly distinguish between facts, arguments, and court findings when possible.
    - If a requested detail is not available in the context, say that it is not available in the provided context.
    - Keep the response clear and structured.

    Context:
    {context}
    """
    response = llm.invoke(prompt)

    return {
        "reader_result": response.content
    }