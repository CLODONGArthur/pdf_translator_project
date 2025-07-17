
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import os, uuid

from utils.pdf_tools import extract_text_from_pdf, create_pdf
from utils.translation import translate_text

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "translated"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.post("/translate-pdf/")
async def translate_pdf(
    file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)
    ):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_translated.pdf")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    original_text = extract_text_from_pdf(input_path)
    translated_text = translate_text(original_text, source_lang, target_lang)
    create_pdf(translated_text, output_path)

    return {"download_url": f"/download/{file_id}"}

@app.get("/download/{file_id}")
def download_translated_pdf(file_id: str):
    output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_translated.pdf")
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="application/pdf", filename="translated.pdf")
    return {"error": "Fichier non trouvé"}


    """source venv/Scripts/activate"""
    """uvicorn main:app --reload"""