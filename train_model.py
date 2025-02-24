import pandas as pd
import xgboost as xgb
import joblib

# Load dataset
df = pd.read_csv("transactions.csv")

# Convert categorical data (One-Hot Encoding)
df = pd.get_dummies(df, columns=["sender_country", "receiver_country"], drop_first=True)

# Define Features & Labels
X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]

# Save feature names **after** defining X
feature_names = X.columns.tolist()
joblib.dump(feature_names, "feature_names.pkl")

# Train Model
model = xgb.XGBClassifier()
model.fit(X, y)

# Save Model
joblib.dump(model, "fraud_model.pkl")
print("✅ Model trained & saved successfully!")
