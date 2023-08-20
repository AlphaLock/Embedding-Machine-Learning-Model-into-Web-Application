#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[3]:


# Setup

#get_ipython().system(' pip install "fastapi[all]"')



# In[ ]:





# ### Import Libraries

# In[4]:


from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import numpy as np


# In[5]:


# Load the trained model
loaded_model = load("logreg_model.joblib")

# Create a FastAPI app
app = FastAPI()

# Create a Pydantic model to define the input schema
class InputData(BaseModel):
    # PRG: float
    # PL: float
    # PR: float
    # SK: float
    # TS: float
    # M11: float
    # BD2: float
    # Age: float

    {
  "PRG": 1.0,
  "PL": 2.0,
  "PR": 3.0,
  "SK": 4.0,
  "TS": 5.0,
  "M11": 6.0,
  "BD2": 7.0,
  "Age": 25.0
}


# Define a POST endpoint to make predictions
@app.post("/predict/")
async def predict(data: InputData):
    # Extract input values from Pydantic model
    input_values = np.array([data.PRG, data.PL, data.PR, data.SK, data.TS, data.M11, data.BD2, data.Age]).reshape(1, -1)
    
    # Make predictions using the loaded model
    prediction = loaded_model.predict(input_values)
    
    return {"prediction": int(prediction[0])}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# In[ ]:




