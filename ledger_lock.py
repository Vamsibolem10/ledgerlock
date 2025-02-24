import pandas as pd
import joblib
import hashlib
import time
import json

# Load Fraud Detection Model
fraud_model = joblib.load("fraud_model.pkl")

# Load Feature Names
feature_names = joblib.load("feature_names.pkl")

# Blockchain Class for Secure & Transparent Transactions
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0", data={"system": "Ledger-Lock Initialized"})

    def create_block(self, previous_hash, data):
        """Creates a new block with transaction data."""
        block_content = json.dumps({"previous_hash": previous_hash, "data": data, "timestamp": time.time()}, sort_keys=True)
        block_hash = hashlib.sha256(block_content.encode()).hexdigest()
        block = {"index": len(self.chain) + 1, "previous_hash": previous_hash, "data": data, "hash": block_hash}
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1] if self.chain else None

# Smart Contract Simulation (Automated Compliance Checks)
class SmartContract:
    @staticmethod
    def check_kyc(transaction):
        """Simulates KYC verification using blockchain identity."""
        verified_users = {"IN12345", "US67890", "SG34567"}  # Sample verified users
        if transaction["sender_id"] in verified_users and transaction["receiver_id"] in verified_users:
            return True
        return False

    @staticmethod
    def enforce_compliance(transaction):
        """Checks for money laundering risk using rule-based and AI models."""
        if transaction["amount"] > 25000:  # Flagging high-value transactions
            return False, "High-risk transaction amount"
        return True, "Compliant"

# AML System with AI + Blockchain
class LedgerLock:
    def __init__(self):
        self.blockchain = Blockchain()

    def process_transaction(self, transaction):
        """Processes and evaluates transactions for fraud detection and compliance."""
        print("\n🔍 Processing Transaction:", transaction)

        # Step 1: Verify KYC Compliance
        if not SmartContract.check_kyc(transaction):
            print("❌ KYC Verification Failed: Sender or receiver is not verified.")
            return "Transaction Rejected: KYC Failed"

        # Step 2: Compliance Check (AML Rule-based)
        compliant, reason = SmartContract.enforce_compliance(transaction)
        if not compliant:
            print(f"⚠️ AML Compliance Failed: {reason}")
            return f"Transaction Rejected: {reason}"

        # Step 3: Machine Learning-based Fraud Detection
        df = pd.DataFrame([transaction])
        df = pd.get_dummies(df, columns=["sender_country", "receiver_country"])
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0
        df = df[feature_names]

        fraud_probability = fraud_model.predict_proba(df)[0][1]
        is_fraud = bool(fraud_probability > 0.5)  # ✅ FIX: Convert NumPy bool_ to Python bool

        # Step 4: Store in Blockchain
        last_block = self.blockchain.get_last_block()
        block_data = {
            "transaction": transaction,
            "fraud_probability": round(fraud_probability * 100, 2),
            "is_fraud": bool(is_fraud)  # ✅ FIX: Convert NumPy bool_ to Python bool
        }
        self.blockchain.create_block(last_block["hash"], block_data)

        # Step 5: Display Final Result
        print(f"🤖 AI Fraud Probability: {round(fraud_probability * 100, 2)}%")
        print(f"🚨 Fraud Detected: {'✅ YES' if is_fraud else '❌ NO'}")
        return "Transaction Processed Successfully"

# Example Transactions (with KYC and AML checks)
transactions_list = [
    {"amount": 5000, "sender_balance": 20000, "receiver_balance": 15000, "transaction_speed": 2,
     "sender_country": "IN", "receiver_country": "US", "sender_id": "IN12345", "receiver_id": "US67890"},

    {"amount": 30000, "sender_balance": 50000, "receiver_balance": 25000, "transaction_speed": 1,
     "sender_country": "UK", "receiver_country": "SG", "sender_id": "UK54321", "receiver_id": "SG34567"},  # No KYC

    {"amount": 12000, "sender_balance": 30000, "receiver_balance": 15000, "transaction_speed": 3,
     "sender_country": "IN", "receiver_country": "IN", "sender_id": "IN12345", "receiver_id": "IN12345"},

    {"amount": 26000, "sender_balance": 70000, "receiver_balance": 20000, "transaction_speed": 1,
     "sender_country": "US", "receiver_country": "UK", "sender_id": "US67890", "receiver_id": "UK54321"}  # High-risk
]

# Start Processing Transactions
ledger_lock = LedgerLock()
print("\n🚀 Starting Ledger-Lock AML System...\n")
for tx in transactions_list:
    result = ledger_lock.process_transaction(tx)
    print(f"📝 Transaction Status: {result}\n")
