import pytest
from werkzeug.datastructures import FileStorage
from src.models.file import allowed_file, UnprocessedFile, ProcessedFile, MissingFileException, InvalidFileTypeException
from io import BytesIO

@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.txt", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_unprocessed_file_valid_pdf():
    file = FileStorage(stream=BytesIO(b"dummy content"), filename="test.pdf")
    unprocessed_file = UnprocessedFile(file)
    assert unprocessed_file.filename == "test.pdf"
    assert unprocessed_file.file_bytes == b"dummy content"

def test_unprocessed_file_invalid_file_type():
    file = FileStorage(stream=BytesIO(b"dummy content"), filename="test.txt")
    try:
        UnprocessedFile(file)
    except InvalidFileTypeException as e:
        assert str(e) == "File type not allowed"

def test_unprocessed_file_missing_file():
    file = FileStorage(stream=BytesIO(b""), filename="")
    try:
        UnprocessedFile(file)
    except MissingFileException as e:
        assert str(e) == "No selected file"

def test_unprocessed_file_empty_file():
    file = FileStorage(stream=BytesIO(b""), filename="test.pdf")
    try:
        UnprocessedFile(file)
    except MissingFileException as e:
        assert str(e) == "File is empty"

def test_processed_file():
    processed_file = ProcessedFile(filename="test.pdf", text_content="Extracted text")
    assert processed_file.filename == "test.pdf"
    assert processed_file.text_content == "Extracted text"