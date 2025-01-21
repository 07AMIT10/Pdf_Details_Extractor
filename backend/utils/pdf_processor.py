import re
import pdfplumber
import pytesseract
import logging
from pdf2image import convert_from_bytes
from io import BytesIO

# Updated patterns with improved phone number handling
EXTRACTION_PATTERNS = {
    'name': re.compile(r'(?i)(?:name\s*[:]\s*)([^:\n\r]+?)(?=\s*(?:phone|$))', re.MULTILINE),
    # Enhanced phone pattern to better handle various formats including parentheses
    'phone': re.compile(r'(?i)(?:phone\s*[:]\s*)(\+?\d[\d\s\-\(\)\.]+\d)(?=\s*(?:address|$))', re.MULTILINE),
    'address': re.compile(r'(?i)(?:address\s*[:]\s*)(.*?)(?=\s*(?:role|$)|\Z)', re.DOTALL)
}

def is_scanned_pdf(pdf_bytes):
    """Determine if PDF is scanned/image-based"""
    try:
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                return len(text.strip()) < 50
    except Exception as e:
        logging.error(f"PDF analysis error: {str(e)}")
        return False

def extract_text(pdf_bytes):
    """Extract text with improved layout handling"""
    try:
        if is_scanned_pdf(pdf_bytes):
            images = convert_from_bytes(pdf_bytes, dpi=300)
            text = '\n'.join([pytesseract.image_to_string(img) for img in images])
        else:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                # Adjusted tolerance values for better text extraction
                text = '\n'.join([
                    page.extract_text(layout=True, x_tolerance=3, y_tolerance=3)
                    for page in pdf.pages
                ])
        return normalize_text(text)
    except Exception as e:
        logging.error(f"Text extraction failed: {str(e)}")
        return ""

def normalize_text(text):
    """Enhanced text normalization with special handling for phone numbers"""
    # Standardize field labels
    text = re.sub(r'(?i)\b(name|phone|address)\s*[:]?\s*', r'\1: ', text)
    
    # Preserve phone number formatting while cleaning up
    text = re.sub(r'(?<=[^\d)])\s+(?=[^\d(])', ' ', text)
    
    # Ensure each field starts on a new line
    text = re.sub(r'(?<=[^\n])\s+(?=(?:Name|Phone|Address):)', '\n', text, flags=re.IGNORECASE)
    
    return text.strip()

def format_phone(raw_phone):
    """Enhanced phone number formatting with better handling of various formats"""
    if not raw_phone:
        return ''
    
    # First, let's clean up the phone number while preserving key characters
    # Keep +, digits, parentheses temporarily
    cleaned = ''.join(c for c in raw_phone if c.isdigit() or c in '+()').strip()
    
    # Remove parentheses but keep their content
    cleaned = re.sub(r'\((\d+)\)', r'\1', cleaned)
    
    # Now we have just + and digits
    digits = ''.join(c for c in cleaned if c.isdigit() or c == '+')
    
    # Handle different formats
    if digits.startswith('+'):
        if digits.startswith('+1'):
            # US format starting with +1
            return digits if len(digits) >= 11 else ''
        return digits  # Other international format
    elif len(digits) == 10:
        # US number without country code
        return f'+1{digits}'
    elif len(digits) > 10:
        # International number without +
        return f'+{digits}'
    
    return digits if digits else 'Not found'

def format_address(raw_address):
    """Clean and format address with improved handling of all components"""
    if not raw_address:
        return ''
    
    # Initial cleanup
    address = re.sub(r'\s+', ' ', raw_address.strip())
    
    # Normalize commas and spaces
    address = re.sub(r'\s*,\s*', ', ', address)
    
    # Handle ordinal numbers in floor numbers (3rd, 2nd, etc.)
    address = re.sub(r'(\d)\s*,?\s*(?:rd|th|st|nd)\s+([Ff]loor)', r'\1rd Floor', address)
    
    # Ensure proper comma separation
    address = re.sub(r'(?<=\d)(?=[A-Za-z])', ', ', address)
    address = re.sub(r'(?<=[a-zA-Z])(?=\d{5})', ', ', address)
    
    # Special handling for United States
    address = re.sub(r',?\s*(United States)$', r', \1', address, flags=re.IGNORECASE)
    
    # Clean up any double commas and spaces
    address = re.sub(r',\s*,', ',', address)
    address = re.sub(r',\s*$', '', address)
    
    return address

def extract_entities(text):
    """Extract entities with improved validation and logging"""
    entities = {key: '' for key in EXTRACTION_PATTERNS}
    
    # Add debug logging
    logging.debug(f"Normalized text for extraction: {text}")
    
    for field, pattern in EXTRACTION_PATTERNS.items():
        match = pattern.search(text)
        if match:
            value = match.group(1).strip()
            logging.debug(f"Found {field}: {value}")
            
            if field == 'phone':
                entities[field] = format_phone(value)
            elif field == 'address':
                entities[field] = format_address(value)
            else:
                entities[field] = value
        else:
            logging.debug(f"No match found for {field}")
    
    return entities

def process_pdf(file):
    """Main processing pipeline with enhanced error handling"""
    try:
        pdf_bytes = file.read()
        text = extract_text(pdf_bytes)
        
        if not text:
            raise ValueError("No extractable text found in PDF")
        
        # Add debug logging
        logging.debug(f"Extracted text from PDF: {text}")
        
        entities = extract_entities(text)
        
        # Validate extracted data
        for key, value in entities.items():
            if not value:
                entities[key] = 'Not found'
        
        return {
            'success': True,
            'data': {
                'name': entities['name'],
                'phone': entities['phone'],
                'address': entities['address']
            }
        }
    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        return {
            'success': False,
            'error': f"Processing Error: {str(e)}"
        }