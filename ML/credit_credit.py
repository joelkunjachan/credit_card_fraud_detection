
# coding: utf-8

# In[16]:


import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)



def predict(data=None):
    if data is None:
        df = pd.read_csv('media/input/test.csv')
    else:
        df = pd.DataFrame(data)
        # Convert string values to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("Columns in df:", df.columns.tolist())
    
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1, inplace=True)
    if '' in df.columns:
        df.drop('', axis=1, inplace=True)
    
    print("Columns after drop:", df.columns.tolist())
    
    clf = joblib.load('ML/model.pkl')
    y_pred = clf.predict(df)
    print("\noutput:\n", y_pred)
    
    if y_pred[0] == 0:
        result = "fraud transaction"
        print("fraud transaction")
    elif y_pred[0] == 1:
        result = "legitimate transaction"
        print("legitimate transaction")
    
    return y_pred[0]
		
