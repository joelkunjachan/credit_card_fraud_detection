
# coding: utf-8

# In[11]:


import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score,recall_score,f1_score,classification_report
from sklearn.metrics import roc_curve, auc
from matplotlib import pyplot as plt
import seaborn as sns
#import sklearn.metrics
import joblib 
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[12]:


df = pd.read_csv('creditcard.csv')
cols = df.columns
features = cols.delete(len(cols)-1)
features = df[features]
labels = df['Class']
df.head()


# In[13]:


df.describe()


# In[15]:

df[df['Class'] == 1].to_csv("fake.csv")

# Time vs Amount in Legit Cases

plt.figure(figsize=(10,5))
fig = plt.scatter(x=df[df['Class'] == 0]['Time'], y=df[df['Class'] == 0]['Amount'], color="#655989")
plt.title("Time vs Amount in Legit Cases")
plt.show()


# In[16]:


# Time vs Amount in Fraud Cases

plt.figure(figsize=(10,5))
fig = plt.scatter(x=df[df['Class'] == 1]['Time'], y=df[df['Class'] == 1]['Amount'], color="#7a9eaf")
plt.title("Time vs Amount in Fraud Cases")
plt.show()


# In[17]:


# Class 0 (inliers) and Class 1 (Outliers)

plt.figure(figsize=(8,6))
fig = sns.countplot(x="Class", data=df)
plt.show()


# In[18]:


# Build train and test sets
features_train, features_test, labels_train, labels_test = train_test_split(features,labels,test_size=0.2,random_state=0)


# In[19]:


# Create from train set a new data set to obtain a balanced data set using SMOTE
oversampler = SMOTE(random_state=0)
os_features,os_labels = oversampler.fit_resample(features_train,labels_train)


# In[20]:


# Perform training of the random forest using the (over sampled) train set
clf = RandomForestClassifier(random_state=0)
clf.fit(os_features,os_labels)


# In[21]:
joblib.dump(clf, 'model.pkl')


# perform predictions on test set
actual = labels_test
predictions = clf.predict(features_test)
# Confusion Matrix
print(classification_report(actual,predictions))


# In[22]:

"""
false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
roc_auc = auc(false_positive_rate, true_positive_rate)
print (roc_auc)
print("\nPrecision: \n",precision_score(actual, predictions, average='weighted'))
print("\nRecall score:\n",recall_score(actual, predictions, average='weighted'))
print("\nF1 score:\n",f1_score(actual, predictions, average='weighted'))"""

