"""
ml.py

This file handles the AI part of the project.

It can:
1. classify a ticket
2. summarize a ticket

If USE_REAL_MODELS=false, it skips loading Hugging Face models.
That helps you test the backend without big downloads or PyTorch errors.
"""

import os

# Check if we want to use the real AI models
USE_REAL_MODELS = os.getenv("USE_REAL_MODELS", "true").lower() == "true"

# Load models only if real models are turned on
if USE_REAL_MODELS:
    from transformers import pipeline

    print("Loading AI models...")

    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True,
        max_length=512,
    )

    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        truncation=True,
        max_length=60,
        min_length=15,
    )

    print("AI models loaded.")
else:
    classifier = None
    summarizer = None
    print("Running without real AI models.")

# Simple keyword map for ticket categories
KEYWORD_MAP = {
    "bug": ["bug", "error", "crash", "broken", "fail", "fix", "issue", "wrong", "not working"],
    "feature": ["feature", "request", "add", "new", "enhance", "improve", "wish", "want", "would be nice"],
    "question": ["how", "what", "why", "where", "when", "?", "help", "confused", "understand"],
    "documentation": ["docs", "documentation", "readme", "guide", "tutorial", "example", "explain"],
}


def classify_ticket(text: str) -> str:
    """
    Classify the ticket into:
    bug, feature, question, or documentation
    """

    # If models are off, return a basic default
    if not USE_REAL_MODELS:
        return "question"

    text_lower = text.lower()

    # Check keywords first
    scores = {}
    for category, keywords in KEYWORD_MAP.items():
        scores[category] = sum(1 for kw in keywords if kw in text_lower)

    best_category = max(scores, key=scores.get)

    if scores[best_category] > 0:
        return best_category

    # If no keyword match, use sentiment model
    result = classifier(text[:512])[0]
    label = result["label"]

    if label == "NEGATIVE":
        return "bug"
    else:
        return "feature"


def summarize_ticket(text: str) -> str:
    """
    Make a short summary of the ticket text
    """

    # If models are off, just return shortened text
    if not USE_REAL_MODELS:
        return text[:100] + ("..." if len(text) > 100 else "")

    # If text is already short, return it
    if len(text) < 30:
        return text

    try:
        result = summarizer(
            text[:1024],
            max_length=60,
            min_length=10,
            do_sample=False
        )
        return result[0]["summary_text"].strip()
    except Exception as e:
        print(f"Summarization failed: {e}")
        return text[:100] + ("..." if len(text) > 100 else "")