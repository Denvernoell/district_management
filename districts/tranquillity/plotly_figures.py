import pandas as pd
import plotly.express as px
import arrow
import geopandas as gpd


get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M")
# file_path = r"\\ppeng.com\pzdata\clients\Tranquillity ID-1075\Ongoing-1075\2000-Data Management System\data\cleaned_data_for_database.xlsx"
# dfs = pd.read_excel(file_path,sheet_name=None)

# class Map:
# 	def __init__(self,df):
# 		self.df = df
	

# 	def plot_points(df,points_to_use):
# 		df = df.loc[df['point_id'].isin(points_to_use)]	
# 		df = df.assign(
# 			lat = lambda y: y.latitude.apply(to_decimal_degrees),
# 			lon = lambda y: y.longitude.apply(to_decimal_degrees),
# 		)

# 		gdf = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(
# 			df.lon,
# 			df.lat,
# 			crs="EPSG:4326"
# 			))

# 		M = leafmap.Map(
# 			google_map="HYBRID",
# 			draw_control=False,
# 		)


# 		M.add_gdf(gdf,layer_name="Monuments",info_mode=False)
# 		for i,y in gdf.iterrows():
# 			M.add_marker(
# 				(y.geometry.y,y.geometry.x),
# 				# popup=y['point_id'],
# 				# popup=popup,
# 				tooltip=y['point_id']
# 				)

# 		# https://leafmap.org/notebooks/11_linked_maps/#change-basemaps
# 		# M.add_marker()
# 		file_path = r'\\ppeng.com\pzdata\clients\Tranquillity ID-1075\GIS\Feature\TID.shp'
# 		boundary = gpd.read_file(file_path)
# 		M.add_gdf(boundary,layer_name="Tranquility Boundary",info_mode=None)

# 		M.to_streamlit()



def create_subsidence_figure(df):
	# df = dfs['TID_extractions_monthly_AF']
	fig = px.scatter(
		df,
		x='date',
		y='elevation',
		color="point_id",
		symbol="point_id",
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
			'text':"Subsidence",# + 10 * "<br>&nbsp;",
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
		title_text = "GSE (ft)",
		# range=[135,55],
		# autorange="reversed",
		ticks='inside',
		)
	fig.update_xaxes(
		title_text = "Date",
		ticks='inside',
		minor_ticks='inside',
		)
	fig.update_layout(autotypenumbers='convert types',)

	# return df
	return fig

def create_dtw_figure(df):
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

	fig.update_layout(autotypenumbers='convert types',)
	# return df
	return fig
	
def create_extractions_figure(df):
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
	