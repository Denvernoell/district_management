import streamlit as st
import sys
sys.path.append('..')
from plotly_figures import create_dtw_figure
import plotly.graph_objects as go
import pandas as pd

import base64
import io

import arrow


from dashboard_shared import Table,Components,export_df





get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M").format("MMMM YYYY")
add_date = lambda df: df.assign(date = [get_date(y['year'],y['month']) for i,y in df.iterrows()])
to_month_year = lambda y: arrow.get(y).format("MMMM D, YYYY")


# @page_wrapper
def main():
	st.subheader('Water Quality')
	
	table_name = 'TID_well_depth_to_water_ft'
	df = Table(table_name).df.sort_values(['date'])
	# st.dataframe(df)
	# df = st.session_state.dfs[table_name]
	wells = [i for i in df['well_id'].unique()]
	wells_to_use = st.multiselect("Wells",wells,default=wells)

	# min_date = df['Date'].sort_values().min
	# max_date = df['Date'].sort_values().max
	# dates_to_use = [
	# 	st.date_input("Start",value=min_date,min_value=min_date,max_value=max_date),
	# 	st.date_input("Stop",value=max_date,min_value=min_date,max_value=max_date)
	# 	]

	data = df.loc[df['well_id'].isin(wells_to_use)]
	# data = data.pipe(add_date)
	pivot = pd.pivot_table(data,values=['dtw_ft'],index=['date'],columns=['well_id']).droplevel(0,axis='columns')
	# if st.button('Graph'):
	st.plotly_chart(create_dtw_figure(data),use_container_width=True)
	# if st.button('Table'):
	pivot.index = [to_month_year(i) for i in pivot.index]

	st.dataframe(pivot.style.applymap(lambda x: 'color: transparent' if pd.isnull(x) else '').format(formatter="{:.2f}"),use_container_width=True)
	export_df(pivot,"DTW.xlsx")
