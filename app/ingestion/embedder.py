from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

def create_embeddings(chunks: list[str]) -> list[list[float]]:
    vectors = embeddings.embed_documents(chunks)

    return vectors