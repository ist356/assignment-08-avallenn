'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

df = pd.read_csv('./cache/top_locations_mappable.csv')
#st.dataframe(df)

st.title('Top Locations for Parking Tickets within Syracuse')
geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
#st.write(geo_df), just adds a geomertry column to the dataframe
map = folium.Map(location=CUSE, zoom_start=ZOOM)
#sf.folium_static(map), prints out the map but does not add any tags
cuse_map = geo_df.explore(geo_df['amount'], m=map, vmin=VMIN, vmax=VMAX, legend=True, legend_name='Amount', marker_kwds = {"radius": 10, "fill": True})
sf.folium_static(cuse_map)