from fastapi import APIRouter, UploadFile, File

from app.ingestion.parser import extract_pdf_text
from app.ingestion.chunker import split_text_into_chunks
from app.ingestion.embedder import create_embeddings

from app.retrieval.vectorstore import store_vectors
from app.retrieval.retriever import answer_question, retrieve_context

from app.agents.intent_router import classify_request, classify_analysis_type
from app.agents.graph import graph

import shutil

import os

router = APIRouter()


# =========================================================
# UPLOAD ENDPOINT
# =========================================================

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffers:
        shutil.copyfileobj(file.file, buffers)

    # Step 1: Extract text from PDF
    extracted_text = extract_pdf_text(file_path)

    # Step 2: Split text into chunks
    chunks = split_text_into_chunks(extracted_text)

    # Step 3: Create embeddings
    vectors = create_embeddings(chunks)

    # Step 4: Store vectors in Pinecone
    stored_vectors = store_vectors(
        chunks,
        vectors,
        file.filename
    )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "total_characters": len(extracted_text),
        "total_chunks": len(chunks),
        "stored_vectors": stored_vectors,
        "first_chunk": chunks[0] if chunks else ""
    }


# =========================================================
# ASK ENDPOINT
# =========================================================

@router.post("/ask")
async def ask_question(
    question: str,
    filename: str
):

    # =====================================================
    # STEP 1: Decide whether this is Q&A or Analysis
    # =====================================================

    intent = classify_request(question)


    # =====================================================
    # NORMAL Q&A
    # =====================================================

    if intent == "qa":

        answer = answer_question(
            question,
            filename
        )

        return {
            "question": question,
            "intent": "qa",
            "answer": answer
        }


    # =====================================================
    # ANALYSIS
    # =====================================================

    # Step 2: Decide which type of analysis is required

    analysis_type = classify_analysis_type(question)


    # =====================================================
    # STEP 3: RETRIEVAL
    # =====================================================

    # Summary uses dynamic retrieval.
    #
    # Dynamic retrieval:
    # approximately 10% of the document's chunks
    # with a maximum of 100 chunks.

    if analysis_type == "summary":

        context = retrieve_context(
            question,
            filename,
            dynamic = True
        )

    else:

        context = retrieve_context(
            question,
            filename
        )


    # =====================================================
    # STEP 4: SEND TO LANGGRAPH
    # =====================================================

    result = graph.invoke({
        "analysis_type": analysis_type,
        "context": context
    })


    # =====================================================
    # STEP 5: GET RESULT FROM SELECTED AGENT
    # =====================================================

    if analysis_type == "reader":

        answer = result["reader_result"]

    elif analysis_type == "risk":

        answer = result["risk_result"]

    else:

        answer = result["summary_result"]


    # =====================================================
    # STEP 6: RETURN RESPONSE
    # =====================================================

    return {
        "question": question,
        "intent": "analysis",
        "analysis_type": analysis_type,
        "answer": answer
    }

#"I initially considered using a larger top-k for summaries, but I kept the V2 retrieval strategy simple because a fixed value isn't necessarily appropriate for documents of very different sizes. A future version could dynamically determine retrieval depth based on document size, with appropriate limits."