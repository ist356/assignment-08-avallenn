'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_folium as sf
import folium
st.set_page_config(layout="wide")

df = pd.read_csv('./cache/tickets_in_top_locations.csv')
st.title('Top Locations for Parking Tickets within Syracuse')
#st.dataframe(df)
locations = df['location'].unique()
new_location = st.selectbox('Select a location', locations)

total_issued = df[df['location'] == new_location].count()
# add up total amount for the specified location from the selectbox
total_amount = df[df['location'] == new_location]['amount'].sum()
st.write(f'Total Amount: {total_amount}')
st.write(f'Total Issued Tickets: {total_issued[0]}')

col1, col2 = st.columns(2)

with col1:
    #Bar Chart: Show the distribution of tickets by day of the week
    fig1, ax1 = plt.subplots()
    ax1.set_title('Tickets Issued by Day of Week')
    sns.countplot(data=df[df['location'] == new_location], x='dayofweek', ax=ax1, hue = 'dayofweek')
    st.pyplot(fig1)

with col2:
    #Line Chart: Show the distribution of tickets by hour of the da
    fig2, ax2 = plt.subplots()
    ax2.set_title('Tickets Issued by Hour of Day')
    sns.countplot(data=df[df['location'] == new_location], x='hourofday', ax=ax2, hue = 'hourofday')
    st.pyplot(fig2)

lat = df[df['location'] == new_location]['lat'].values[0]
lon = df[df['location'] == new_location]['lon'].values[0]
location = (lat, lon)
map = folium.Map(location=location, zoom_start=14)
new_map = folium.Marker(location=location, popup=new_location).add_to(map)
sf.folium_static(map)
