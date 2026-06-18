from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import sys
import sqlite3

# Add root folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database import init_db
from phishing_detector import phishing_detector, risk_level

# Initialize database
init_db()

app = Flask(__name__)
CORS(app)

# Database path
DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "database",
    "history.db"
)

# Load ML model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "model.pkl"
)

VECTORIZER_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "vectorizer.pkl"
)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)


@app.route("/")
def home():
    return "Spam Detection API Running"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    email = data.get("email", "").strip()

    if not email:
        return jsonify({"error": "Email text required"}), 400

    # ML Prediction
    email_vector = vectorizer.transform([email]).toarray()
    prediction = model.predict(email_vector)[0]
    prediction_label = "SPAM" if prediction == 1 else "HAM"

    # Confidence
    probabilities = model.predict_proba(email_vector)[0]
    confidence = round(max(probabilities) * 100, 2)

    # Phishing Detection
    score, reasons = phishing_detector(email)
    risk = risk_level(score)

    # Save to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history
        (email, prediction, confidence, phishing_score, risk_level)
        VALUES (?, ?, ?, ?, ?)
    """, (
        email,
        prediction_label,
        confidence,
        score,
        risk
    ))

    conn.commit()
    conn.close()

    result = {
        "prediction": prediction_label,
        "confidence": confidence,
        "phishing_score": score,
        "risk_level": risk,
        "reasons": reasons
    }

    return jsonify(result)


@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, prediction, confidence, phishing_score, risk_level, created_at
        FROM scan_history
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    history_data = []

    for row in rows:
        history_data.append({
            "id": row[0],
            "prediction": row[1],
            "confidence": row[2],
            "score": row[3],
            "risk_level": row[4],
            "created_at": row[5]
        })

    return jsonify(history_data)


@app.route("/stats", methods=["GET"])
def stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction='SPAM'")
    spam = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction='HAM'")
    ham = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level='HIGH'")
    high_risk = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total": total,
        "spam": spam,
        "ham": ham,
        "high_risk": high_risk
    })


if __name__ == "__main__":
    app.run(debug=True)