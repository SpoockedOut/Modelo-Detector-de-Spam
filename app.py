from flask import Flask, render_template, request
import pickle
from utils import extract_features
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import os


app = Flask(__name__)


def generate_fake_data(n=500):
    X = []
    y = []
    for _ in range(n):
        # Spam
        x_spam = [
            np.random.randint(3, 7),   # suspicious words
            np.random.randint(1, 5),   # links
            1,                         # unknown sender
            np.random.randint(1, 8)    # malicious score
        ]
        X.append(x_spam)
        y.append(1)

        # Not spam
        x_ham = [
            np.random.randint(0, 3),
            np.random.randint(0, 2),
            0,
            np.random.randint(0, 3)
        ]
        X.append(x_ham)
        y.append(0)
    return np.array(X), np.array(y)

def train_model():
    X, y = generate_fake_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = MLPClassifier(hidden_layer_sizes=(6,), max_iter=1000, random_state=42)
    model.fit(X_scaled, y)

    with open("model.pkl", "wb") as f:
        pickle.dump((model, scaler), f)

if __name__ == "__main__":
    train_model()


with open("model.pkl", "rb") as f:
    model, scaler = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email_text = request.form.get("email")
        sender = request.form.get("sender")

        features = extract_features(email_text, sender)
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        result = "Spam" if prediction == 1 else "Não é spam"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
