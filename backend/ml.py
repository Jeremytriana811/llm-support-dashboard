"""
ml.py — AI/ML module using Hugging Face Transformers.

This file uses two pre-trained models:
  1. A text-classification model to categorize tickets
  2. A summarization model to generate one-sentence summaries

KEY CONCEPT: "Inference" means using an already-trained model to make
predictions on new data. We are NOT training anything here — just using
models that others already trained.

The pipeline() function from Hugging Face is a high-level helper that
handles tokenization, model loading, and prediction in one call.
"""

import os
from transformers import pipeline

# ---------------------------------------------------------------------------
# 1. Load models (this happens once when the server starts)
# ---------------------------------------------------------------------------
# We use an environment variable to allow skipping model loading in tests
# or when you just want to test the API without waiting for big downloads.
USE_REAL_MODELS = os.getenv("USE_REAL_MODELS", "true").lower() == "true"

if USE_REAL_MODELS:
    print("⏳ Loading AI models (this may take a minute on first run)...")

    # --- Classification Model ---
    # This model outputs labels like "POSITIVE" or "NEGATIVE".
    # We'll map those to support categories below.
    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True,
        max_length=512,
    )

    # --- Summarization Model ---
    # distilbart-cnn-12-6 is a smaller, faster summarization model (~1.2 GB).
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        truncation=True,
        max_length=60,
        min_length=15,
    )

    print("✅ AI models loaded successfully!")
else:
    classifier = None
    summarizer = None
    print("⚠️  Running WITHOUT AI models (USE_REAL_MODELS=false)")


# ---------------------------------------------------------------------------
# 2. Category mapping
# ---------------------------------------------------------------------------
# The sentiment model only knows POSITIVE/NEGATIVE, so we map those to
# support categories using simple keyword heuristics + sentiment.
#
# In a real production system, you'd fine-tune a model on actual ticket data.
# This is a great talking point in interviews!

KEYWORD_MAP = {
    "bug":           ["bug", "error", "crash", "broken", "fail", "fix", "issue", "wrong", "not working"],
    "feature":       ["feature", "request", "add", "new", "enhance", "improve", "wish", "want", "would be nice"],
    "question":      ["how", "what", "why", "where", "when", "?", "help", "confused", "understand"],
    "documentation": ["docs", "documentation", "readme", "guide", "tutorial", "example", "explain"],
}


def classify_ticket(text: str) -> str:
    """
    Classify a ticket's description into one of:
    bug, feature, question, documentation.

    Strategy:
      1. Check for keyword matches first (most reliable for support tickets).
      2. Fall back to the sentiment model (NEGATIVE → bug, POSITIVE → feature).
    """
    if not USE_REAL_MODELS:
        return "question"    # Default when models are disabled

    text_lower = text.lower()

    # --- Keyword-based classification ---
    scores = {}
    for category, keywords in KEYWORD_MAP.items():
        scores[category] = sum(1 for kw in keywords if kw in text_lower)

    best_category = max(scores, key=scores.get)
    if scores[best_category] > 0:
        return best_category

    # --- Fallback: sentiment-based classification ---
    result = classifier(text[:512])[0]
    label = result["label"]           # "POSITIVE" or "NEGATIVE"

    if label == "NEGATIVE":
        return "bug"
    else:
        return "feature"


def summarize_ticket(text: str) -> str:
    """
    Generate a one-sentence summary of the ticket description.

    If the text is very short (< 30 chars), we just return it as-is
    because summarization models need enough text to work with.
    """
    if not USE_REAL_MODELS:
        return text[:100] + ("..." if len(text) > 100 else "")

    # Summarization models need a minimum amount of text
    if len(text) < 30:
        return text

    try:
        result = summarizer(text[:1024], max_length=60, min_length=10, do_sample=False)
        return result[0]["summary_text"].strip()
    except Exception as e:
        # If summarization fails for any reason, return a truncated version
        print(f"⚠️  Summarization failed: {e}")
        return text[:100] + ("..." if len(text) > 100 else "")
