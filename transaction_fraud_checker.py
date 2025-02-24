import pandas as pd
import joblib
import hashlib
import time
import random

# Load Fraud Detection Model
fraud_model = joblib.load("fraud_model.pkl")

# Load Feature Names
feature_names = joblib.load("feature_names.pkl")

# Blockchain Class (For Secure Transaction Storage)
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0", data={"system": "Blockchain Initialized"})

    def create_block(self, previous_hash, data):
        block_content = f"{previous_hash}{data}{time.time()}"
        block_hash = hashlib.sha256(block_content.encode()).hexdigest()
        block = {"index": len(self.chain) + 1, "previous_hash": previous_hash, "data": data, "hash": block_hash}
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1] if self.chain else None

# Initialize Blockchain
blockchain = Blockchain()

# Risk Analysis Function (Before AI Prediction)
def assess_risk(transaction):
    risk_score = 0
    risk_factors = []

    if transaction["amount"] > 10000:
        risk_score += 2
        risk_factors.append("🔴 High Transaction Amount")

    if transaction["transaction_speed"] < 2:
        risk_score += 1
        risk_factors.append("🟠 Very Fast Transaction")

    if transaction["sender_country"] != transaction["receiver_country"]:
        risk_score += 1
        risk_factors.append("🟡 Cross-Border Transfer")

    return risk_score, risk_factors

# Process Transactions (Multiple Transactions Supported)
def process_transactions(transactions):
    results = []

    for tx in transactions:
        print("\n🔍 Processing Transaction:")
        print(tx)

        # Perform Risk Analysis
        risk_score, risk_factors = assess_risk(tx)
        print(f"📊 Risk Score: {risk_score} / 4")
        for factor in risk_factors:
            print(f"   - {factor}")

        # Convert Transaction to DataFrame
        df = pd.DataFrame([tx])

        # One-hot encoding (matching training features)
        df = pd.get_dummies(df, columns=["sender_country", "receiver_country"])

        # Ensure all expected columns exist (add missing ones with value 0)
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0

        # Reorder columns to match training order
        df = df[feature_names]

        # AI Fraud Prediction
        fraud_probability = fraud_model.predict_proba(df)[0][1]  # Get probability
        is_fraud = fraud_probability > 0.5  # Threshold-based fraud detection

        # Blockchain Storage
        last_block = blockchain.get_last_block()
        blockchain.create_block(last_block["hash"], {"transaction": tx, "fraud_probability": round(fraud_probability * 100, 2)})

        # Display Results
        print(f"🤖 AI Fraud Probability: {round(fraud_probability * 100, 2)}%")
        print(f"🚨 Fraud Detected: {'✅ YES' if is_fraud else '❌ NO'}")

        results.append({"transaction": tx, "fraud_probability": round(fraud_probability * 100, 2), "is_fraud": is_fraud})

    return results

# Example Transactions
transactions_list = [
    {"amount": 5000, "sender_balance": 20000, "receiver_balance": 15000, "transaction_speed": 2, "sender_country": "IN", "receiver_country": "US"},
    {"amount": 15000, "sender_balance": 50000, "receiver_balance": 30000, "transaction_speed": 1, "sender_country": "UK", "receiver_country": "SG"},
    {"amount": 800, "sender_balance": 4000, "receiver_balance": 2000, "transaction_speed": 3, "sender_country": "IN", "receiver_country": "IN"},
    {"amount": 22000, "sender_balance": 60000, "receiver_balance": 10000, "transaction_speed": 1, "sender_country": "US", "receiver_country": "UK"}
]

# Start Processing
print("\n🚀 Starting Transaction Processing...")
processed_results = process_transactions(transactions_list)
