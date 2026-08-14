from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def check_similarity(input_text, documents):
    """
    Calculate cosine similarity between the input text
    and a list of reference documents.

    Parameters:
        input_text (str): Text submitted for plagiarism checking.
        documents (list): List of reference document texts.

    Returns:
        list: Similarity scores between 0 and 1.
    """

    if not input_text or not input_text.strip():
        raise ValueError("Input text cannot be empty.")

    if not documents:
        raise ValueError("At least one reference document is required.")

    # Combine input text with reference documents
    texts = [input_text] + documents

    # Convert text into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compare input text with all reference documents
    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )

    return similarity_scores[0]


def classify(score):
    """
    Classify similarity score into a plagiarism category.

    Parameters:
        score (float): Similarity score between 0 and 1.

    Returns:
        str: Classification label.
    """

    if score < 0.30:
        return "Original"

    elif score < 0.70:
        return "Suspected"

    else:
        return "Copied"


def get_similarity_percentage(score):
    """
    Convert similarity score from decimal to percentage.

    Example:
        0.82 -> 82.0
    """

    return round(score * 100, 2)
