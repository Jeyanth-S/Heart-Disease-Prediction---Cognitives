import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load data (adjust filename if needed)
df = pd.read_csv('heart.csv')
X = df.drop('condition', axis=1)    # Features
y = df['condition']                 # Target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save model to disk
import os
os.makedirs('model', exist_ok=True)  # Create model dir if doesn't exist
with open('model/heart_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved to model/heart_model.pkl")
