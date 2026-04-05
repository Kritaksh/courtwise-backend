from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader

app = FastAPI()

# Health check endpoint (already working)
@app.get("/")
def health_check():
    return {"status": "Courtwise backend is running"}

# File upload endpoint (NEW)
@app.post("/upload")
async def upload_case_file(file: UploadFile = File(...)):

    # 1️⃣ Read uploaded file bytes
    contents = await file.read()

    # 2️⃣ Save temporarily as PDF
    with open("temp.pdf", "wb") as f:
        f.write(contents)

    # 3️⃣ Open PDF using PdfReader
    reader = PdfReader("temp.pdf")

    text = ""

    # 4️⃣ Extract text page by page
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # 5️⃣ Return preview (first 1000 characters only)
    return {
        "filename": file.filename,
        "text_preview": text[:1000]
    }