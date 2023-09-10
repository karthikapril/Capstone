#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import json
import os
import mysql.connector as sql


# In[4]:


#Creating a DataFrame of Aggregated transaction
# AGT ----> Aggregated transaction

path = r'C:/Users/VICTUS/Desktop/PhonePe pulse/pulse/data/aggregated/transaction/country/india/state/'
AGT_list = os.listdir(path)

columns = {'State': [], 'Year': [], 'Quarter': [], 'Type': [], 'Count':[] , 'Amount': []}

# AGY_list---------> Aggregated year list
# AGT ----> Aggregated transaction list

for state in AGT_list:
    cstate = path + state + '/'
    AGY_list = os.listdir(cstate)
    
#Aggregated file    
    for year in AGY_list:
        cyear = cstate + year + '/'
        AGF_list = os.listdir(cyear)
        
        for file in AGF_list:
            cfile = cyear + file
            data = open(cfile, 'r')
            json1 = json.load(data)
            
            for i in json1['data']['transactionData']:
                t_type = i['name']
                t_count = i['paymentInstruments'][0]['count']
                t_amount = i['paymentInstruments'][0]['amount']
                columns['Type'].append(t_type)
                columns['Count'].append(t_count)
                columns['Amount'].append(t_amount)    
                columns['State'].append(state)
                columns['Year'].append(year)
                columns['Quarter'].append(int(file.strip('.json')))
                
df_AGT = pd.DataFrame(columns)


# In[20]:


# AGU ------------> Aggregated user

path_2 = r'C:/Users/VICTUS/Desktop/PhonePe pulse/pulse/data/aggregated/user/country/india/state/'
AGU_list = os.listdir(path_2)

columns_2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count':[] , 'Percentage': []}

for state in AGU_list:
    c_state = path_2 + state + '/'
    AGU_year = os.listdir(c_state)
    
    for year in AGU_year:
        c_year = c_state + year + '/'
        AGU_files = os.listdir(c_year)
        
        for file in AGU_files:
            c_file = c_year + file
            data = open(c_file, 'r')
            json2 = json.load(data)
            try:
            
                for i in json2['data']['usersByDevice']:
                    brandname = i['brand']
                    no_of_count = i['count']
                    percent = i['percentage']
                    columns_2['Brands'].append(brandname)
                    columns_2['Count'].append(no_of_count)
                    columns_2['Percentage'].append(percent)
                    columns_2['State'].append(state)
                    columns_2['Year'].append(year)
                    columns_2['Quarter'].append(int(file.strip('.json')))
            except:
                pass
                
df_AGU = pd.DataFrame(columns_2)


# In[26]:


# Map transaction list ------------> MT_list
path_3 = r'C:/Users/VICTUS/Desktop/PhonePe pulse/pulse/data/map/transaction/hover/country/india/state/'
MT_list = os.listdir(path_3)

columns_3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Type': [], 'Count':[],'Amount':[] }

for state in MT_list:
    c_state = path_3 + state +'/'
    MT_year = os.listdir(c_state)
    
    for year in MT_year:
        c_year = c_state + year + '/'
        MT_file = os.listdir(c_year)
        
        for file in MT_file:
            c_file = c_year + file
            data = open(c_file, 'r')
            json_3 = json.load(data)
            
            for i in json_3['data']['hoverDataList']:
                district = i['name']
                t_type = i['metric'][0]['type']
                count = i['metric'][0]['count']
                amount = i['metric'][0]['amount']
                columns_3['Type'].append(t_type)
                columns_3['Count'].append(count)
                columns_3['Amount'].append(amount)
                columns_3['State'].append(state)
                columns_3['Year'].append(year)
                columns_3['District'].append(district)
                columns_3['Quarter'].append(int(file.strip('.json')))
                
df_MT = pd.DataFrame(columns_3)


# In[40]:


# MU_list ----------> Map user list

path_4 = r'C:/Users/VICTUS/Desktop/PhonePe pulse/pulse/data/map/user/hover/country/india/state/'
MU_list = os.listdir(path_4)

columns_4 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Registered_Users': [], 'App_Opens': []}

# MU_year -----> map user year

for state in MU_list:
    c_state =path_4 + state + '/'
    MU_year = os.listdir(c_state)
    
    for year in MU_year:
        c_year = c_state + year + '/'
        MU_file = os.listdir(c_year)
        
        for file in MU_file:
            c_file = c_year + file
            data = open(c_file, 'r')
            json_4 = json.load(data)
            
            for i in json_4['data']['hoverData'].items():
                district = i[0]
                registereduser = i[1]['registeredUsers']
                appopens = i[1]['appOpens']
                columns_4['District'].append(district)
                columns_4['Registered_Users'].append(registereduser)
                columns_4['App_Opens'].append(appopens)
                columns_4['State'].append(state)
                columns_4['Year'].append(year)
                columns_4['Quarter'].append(int(file.strip('.json')))
                                        
df_MU = pd.DataFrame(columns_4)


# In[43]:


# TT_list -----------> Top transaction list

path_5 = r'C:/Users/VICTUS/Desktop/PhonePe pulse/pulse/data/top/transaction/country/india/state/'
TT_list = os.listdir(path_5)

columns_5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Type': [], 'Amount': [], 'Count': []}

for state in TT_list:
    c_state = path_5 + state + '/'
    TT_year = os.listdir(c_state)
    
    for year in TT_year:
        c_year = c_state + year + '/'
        TT_file = os.listdir(c_year)
        
        for file in TT_file:
            c_file = c_year + file
            data = open(c_file, 'r')
            json_5 = json.load(data)
            
            for i in json_5['data']['pincodes']:
                Pincode = i['entityName']
                T_type = i['metric']['type']
                amount = i['metric']['amount']
                count = i['metric']['count']
                columns_5['State'].append(state)
                columns_5['Year'].append(year)
                columns_5['Quarter'].append(int(file.strip('.json')))
                columns_5['Pincode'].append(Pincode)
                columns_5['Type'].append(T_type)
                columns_5['Amount'].append(amount)
                columns_5['Count'].append(count)
                
df_TT = pd.DataFrame(columns_5)


# In[44]:


# TU_list ----------------> Top users list

path_6 = r'C:/Users/VICTUS/Desktop/PhonePe pulse/pulse/data/top/user/country/india/state/'
TU_list = os.listdir(path_6)
columns_6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Registered_Users': []}

for state in TU_list:
    c_state = path_6 + state + '/'
    TU_year = os.listdir(c_state)
    
    for year in TU_year:
        c_year = c_state + year + '/'
        TU_file = os.listdir(c_year)
        
        for file in TU_file:
            c_file = c_year + file
            data = open(c_file, 'r')
            json_6 = json.load(data)
            
            for i in json_6['data']['pincodes']:
                pincode = i['name']
                registeruser = i['registeredUsers']
                columns_6['State'].append(state)
                columns_6['Year'].append(year)
                columns_6['Pincode'].append(pincode)
                columns_6['Registered_Users'].append(registeruser)
                columns_6['Quarter'].append(int(file.strip('.json')))
                
df_TU = pd.DataFrame(columns_6)


# # SQL, creating table

# In[14]:


# Connection
sql = sql.connect(host="localhost",
                   user="root",
                   password="1234",
                   database= "phonepe"
                  )
sql_cursor = sql.cursor(buffered=True)


# In[3]:


csv_file = r"C:\Users\VICTUS\Desktop\District.csv" # Replace with the path to your CSV file
df = pd.read_csv(csv_file, header=None, names=["District"])


# In[4]:


create_table_query = """CREATE TABLE IF NOT EXISTS district (
    id INT AUTO_INCREMENT PRIMARY KEY,
    District VARCHAR(255))"""


# In[15]:


# cursor = sql.cursor()
# sql_cursor.execute(create_table_query)

# for index, row in df.iterrows():
#     insert_query = f"INSERT INTO district (District) VALUES ('{row['District']}')"
#     sql_cursor.execute(insert_query)

# sql.commit()
# sql.close()


# In[ ]:





# In[50]:


# sql_cursor.execute('use phonepe')


# In[53]:


# Agg_transaction_table = '''CREATE TABLE aggregated_transaction (State varchar(100), year int, Quater int, Transaction_type varchar(100), Count bigint, Amount DOUBLE)'''


# In[54]:


# sql_cursor.execute(Agg_transaction_table)


# In[58]:


# Agg_user_table = '''CREATE TABLE aggregated_user (State varchar(100), Year int, Quarter int, Brands char, Count bigint, Percentage DOUBLE)'''


# In[59]:


# sql_cursor.execute(Agg_user_table)


# In[61]:


# Map_transaction_table = ''' CREATE TABLE Map_transaction (State varchar(100), Year int, Quarter int, District char, Transaction_type varchar(100), Count varchar(100), Amount DOUBLE)'''


# In[62]:


# sql_cursor.execute(Map_transaction_table)


# In[66]:


# Map_user_table = '''CREATE TABLE Map_user (State varchar(100), Year int, Quarter int, District Varchar(100), Registered_Users bigint, App_opens bigint )'''


# In[67]:


# sql_cursor.execute(Map_user_table)


# In[77]:


# Top_transaction_table = '''CREATE TABLE Top_transaction (State varchar(100), Year int, Quarter int, Pindcode varchar(100), Transaction_type varchar(100), Amount DOUBLE, Count varchar(100))'''


# In[78]:


# sql_cursor.execute(Top_transaction_table)


# In[80]:


# Top_user_table = '''CREATE TABLE Top_user (State varchar(100), Year int, Quarter int, Pincode varchar(100), Registered_user bigint)'''


# In[81]:


# sql_cursor.execute(Top_user_table)


# # Inserting values

# In[37]:


# for i, row in df_AGT.iterrows():
#     query = 'INSERT into aggregated_transaction VALUES (%s,%s,%s,%s,%s,%s)'
#     sql_cursor.execute(query, tuple(row))
#     sql.commit()


# In[36]:


# for i, row in df_AGU.iterrows():
#     query = 'INSERT into aggregated_user VALUES (%s,%s,%s,%s,%s,%s)'
#     sql_cursor.execute(query, tuple(row))
#     sql.commit()


# In[35]:


# for i, row in df_MT.iterrows():
#     query = 'INSERT into Map_transaction VALUES (%s,%s,%s,%s,%s,%s,%s)'
#     sql_cursor.execute(query, tuple(row))
#     sql.commit()


# In[41]:


# for i, row in df_MU.iterrows():
#     query = 'INSERT into Map_user VALUES (%s,%s,%s,%s,%s,%s)'
#     sql_cursor.execute(query, tuple(row))
#     sql.commit()


# In[46]:


# for i, row in df_TT.iterrows():
#     query = 'INSERT into Top_transaction VALUES (%s,%s,%s,%s,%s,%s,%s)'
#     sql_cursor.execute(query, tuple(row))
#     sql.commit()


# In[48]:


# for i, row in df_TU.iterrows():
#     query = 'INSERT into Top_user VALUES (%s,%s,%s,%s,%s)'
#     sql_cursor.execute(query, tuple(row))
#     sql.commit()


# In[52]:


sql_cursor.execute("show tables")
sql_cursor.fetchall()


# In[ ]:




