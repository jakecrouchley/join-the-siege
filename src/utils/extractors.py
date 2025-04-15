import fitz
import easyocr

@staticmethod
def extract_text_from_pdf(file_stream):
    text = ""
    with fitz.Document(stream=file_stream) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

@staticmethod
def extract_text_from_image(file_stream):
    reader = easyocr.Reader(['en'])
    try:
        result = reader.readtext(file_stream)
    except Exception as e:
        raise RuntimeError(f"Error reading image")
    text = ""
    for detection in result:
        text += detection[1] + "\n"
    return text