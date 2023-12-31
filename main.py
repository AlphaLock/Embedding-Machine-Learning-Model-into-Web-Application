#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import joblib
from fastapi import FastAPI
import uvicorn
import numpy as np
import os


# In[6]:


app = FastAPI()

def load_model():
    cwd = os.getcwd()
    destination = os.path.join(cwd, "Assets")

    imputer_filepath = os.path.join(destination, "numerical_imputer.joblib")
    scaler_filepath = os.path.join(destination, "scaler.joblib")
    model_filepath = os.path.join(destination, "logreg.joblib")

    num_imputer = joblib.load(imputer_filepath)
    scaler = joblib.load(scaler_filepath)
    model = joblib.load(model_filepath)

    return num_imputer, scaler, model


# In[ ]:


def preprocess_input_data(input_data, num_imputer, scaler):
    input_data_df = pd.DataFrame([input_data])
    num_columns = [col for col in input_data_df.columns if input_data_df[col].dtype != 'object']
    input_data_imputed_num = num_imputer.transform(input_data_df[num_columns])
    input_scaled_df = pd.DataFrame(scaler.transform(input_data_imputed_num), columns=num_columns)
    return input_scaled_df


# In[ ]:


@app.get("/")
def read_root():
    return "Sepsis Prediction App"

@app.get("/sepsis/predict")
def predict_sepsis_endpoint(PRG: float, PL: float, PR: float, SK: float, TS: float,
                            M11: float, BD2: float, Age: float, Insurance: int):
    num_imputer, scaler, model = load_model()

    input_data = {
        'PRG': [PRG],
        'PL': [PL],
        'PR': [PR],
        'SK': [SK],
        'TS': [TS],
        'M11': [M11],
        'BD2': [BD2],
        'Age': [Age],
        'Insurance': [Insurance]
    }

    input_scaled_df = preprocess_input_data(input_data, num_imputer, scaler)

    probabilities = model.predict_proba(input_scaled_df)[0]
    prediction = np.argmax(probabilities)

    sepsis_status = "Positive" if prediction == 1 else "Negative"
    
    probability = probabilities[1] if prediction == 1 else probabilities[0]

    #statement = f"The patient is {sepsis_status}. There is a {'high' if prediction == 1 else 'low'} probability ({probability:.2f}) that the patient is susceptible to developing sepsis."

    if prediction == 1:
        status_icon = "✔"  # Red 'X' icon for positive sepsis prediction
        sepsis_explanation = "Sepsis is a life-threatening condition caused by an infection. A positive prediction suggests that the patient might be exhibiting sepsis symptoms and requires immediate medical attention."
    else:
        status_icon = "✘"  # Green checkmark icon for negative sepsis prediction
        sepsis_explanation = "Sepsis is a life-threatening condition caused by an infection. A negative prediction suggests that the patient is not currently exhibiting sepsis symptoms."

    statement = f"The patient's sepsis status is {sepsis_status} {status_icon} with a probability of {probability:.2f}. {sepsis_explanation}"

    user_input_statement = "Please note this is the user-inputted data: "

    output_df = pd.DataFrame([input_data])

    result = {'predicted_sepsis': sepsis_status, 'statement': statement, 'user_input_statement': user_input_statement, 'input_data_df': output_df.to_dict('records')}

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)




