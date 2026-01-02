from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def check_similarity(input_text, documents):
    texts = [input_text] + documents

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return similarity_scores[0]
def classify(score):
    if score < 0.3:
        return "Original"
    elif score < 0.7:
        return "Suspected"
    else:
        return "Copied"
