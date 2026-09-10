from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from openai import OpenAI
import os

#this will help the user in copying the name of the file without typing .PDF  everytime while asking question
def normalize_filename(filename: str) -> str:

    filename = filename.strip()

    if not filename.lower().endswith(".pdf"):
        filename = filename + ".PDF"

    return filename


# 1. Create embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# 2. Connect to Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("legal-documents")


# 3. Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def retrieve_context(question, filename, top_k=5, dynamic = False):

    filename = normalize_filename(filename)

    namespace = filename

    # If top_k is not manually provided,
    # retrieve based on document size.
    if dynamic:

        stats = index.describe_index_stats()

        namespace_stats = stats["namespaces"].get(namespace)

        if not namespace_stats:
            return ""

        total_chunks = namespace_stats["vector_count"]

        # Retrieve approximately 10% of the document
        top_k = round(total_chunks * 0.10)

        # Minimum 5 chunks
        top_k = max(5, top_k)

        # Maximum of 100 results
        top_k = min(100, top_k)

    # Convert question into embedding
    query_vector = embeddings.embed_query(question)

    # Search Pinecone
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        namespace= namespace,      
        include_metadata=True
    )

    # Extract retrieved chunks
    retrieved_chunks = []

    for match in results["matches"]:
        retrieved_chunks.append(
            match["metadata"]["text"]
        )

    # Combine retrieved chunks into context
    context = "\n\n".join(retrieved_chunks)

    return context



def answer_question(question,filename, top_k=2):

    filename = normalize_filename(filename)

    namespace =filename

    # Convert question into embedding
    query_vector = embeddings.embed_query(question)

    # Search Pinecone
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        namespace= namespace,
        include_metadata=True
    )

    # Extract retrieved chunks
    retrieved_chunks = []

    for match in results["matches"]:
        retrieved_chunks.append(
            match["metadata"]["text"]
        )

    # Combine chunks into context
    context = "\n\n".join(retrieved_chunks)

    # Send context + question to LLM
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer based only on the provided context.
"""
    )

    return response.output_text


# Test has been deleted because we are directly testing this with  python -c "from app.retrieval.retriever import answer_question; print(answer_question('Give me brief facts of the case'))"
