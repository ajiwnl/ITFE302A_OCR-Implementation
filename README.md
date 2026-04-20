# ITFE302A_OCR-Implementation PDF OCR API

A lightweight FastAPI-based service for extracting text from PDF documents using a combination of PyMuPDF and EasyOCR. This API provides intelligent text extraction that first attempts direct text extraction from PDFs and falls back to OCR for image-based or scanned documents.

## Features

- **Dual Extraction Methods**: Combines PyMuPDF for fast text extraction with EasyOCR fallback for scanned/image-based PDFs
- **RESTful API**: Clean FastAPI endpoints for easy integration
- **File Upload Support**: Accept PDF files via multipart upload
- **URL Processing**: Download and process PDFs directly from URLs
- **Page-by-Page Results**: Returns structured JSON with text content for each page
- **Error Handling**: Comprehensive error handling with meaningful messages

## API Endpoints

### GET `/ocr/check`
Health check endpoint to verify the service is running.

**Response:**
```json
{
  "message": "OCR service is working"
}
```

### POST `/ocr/`
Extract text from a PDF using intelligent extraction (text first, OCR fallback).

**Parameters:**
- `file` (optional): PDF file upload
- `url` (optional): URL to a PDF file

**Response:**
```json
{
  "filename": "document.pdf",
  "total_pages": 3,
  "pages": [
    {
      "page": 1,
      "content": "Extracted text content..."
    }
  ]
}
```

### POST `/ocr/extract-image`
Extract text from a PDF using OCR only (optimized for scanned documents).

**Parameters:**
- `file` (optional): PDF file upload
- `url` (optional): URL to a PDF file

**Response:** Same format as `/ocr/` endpoint.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ITFE302A_OCR-Implementation
```

2. Create a virtual environment:
```bash
python -m venv ocrenv
```

3. Activate the virtual environment:
```bash
# Windows
ocrenv\Scripts\activate
# Linux/Mac
source ocrenv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### Example Usage

#### Using curl to upload a PDF file:
```bash
curl -X POST "http://localhost:8000/ocr/" \
     -F "file=@document.pdf"
```

#### Using curl with a PDF URL:
```bash
curl -X POST "http://localhost:8000/ocr/" \
     -F "url=https://example.com/document.pdf"
```

#### Using Python requests:
```python
import requests

# Upload file
with open('document.pdf', 'rb') as f:
    response = requests.post('http://localhost:8000/ocr/', files={'file': f})

# Or use URL
response = requests.post('http://localhost:8000/ocr/',
                        data={'url': 'https://example.com/document.pdf'})

print(response.json())
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **PyMuPDF**: High-performance PDF processing library
- **EasyOCR**: OCR library for text extraction from images
- **NumPy**: Numerical computing library
- **Pillow**: Image processing library
- **Requests**: HTTP library for downloading PDFs

## Architecture

The application is structured as follows:

- `main.py`: FastAPI application entry point
- `routes/routes.py`: API route definitions
- `services/ocr_service.py`: Core OCR processing logic
- `requirements.txt`: Python dependencies

### OCR Service Logic

The service implements two processing modes:

1. **Intelligent Mode** (`/ocr/`): Attempts direct text extraction first. If no text is found, falls back to OCR.
2. **OCR-Only Mode** (`/ocr/extract-image`): Always uses OCR, optimized for scanned documents.

Both modes process PDFs page by page and return structured results.

## Error Handling

The API provides comprehensive error handling:

- Invalid file types (non-PDF)
- Failed PDF downloads
- OCR processing failures
- Missing required parameters

All errors return appropriate HTTP status codes with descriptive messages.

## Performance Considerations

- OCR processing is computationally intensive and may take time for large or image-heavy PDFs
- The service uses CPU-based OCR (gpu=False) for broader compatibility
- Consider the `/ocr/extract-image` endpoint only when you know the PDF contains scanned images

## License

[Add license information here]
# ITFE302A_OCR-Implementation
