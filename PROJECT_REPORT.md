# Project Report — Phishing Email Detection Model

## Abstract
Phishing emails are fraudulent messages designed to trick users into revealing credentials, financial information, or other sensitive data. This project develops a machine learning based phishing email detector using Scikit-learn. The system converts email text into TF-IDF features and trains a Logistic Regression classifier to distinguish phishing emails from safe emails. A Flask web interface allows users to paste an email and instantly receive the predicted class, confidence score, suspicious signals, and model evaluation information.

## Objectives
1. Detect phishing emails automatically.
2. Extract useful textual and URL-related features.
3. Train and evaluate a supervised machine learning model.
4. Display accuracy and confusion matrix.
5. Provide an easy-to-use browser interface.

## Methodology
Dataset → preprocessing → TF-IDF feature extraction → Logistic Regression training → testing → prediction → web display.

## Technologies
Python, Flask, Scikit-learn, Pandas, NumPy, Joblib, HTML, CSS and JavaScript.

## Modules
- Dataset Management
- Text Feature Extraction
- ML Model Training
- Email Prediction
- URL/Suspicious Signal Analysis
- Model Evaluation
- Web Dashboard

## Future Scope
A future version can use a much larger real-world dataset, email header analysis, sender/domain reputation, HTML inspection, attachment analysis, deep learning models, and an API for enterprise mail gateways.

## Conclusion
The project demonstrates how supervised machine learning can be applied to email security. TF-IDF captures important textual patterns while Logistic Regression provides a lightweight and interpretable classification model. The Flask interface makes the trained model accessible to non-technical users.
