
from transformers import pipeline

def generate_summary(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]["summary_text"]
