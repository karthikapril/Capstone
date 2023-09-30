#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize


# In[2]:


df = pd.read_excel(r"C:\Users\VICTUS\Desktop\Copper_Set.xlsx")


# In[3]:


df.head()

# There are two things here, We are going to deal with both classification and regression problem here. 
# 1. first we are going to deal with regression and the classification
# 2. Lets start with data cleaning
# # Data  cleaning

# In[4]:


df.isnull().sum()


# In[5]:


df.shape


# In[6]:


df['material_ref'] =df['material_ref'].apply(lambda x: np.nan if str(x).startswith('00000') else x)


# In[7]:


df.isnull().sum()


# In[8]:


df.drop('id', axis = 1, inplace = True)


# In[9]:


columns = df.columns.values.tolist()


# In[10]:


columns


# In[11]:


categorical_mode = ['item_date', 'customer', 'country', 'status', 'item type','application','material_ref', 'product_ref', 'delivery date' ]
continous_mean = ['quantity tons','thickness', 'width','selling_price' ]


# In[12]:


df['item_date'] = df['item_date'].replace(19950000, np.nan)
df['item_date'] = df['item_date'].replace(20191919, np.nan)
df['delivery date'] = df['delivery date'].replace(20212222, np.nan)
df['delivery date'] = df['delivery date'].replace(30310101, np.nan)


# In[13]:


for i in columns:
    if i in categorical_mode:
        df[i].fillna(df[i].mode()[0], inplace = True)


# In[14]:


df.isnull().sum()


# In[15]:


df.dtypes


# In[16]:


df['quantity tons'].replace('e', np.nan, inplace = True)


# In[17]:


df['quantity tons'] = df['quantity tons'].astype('float')


# In[18]:


for i in columns:
    if i in continous_mean:
        df[i].fillna(df[i].mean(), inplace = True)


# In[19]:


df.isnull().sum()


# In[20]:


df.dtypes


# In[21]:


df['item_date'] = pd.to_datetime(df['item_date'].astype('int64'),format='%Y%m%d')
df['delivery date'] = pd.to_datetime(df['delivery date'].astype('int64'),format='%Y%m%d')


# In[22]:


df['customer'] = df['customer'].astype('int64')
df['country'] = df['country'].astype('int64')
df['application'] = df['application'].astype('int64')


# In[23]:


df.dtypes


# In[24]:


df.head()


# # EDA

# In[25]:


df.plot(kind = 'box', subplots = True, layout = (2,4), figsize=(25,8))
plt.show()


# In[26]:


df.hist(layout=(2,5),figsize=(20,8))
plt.show()


# In[27]:


#Quantity tons IQR
column_name = 'Quantity tons'
Q1 = df['quantity tons'].quantile(0.25)
Q3 = df['quantity tons'].quantile(0.75)
IQR = Q3-Q1
Min = Q1 - 1.5*IQR
Max = Q3 + 1.5*IQR
print(f'For the column {column_name} the MIN and MAX of IQR is {Min} and {Max} respectively where the MEDIAN(IQR) is {IQR}')

#Thickness IQR
column_name = 'Thickness'
Q1 = df['thickness'].quantile(0.25)
Q3 = df['thickness'].quantile(0.75)
IQR = Q3-Q1
Min = Q1 - 1.5*IQR
Max = Q3 + 1.5*IQR
print(f'For the column {column_name} the MIN and MAX of IQR is {Min} and {Max} respectively where the MEDIAN(IQR) is {IQR}')

#width IQR
column_name = 'width'
Q1 = df['width'].quantile(0.25)
Q3 = df['width'].quantile(0.75)
IQR = Q3-Q1
Min = Q1 - 1.5*IQR
Max = Q3 + 1.5*IQR
print(f'For the column {column_name} the MIN and MAX of IQR is {Min} and {Max} respectively where the MEDIAN(IQR) is {IQR}')

#selling_price IQR
column_name = 'selling_price'

Q1 = df['selling_price'].quantile(0.25)
Q3 = df['selling_price'].quantile(0.75)
IQR = Q3-Q1
Min = Q1 - 1.5*IQR
Max = Q3 + 1.5*IQR
print(f'For the column {column_name} the MIN and MAX of IQR is {Min} and {Max} respectively where the MEDIAN(IQR) is {IQR}')


# In[28]:


max(df['selling_price'])
min(df['selling_price'])


# In[29]:


p_low = 0.05
p_high = 0.05
columns_to_winsorize = ['quantity tons','thickness','width','selling_price']
for columns in columns_to_winsorize:
    df[columns] = winsorize(df[columns], limits = (p_low, p_high))
df.plot(kind='box',subplots=True,layout=(2,4),figsize=(20,10))
plt.show


# In[30]:


min(df['selling_price'])


# In[31]:


df.hist(layout=(2,5),figsize=(20,8))
plt.show()


# In[32]:


df.skew()


# In[33]:


# days to deliver

df['Days_for_delivery'] = (df['delivery date'] - df['item_date']).abs().dt.days


# In[34]:


df.head()


# # Encoding ---------> Splittiing ---------> Scaling

# In[35]:


#Encoding
from sklearn.preprocessing import LabelEncoder
import pickle

label_encoding = LabelEncoder()

categorical_labelencoding = ['customer', 'country', 'status', 'item type','application','material_ref', 'product_ref', 'Days_for_delivery']
for col in categorical_labelencoding:
        df[col] = label_encoding.fit_transform(df[col])
        
        
save_data = {
    'data_frame': df,
    'label_encoders': {col: label_encoding for col in categorical_labelencoding}
}

with open('label_encoding.pkl', 'wb') as pickle_file:
    pickle.dump(save_data, pickle_file)


# In[36]:


df.head()


# In[37]:


import seaborn as sns

annot_kws = {"fontsize": 7, "fontweight": "bold"}
sns.heatmap(df.corr(), cmap=None, annot=True,linecolor='white',fmt=".2f", annot_kws=annot_kws)


# In[38]:


from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import pickle

x = df[['quantity tons','item type','country','application','thickness','width', 'product_ref','Days_for_delivery']].values
y = df[['selling_price']].values

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

with open('Scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

models = []


# In[39]:


#Finding the best value for K
param_grid = {'n_neighbors': [1, 3, 5, 7, 9]}
search = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5)
search.fit(X_train_scaled, y_train)

k = search.best_params_


# In[40]:


k


# In[41]:


#KNN Regressor

knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('Mean_squared_error:', mse)
print('r2 score:', r2)


# In[42]:


#Decison tree regressor

from sklearn.tree import DecisionTreeRegressor

Decisontree = DecisionTreeRegressor(random_state = 43)
Decisontree.fit(X_train_scaled, y_train)
y_pred = Decisontree.predict(X_test_scaled)

feature_importances = Decisontree.feature_importances_
for i,v in zip(['quantity tons','customer','item type','country','application','thickness','width', 'product_ref','Days_for_delivery'], feature_importances):
    print('Feature importances',(i,v))
    
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('\n\n')
print('Mean_squared_error:', mse)
print('r2 score:', r2)


# In[43]:


#Extra tree regressor

from sklearn.ensemble import ExtraTreesRegressor

Extra_tree_regressor = ExtraTreesRegressor(n_estimators=100, random_state=44)
Extra_tree_regressor.fit(X_train_scaled, y_train.ravel())
y_pred = Extra_tree_regressor.predict(X_test_scaled)
feature_importances = Extra_tree_regressor.feature_importances_


features = ['quantity tons','customer','item type','country','application','thickness','width', 'product_ref']
feature_importance_dict = dict(zip(features, feature_importances))
sorted_feature_importance = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

for feature, importance in sorted_feature_importance:
    print(f"{feature}: {importance:.4f}")

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


# In[44]:


print('Mean_squared_error:', mse)
print('r2 score:', r2)


# In[45]:


# Since Extra tree regressor performs well, we are going to save this use for predictions. 


# In[46]:


Extra_tree_regressor = ExtraTreesRegressor(n_estimators=100, random_state=44)
Extra_tree_regressor.fit(X_train_scaled, y_train.ravel())
y_pred = Extra_tree_regressor.predict(X_test_scaled)

with open('Best_Prediction_mdoel.pkl', 'wb') as file:
    pickle.dump(Extra_tree_regressor, file)


# # Classification

# In[47]:


#Now lets filter out won and lost from the data frame DF.


# In[48]:


classification_status = df[(df['status'] == 1) | (df['status'] == 7)]


# In[49]:


classification_status.head()


# In[50]:


classification_status['status'].unique()


# In[51]:


classification_status['status'] = label_encoding.fit_transform(classification_status['status'])


# In[52]:


#Splitting feature and target column

x = classification_status[['quantity tons','country', 'item type', 'application','thickness','width','product_ref','selling_price','Days_for_delivery']].values
y = classification_status[['status']].values


# In[53]:


classification_status['status'].value_counts()


# In[54]:


classification_status.head()


# In[55]:


# Due to data imbalance we are using SMOTE over sampling here for data balance

from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy='auto', random_state=42)
x,y = smote.fit_resample(x, y)


# In[56]:


class_distribution = pd.Series(y).value_counts()

# Display the class distribution
print(class_distribution)


# In[57]:


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=452)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

with open('classification_for_scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)


# In[58]:


#Finding the best value for K
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

param_grid = {'n_neighbors': [1, 3, 5, 7, 9]}
search = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)
search.fit(X_train_scaled, y_train)

k = search.best_params_


# In[59]:


k


# In[60]:


from sklearn.metrics import classification_report, confusion_matrix

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

accuracy = knn.score(X_test, y_test)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)


# In[61]:


print(accuracy)
print(conf_matrix)
print(class_report)


# In[62]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

Decision_tree_classifier = DecisionTreeClassifier(random_state=42)
Decision_tree_classifier.fit(X_train, y_train)

y_pred = Decision_tree_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)


# In[63]:


print(accuracy)
print(conf_matrix)
print(class_report)


# In[64]:


from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

Extra_tree_classifier = ExtraTreesClassifier(n_estimators=100, random_state=42)
Extra_tree_classifier.fit(X_train, y_train)
y_pred = Extra_tree_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)


# In[65]:


print(accuracy)
print(conf_matrix)
print(class_report)


# In[66]:


# Extra_tree_classifier performs well saving this file

with open('Class_for_extra_model.pkl', 'wb') as file:
    pickle.dump(Extra_tree_classifier, file)


# # Streamlit Code

# In[67]:


df.head()


# In[ ]:




