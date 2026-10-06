
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import re, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "emails.csv")
MODEL_DIR = os.path.join(BASE, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(MODEL_DIR, "email_model.joblib")
meta_path = os.path.join(MODEL_DIR, "metadata.joblib")

def url_features(text):
    urls = re.findall(r'https?://[^\s<>"\']+', text.lower())
    url_count = len(urls)
    suspicious_words = ["login", "verify", "secure", "account", "update", "confirm",
                        "password", "otp", "bank", "urgent", "claim", "refund", "payment"]
    keyword_count = sum(text.lower().count(k) for k in suspicious_words)
    special_count = sum(text.count(c) for c in ["@", "$", "!", "%"])
    return {
        "urls": url_count,
        "suspicious_keywords": keyword_count,
        "special_characters": special_count,
        "has_http_url": int(url_count > 0),
        "has_ip_like_url": int(bool(re.search(r'https?://\d{1,3}(?:\.\d{1,3}){3}', text.lower()))),
    }

def train_model():
    df = pd.read_csv(DATA).dropna()
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
    )
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english",
                                  ngram_range=(1,2), max_features=5000)),
        ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced"))
    ])
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred, labels=["Safe", "Phishing"])
    meta = {
        "accuracy": round(float(acc) * 100, 2),
        "samples": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "confusion_matrix": cm.tolist(),
        "classes": ["Safe", "Phishing"],
        "report": classification_report(y_test, pred, output_dict=True, zero_division=0)
    }
    joblib.dump(pipeline, model_path)
    joblib.dump(meta, meta_path)
    return pipeline, meta

if os.path.exists(model_path) and os.path.exists(meta_path):
    model = joblib.load(model_path)
    metadata = joblib.load(meta_path)
else:
    model, metadata = train_model()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", meta=metadata)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = (data.get("email") or "").strip()
    if len(text) < 5:
        return jsonify({"error": "Please enter a complete email message."}), 400

    pred = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    classes = list(model.classes_)
    confidence = float(probabilities[classes.index(pred)]) * 100
    features = url_features(text)

    # Add simple explainability based on suspicious signals.
    reasons = []
    lower = text.lower()
    if features["urls"] > 0:
        reasons.append(f"{features['urls']} URL(s) detected")
    if features["suspicious_keywords"] > 0:
        reasons.append(f"{features['suspicious_keywords']} suspicious keyword matches")
    if features["has_ip_like_url"]:
        reasons.append("URL contains an IP address")
    if any(k in lower for k in ["otp", "password", "bank details", "card details"]):
        reasons.append("Requests sensitive credentials or financial information")
    if any(k in lower for k in ["urgent", "immediate", "final notice", "today"]):
        reasons.append("Uses urgency or pressure language")
    if not reasons:
        reasons.append("No major suspicious signal detected")

    return jsonify({
        "prediction": pred,
        "confidence": round(confidence, 2),
        "features": features,
        "reasons": reasons
    })

@app.route("/retrain", methods=["POST"])
def retrain():
    global model, metadata
    model, metadata = train_model()
    return jsonify({"message": "Model retrained successfully.", "meta": metadata})

if __name__ == "__main__":
    app.run(debug=True)
