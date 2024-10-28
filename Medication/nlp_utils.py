from transformers import pipeline

# Load a pre-trained sentiment analysis model from Hugging Face
sentiment_analysis = pipeline("sentiment-analysis")

def analyze_side_effect_severity(description):
    print(f"Analyzing: {description}")

    # keyword-based rules to determine severity
    keywords_mild = ["slight", "rare", "minor"]
    keywords_moderate = ["common", "frequent", "manageable"]
    keywords_severe = ["severe", "intense", "persistent"]

    if any(word in description.lower() for word in keywords_mild):
        return {"label": "mild", "score": 0.3}
    elif any(word in description.lower() for word in keywords_moderate):
        return {"label": "moderate", "score": 0.6}
    elif any(word in description.lower() for word in keywords_severe):
        return {"label": "severe", "score": 0.9}

    # Default to sentiment analysis if no keyword match
    result = sentiment_analysis(description)[0]
    print(f"Sentiment Analysis Result: {result}")  
    label = result['label']  # Positive, Negative, or Neutral
    score = result['score']  # Confidence score

    # Map sentiment labels to severity with adjusted thresholds
    if label == "POSITIVE":
        severity_label = "mild"
        severity_score = score * 0.3
    elif label == "NEUTRAL":
        severity_label = "moderate"
        severity_score = score * 0.5
    elif label == "NEGATIVE" and score < 0.95:
        severity_label = "moderate"
        severity_score = score * 0.7
    else:
        severity_label = "severe"
        severity_score = score * 1.0

    return {"label": severity_label, "score": severity_score}
