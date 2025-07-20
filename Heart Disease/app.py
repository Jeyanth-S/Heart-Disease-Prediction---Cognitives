from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model_path = 'model/heart_model.pkl'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file {model_path} not found. Train the model first.")
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Feature names must match training data
feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

@app.route('/')
def home():
    return render_template('index.html', features=feature_names)

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data and convert to float
    features = [float(request.form.get(f)) for f in feature_names]
    # Reshape for single prediction
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)[0]
    # Map prediction to a user-friendly label
    result = "Heart Disease Predicted" if prediction == 1 else "No Heart Disease Predicted"
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
