import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium

st.set_page_config(page_title= 'Airbnb', page_icon= '🏨', layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(':red[Airbnb] | :red[Vacation rental company :mag:]')

tab1, tab2, tab3 = st.tabs(["Home", "Search", "About"])

df = pd.read_csv(r"C:\Users\VICTUS\Desktop\Airbnb 3\Airbnb_clean_data3.csv")

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        countries = df['Country'].unique()
        selected_option = st.selectbox("Select an country:", countries)

        filtered_df = df[df['Country'] == selected_option]


        property_prices = filtered_df.groupby('property_type')['price'].mean().reset_index()

        fig = px.bar(
            property_prices,
            x='property_type',
            y='price',
            title=f'Average Price by Property Type in {selected_option}',
            labels={'Property Type': 'Property Type', 'price': 'Average Price'},
        )
        st.plotly_chart(fig)

        property_type= df['property_type'].unique()
        No_of_guest = df['accommodates'].unique()
        room_type = df['room_type'].unique()
        select_option_propertytype = st.selectbox("Select a property type:", property_type)
        select_option_No_of_guest = st.selectbox("No of Guest:", No_of_guest)
        select_option_room_type = st.selectbox("Select a Room Type:", room_type)

    filtered_data = filtered_df[
    (filtered_df['property_type'] == select_option_propertytype) &
    (filtered_df['accommodates'] == select_option_No_of_guest) &
    (filtered_df['room_type'] == select_option_room_type)
    ]

    # Create a table with selected columns
    table_columns = ["name", "hostname", "price", 'description']
    st.table(filtered_data[table_columns])





    with col2:
        sort_option = st.radio("Sort Countries", ["Price Low - Price High", "Price High - Price Low", "Best Rating"])
        filtered_df = df.copy()
        if sort_option == 'Price Low - Price High':
            country_stats = filtered_df.groupby("Country").agg({"price": "mean", "Rating": "mean"}).reset_index()
            country_stats = country_stats.sort_values(by='price', ascending=True)


        elif sort_option == 'Price High - Price Low':
            country_stats = filtered_df.groupby("Country").agg({"price": "mean", "Rating": "mean"}).reset_index()
            country_stats = country_stats.sort_values(by='price', ascending= False)


        elif sort_option == 'Best Rating':
            country_stats = filtered_df.groupby("Country").agg({"price": "mean", "Rating": "mean"}).reset_index()
            country_stats = country_stats.sort_values(by='Rating', ascending= False)

        columns_to_display = ["Country", "price", "Rating"]
        st.table(country_stats[columns_to_display])

    df_grouped = df.groupby('Country')['price'].mean().reset_index()

    fig = px.choropleth(
        df_grouped,
        locations='Country',  # Column containing country names
        locationmode='country names',  # Use country names for location mode
        color='price',  # Color based on the average price
        hover_name='Country',  # Hover text displays country names
        color_continuous_scale='Viridis',  # Choose a color scale
        title='Average Airbnb Prices by Country'
    )

    st.plotly_chart(fig)

    df_grouped_rating = df.groupby('Country')['Rating'].mean().reset_index()

    fig = px.choropleth(
        df_grouped_rating,
        locations='Country',  # Column containing country names
        locationmode='country names',  # Use country names for location mode
        color='Rating',  # Color based on the average price
        hover_name='Country',  # Hover text displays country names
        color_continuous_scale='Inferno',  # Choose a color scale
        title='Average Airbnb rating by Country'
    )

    st.plotly_chart(fig)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Airbnb is a community built on a sharing economy. It is an online platform that allows property owners to list their place as holiday accommodation and allows travellers to find a place to stay while they are away from home.')
        st.subheader(':red[Hotels are a far more traditional concept, with guest rooms and occasional suites. Airbnbs, on the other hand, typically offer residential-style amenities like living rooms, kitchens, dining rooms, laundry facilities and, in some locations, a private place to park your car.]')
    with col2:
        st.image('air.webp')
    st.subheader('What is the main purpose of Airbnb? The idea behind Airbnb is simple: matching local people with a spare room or entire home to rent to others who are visiting the area. Hosts using the platform get to advertise their rentals to millions of people worldwide, with the reassurance that a big company will handle payments and offer other support')

with tab3:
    st.subheader(':red[Skills take away From This Project:] Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb, PowerBI')
    st.subheader(':red[Domain:] Travel Industry, Property Management and Tourism')
    st.subheader(":red[LinkedIn]: [Check out my linkedin profile](linkedin.com/in/karthikapril)")
    st.subheader(":red[GitHub]: [Check out my projects here](https://github.com/karthikapril/Capstone.git)")





