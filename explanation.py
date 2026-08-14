def generate_explanation(score, source_name):
    """
    Generate a human-readable explanation
    based on the similarity score.
    """

    # Convert decimal score to percentage
    percentage = score * 100 if score <= 1 else score

    if score < 0.30:
        return (
            f"🟢 Low similarity with {source_name}. "
            f"The similarity score is {percentage:.2f}%, "
            "which suggests that the submitted text has "
            "relatively little textual overlap with this document."
        )

    elif score < 0.70:
        return (
            f"🟠 Moderate similarity with {source_name}. "
            f"The similarity score is {percentage:.2f}%, "
            "which indicates some notable textual overlap. "
            "The content should be reviewed manually."
        )

    else:
        return (
            f"🔴 High similarity with {source_name}. "
            f"The similarity score is {percentage:.2f}%, "
            "which indicates substantial textual overlap. "
            "Further manual review is recommended."
        )
