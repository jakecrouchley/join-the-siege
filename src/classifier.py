from werkzeug.datastructures import FileStorage
from sentence_transformers import SentenceTransformer, util
from src.models.file import ProcessedFile
from src.utils.config import Config


def classify_file(file: ProcessedFile):
    model = SentenceTransformer(Config.model)
    
    label_keywords = Config.label_keywords
    
    # Generate embeddings for candidate labels
    candidate_labels = list(label_keywords.keys())
    label_embeddings = model.encode(candidate_labels)

    # Generate embeddings for the keywords
    keyword_embeddings = {}
    for label, keywords in label_keywords.items():
        keyword_embeddings[label] = model.encode(keywords)
    
    # Generate embeddings for the document text
    doc_embedding = model.encode(file.text_content)

    # Compute similarity between document and labels
    label_similarities = util.cos_sim(doc_embedding, label_embeddings)

    # Compute similarity between document and keywords
    keyword_similarities = {}
    for label, keyword_embedding in keyword_embeddings.items():
        keyword_similarities[label] = util.cos_sim(doc_embedding, keyword_embedding)

    # Combine similarities
    combined_similarities = {}
    for label in candidate_labels:
        label_similarity = float(label_similarities[0][candidate_labels.index(label)])
        keyword_similarity = float(keyword_similarities[label][0][0])
        combined_similarities[label] = (label_similarity + keyword_similarity) / 2

    predicted_label = max(combined_similarities, key=combined_similarities.get)
    if combined_similarities[predicted_label] > Config.threshold:
        return predicted_label
    else:
        return "unknown file"

