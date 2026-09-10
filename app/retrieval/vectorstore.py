from pinecone import Pinecone

import os

from dotenv import load_dotenv

load_dotenv()


pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("legal-documents")


def store_vectors(
    chunks: list[str],
    vectors: list[list[float]],
    source: str               
):
    namespace = source

    records = []

    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):

        record = {
            "id": f"{source}-chunk-{i}",
            "values": vector,
            "metadata": {
                "text": chunk,
                "source": source,
                "chunk_index": i
            }
        }

        records.append(record)

    index.upsert(vectors=records,            #Store these vector records in the Pinecone index.           
                 namespace= namespace)         

    return len(records)