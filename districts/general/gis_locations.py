import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
from shapely import wkb,wkt
import supabase

# create a web app with streamlit that uses geopandas to read the files in the gis folder and leafmap to display the gis files

# st.session_state['client'] = supabase.create_client(st.secrets['supabase_url'],st.secrets['supabase_key'])
def get_table(table_name):
	return pd.DataFrame(st.session_state['client'].table(table_name).select('*').execute().data)

@st.cache_data
def get_gdfs(layers):
	return {
			layer:gpd.GeoDataFrame(get_table(layer),geometry=get_table(layer)['geometry'].apply(wkt.loads),crs="EPSG:4326")
			for layer in layers
		}

def main():
	st.subheader('GIS Web Viewer')

	layers = [
		'GEN_CDEC',
		'GEN_CIMIS',
		# 'GEN_ETC_Zones',
		'GEN_Water_Districts',
	]
	layers_to_display = st.multiselect('Select layers to display',options=layers,default=layers)
	if st.button('Display layers'):
		M = leafmap.Map()
		gdfs = get_gdfs(layers_to_display)
		for name,gdf in gdfs.items():
			M.add_gdf(gdf,layer_name=name,info_mode='on_click')
		M.to_streamlit()

	# 	st.markdown(type(gdf))
	# 	st.markdown(type(gdf.geometry.iloc[0]))
	# 	# st.markdown(type(gdf.geometry.iloc[0] == ))

	# 	M.add_gdf(gdf,layer_name=name,info_mode='on_click')


	# # display the map
	# M.to_streamlit()

