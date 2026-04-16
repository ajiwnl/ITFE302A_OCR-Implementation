from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from services.ocr_service import process_pdf, process_pdf_image_only, download_pdf

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.get("/check")
async def check():
    return {"message": "OCR service is working"}


@router.post("/")
async def perform_ocr(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None)
):
    if not file and not url:
        raise HTTPException(status_code=400, detail="Either a file or a URL must be provided.")

    if file:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        content = await file.read()
        filename = file.filename
    else:
        content = download_pdf(url)
        filename = "downloaded_file.pdf"

    result = await process_pdf(content, filename)
    return result


@router.post("/extract-image")
async def perform_ocr_image(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None)
):
    if not file and not url:
        raise HTTPException(status_code=400, detail="Either a file or a URL must be provided.")

    if file:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        content = await file.read()
        filename = file.filename
    else:
        content = download_pdf(url)
        filename = "downloaded_file.pdf"

    result = await process_pdf_image_only(content, filename)
    return result