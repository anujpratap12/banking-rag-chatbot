from fastapi import APIRouter, UploadFile, File
import os
import shutil

from backend.rag.extractor import extract_text
from backend.rag.chunker import chunk_text
from backend.rag.embeddings import generate_embeddings
from backend.rag.vector_store import store_chunks

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".docx", ".txt"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        return {
            "error": "Only PDF, DOCX, and TXT files are allowed"
        }

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text(file_path)

    chunks = chunk_text(extracted_text)

    embeddings = generate_embeddings(chunks)

    store_chunks(chunks, embeddings)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "text_length": len(extracted_text),
        "total_chunks": len(chunks),
        "embeddings_created": len(embeddings)
    }