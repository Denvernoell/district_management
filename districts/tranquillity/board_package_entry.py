import streamlit as st
import sys
import numpy as np

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



def main():
	# source_pdf = st.file_uploader("Upload a PDF", type="pdf")
	source_pdf = st.text_input("PDF path")

	# G:\Tranquillity ID-1075\Ongoing-1075\2000-Data Management System\data\District Meetings
	tabs = [
		"Domestic Water Monthly Use Report",
		"Surface Water",
		"Well Tracking Report",
		"Total Water Used Lift and Wells",
		"TDS Readings - Out of District",
		"PH / T.D.S. - In District",
		"Well Depths",
	]
	tab = st.selectbox("Select a tab",tabs)
	if tab == "Domestic Water Monthly Use Report":
		T = Table('TID_domestic_water_use_gallons')
		st.dataframe(T.df,use_container_width=True)

		mode = st.radio('Select a source',['Add','Delete','Edit'])
		
		if mode == 'Add':
			year = st.number_input('Year',min_value=1900,max_value=2100,value=2023)
			month = st.number_input('Month',min_value=1,max_value=12,value=1)
			gallons = st.number_input('Gallons',min_value=0,value=0)
			data = {
				'index':len(T.df),
				'source':source_pdf,
				'year':year,
				'month':month,
				'water_use_gallons':gallons,
			}

			if st.button('Add data'):
				T.append(data)
		if mode == 'Edit':
			row = st.number_input('Row',min_value=0,max_value=T.df['index'].max(),value=T.df['index'].max())
			st.dataframe(T.df.iloc[row:row+1],use_container_width=True)
			year = st.number_input('Year',min_value=1900,max_value=2100,value=T.df.iloc[row]['year'])
			month = st.number_input('Month',min_value=1,max_value=12,value=T.df.iloc[row]['month'])
			# gallons = st.number_input('Gallons',min_value=0,value=T.df.iloc[row]['water_use_gallons'])
			gallons = st.text_input('Gallons',value=T.df.iloc[row]['water_use_gallons'])

			data = {
				'index':len(T.df),
				'source':source_pdf,
				'year':year,
				'month':month,
				'water_use_gallons':float(gallons),
			}

			if st.button('Edit row'):
				T.edit(data,row)

		if mode == 'Delete':
			# row = st.number_input('Row',min_value=0,max_value=len(T.df)-1,value=0)
			row = st.number_input('Row',min_value=0,max_value=T.df['index'].max(),value=T.df['index'].max())
			st.dataframe(T.df.loc[T.df["index"] == row],use_container_width=True)
			if st.button('Delete row'):
				st.write('Deleted')
				T.delete(row)


	# if tab == "Surface Water":
	# if tab == "Well Tracking Report":
	# if tab == "Total Water Used Lift and Wells":
	# if tab == "TDS Readings - Out of District":
	# if tab == "PH / T.D.S. - In District":
	# if tab == "Well Depths":
