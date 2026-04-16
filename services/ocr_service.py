import io
import fitz  # PyMuPDF
import easyocr
import numpy as np
from PIL import Image

# Initialize OCR once
reader = easyocr.Reader(['en'], gpu=False)


async def process_pdf(file):
    try:
        content = await file.read()
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
            "filename": file.filename,
            "total_pages": len(results),
            "pages": results
        }

    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")


async def process_pdf_image_only(file):
    try:
        content = await file.read()
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
            "filename": file.filename,
            "total_pages": len(results),
            "pages": results
        }

    except Exception as e:
        raise Exception(f"Image-based OCR processing failed: {str(e)}")