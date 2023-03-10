# "G:\Tranquillity ID-1075\Ongoing-1075\170-O&M\Data Managment System\10_2020 DMS\Well Locations MASTER.xls"

import streamlit as st
import sys
# sys.path.append('..')
from districts.tranquillity.plotly_figures import create_subsidence_figure
# import plotly.graph_objects as go
import pandas as pd

import base64
import io

import arrow

import geopandas as gpd

from dashboard_shared import Table,Components,export_df
import leafmap.foliumap as leafmap

# C = Components("Tranquillity")
# C.header()

get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M").format("MMMM YYYY")
add_date = lambda df: df.assign(date = [get_date(y['year'],y['month']) for i,y in df.iterrows()])

def to_decimal_degrees(coord):
	C = coord.split(' ')

	decimal_degree = (float(C[0])) + (float(C[1]) / 60) + (float(C[2]) / 60 / 60)
	if C[3] == 'W':
		return decimal_degree * -1
	else:
		return decimal_degree
# def get_table(table_name):
def plot_positions(df,points_to_use):
	df = df.loc[df['point_id'].isin(points_to_use)]	
	df = df.assign(
		lat = lambda y: y.latitude.apply(to_decimal_degrees),
		lon = lambda y: y.longitude.apply(to_decimal_degrees),
	)

	gdf = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(
		df.lon,
		df.lat,
		crs="EPSG:4326"
		))

	M = leafmap.Map(
		google_map="HYBRID",
		draw_control=False,
	)
	# img_path = r'G:\Tranquillity ID-1075\Ongoing-1075\2000-Data Management System\produced\tranquility_streamlit\pages\K1227.png'
	# # img_path = r'K1227.png'
	# url = f'file://{img_path}'
	# popup = f'<img src="{url}"/>"'
	# # popup = f""

	# popup = folium.Popup()
	M.add_gdf(gdf,layer_name="Monuments",info_mode=False)
	for i,y in gdf.iterrows():
		M.add_marker(
			(y.geometry.y,y.geometry.x),
			# popup=y['point_id'],
			# popup=popup,
			tooltip=y['point_id']
			)

	# https://leafmap.org/notebooks/11_linked_maps/#change-basemaps
	# M.add_marker()
	# file_path = r'\\ppeng.com\pzdata\clients\Tranquillity ID-1075\GIS\Feature\TID.shp'
	
	# file_path = r'data\TID.shp'
	# boundary = gpd.read_file(
	# 	file_path,
	# 	# epsg="EPSG:4326",
	# 	epsg='4326',
	# 	)#.to_crs("EPSG:4326")
	# 	# ! figure out why this doesnt work
	
	table_name = 'TID_gis_boundaries'
	# boundaries = get_table(table_name)
	boundaries = Table(table_name).df

	boundaries_df = boundaries.loc[boundaries['file_name'].isin(['Tranquillity Irrigation District',"Fresno Slough Water District"])]
	from shapely import wkb,wkt
	boundaries_gdf = gpd.GeoDataFrame(boundaries_df,geometry=boundaries_df['geometry'].apply(wkt.loads),crs="EPSG:4326")
	
	M.add_gdf(boundaries_gdf,layer_name="Boundaries",info_mode='on_click')

	M.to_streamlit()

def gse(df,points_to_use):
	data = df.loc[df['point_id'].isin(points_to_use)]
	pivot = pd.pivot_table(data,values=['elevation'],index=['date'],columns=['point_id']).droplevel(0,axis='columns')
	st.plotly_chart(create_subsidence_figure(data))

	# st.dataframe(pivot)
	return points_to_use
# 	return pd.DataFrame(st.session_state['client'].table(table_name).select('*').execute().data)
def main():
	st.subheader('Subsidence')
	table_name = 'TID_subsidence_points'
	# positions = get_table(table_name)
	positions = Table(table_name).df

	points = [i for i in positions['point_id'].unique()]
	points_to_use = st.multiselect("Points",points,default=points)
	if points_to_use:
		plot_positions(positions,points_to_use)
		elevations = Table('TID_subsidence_elevations').df
		gse(elevations,points_to_use)