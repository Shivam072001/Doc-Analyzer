def preprocess_text(text):
    """Implement text cleaning steps."""
    text = text.strip().replace('\n', ' ').replace('\r', '')
    return text