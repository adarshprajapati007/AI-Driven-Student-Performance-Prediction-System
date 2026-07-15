# AI-Driven Student Performance Prediction System
**Developed for the AICTE & IBM Internship Program**

## Overview
This machine learning application predicts a student's final academic grade based on their study habits, attendance, and previous scores. It is designed to act as an early-warning system for educational institutions to identify at-risk students and provide early academic intervention.

## Technologies Used
* **Python 3.10+**
* **Scikit-Learn:** Built a Random Forest Regressor model for high-accuracy predictions.
* **Pandas:** Managed and pre-processed the tabular dataset.
* **Streamlit:** Developed the interactive front-end dashboard.

## How to Run Locally
1. Clone or download this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

## Model Evaluation
The system utilizes a Random Forest Regressor, evaluated using Mean Absolute Error (MAE) and the R-squared ($R^2$) metric to ensure predictive reliability.