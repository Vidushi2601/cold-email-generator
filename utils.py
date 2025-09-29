import re

def clean_text(text):
    text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML tags
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)  # Keep basic punctuation
    text = re.sub(r'\s{2,}', ' ', text)  # Collapse multiple spaces
    return text.strip()