import io
import fitz  # PyMuPDF
import easyocr
import numpy as np
import re
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="PDF OCR API with Keyword Search",
    description="Extract text from PDFs and search for keywords using regex",
    version="1.1.0"
)

# Initialize OCR
print("Loading EasyOCR models...")
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/check")
async def root():
    return {"message": "PDF OCR API is running. Use /ocr to upload a PDF file."}


@app.post("/ocr")
async def perform_ocr(
    file: UploadFile = File(...),
    keyword: str = Query(None, description="Keyword to search in the PDF")
):
    """
    Upload PDF → Extract text → Search keyword (optional)
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        content = await file.read()
        pdf_document = fitz.open(stream=content, filetype="pdf")

        results = []
        total_matches = 0
        pages_found = []

        # Compile regex pattern (case-insensitive, whole word match)
        pattern = None
        if keyword:
            pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # Try fast extraction
            text = page.get_text().strip()

            # Fallback to OCR if empty
            if not text:
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                img_np = np.array(img)

                ocr_text_list = reader.readtext(img_np, detail=0)
                text = " ".join(ocr_text_list)

            # Keyword search
            matches = []
            if pattern:
                matches = pattern.findall(text)
                if matches:
                    total_matches += len(matches)
                    pages_found.append(page_num + 1)

            results.append({
                "page": page_num + 1,
                "content": text,
                "matches": matches if keyword else []
            })

        pdf_document.close()

        response = {
            "filename": file.filename,
            "total_pages": len(results),
            "pages": results
        }

        # Add keyword summary if provided
        if keyword:
            response["keyword_search"] = {
                "keyword": keyword,
                "total_matches": total_matches,
                "pages_found": pages_found
            }

        return JSONResponse(content=response)

    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)