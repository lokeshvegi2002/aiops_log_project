import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
import sys # <-- CHANGE 1: Import the 'sys' module

print("Starting AI model...")

# --- 1. Load and Prepare the Data ---
try:
    log_data_raw = pd.read_csv(
        'app.log', 
        sep=' - ', 
        header=None, 
        names=['timestamp', 'logger', 'level', 'message'],
        engine='python'
    )
except FileNotFoundError:
    print("Error: 'app.log' not found.")
    print("This is normal in a CI pipeline, no anomalies to report.")
    sys.exit(0) # Exit successfully if no log file exists
except pd.errors.EmptyDataError:
    print("Error: 'app.log' is empty.")
    print("No data to analyze, no anomalies to report.")
    sys.exit(0) # Exit successfully if log file is empty

# Filter out the 'Application starting up...' message
log_data = log_data_raw[log_data_raw['message'] != 'Application starting up...'].copy()

if log_data.empty:
    print("Log file only contained startup messages. No data to analyze.")
    sys.exit(0) # Exit successfully

print(f"Loaded {len(log_data_raw)} log entries. Analyzing {len(log_data)} runtime entries.")


# --- 2. Convert Text Logs into Numbers (Vectorization) ---
vectorizer = TfidfVectorizer()
log_vectors = vectorizer.fit_transform(log_data['message'])

print("Converted log messages into numerical vectors.")

# --- 3. Train the AI Model (Isolation Forest) ---
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(log_vectors)

print("AI model trained.")

# --- 4. Predict Anomalies ---
predictions = model.predict(log_vectors)
log_data['anomaly_score'] = predictions

# --- 5. Show the Results ---
anomalies = log_data[log_data['anomaly_score'] == -1]


# --- CHANGE 2: Updated if/else block ---
if anomalies.empty:
    print("\n--- AI Model Report ---")
    print("✅ No anomalies detected. All logs look normal.")
    print("-------------------------------------------------")
    sys.exit(0) # Exit with a "success" code
else:
    print("\n--- 🚨 AI Model Report: Anomalies Detected! ---")
    print(f"Found {len(anomalies)} suspicious log entries:")
    
    for message in anomalies['message'].unique():
        print(f"  -> {message}")
    print("-------------------------------------------------")
    sys.exit(1) # Exit with a "failure" code