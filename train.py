import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Define relevant features per disease
feature_sets = {
    "Diabetes": ['Age', 'Sex', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'GenHlth'],
    "Stroke": ['Age', 'Sex', 'MentHlth', 'PhysHlth', 'DiffWalk', 'PhysActivity', 'Fruits', 'Veggies', 'GenHlth'],
    "HighBP": ['Age', 'Sex', 'HighChol', 'BMI', 'Smoker', 'HvyAlcoholConsump', 'GenHlth']
}

# Load and train models for each disease
def train_model_safe(disease, csv_path, target_column, suggested_features):
    df = pd.read_csv(csv_path)

    # Convert YES/NO and categorical fields to 0/1
    binary_cols = ['Sex', 'HighChol', 'CholCheck', 'Smoker', 'HeartDiseaseorAttack',
                   'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'DiffWalk']
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: 1 if str(x).lower() in ['yes', '1', 'male', 'active'] else 0)

    # Use only available features
    features = [col for col in suggested_features if col in df.columns]

    X = df[features]
    y = df[target_column].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluation metrics
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    # Print metrics
    print(f"\n✅ Trained {disease} model")
    print(f"Accuracy: {acc*100:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")
    print(f"Confusion Matrix:\n{cm}")
    print(f"Features used: {features}")

    # Optional: Detailed classification report
    print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

    # Save model and used feature list
    with open(f"{disease.lower()}_model.pkl", "wb") as f:
        pickle.dump((model, features), f)

# Train all models
train_model_safe("Diabetes", "diabetes_data.csv", "Diabetes", feature_sets["Diabetes"])
train_model_safe("Stroke", "stroke_data.csv", "Stroke", feature_sets["Stroke"])
train_model_safe("HighBP", "highbp_data.csv", "HighBP", feature_sets["HighBP"])

print("\n✅✅✅ All models trained and saved successfully!")
