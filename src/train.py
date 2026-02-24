import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
from telemetry import calculate_telemetry
from features import  get_features_and_labels
from label_module import generate_labels
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FOLDER = os.path.join(BASE_DIR, "..", "models")
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")
def get_all_datasets():
    # Automatically get all CSV files
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    
    if not files:
        raise Exception("No CSV files found in data folder!")

    return files


def select_dataset(files):
    print("\nAvailable Datasets:\n")
    
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")

    while True:
        try:
            choice = int(input("\nSelect dataset number: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a valid number.")
def train():
    files=get_all_datasets()
    selected_file=select_dataset(files)
    file_path = os.path.join(DATA_FOLDER, selected_file)
    print(f"\nUsing dataset: {selected_file}\n")

    df = pd.read_csv(file_path)

    df = calculate_telemetry(df)
    df = generate_labels(df)
    X, y = get_features_and_labels(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    train_data=pd.concat([X_train,y_train],axis=1)
    train_data.to_csv("data/train/train.csv",index=False)
    test_data=pd.concat([X_test,y_test],axis=1)
    test_data.to_csv("data/test/test.csv",index=False)
    
    accuracy = model.score(X_test, y_test)
    today_date=datetime.now().strftime("%y-%m-%d")
    os.makedirs(MODEL_FOLDER, exist_ok=True)
    model_name = f"model_{today_date}.pkl"
    model_path = os.path.join(MODEL_FOLDER, model_name)


    joblib.dump(model,model_path)

    print("Model trained successfully!")
    print("Accuracy:", accuracy)


if __name__ == "__main__":
    train()


