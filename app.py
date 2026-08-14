import streamlit as st
import matplotlib.pyplot as plt
from plagiarism import check_similarity
from explanation import generate_explanation


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Plagiarism Detector",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 AI Plagiarism Detection System")
st.markdown(
    """
    **Analyze text similarity using NLP, TF-IDF and Cosine Similarity.**

    Paste your text and upload reference documents to identify
    potential plagiarism or high textual similarity.
    """
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ How It Works")

    st.markdown(
        """
        1. Enter the text you want to analyze.
        2. Upload one or more reference `.txt` files.
        3. Click **Check Plagiarism**.
        4. The system calculates similarity scores.
        5. Review the score, classification and explanation.
        """
    )

    st.divider()

    st.info(
        "The system uses TF-IDF vectorization and "
        "Cosine Similarity for text comparison."
    )


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Text to Analyze")

    input_text = st.text_area(
        "Paste your text here:",
        height=300,
        placeholder="Enter or paste the text you want to check..."
    )


with col2:
    st.subheader("📚 Reference Documents")

    uploaded_files = st.file_uploader(
        "Upload reference .txt files:",
        type=["txt"],
        accept_multiple_files=True
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
                    f"Could not read {uploaded_file.name}. "
                    "Please upload a valid UTF-8 text file."
                )

        if documents:
            st.success(
                f"{len(documents)} reference document(s) uploaded."
            )


# --------------------------------------------------
# ANALYSIS BUTTON
# --------------------------------------------------

st.divider()

check_button = st.button(
    "🔍 Check Plagiarism",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# PLAGIARISM ANALYSIS
# --------------------------------------------------

if check_button:

    # Validate input text
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to analyze.")

    # Validate reference documents
    elif not documents:
        st.warning(
            "⚠️ Please upload at least one reference .txt document."
        )

    else:

        with st.spinner("Analyzing text similarity..."):

            try:

                scores = check_similarity(
                    input_text,
                    documents
                )

            except Exception as e:

                st.error(
                    "An error occurred while analyzing the text."
                )

                st.exception(e)

                st.stop()


        # --------------------------------------------------
        # RESULTS
        # --------------------------------------------------

        st.subheader("📊 Analysis Results")

        # Convert scores to percentages
        percentages = [
            score * 100 if score <= 1 else score
            for score in scores
        ]

        # Find highest similarity
        max_score = max(percentages)
        max_index = percentages.index(max_score)

        highest_source = document_names[max_index]


        # --------------------------------------------------
        # SUMMARY METRICS
        # --------------------------------------------------

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric(
                "Highest Similarity",
                f"{max_score:.2f}%"
            )

        with metric2:
            st.metric(
                "Reference Documents",
                len(documents)
            )

        with metric3:

            if max_score >= 80:
                status = "🔴 High"
            elif max_score >= 50:
                status = "🟠 Moderate"
            else:
                status = "🟢 Low"

            st.metric(
                "Similarity Level",
                status
            )


        st.divider()


        # --------------------------------------------------
        # CLASSIFICATION
        # --------------------------------------------------

        st.subheader("🎯 Overall Assessment")

        if max_score >= 80:

            st.error(
                f"🔴 **High Similarity Detected**\n\n"
                f"The analyzed text has **{max_score:.2f}% similarity** "
                f"with **{highest_source}**."
            )

        elif max_score >= 50:

            st.warning(
                f"🟠 **Moderate Similarity Detected**\n\n"
                f"The analyzed text has **{max_score:.2f}% similarity** "
                f"with **{highest_source}**."
            )

        else:

            st.success(
                f"🟢 **Low Similarity Detected**\n\n"
                f"The highest similarity score is "
                f"**{max_score:.2f}%**."
            )


        # --------------------------------------------------
        # INDIVIDUAL RESULTS
        # --------------------------------------------------

        st.subheader("📄 Document-wise Results")

        labels = []

        for i, score in enumerate(percentages):

            document_name = document_names[i]

            labels.append(document_name)

            with st.expander(
                f"📄 {document_name} — {score:.2f}% similarity"
            ):

                st.progress(
                    min(int(score), 100)
                )

                try:

                    explanation = generate_explanation(
                        score / 100 if score > 1 else score,
                        document_name
                    )

                    st.write(explanation)

                except Exception:

                    st.write(
                        "Similarity analysis completed for this document."
                    )


        # --------------------------------------------------
        # BAR CHART
        # --------------------------------------------------

        st.subheader("📈 Similarity Comparison")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            labels,
            percentages
        )

        ax.set_ylabel("Similarity (%)")
        ax.set_xlabel("Reference Document")
        ax.set_title("Document Similarity Scores")

        ax.set_ylim(0, 100)

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(fig)


        # --------------------------------------------------
        # FINAL NOTE
        # --------------------------------------------------

        st.divider()

        st.info(
            """
            **Note:** Similarity score indicates textual similarity
            between the submitted text and reference documents.
            A high similarity score does not automatically prove
            intentional plagiarism and should be reviewed in context.
            """
        )
