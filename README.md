# PhishGuard AI — Phishing Email Detection Model

A college-ready machine learning project built with **Python, Flask and Scikit-learn**. It trains a TF-IDF + Logistic Regression classifier on labeled email text and provides a browser interface for prediction.

## Features
- Train on phishing and legitimate email dataset
- TF-IDF text feature extraction with unigrams + bigrams
- Logistic Regression classifier
- URL and suspicious-keyword feature analysis
- Phishing/Safe classification
- Confidence score
- Confusion matrix and test accuracy
- Retrain button
- Clean responsive web dashboard

## Project Structure
```
phishing_email_detection_model/
├── app.py
├── requirements.txt
├── data/
│   └── emails.csv
├── model/                 # generated automatically
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run on Windows
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Open Terminal and run:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
4. Open `http://127.0.0.1:5000` in your browser.

## How the model works
1. Email text is cleaned and converted into TF-IDF numerical features.
2. Logistic Regression learns patterns associated with Safe and Phishing emails.
3. The trained model predicts the class of a new email.
4. Additional rule-based signals inspect URLs, suspicious keywords and credential requests.
5. The dashboard displays prediction, confidence, extracted features and confusion matrix.

## Important academic note
The included CSV is a small **educational/demo dataset**. For a stronger final submission, replace `data/emails.csv` with a larger labeled dataset of real phishing and legitimate emails, then click **Retrain Model**. Do not claim production-level accuracy from this demo dataset.

## Viva points
**Algorithm:** Logistic Regression  
**Feature extraction:** TF-IDF  
**Evaluation:** Accuracy + Confusion Matrix  
**Frontend:** HTML/CSS/JavaScript  
**Backend:** Flask  
**Libraries:** Pandas, NumPy, Scikit-learn, Joblib
