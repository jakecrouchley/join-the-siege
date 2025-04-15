from werkzeug.datastructures import FileStorage
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import fitz
import easyocr

def extract_text_from_pdf(file_stream):
    text = ""
    with fitz.Document(stream=file_stream) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_image(file_stream):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_stream)
    text = ""
    for detection in result:
        text += detection[1] + "\n"
    return text


def classify_file(file: FileStorage):
    filename = file.filename.lower()
    file_bytes = file.read()

    if filename.endswith('.pdf'):
        text_content = extract_text_from_pdf(file_bytes)
    elif filename.endswith(('.png', '.jpg', '.jpeg')):
        text_content = extract_text_from_image(file_bytes)
    else:
        return "unknown file"
    print(text_content)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    label_keywords = {
        'drivers_licence': 'license driver DMV identification permission',
        'bank_statement': 'account balance transaction bank statement',
        'invoice': 'invoice payment due amount description total cost',
        'cv': 'skills experience resume education work history role',
    }
    # Generate embeddings for candidate labels
    candidate_labels = list(label_keywords.keys())
    label_embeddings = model.encode(candidate_labels)

    # Generate embeddings for the keywords
    keyword_embeddings = {}
    for label, keywords in label_keywords.items():
        keyword_embeddings[label] = model.encode(keywords)
    
    # Generate embeddings for the document text
    doc_embedding = model.encode(text_content)

    # Compute similarity
    label_similarities = util.cos_sim(doc_embedding, label_embeddings)

    keyword_similarities = {}
    for label, keyword_embedding in keyword_embeddings.items():
        keyword_similarities[label] = util.cos_sim(doc_embedding, keyword_embedding)
    print(label_similarities)
    print(keyword_similarities)

    # Combine similarities
    combined_similarities = {}
    for label in candidate_labels:
        label_similarity = float(label_similarities[0][candidate_labels.index(label)])
        keyword_similarity = float(keyword_similarities[label][0][0])
        combined_similarities[label] = (label_similarity + keyword_similarity) / 2

    predicted_label = max(combined_similarities, key=combined_similarities.get)
    print(combined_similarities)
    print(predicted_label)
    if combined_similarities[predicted_label] > 0.3:
        return predicted_label
    else:
        return "unknown file"

