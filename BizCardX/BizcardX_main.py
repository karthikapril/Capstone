import streamlit as st
import os
from streamlit_option_menu import option_menu
import mysql.connector as sql
import easyocr
import cv2
import matplotlib.pyplot as plt
import re
import pandas as pd
import base64


sqlconn = sql.connect(host='',
                  user='',
                  password='',
                  database= ''
                  )
cursor = sqlconn.cursor(buffered=True)

# __________________________________________creating a def function toectract the details from bizcard___________________________________________

def Convert_bizcard(image_path):
    reader = easyocr.Reader(['en'])
    res = reader.readtext(image_path)
    detail = []
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        
    image = base64.b64encode(image_data).decode('utf-8')

    for i in range(len(res)):
        detail.append(res[i][1])

    name = []
    designation = []
    street = []
    city = []
    state = []
    pincode = []
    email = []
    website = []
    phone = []
    Business_name = []

    for i in range(len(detail)):
        address_pattern_1 = re.findall('([0-9]+ [A-Za-z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)',detail[i])
    #     address_pattern_2 = re.findall('([0-9]+\s[A-Za-z]+\s[A-Za-z]+)., ([a-zA-Z]+)', detail[i])
        address_pattern_2 = re.findall('([0-9]+ [A-Za-z]+ [A-Za-z]+)., ([a-zA-Z]+)', detail[i])
        address_pattern_3 = re.findall('([A-Za-z]+) ([0-9]+)', detail[i])
        address_pattern_4 = re.findall('([0-9]+ [A-Za-z]+)', detail[i])
        city_pattern = re.findall('^[E].+[a-z]', detail[i])
        pincode_pattern = re.findall('\d{6}', detail[i])
        website_pattern = re.findall('[A-Za-z]+\.[A-Za-z]+\.+[A-Za-z]+', detail[i])

        
        if detail[i] == detail[0]:
            name.append(detail[i]) #Done

        elif detail[i] == detail[1]:
            designation.append(detail[i]) #Done
            
        elif address_pattern_1:
            street.append(address_pattern_1[0][0])
            city.append(address_pattern_1[0][1])
            state.append(address_pattern_1[0][2])
            
        elif address_pattern_2:
            street.append(address_pattern_2[0][0])
            city.append(address_pattern_2[0][1])
            
        elif address_pattern_3:
            state.append(address_pattern_3[0][0])
            pincode.append(address_pattern_3[0][1])
            
        elif address_pattern_4:
            street.append(address_pattern_4[0]+' St')
            
        elif city_pattern:
            city.append(city_pattern[0])
            
        elif pincode_pattern:
            pincode.append(pincode_pattern[0])
            
        elif '-' in detail[i]:
            phone.append(detail[i])     
            
        elif website_pattern:
            website.append(website_pattern[0])
            
        elif 'www' in detail[i]:
            website.append(detail[i])
        
        elif 'WWW ' in detail[i]:
            website.append(detail[i])
            
        elif 'WW' in detail[i]:
            website.append(detail[i] +'.'+ detail[i+1])

            
        elif '@' in detail[i]:
            email.append(detail[i])
            
        else:
            Business_name.append(detail[i])
    if len(Business_name) > 1:
        Business_name = Business_name[0] + ' '+ Business_name[1]
        print(Business_name)
        
    else:
        print(Business_name[0])
        
    Extracted_data = {'name': name[0], 'designation': designation[0] , 'phone': phone[0] ,'Email': email[0] ,'website': website[0] ,'Street': street[0] ,'city': city[0] ,'state':state[0] ,
                'pincode': pincode[0] ,'Business_name': Business_name ,'binary_image': image }
    return Extracted_data

# Streamlit code__________________________________________________________________________________________________________

st.set_page_config(
    page_title="BizCardX: Extracting Business Card Data with OCR",
    layout="wide")

with st.sidebar:
    selected = option_menu("Menu", ["About", "Upload and extract", "Modify", 'View Data'],
                        icons=["house", "gear", "tools"]
                        )

if selected == "Upload and extract":
    st.markdown("### Here we go, upload your file to extract details 💻")

    #Creating a uploader widget
    Upload = st.file_uploader('', type=["jpeg", "png", "jpg"])

    if Upload is not None:

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.image(Upload)

# Using Opencv - cv2 We are creating a box and to the recognized characters
        with col2:
            with st.spinner("Processing image..."):
                path = os.path.join(os.getcwd(), 'cards', Upload.name)
                image = cv2.imread(path)
                reader = easyocr.Reader(['en'])
                result = reader.readtext(path)
                for detection in result:
                    top_left =tuple([int(val) for val in detection[0][0]])
                    bottom_right =tuple([int(val) for val in detection[0][2]])
                    text = detection[1]
                    font =cv2.FONT_HERSHEY_SIMPLEX
                    image = cv2.rectangle(image, top_left, bottom_right, (0,255,0), 2)
                    image = cv2.putText(image, text, top_left, font, 1, (255,0,0),1, cv2.LINE_AA)
                st.image(image)
                ed = Convert_bizcard(path)

                df = pd.DataFrame([ed])
                st.table(df)

                if st.button("Save"):
                    with st.spinner("Uploading..."):
                        for index, row in df.iterrows():
                            sql = """INSERT INTO bizcard_info VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                            cursor.execute(sql, tuple(row))
                            sqlconn.commit()
                            st.toast('You have successfully saved the details to datatbase ✅') 


# giving multiple options to modify details

if selected == "Modify":
    try:
        st.markdown("### Select Card Holder's name to modify")
        cursor.execute("SELECT name FROM bizcard_info")
        result = cursor.fetchall()
        # print(result)
        B_cards = [item for sublist in result for item in sublist]
        # print(B_cards)
        selected_card = st.selectbox("", B_cards)


        st.markdown("### Make changes...")
        query = f"""
            SELECT Business_name, name, designation, phone, email, 
            website, Street, city, state, pincode FROM bizcard_info 
            WHERE name = '{selected_card}'
        """
        cursor.execute(query)
        result = cursor.fetchall()

        Business_name = st.text_input("Business_name", result[0][0])
        name = st.text_input("name", result[0][1])
        designation = st.text_input("designation", result[0][2])
        phone = st.text_input("phone", result[0][3])
        email = st.text_input("email", result[0][4])
        website = st.text_input("website", result[0][5])
        Street = st.text_input("Street", result[0][6])
        city = st.text_input("City", result[0][7])
        state = st.text_input("state", result[0][8])
        pincode = st.text_input("pincode", result[0][9])

# Creating a button to save changes

        if st.button("Save changes"):

            cursor.execute("UPDATE bizcard_info SET Business_name=%s, name=%s, designation=%s, phone=%s, email=%s, website=%s, Street=%s, city=%s, state=%s, pincode=%s WHERE name=%s ", (Business_name, name, designation,
                        phone, email, website,Street, city, state, pincode, selected_card))


            
            sqlconn.commit()
            st.success('Updated ✅')

        st.markdown("### Delete selected card")
        cursor.execute("SELECT name FROM bizcard_info")
        res = cursor.fetchall()
        names = [item for i in res for item in i]
        selected_card = st.selectbox("Select a card holder name to Delete", B_cards)
        st.write(f"##### Delete :red[**{selected_card}'s**] card ?")

# Creating button to delete details

        if st.button("Confirm"):
            query = f'''Delete from bizcard_info where name = "{selected_card}"'''
            cursor.execute(query)
            sqlconn.commit()
            st.toast("Deleted")

       
    except:
        st.warning("No data to display") 

if selected == 'View Data':
    query1 = 'SELECT * FROM bizcard_info'
    # df = pd.DataFrame(query1)
    cursor.execute(query1)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[column[0] for column in cursor.description])
    st.write(df)


if selected == 'About':
    st.header('Project Title: BizCardX: Extracting Business Card Data with OCR', divider='rainbow')
    st.subheader('BizCardX is a technology and software solution designed to streamline the process of extracting data from physical business cards using Optical Character Recognition (OCR) technology. Business cards remain a popular and convenient way to exchange contact information, but manual data entry from these cards can be time-consuming and error-prone. BizCardX addresses this challenge by automating the extraction of essential information such as names, phone numbers, email addresses, company names, and more from business cards.')
    st.markdown('## :red[Technologies used:] OCR,streamlit GUI, SQL,Data Extraction')

    linkedin_url = 'linkedin.com/in/karthikapril'
    github_url = 'https://github.com/karthikapril/Capstone.git'
    st.markdown('## :red[Lets get connected 🤝:]')
    st.markdown(f'### LinkedIn: [{linkedin_url}]({linkedin_url})')
    st.markdown(f'### GitHub: [{github_url}]({github_url})')