from fastapi import FastAPI
from routes.routes import router as ocr_router

app = FastAPI(
    title="PDF OCR API",
    description="Extract text from PDFs using PyMuPDF + EasyOCR",
    version="1.0.0"
)

# Register routes
app.include_router(ocr_router)


@app.get("/")
async def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)