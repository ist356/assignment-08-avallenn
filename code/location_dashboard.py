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
    fig1, ax1 = plt.subplots()
    ax1.set_title('Tickets Issued by Hour of Day')
    sns.barplot(data=df[df['location'] == new_location], x="hourofday", y="count", estimator="sum", hue="hourofday", ax=ax1)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.set_title('Tickets Issued by Day of Week')
    sns.barplot(data=df[df['location'] == new_location], x="dayofweek", y="count", estimator="sum", hue="dayofweek", ax=ax2)
    st.pyplot(fig2)

filtered_df = df[df['location'] == new_location]
st.map(filtered_df[['lat', 'lon']])

