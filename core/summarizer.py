import re

def summarizer_check(text, max_sentences=3):
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = ' '.join(sentences[:max_sentences])
    return summary.strip()
