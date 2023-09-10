import mysql.connector as sql
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd

mydb = sql.connect(host="localhost",
                   user="root",
                   password="1234",
                   database= "phonepe"
                  )
mysqlcursor = mydb.cursor(buffered=True)


st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By: Karthikeyan.B",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """Its a Phonepe Pulse Data Visualization  Exploration: A User-Friendly Tool Using Streamlit  Plotly project Done by: Karthikeyan."""})

st.title(':blue[PhonePe Pulse] | :blue[Data Visualization and Exploration :mag:]')

tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Explore Data', 'Insights','About'])

with tab1:
   st.header('Welcome to a User-Friendly Tool this project will be a live geo visualization dashboard that displays information and insights from the Phonepe pulse :earth_asia:')
   st.subheader(':blue[What are we ?] ')
   st.image('Phone.jpg', use_column_width=True)
   st.subheader('PhonePe Pulse is our way of giving back to the digital payments ecosystem. This data has been structured to provide details on data cuts of Transactions and Users on the Explore tab. A home for the data that powers the PhonePe Pulse website.')
   st.subheader(':blue[Customer centricity, simple products and collaborative approach: key to democratising financial services]')
   st.subheader('India is steadily progressing towards the vision of becoming a cashless economy, and the digital payments ecosystem is fuelling this unprecedented growth. With users becoming comfortable with various digital modes of payments, fintech players are making efforts to bring in the next wave of digital financial inclusion and PhonePe is leading the charge.')

with tab4:
   st.subheader(':blue[Project Title:]  PhonePe Pulse Data Visualization and Exploration')
   st.subheader(':blue[Technologies Used:] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.')
   st.subheader(':blue[Inspired from:] PhonePe Pulse')
   st.subheader('Get in touch... ')
   linkedin_url = "linkedin.com/in/karthikapril"
   st.markdown(f"[:pushpin: Follow me on linkedIn for DataScience talk]({linkedin_url})", unsafe_allow_html=True)
   github_url = "https://github.com/karthikapril/Capstone.git"
   st.markdown(f"[:loud_sound: Get to know more about my Projects here on Github ]({github_url})", unsafe_allow_html=True)


with tab2:
   st.markdown("## :violet[Explore Data]")
   Select_box1 = st.selectbox("Type", ("Transactions", "Users"))
   st.write('Showing results for:', Select_box1)
   Year = st.slider("**Year**", min_value=2018, max_value=2024)
   Quarter = st.slider('**Quarter**',min_value=1, max_value=4)

   if Select_box1 == 'Transactions':
      col1, col2, col3 = st.columns([2,2,2])

      with col1:
         st.markdown("### :violet[State]")
         mysqlcursor.execute(f'SELECT state, sum(Count) as Total_transaction_count, sum(Amount) as Total_Amount from aggregated_transaction where Year = {Year} and Quater = {Quarter} group by state order by Total_Amount DESC limit 10')
         df = pd.DataFrame(mysqlcursor.fetchall(), columns = ['State', 'Count', 'Amount'])
         fig = px.pie(df, values='Amount', names='State',
             title='Top 10 State transactions',
             hover_data=['Count'], labels={'Count':'Transaction_count'})
         fig.update_traces(textposition='inside', textinfo='percent+label')
         st.plotly_chart(fig, use_container_width=True)


      with col2:
         st.markdown("### :violet[District]")
         mysqlcursor.execute(f'SELECT District, sum(Count) as Total_transaction_count, sum(Amount) as Total_Amount from map_transaction where Year = {Year} and Quarter = {Quarter} group by District order by Total_Amount DESC limit 10')
         df = pd.DataFrame(mysqlcursor.fetchall(), columns = ['District', 'Count', 'Amount'])
         fig = px.pie(df, values='Amount', names='District',
             title='Top 10 District transactions',
             hover_data=['Count'], labels={'Count':'Transaction_count'})
         fig.update_traces(textposition='inside', textinfo='percent+label')
         st.plotly_chart(fig, use_container_width=True)

      with col3:
         st.markdown("### :violet[Postalcode]")
         mysqlcursor.execute(f'SELECT Pincode, sum(Amount) as Total_Amount, sum(Count) as Total_transaction_count from top_transaction where Year = {Year} and Quarter = {Quarter} group by Pincode order by Total_Amount DESC limit 10')
         df = pd.DataFrame(mysqlcursor.fetchall(), columns = ['Pincode', 'Amount', 'Count'])
         fig = px.pie(df, values='Amount', names='Pincode',
             title='Top 10 Postalcode transactions',
             hover_data=['Count'], labels={'Count':'Transaction_count'})
         fig.update_traces(textposition='inside', textinfo='percent+label')
         st.plotly_chart(fig, use_container_width=True)

   if Select_box1 == 'Users':
      col1, col2, col3 = st.columns([2,2,2])

      with col1:
         st.markdown("### :violet[State]")
         mysqlcursor.execute(f'SELECT State, sum(Registered_Users) as Total_user from map_user where Year = {Year} and Quarter = {Quarter} group by State order by Total_user DESC limit 10 ')
         df = pd.DataFrame(mysqlcursor.fetchall(), columns = ['State', 'Total_user'])
         fig = px.bar(df, y='Total_user', x='State', text_auto='.2s',
         title="Top 10 Users based on State")
         fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
         st.plotly_chart(fig,use_container_width=True )

      with col2:
         st.markdown("### :violet[District]")
         mysqlcursor.execute(f'SELECT District, sum(Registered_Users) as Total_users from map_user where Year = {Year} and Quarter = {Quarter} group by District order by Total_users DESC limit 10')
         df = pd.DataFrame(mysqlcursor.fetchall(), columns = ['District', 'Total_users'])
         fig = px.bar(df, y='Total_users', x='District', text_auto='.2s',
         title="Top 10 Users based on District")
         fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
         st.plotly_chart(fig,use_container_width=True )

      with col3:
         st.markdown("### :violet[Postalcode]")
         mysqlcursor.execute(f'SELECT Pincode, sum(Registered_user) as Total_users from top_user where Year = {Year} and Quarter = {Quarter} group by Pincode order by Total_users DESC limit 10')
         df = pd.DataFrame(mysqlcursor.fetchall(), columns = ['Pincode', 'Total_users'])
         fig = px.pie(df, values='Total_users',names='Pincode',
         title="Top 10 Users based on Postalcode")
         fig.update_traces(textposition='inside', textinfo='percent+label')
         st.plotly_chart(fig,use_container_width=True )

with tab3:
   Year = st.slider("**Year**", min_value=2018, max_value=2023, value = 2019)
   Quarter = st.slider("**Quarter**", min_value=0, max_value=4, value = 2)
   Type = st.selectbox("**Type**", ("Transactions", "Users"))

   col1, col2 = st.columns([1,1])

   if Type == 'Transactions':

      with col1:    
         st.markdown("## :violet[Total Transaction Amount - State ]")
         mysqlcursor.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where Year = {Year} and Quarter = {Quarter} group by state order by state")
         Total_Transaction_Amount_State_DF = pd.DataFrame(mysqlcursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
         States_DF = pd.read_csv(r"C:\Users\VICTUS\Desktop\States.csv")
         Total_Transaction_Amount_State_DF.State = States_DF

         fig = px.choropleth(Total_Transaction_Amount_State_DF, geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
                     locations="State", featureidkey="properties.ST_NM",color='Total_amount', color_continuous_scale='sunset')
         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
         fig.update_geos(fitbounds="locations", visible=False)
         st.plotly_chart(fig,use_container_width=True)

         


      with col2:
         st.markdown("## :violet[Total Transaction count - State ]")
         mysqlcursor.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where Year = {Year} and Quarter = {Quarter} group by state order by state")
         Total_Transaction_count_State_DF = pd.DataFrame(mysqlcursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
         States_DF = pd.read_csv(r"C:\Users\VICTUS\Desktop\States.csv")
         Total_Transaction_count_State_DF.State = States_DF
         # merged_data = States_DF.merge(Total_Transaction_count_State_DF, on='State')

         fig = px.choropleth(
         Total_Transaction_count_State_DF,
         geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',  # Replace with the path to your state boundaries shapefile
         locations='State',
         featureidkey="properties.ST_NM",color='Total_Transactions',color_continuous_scale='Viridis')
         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
         fig.update_geos(fitbounds="locations", visible=False)
         st.plotly_chart(fig,use_container_width=True)

      st.markdown("## :violet[Select any State to explore more]")
      selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
      
      colm1, colm2 = st.columns([1,1])

      with colm1:
# gauge chart for total transactions in state--------------------

         mysqlcursor.execute(f"select State,year,quarter, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State,year,quarter order by state")
         df1 = pd.DataFrame(mysqlcursor.fetchall(), columns=['State','Year','Quarter',
                                                            'Total_Transactions','Total_amount'])
         gauge_value = df1['Total_Transactions'].sum()
         

         fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_value,
            title={'text': f"Total Transactions in {selected_state} for Year {Year}, Quarter {Quarter}"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, df1['Total_Transactions'].max()]},
                  'bar': {'color': "purple"},
                  'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': gauge_value
                  }
                  }
         ))
         st.plotly_chart(fig)


# Gauge chart for app opens- -----------------------------------

         mysqlcursor.execute(f"select State,Year,Quarter,District,sum(Registered_users) as Total_Users, sum(App_Opens) as Total_AppOpens from map_user where Year = {Year} and Quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
         df = pd.DataFrame(mysqlcursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_AppOpens'])
         gauge_value1 = df['Total_AppOpens'].sum()

         fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_value1,
            title={'text': f"Total AppOpens in {selected_state} for Year {Year}, Quarter {Quarter}"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, df['Total_AppOpens'].max()]},
                  'bar': {'color': "purple"},
                  'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': gauge_value1
                  }
                  }
         ))
         st.plotly_chart(fig)


      with colm2:
# barchart for total transaction district wise---------------------------------------------------------------

         mysqlcursor.execute(f"select State,District, year,quarter, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State,District, year,quarter order by State, District")
         df1 = pd.DataFrame(mysqlcursor.fetchall(), columns=['State','District','Year','Quarter', 'Total_Transactions','Total_amount'])
         fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_Transactions',
                     color_continuous_scale=px.colors.sequential.Agsunset)
         st.plotly_chart(fig,use_container_width=True)

# bar chart for total user district wise -----------------------------------------------------------------------------

         mysqlcursor.execute(f"select State,Year,Quarter,District,sum(Registered_users) as Total_Users, sum(App_Opens) as Total_AppOpens from map_user where Year = {Year} and Quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
         df = pd.DataFrame(mysqlcursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        
         fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
         st.plotly_chart(fig,use_container_width=True)

   if Type == 'Users':
      with col1: #bar chart of payment type ----------------------------------

         st.markdown("## :violet[Payment Type]")
         mysqlcursor.execute(f"select Transaction_type, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from aggregated_transaction where Year= {Year} and Quater = {Quarter} group by Transaction_type order by Transaction_type")
         df = pd.DataFrame(mysqlcursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

         fig = px.bar(df,
                        title='Transaction Types vs Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
         st.plotly_chart(fig,use_container_width=False)

      with col2: #bar chart mobile brand users ---------------------------------

         st.markdown("## :violet[Frequent Mobile brand users ]")
         mysqlcursor.execute(f"Select Brands, sum(Count) as total_count from aggregated_user where Year = {Year} and Quarter = {Quarter} group by Brands order by total_count")
         df1 = pd.DataFrame(mysqlcursor.fetchall(),columns= ['Brands', 'total_count'])
         fig = px.bar(df1, x='Brands', y='total_count',color='total_count', color_continuous_scale=px.colors.sequential.Agsunset)
         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
         st.plotly_chart(fig,use_container_width=False)



