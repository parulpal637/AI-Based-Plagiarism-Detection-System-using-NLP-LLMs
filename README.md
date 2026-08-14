# AI-Based Plagiarism Detection System (NLP Project)

## Overview

This project is an NLP-based plagiarism detection system that compares input text with reference documents and identifies similarity using machine learning techniques. It uses TF-IDF vectorization and cosine similarity to measure how closely two texts match and classifies them as Original, Suspected, or Copied.

## Features

* Text similarity detection using NLP
* TF-IDF based feature extraction
* Cosine similarity calculation
* Classification of text into:

  * Original
  * Suspected
  * Copied
* Modular Python implementation
* Simple and easy-to-use design

## Technologies Used

* Python
* Scikit-learn
* TF-IDF Vectorizer
* Cosine Similarity
* NLP (Natural Language Processing)

## Project Workflow

1. Input text is provided by the user.
2. Reference documents are loaded.
3. Text is converted into numerical vectors using TF-IDF.
4. Cosine similarity is calculated between documents.
5. Based on similarity score, text is classified:

   * Low similarity → Original
   * Medium similarity → Suspected
   * High similarity → Copied

## Classification Logic

* Score < 0.3 → Original
* Score 0.3 – 0.7 → Suspected
* Score > 0.7 → Copied

## Example

Input Text:
Artificial Intelligence is a branch of computer science.

Reference:
Machine learning allows computers to learn from data.

Output:
Suspected / Similar content detected

## Learning Outcomes

* Understanding Natural Language Processing (NLP)
* TF-IDF vectorization technique
* Cosine similarity for text comparison
* Text classification using threshold logic
* Building modular Python ML applications

## Limitations

* Works only on text-based similarity
* Does not understand deep semantic meaning
* No deep learning or transformer models used
* Requires manual input of reference documents

## Future Improvements

* Integrate transformer models like BERT or LLMs
* Add file upload support (PDF, DOCX)
* Build web interface using Streamlit or Flask
* Improve accuracy using advanced NLP techniques
* Add multi-language support

## Author

Parul Pal
BCA Student | Aspiring AI/ML Engineer
