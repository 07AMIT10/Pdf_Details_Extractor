
# PDF Information Extraction System

A full-stack solution for automatically extracting contact details (Name, Phone, Address) from PDF documents and populating web form fields.

#System Architecture (https://imgur.com/a/LHyZvPE)

## Problem Statement
Many organizations manually extract contact details from PDF documents like resumes/invoices. This system automates:
- PDF text extraction (both digital and scanned)
- Structured data recognition using NLP+Regex
- Auto-population of web forms
- Simple API integration

## Key Features
- **Multi-Format PDF Handling**: Works with text-based and scanned PDFs
- **Hybrid Extraction**: Combines regex patterns + spaCy NER
- **Error-Resilient Processing**: Fallback mechanisms at each stage
- **Simple UI**: Drag-and-drop PDF uploader
- **REST API**: Easy integration with other systems

## Tech Stack
**Backend**  
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
- PDF Parsing: `pdfplumber` + `pytesseract`
- NLP: `spaCy` (en_core_web_sm)
- API: `Flask`

**Frontend**  
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
- File Handling: `axios`
- UI: Basic HTML5 form

**Infrastructure**  
![Docker](https://img.shields.io/badge/Docker-optional-2496ED?logo=docker)

## System Architecture
```
system/
├── backend/        # Flask API
│   ├── app.py
│   └── utils/
│       └── pdf_processor.py
├── frontend/       # React App
│   ├── src/
│   │   └── components/
│   │       └── UploadForm.js
└── README.md
```

## Installation

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```

### 3. System Dependencies
- **Tesseract OCR**: [Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- **libmagic**: `brew install libmagic` (Mac) / `apt-get install libmagic1` (Linux)

## Configuration
Create `.env` in backend:
```ini
FLASK_ENV=development
FLASK_APP=app.py
MAX_FILE_SIZE=10485760  # 10MB
```

## Running Locally
**Backend** (Port 5000)
```bash
flask run --host=0.0.0.0
```

**Frontend** (Port 3000)
```bash
npm start
```

## Deployment
1. **Frontend**: [Vercel](https://vercel.com)  
   `vercel --prod`

2. **Backend**: [Render](https://render.com)  
   Add build command: `pip install -r requirements.txt`

## Usage
1. Access frontend at `http://localhost:3000`
2. Upload PDF document
3. System auto-populates:
   - Name
   - Phone Number (formatted)
   - Address

## Solution Approach
1. **PDF Processing**:
   - Digital PDFs: Layout-aware extraction via `pdfplumber`
   - Scanned PDFs: OCR with `pytesseract`

2. **Data Extraction**:
   ```mermaid
   graph TD
   A[Raw Text] --> B{Structured Format?}
   B -->|Yes| C[Regex Patterns]
   B -->|No| D[spaCy NER]
   C --> E[Validation]
   D --> E
   E --> F[Formatted Output]
   ```

3. **Error Handling**:
   - Multi-layer fallback (Regex → NLP → Manual validation)
   - File type/size validation
   - Graceful degradation for partial matches

## Troubleshooting
**Common Issues**:
1. `libmagic` Errors:
   ```bash
   # Ubuntu
   sudo apt-get install libmagic1
   ```

2. Tesseract Path:
   ```python
   # In pdf_processor.py
   pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' 
   ```

3. Large File Handling:
   ```python
   # .env
   MAX_FILE_SIZE=20971520  # 20MB
   ```

## Future Improvements
- [ ] Add multi-document batch processing
- [ ] Implement address validation via Google Maps API
- [ ] Add support for international phone formats
- [ ] Train custom NER model on document dataset

---


**Live Demo**: [https://pdf-extractor.vercel.app](https://pdf-extractor.vercel.app)
```

