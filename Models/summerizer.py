from transformers import T5Tokenizer, T5ForConditionalGeneration
from fpdf import FPDF
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from sklearn.preprocessing import StandardScaler
import pandas as pd

print("Loading FLAN-T5 model...")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
print("T5 Model Ready!\n")

print("Training prediction model...")

# ✅ WORKING DATASET LINK
csv_url = "https://gist.githubusercontent.com/keshavsingh4522/9bba1fef273186b1ec61a7bb71a54802/raw/heart.csv"
df = pd.read_csv(csv_url)

# ✅ Match actual column names in the dataset
df = df.rename(columns={
    'cp': 'chest_pain_type',
    'trtbps': 'trestbps',
    'chol': 'chol',
    'fbs': 'fbs',
    'restecg': 'restecg',
    'thalachh': 'thalach',
    'exng': 'exang',
    'output': 'target'
})

features = ['age', 'sex', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang']
X = df[features]
y = df['target']

# Scale and train
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
print(f"Recall: {recall_score(y_test, y_pred):.2f}\n")

# ✅ User input
def get_user_input():
    print("Enter patient info:")
    def geti(p): return int(input(p).strip())
    def getb(p): return 1 if input(p+" (yes/no): ").strip().lower()=="yes" else 0
    return {
        'age': geti("Age (years): "),
        'sex': getb("Male?"),
        'trestbps': geti("Resting BP (mmHg): "),
        'chol': geti("Cholesterol (mg/dL): "),
        'fbs': getb("Fasting Blood Sugar >120?"),
        'restecg': geti("Resting ECG (0 normal, 1 abnormal): "),
        'thalach': geti("Max Heart Rate Achieved: "),
        'exang': getb("Exercise-induced angina?")
    }

def create_prompt(data, pred):
    status = "likely to have cardiovascular disease." if pred else "not likely to have cardiovascular disease."
    return f"""
Patient Profile:
- Age: {data['age']} years
- Gender: {'Male' if data['sex'] else 'Female'}
- Resting BP: {data['trestbps']} mmHg
- Cholesterol: {data['chol']} mg/dL
- Fasting Blood Sugar >120: {'Yes' if data['fbs'] else 'No'}
- Resting ECG: {'Abnormal' if data['restecg'] else 'Normal'}
- Max HR: {data['thalach']}
- Exercise Angina: {'Yes' if data['exang'] else 'No'}

Prediction: Patient is {status}

TASK:
Write a structured medical report with:
1. Patient Vitals Summary
2. Risk Factor Explanation
3. Comparison to Healthy Adult
4. Health Recommendations
5. Final Summary
"""

def generate_explanation(prompt):
    ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
    out = model.generate(ids, max_length=512, num_beams=4, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def save_pdf(report, filename="cardio_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=15)
    pdf.set_font("Arial",'B',16)
    pdf.multi_cell(0,10,"Cardiovascular Risk Assessment\n", align='C')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0,10,report)
    pdf.output(filename)
    print(f"\nPDF saved as {filename}")

if __name__ == "__main__":
    user_data = get_user_input()
    df_user = pd.DataFrame([user_data])[features]
    df_user_scaled = scaler.transform(df_user)
    pred = clf.predict(df_user_scaled)[0]

    prompt = create_prompt(user_data, pred)
    print("\nGenerating summary…")
    summary = generate_explanation(prompt)

    print("\nSummary Preview:\n", summary)
    save_pdf(summary)
