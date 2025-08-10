import sys
import json
import numpy as np
import pandas as pd
import xgboost as xgb
from catboost import CatBoostClassifier
import lightgbm as lgb

# Load models (assumes files are in the same directory)
xgb_model = xgb.Booster()
xgb_model.load_model(r'../../Models/xgboost_model.json')

cat_model = CatBoostClassifier()
cat_model.load_model(r'../../Models/catboost_model.cbm')

lgb_model = lgb.Booster(model_file=r'../../Models/lightgbm_model.txt')

# Read input JSON from stdin
input_json = sys.stdin.read()
data = json.loads(input_json)

# Feature engineering
age_years = data["age"] // 365
height_m = data["height"] / 100.0
bmi = data["weight"] / (height_m ** 2)
pulse_pressure = data["ap_hi"] - data["ap_lo"]
hypertension = 1 if (data["ap_hi"] >= 140 or data["ap_lo"] >= 90) else 0

# Prepare features dictionary for XGBoost with feature names
xgb_features = {
    "gender": data["gender"],
    "height_cm": data["height"],
    "weight_kg": data["weight"],
    "ap_hi": data["ap_hi"],
    "ap_lo": data["ap_lo"],
    "cholesterol": data["cholesterol"],
    "gluc": data["gluc"],
    "smoke": data["smoke"],
    "alco": data["alco"],
    "active": data["active"],
    "age_years": age_years,
    "bmi": bmi,
    "pulse_pressure": pulse_pressure,
    "hypertension": hypertension
}

# Convert to DataFrame for XGBoost
X_xgb = xgb.DMatrix(pd.DataFrame([xgb_features]))

# For CatBoost and LightGBM use arrays (no feature names needed)
base_features = [
    data["age"],
    data["gender"],
    data["height"],
    data["weight"],
    data["ap_hi"],
    data["ap_lo"],
    data["cholesterol"],
    data["gluc"],
    data["smoke"],
    data["alco"],
    data["active"]
]

lgb_features = [
    data["gender"],
    data["height"],
    data["weight"],
    data["ap_hi"],
    data["ap_lo"],
    data["cholesterol"],
    data["gluc"],
    data["smoke"],
    data["alco"],
    data["active"],
    age_years,
    bmi,
    pulse_pressure,
    hypertension
]
cat_features = [
    data["gender"],
    data["height"],
    data["weight"],
    data["ap_hi"],
    data["ap_lo"],
    data["cholesterol"],
    data["gluc"],
    data["smoke"],
    data["alco"],
    data["active"],
    age_years,
    bmi,
    pulse_pressure,
    hypertension
]

X_cat = np.array([cat_features])


X_lgb = np.array([lgb_features])

# Make predictions
xgb_pred = xgb_model.predict(X_xgb)[0]
cat_pred = cat_model.predict_proba(X_cat)[0][1]  # positive class probability
lgb_pred = lgb_model.predict(X_lgb)[0]

# Print predictions as JSON string
print(json.dumps({
    "xgboost": float(xgb_pred),
    "catboost": float(cat_pred),
    "lightgbm": float(lgb_pred)
}))

# import sys
# import json
# import numpy as np
# import xgboost as xgb
# from catboost import CatBoostClassifier
# import lightgbm as lgb

# # Load models (assumes files are in the same directory)



# # Read input JSON from stdin
# input_json = sys.stdin.read()
# data = json.loads(input_json)

# # Feature engineering
# age_years = data["age"] // 365
# height_m = data["height"] / 100.0
# bmi = data["weight"] / (height_m ** 2)
# pulse_pressure = data["ap_hi"] - data["ap_lo"]
# hypertension = 1 if (data["ap_hi"] >= 140 or data["ap_lo"] >= 90) else 0

# # Prepare feature arrays for each model

# # XGBoost and CatBoost originally used the simpler set (based on your first input)
# base_features = [
#     data["age"],
#     data["gender"],
#     data["height"],
#     data["weight"],
#     data["ap_hi"],
#     data["ap_lo"],
#     data["cholesterol"],
#     data["gluc"],
#     data["smoke"],
#     data["alco"],
#     data["active"]
# ]

# # LightGBM expects the extended feature set:
# lgb_features = [
#     data["gender"],
#     data["height"],         # height_cm
#     data["weight"],         # weight_kg
#     data["ap_hi"],
#     data["ap_lo"],
#     data["cholesterol"],
#     data["gluc"],
#     data["smoke"],
#     data["alco"],
#     data["active"],
#     age_years,
#     bmi,
#     pulse_pressure,
#     hypertension
# ]

# X_xgb = xgb.DMatrix(np.array([base_features]))
# X_cat = np.array([base_features])
# X_lgb = np.array([lgb_features])

# # Predictions
# xgb_pred = xgb_model.predict(X_xgb)[0]
# cat_pred = cat_model.predict_proba(X_cat)[0][1]  # probability of positive class
# lgb_pred = lgb_model.predict(X_lgb)[0]

# # Return JSON prediction
# print(json.dumps({
#     "xgboost": float(xgb_pred),
#     "catboost": float(cat_pred),
#     "lightgbm": float(lgb_pred)
# }))
