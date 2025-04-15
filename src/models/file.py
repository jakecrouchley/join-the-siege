from dataclasses import dataclass
from werkzeug.datastructures import FileStorage
from src.utils.extractors import extract_text_from_pdf, extract_text_from_image

class MissingFileException(Exception):
    pass
class InvalidFileTypeException(Exception):
    pass

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UnprocessedFile:
  """File object to be processed."""
  filename: str
  file_bytes: bytes

  def __init__(self, file: FileStorage):
    self.filename = file.filename

    if not isinstance(file, FileStorage):
        raise TypeError("Expected a FileStorage object")
    if self.filename == '':
        raise MissingFileException("No selected file")
    if not allowed_file(file.filename):
        raise InvalidFileTypeException("File type not allowed")
    
    self.file_bytes = file.read()
    if not self.file_bytes:
        raise MissingFileException("File is empty")

  def extract_text(self) -> 'ProcessedFile':
    """Extract text content from the file, returning a ProcessedFile."""
    if self.filename.endswith('.pdf'):
        text_content = extract_text_from_pdf(self.file_bytes)
    elif self.filename.endswith(('.png', '.jpg', '.jpeg')):
        text_content = extract_text_from_image(self.file_bytes)
    else:
        raise InvalidFileTypeException("Unsupported file type")
    
    return ProcessedFile(self.filename, text_content)
  
@dataclass
class ProcessedFile:
    """File object containing the extracted text, ready for classification."""
    filename: str
    text_content: str