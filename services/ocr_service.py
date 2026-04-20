import io
import fitz  # PyMuPDF
import requests
import easyocr
import numpy as np
from PIL import Image


# Initialize OCR once
reader = easyocr.Reader(['en'], gpu=False)


def download_pdf(url: str) -> bytes:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        if "application/pdf" not in response.headers.get("Content-Type", "").lower():
            # Check file extension as fallback
            if not url.lower().endswith(".pdf"):
                raise Exception("The provided URL does not point to a PDF file.")
        return response.content
    except Exception as e:
        raise Exception(f"Failed to download PDF from URL: {str(e)}")


async def process_pdf(content: bytes, filename: str):
    try:
        pdf_document = fitz.open(stream=content, filetype="pdf")

        results = []

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # Fast extraction
            text = page.get_text().strip()

            # Fallback to OCR
            if not text:
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                img_np = np.array(img)

                ocr_text_list = reader.readtext(img_np, detail=0)
                text = " ".join(ocr_text_list)

            results.append({   
                "page": page_num + 1,
                "content": text
            })

        pdf_document.close()

        return {
            "filename": filename,
            "total_pages": len(results),
            "pages": results
        }

    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")


async def process_pdf_image_only(content: bytes, filename: str):
    try:
        pdf_document = fitz.open(stream=content, filetype="pdf")

        results = []

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # Always use OCR for image extraction
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Direct conversion to PIL Image as per user suggestion
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_np = np.array(img)

            ocr_text_list = reader.readtext(img_np, detail=0)
            text = " ".join(ocr_text_list)

            results.append({
                "page": page_num + 1,
                "content": text
            })

        pdf_document.close()

        return {
            "filename": filename,
            "total_pages": len(results),
            "pages": results
        }

    except Exception as e:
        raise Exception(f"Image-based OCR processing failed: {str(e)}")