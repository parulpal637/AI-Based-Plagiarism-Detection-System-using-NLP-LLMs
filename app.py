import streamlit as st
import matplotlib.pyplot as plt

from plagiarism import (
    check_similarity,
    classify,
    get_similarity_percentage
)

from explanation import generate_explanation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Plagiarism Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Cards */
    .info-card {
        padding: 22px;
        border-radius: 14px;
        background-color: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Section headings */
    .section-title {
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* Result cards */
    .result-card {
        padding: 20px;
        border-radius: 14px;
        background-color: white;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    .result-number {
        font-size: 30px;
        font-weight: 800;
    }

    .result-label {
        color: #64748b;
        font-size: 14px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 40px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧠 AI Plagiarism Detector")

    st.divider()

    st.markdown("### ⚙️ How It Works")

    st.markdown(
        """
        **1. Enter text**

        Paste the content you want to analyze.

        **2. Upload references**

        Upload one or more `.txt` files.

        **3. Analyze**

        The system compares the submitted text with the references.

        **4. Review results**

        Get similarity scores, classification and explanations.
        """
    )

    st.divider()

    st.markdown("### 🔬 Technology")

    st.markdown(
        """
        - Python
        - Streamlit
        - Scikit-learn
        - TF-IDF
        - Cosine Similarity
        - NLP
        """
    )

    st.divider()

    st.info(
        "A high similarity score indicates textual overlap. "
        "It does not automatically prove intentional plagiarism."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧠 AI Plagiarism Detection System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'NLP-powered text similarity analysis using TF-IDF and Cosine Similarity'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

left, right = st.columns(2)


# ------------------------------------------------------------
# TEXT INPUT
# ------------------------------------------------------------

with left:

    st.markdown(
        '<div class="section-title">📝 Text to Analyze</div>',
        unsafe_allow_html=True
    )

    input_text = st.text_area(
        "Paste the content you want to check:",
        height=280,
        placeholder=(
            "Example:\n\n"
            "Machine learning is a branch of artificial intelligence..."
        ),
        label_visibility="collapsed"
    )

    if input_text:
        word_count = len(input_text.split())
        character_count = len(input_text)

        st.caption(
            f"Words: {word_count}  •  Characters: {character_count}"
        )


# ------------------------------------------------------------
# DOCUMENT UPLOAD
# ------------------------------------------------------------

with right:

    st.markdown(
        '<div class="section-title">📚 Reference Documents</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload reference documents:",
        type=["txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    documents = []
    document_names = []

    if uploaded_files:

        for uploaded_file in uploaded_files:

            try:

                text = uploaded_file.read().decode("utf-8")

                if text.strip():

                    documents.append(text)
                    document_names.append(uploaded_file.name)

            except Exception:

                st.error(
                    f"Unable to read {uploaded_file.name}."
                )

        if documents:

            st.success(
                f"✅ {len(documents)} reference document(s) ready."
            )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze = st.button(
    "🔍 Analyze Text",
    type="primary",
    use_container_width=True
)


# ============================================================
# VALIDATION + ANALYSIS
# ============================================================

if analyze:

    if not input_text.strip():

        st.warning(
            "⚠️ Please enter some text before starting the analysis."
        )

        st.stop()

    if not documents:

        st.warning(
            "⚠️ Please upload at least one reference `.txt` file."
        )

        st.stop()

    # --------------------------------------------------------
    # RUN MODEL
    # --------------------------------------------------------

    with st.spinner("🧠 Analyzing text similarity..."):

        try:

            scores = check_similarity(
                input_text,
                documents
            )

        except Exception as error:

            st.error(
                "Something went wrong during analysis."
            )

            st.exception(error)

            st.stop()


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Analysis Summary</div>',
        unsafe_allow_html=True
    )


    # Convert scores to percentages
    percentages = [
        get_similarity_percentage(float(score))
        for score in scores
    ]


    # Highest similarity
    highest_score = max(percentages)

    highest_index = percentages.index(highest_score)

    highest_document = document_names[highest_index]

    highest_classification = classify(
        float(scores[highest_index])
    )


    # ========================================================
    # METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Highest Similarity",
            f"{highest_score:.2f}%"
        )


    with col2:

        st.metric(
            "Documents Checked",
            len(documents)
        )


    with col3:

        if highest_classification == "Original":

            risk = "🟢 Low"

        elif highest_classification == "Suspected":

            risk = "🟠 Moderate"

        else:

            risk = "🔴 High"

        st.metric(
            "Similarity Risk",
            risk
        )


    # ========================================================
    # OVERALL ASSESSMENT
    # ========================================================

    st.markdown("")

    if highest_classification == "Original":

        st.success(
            f"🟢 **Low Similarity** — "
            f"The highest similarity found was "
            f"**{highest_score:.2f}%** with `{highest_document}`."
        )

    elif highest_classification == "Suspected":

        st.warning(
            f"🟠 **Moderate Similarity** — "
            f"The highest similarity found was "
            f"**{highest_score:.2f}%** with `{highest_document}`. "
            f"Manual review is recommended."
        )

    else:

        st.error(
            f"🔴 **High Similarity** — "
            f"The highest similarity found was "
            f"**{highest_score:.2f}%** with `{highest_document}`. "
            f"Further review is recommended."
        )


    # ========================================================
    # DOCUMENT RESULTS
    # ========================================================

    st.markdown("### 📄 Document-wise Results")


    for i, score in enumerate(scores):

        percentage = percentages[i]

        document_name = document_names[i]

        classification = classify(
            float(score)
        )


        with st.expander(
            f"📄 {document_name}  •  {percentage:.2f}% similarity"
        ):

            st.progress(
                min(max(float(score), 0.0), 1.0)
            )

            if classification == "Original":

                st.success(
                    f"Classification: **{classification}**"
                )

            elif classification == "Suspected":

                st.warning(
                    f"Classification: **{classification}**"
                )

            else:

                st.error(
                    f"Classification: **{classification}**"
                )


            explanation = generate_explanation(
                float(score),
                document_name
            )

            st.write(explanation)


    # ========================================================
    # CHART
    # ========================================================

    st.markdown("### 📈 Similarity Comparison")


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    ax.bar(
        document_names,
        percentages
    )


    ax.set_ylabel(
        "Similarity (%)"
    )

    ax.set_xlabel(
        "Reference Documents"
    )

    ax.set_title(
        "Text Similarity Scores"
    )

    ax.set_ylim(
        0,
        100
    )


    plt.xticks(
        rotation=35,
        ha="right"
    )

    plt.tight_layout()

    st.pyplot(
        fig
    )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.info(
        """
        **Important:** Similarity detection identifies textual overlap
        between documents. A high score does not automatically prove
        intentional plagiarism. Results should be reviewed in context.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Built with Python • Streamlit • Scikit-learn • NLP
        <br>
        AI Plagiarism Detection System
    </div>
    """,
    unsafe_allow_html=True
)