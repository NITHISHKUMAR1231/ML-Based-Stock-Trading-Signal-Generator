import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from telemetry import calculate_telemetry
from features import generate_labels, get_features_and_labels


def train():
    df = pd.read_csv("../data/stock_data.csv")

    df = calculate_telemetry(df)
    df = generate_labels(df)
    X, y = get_features_and_labels(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    joblib.dump(model, "../models/model.pkl")

    print("Model trained successfully!")
    print("Accuracy:", accuracy)


if __name__ == "__main__":
    train()


