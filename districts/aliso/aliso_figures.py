

import plotly.express as px
def create_dtw_figure(client,df):
	# colors = px.colors.qualitative.Plotly
	y = 'gsws'
	fig = px.scatter(
		df,
		x='date',
		y=y,
		color='Well Name (AWD ID)',
		# color_discrete_sequence=colors,
		symbol='Well Name (AWD ID)',
	)
	# fig.
	# change line color to blue
	# unique colors for each well
	# https://plotly.com/python/line-and-scatter/
	# fig.update_traces(
	# print(colors)

	fig.update_traces(
		selector={"mode":'markers'},
		# mode='lines',
		mode='lines+markers',
		# mode='markers',
		connectgaps=True,
		# line_color='green',
		# marker_color='green',
	)

	fig.update_yaxes(
		title_text = "Depth to water (ft)",
		range=[df[y].max() + 10,0],
		# autorange="reversed",
		ticks='inside',
		gridcolor='black',
		# range=[
		# 	df[y].max() + 10,
		# 	0,
		# 	],
		)

	fig.update_xaxes(
		title_text = "Date",
		ticks='inside',
		minor_ticks='inside',
		tickformat="%b %Y",
		gridcolor='black',
		)

	# https://plotly.com/python/hover-text-and-formatting/
	fig.update_layout(
		title={
			# 'text':f"{client}:{well}<br>Depth to water readings (ft)",# + 10 * "<br>&nbsp;",
			'text':f"{client}",
			# 'xanchor':'left',
			# 'yanchor':'top',
		},
		width=1000,
		height=500,
		# hovermode="x",
		# hovermode="x unified",
		# https://plotly.com/python/legend/
		# yaxis_range=[
		# 	0,
		# 	
		# 	],
		)
	# fig.update_yaxes(range=[0,df[y].max() + 10])
	# y bounds starting at 0
	# https://plotly.com/python/reference/layout/#layout-yaxis-range
	# fig.update_layout(
	# 	autotypenumbers='convert types',
	# 	# yaxis=dict(range=[0, 100]),
	# 	# legend_orientation="h",
	# 	# grid
	# 	# https://plotly.com/python/reference/layout/#layout-xaxis-gridcolor
	# 	# https://plotly.com/python/reference/layout/#layout-xaxis-gridwidth
	# 	# https://plotly.com/python/reference/layout/#layout-xaxis-showgrid
	# 	# grid=dict(),

	# 	)
	# show month
	# fig.update_xaxes(

	# return df
	return fig
	
client = 'Nilu Farms LLC'
# for well_id,well_name in wells.items():

figure = create_dtw_figure(
	client=client,
	df=dtw_to_plot.sort_values(by=['date']),
	)

display(figure)