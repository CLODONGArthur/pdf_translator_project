
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
import os, uuid

from utils.pdf_tools import extract_text_from_pdf, create_pdf
from utils.translation import translate_text

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "translated"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
        <head><title>Traducteur de PDF</title></head>
        <body>
            <h2>Uploader un fichier PDF à traduire</h2>
            <form action="/translate-pdf/" enctype="multipart/form-data" method="post">
                <label>Fichier PDF :</label>
                <input type="file" name="file" accept=".pdf" required><br><br>
                <label>Langue source :</label>
                <input type="text" name="source_lang" placeholder="ex: fr" required><br><br>
                <label>Langue cible :</label>
                <input type="text" name="target_lang" placeholder="ex: en" required><br><br>
                <input type="submit" value="Traduire">
            </form>
        </body>
    </html>
    """

@app.post("/translate-pdf/", response_class=HTMLResponse)
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

    return f"""
    <html>
        <body>
            <h3>Traduction terminée !</h3>
            <a href="/download/{file_id}">📥 Télécharger le PDF traduit</a><br><br>
            <a href="/">⬅ Retour</a>
        </body>
    </html>
    """

@app.get("/download/{file_id}")
def download_translated_pdf(file_id: str):
    output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_translated.pdf")
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="application/pdf", filename="translated.pdf")
    return {"error": "Fichier non trouvé"}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return '''
    <html>
        <head>
            <title>PDF Translator</title>
            <style>
                body { font-family: Arial; margin: 40px; background-color: #f5f5f5; }
                form { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
                input, select { width: 100%; padding: 10px; margin-top: 10px; }
                button { padding: 10px 20px; background-color: #007BFF; color: white; border: none; border-radius: 4px; margin-top: 10px; }
                button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <form action="/translate-pdf/" enctype="multipart/form-data" method="post">
                <h2>📄 PDF Translator</h2>
                <input type="file" name="file" accept="application/pdf" required>
                <label>Langue source :</label>
                <select name="source_lang">
                    <option value="fr">Français</option>
                    <option value="en">Anglais</option>
                    <option value="es">Espagnol</option>
                </select>
                <label>Langue cible :</label>
                <select name="target_lang">
                    <option value="en">Anglais</option>
                    <option value="fr">Français</option>
                    <option value="de">Allemand</option>
                </select>
                <button type="submit">Traduire</button>
            </form>
        </body>
    </html>
    '''
    

    """source venv/Scripts/activate"""
    """uvicorn main:app --reload"""
    """git add .
       git commit -m "Préparation déploiement Render"
       git push origin master"""