from fastapi import APIRouter, File, UploadFile, HTTPException
from services.ocr_service import process_pdf, process_pdf_image_only

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.get("/check")
async def check():
    return {"message": "OCR service is working"}


@router.post("/")
async def perform_ocr(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    result = await process_pdf(file)
    return result


@router.post("/extract-image")
async def perform_ocr_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    result = await process_pdf_image_only(file)
    return result