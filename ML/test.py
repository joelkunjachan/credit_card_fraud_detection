
# coding: utf-8

# In[16]:


import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)




# In[12]:


df = pd.read_csv('test.csv')
df.drop("Unnamed: 0",axis=1,inplace=True)
df


# In[ ]:


clf=joblib.load('model.pkl')


# In[7]:


#test=df.iloc[0:1,:]
#test.to_csv("test.csv")


# In[13]:


y_pred = clf.predict(df)
print("\noutput:\n",y_pred) 

if y_pred[0]==0:
	print("fraud transaction")
elif y_pred[0]==1:
	print("legitimate transaction transaction")
	
