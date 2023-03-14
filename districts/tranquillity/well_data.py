import streamlit as st
# import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import base64
import io

import arrow

import geopandas as gpd


from dashboard_shared import Table,Components,export_df

st.subheader('Well Locations, Extractions, and Water Levels')

get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M").format("MMMM YYYY")
add_date = lambda df: df.assign(date = [get_date(y['year'],y['month']) for i,y in df.iterrows()])


import leafmap.foliumap as leafmap
# import leafmap.leafmap as leafmap  # for ipyleaflet only

# format_df = lambda df:df.style.applymap(lambda x: 'color: transparent' if pd.isnull(x) else '').format(formatter="{:.2f}")
format_df = lambda df:df.style.applymap(lambda x: 'color: transparent' if pd.isnull(x) else '')



# class Well that makes graphs and maps if the data is available
class Well:
	def __init__(self,well_info):
		# this only grabs the top row of the well_info dataframe (look into Well No.21 and City Well #7)
		well_aliases = well_info.iloc[0]
		self.well_aliases = well_aliases

		# st.markdown(well_aliases['Alias - Locations'] is np.nan)
		# st.markdown(f"Location = {well_aliases['Alias - Locations']})
		# st.markdown(f"DTW = "+  well_aliases['Alias - Depth to water'])
		# st.markdown(f"Extractions = " + well_aliases['Alias - Extractions'])

		name = well_aliases['Alias - Locations']
		if name is not None:
			# locations = st.session_state['dfs']['TID_well_locations']
			locations = Table('TID_well_locations').df
			well_location = locations.loc[locations['well_id'] == name]
			st.dataframe(well_location,use_container_width=True)
			self.well_map(well_location)
		
		name = well_aliases['Alias - Extractions']
		if name is not None:
			# extractions = st.session_state['dfs']['TID_extractions_monthly_AF']
			extractions = Table('TID_extractions_monthly_AF').df.sort_values(['date'])
			# ! Check if Extractions.1 affects this
			well_extractions = extractions.loc[extractions['well_id'] == name]
			st.plotly_chart(
				self.well_extractions_figure(well_extractions),use_container_width=True
			)
			st.dataframe(well_extractions,use_container_width=True)
			export_df(well_extractions,'well_extractions.xlsx',index=False)
		
		name = well_aliases['Alias - Depth to water']
		if name is not None:
			# depth_to_water = st.session_state['dfs']['TID_well_depth_to_water_ft']
			depth_to_water = Table('TID_well_depth_to_water_ft').df.sort_values(['date'])
			st.dataframe(depth_to_water,use_container_width=True)

			well_depth_to_water = depth_to_water.loc[depth_to_water['well_id'] == name]
			# st.markdown(name)
			st.plotly_chart(self.create_dtw_figure(well_depth_to_water),use_container_width=True)

			st.dataframe(well_depth_to_water,use_container_width=True)
			export_df(well_depth_to_water,'well_depth_to_water.xlsx',index=False)
	
	def create_dtw_figure(self,df):
		# df = dfs['TID_extractions_monthly_AF']
		fig = px.scatter(
			df,
			x='date',
			y='dtw_ft',
			color="well_id",
			symbol="well_id",
		)
		fig.update_traces(
			selector={"mode":'markers'},
			# mode='lines',
			mode='lines+markers',
			# mode='markers',
			connectgaps=True,
		)
		# https://plotly.com/python/hover-text-and-formatting/
		fig.update_layout(
			title={
				'text':"Depth to water readings (ft)",# + 10 * "<br>&nbsp;",
				'xanchor':'left',
				'yanchor':'top',
			},
			width=1000,
			height=500,
			# hovermode="x",
			# hovermode="x unified",
			# https://plotly.com/python/legend/
			)
		fig.update_yaxes(
			title_text = "Depth to water (ft)",
			# range=[135,55],
			autorange="reversed",
			ticks='inside',
			)
		fig.update_xaxes(
			title_text = "Date",
			ticks='inside',
			minor_ticks='inside',
			)

		# return df
		return fig
	

	def well_extractions_figure(self,df):
		# df = dfs['TID_extractions_monthly_AF']
		df = df.assign(
			date = [get_date(y['year'],y['month']) for i,y in df.iterrows()]
		)
		fig = px.scatter(
			df,
			x='date',
			y='monthly_extraction_AF',
			color="well_id",
			symbol="well_id",
			# hover_name="well_id",
			# hover_data=['source'],
			# labels={'PPENG_ID':'Well ID'},
		)
		fig.update_traces(
			selector={"mode":'markers'},
			# mode='lines',
			mode='lines+markers',
			# mode='markers',
			connectgaps=True,
		)
		# https://plotly.com/python/hover-text-and-formatting/
		fig.update_layout(
			title={
				'text':"Monthly Extractions",# + 10 * "<br>&nbsp;",
				'xanchor':'left',
				'yanchor':'top',
			},
			width=1000,
			height=500,
			# hovermode="x",
			# hovermode="x unified",
			# https://plotly.com/python/legend/
			)
		fig.update_yaxes(
			title_text = "Volume Extracted (AF)",
			# range=[135,55],
			# autorange="reversed",
			ticks='inside',
			)
		fig.update_xaxes(
			title_text = "Date",
			ticks='inside',
			minor_ticks='inside',
			)

		# return df
		return fig
				

	def well_map(self,df):
		gdf = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(
			df['longitude'],
			df['latitude'],
			crs="EPSG:4326"
			))

		M = leafmap.Map(
			google_map="HYBRID",
			draw_control=False,
		)


		M.add_gdf(
			gdf[['geometry']],
			layer_name="Wells",
			info_mode=True
			)

		for i,y in gdf.iterrows():
			M.add_marker(
				(y.geometry.y,y.geometry.x),
				# popup=y['point_id'],
				# popup=popup,
				# tooltip=y['well_id']
				)

		# https://leafmap.org/notebooks/11_linked_maps/#change-basemaps
		# M.add_marker()
		# file_path = r'\\ppeng.com\pzdata\clients\Tranquillity ID-1075\GIS\Feature\TID.shp'
		# file_path = r'data\TID.shp'

		# boundary = gpd.read_file(
		# 	file_path,
		# 	crs="EPSG:4326"
		# 	)
		# # ! figure out why this doesnt work

		boundaries = Table('TID_gis_boundaries').df
		boundaries_df = boundaries.loc[boundaries['file_name'].isin(['Tranquillity Irrigation District',"Fresno Slough Water District"])]
		from shapely import wkb,wkt
		boundaries_gdf = gpd.GeoDataFrame(boundaries_df,geometry=boundaries_df['geometry'].apply(wkt.loads),crs="EPSG:4326")
		
		M.add_gdf(boundaries_gdf,layer_name="Boundaries",info_mode='on_click')


		# M.add_gdf(
		# 	boundary,
		# 	layer_name="Boundaries",
		# 	info_mode=None,
		# 	)

		M.to_streamlit()




def main():
	# name_df = st.session_state['dfs']['TID_well_names']
	name_df = Table('TID_well_names').df
	if st.checkbox("Show well names"):
		st.dataframe(name_df.pipe(format_df),use_container_width=True)

	cols = [
		# "well_id",
		"Alias - Folder Name",
		"Alias - Locations",
		"Alias - Extractions",
		"Alias - Extractions.1",
		"Alias - Depth to water",
		"Alias - Board Packages",
		"Alias - Reassign from Ag to City",
		"Alias - SGMA DM",
		"Alias - Other",
	]
	well_lists = [name_df[col].unique() for col in cols]
	import numpy as np
	well_names = [name for names in well_lists for name in names if name != np.nan]
	wells_to_use = st.selectbox("Well",well_names)


	well_info = name_df.loc[name_df.isin([wells_to_use]).any(axis='columns')]
	st.dataframe(well_info,use_container_width=True)

	W = Well(well_info)
	# W
	# if points_to_use:
	# 	plot_positions(positions,points_to_use)
	# 	elevations = st.session_state.dfs['TID_subsidence_elevations']
	# 	gse(elevations,points_to_use)