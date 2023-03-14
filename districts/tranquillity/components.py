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