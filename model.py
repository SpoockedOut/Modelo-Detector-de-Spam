import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

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