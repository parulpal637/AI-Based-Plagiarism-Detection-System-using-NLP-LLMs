import streamlit as st
import matplotlib.pyplot as plt
from plagiarism import check_similarity
from explanation import generate_explanation

documents = [
    open("dataset/doc1.txt").read(),
    open("dataset/doc2.txt").read()
]

st.title("🧠 AI Plagiarism Detection Tool")

input_text = st.text_area("Paste your text here")

if st.button("Check Plagiarism"):
    scores = check_similarity(input_text, documents)

    labels = []
    for i, score in enumerate(scores):
        labels.append(f"Source {i+1}")
        st.write(generate_explanation(score, labels[i]))

    # Bar Chart
    plt.bar(labels, scores)
    plt.ylabel("Similarity Score")
    plt.title("Plagiarism Similarity Chart")
    st.pyplot(plt)
