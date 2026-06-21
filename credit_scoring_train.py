import pandas as pd
import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

warnings.filterwarnings("ignore")


def load_and_prepare(path="credit_data.csv"):
    df = pd.read_csv(path)
    drop_cols = [c for c in ["Race", "Gender"] if c in df.columns]
    if drop_cols:
        print(f"Dropping protected attributes: {drop_cols}")
        df = df.drop(columns=drop_cols)
    else:
        print("Columns Race/Gender not found — proceeding with available data.")
    required = ["Zip_Code", "Income", "target"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def main():
    df = load_and_prepare()

    features = ["Zip_Code", "Income"]
    target = "target"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print(f"Feature importances: {dict(zip(features, model.feature_importances_))}")


if __name__ == "__main__":
    main()
