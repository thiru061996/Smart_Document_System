import easyocr

# Initialize once (heavy operation)
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(filepath: str) -> str:
    try:
        results = reader.readtext(filepath, detail=0)
        return " ".join(results)
    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}")