

from transformers import T5Tokenizer, T5ForConditionalGeneration
from fpdf import FPDF
import torch

print(" Loading FLAN-T5 model...")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
print("Model ready!\n")


def get_user_input():
    print("📋 Please enter patient information:")
    def get_int(prompt): return int(input(prompt).strip())
    def get_bin(prompt): return 1 if input(prompt + " (yes/no): ").strip().lower() == "yes" else 0

    return {
        'age': get_int("Age (in years): ") * 365,
        'gender': get_int("Gender (1: Female, 2: Male): "),
        'height': get_int("Height (cm): "),
        'weight': get_int("Weight (kg): "),
        'ap_hi': get_int("Systolic BP (e.g., 120): "),
        'ap_lo': get_int("Diastolic BP (e.g., 80): "),
        'cholesterol': get_int("Cholesterol (1: Normal, 2: Above Normal, 3: High): "),
        'gluc': get_int("Glucose (1: Normal, 2: Above Normal, 3: High): "),
        'smoke': get_bin("Do you smoke?"),
        'alco': get_bin("Do you consume alcohol?"),
        'active': get_bin("Are you physically active?")
    }



def create_prompt(data, prediction):
    age = data['age'] // 365
    gender = "male" if data['gender'] == 2 else "female"
    bp = f"{data['ap_hi']}/{data['ap_lo']} mmHg"
    cholesterol = ["normal", "above normal", "high"][data['cholesterol'] - 1]
    glucose = ["normal", "above normal", "high"][data['gluc'] - 1]

    risk_status = "The patient is likely to have cardiovascular disease." if prediction == 1 else "The patient is currently not likely to have cardiovascular disease."

    prompt = f"""
Patient Profile:
- Age: {age} years
- Gender: {gender}
- Height: {data['height']} cm
- Weight: {data['weight']} kg
- Blood Pressure: {bp}
- Cholesterol: {cholesterol}
- Glucose: {glucose}
- Smoking: {"yes" if data['smoke'] else "no"}
- Alcohol: {"yes" if data['alco'] else "no"}
- Physically Active: {"yes" if data['active'] else "no"}

Prediction Result: {risk_status}

TASK:
Write a structured medical report with the following sections:
1. Patient Vitals Summary
2. Risk Factor Explanation
3. Comparison to Healthy Adult
4. Health Recommendations (if any)
5. Final Summary

Use clear and medically accurate language.
"""
    return prompt.strip()


def generate_explanation(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
    outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def save_pdf(report, filename="cardio_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    title = " Cardiovascular Risk Assessment Report\n"
    pdf.set_font("Arial", 'B', 14)
    pdf.multi_cell(0, 10, title)

    pdf.set_font("Arial", size=12)
    for line in report.split('\n'):
        pdf.multi_cell(0, 10, line.strip())

    pdf.output(filename)
    print(f"\n PDF report saved as {filename}")



def mock_predict(data):
    if data['ap_hi'] > 140 or data['ap_lo'] > 90 or data['cholesterol'] > 1:
        return 1
    return 0


if __name__ == "__main__":
    user_data = get_user_input()
    prediction = mock_predict(user_data)
    prompt = create_prompt(user_data, prediction)
    print("Generating AI medical summary...")
    summary = generate_explanation(prompt)

    print("\n Summary Preview:\n")
    print(summary)

    save_pdf(summary)
#precison and recall