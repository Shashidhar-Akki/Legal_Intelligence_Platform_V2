from fastapi import FastAPI ,UploadFile ,File
from app.parser import extract_pdf_text

import shutil

app = FastAPI()

@app.post("/upload")
async def upload_file(file : UploadFile=File(...)):

    file_path = f"uploads/{file.filename}"
    
    with open(file_path,"wb") as buffers:
        shutil.copyfileobj(file.file,buffers)

    extracted_text = extract_pdf_text(file_path) #we are calling the funcincion in parser.py with an argument file_path, and the new extracted text is we get


    return {
    "message": "PDF uploaded successfully",
    "filename": file.filename,
    "extracted_text" : extracted_text}   
