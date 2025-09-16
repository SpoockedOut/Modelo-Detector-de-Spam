from flask import Flask, render_template, request
import pickle
from utils import extract_features

app = Flask(__name__)

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
    app.run(debug=True)