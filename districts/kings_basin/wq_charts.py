import streamlit as st
import pandas as pd
import numpy as np
import polars as pl
import plotly.express as px
from pathlib import Path

# st.set_page_config(
# 	layout="wide",
# 	page_icon="🧊",
# 	page_title="GSA Water Quality Dashboard",
# 	)
def main():
		
	# data_path = Path("data")
	data_path = Path("districts/kings_basin/data")

	@st.cache_data
	def load_data(ps_codes,chemicals_to_check):
		return pl.read_parquet(
			# r"C:\Users\Denver\Downloads\SWRCB_WQ\swrcb_wq.parquet"
			# r"C:\Users\Denver\Downloads\SWRCB_WQ\cleaned_swrcb_wq.parquet"
			data_path.joinpath("gsa_swrcb_wq.parquet")
			).filter(
				# pl.col('PS Code').str.strip() == f'{id}'
				pl.col('PS Code').str.strip().is_in(ps_codes)
				).select(
					pl.col(pl.Utf8).str.strip()
					).with_columns(
						pl.col("Sample Date").str.strptime(pl.Date, fmt="%m-%d-%Y").alias("Date")
						).filter(
							pl.col('Date') > pl.date(2015,1,1)
							# ).filter(
							# 	pl.col('Date') < pl.date(2022,1,1)
								).filter(
									pl.col('Analyte Name').is_in(chemicals_to_check)
									# ).with_columns(
									# 	pl.col('Result').cast(pl.Float32,strict=True).fill_null(-1).alias("reading")
										).sort("Date", descending=True)




	class GSA:
		def __init__(self, dfs,name):
			self.name = name
			self.public_wells = dfs['public_wells'].pipe(lambda df:df.loc[df['GSA'] == name])
			self.ps_codes = [i for i in self.public_wells['PS Code'].unique()]
			# st.dataframe(dfs['chemical_crosswalk'])
			self.chemical_names = dfs['chemical_crosswalk'].pipe(lambda df:df.loc[df['GSA'] == name])
			self.chemicals_to_check = [i for i in self.chemical_names['public_name']]
			self.chemical_titles = [i for i in self.chemical_names['pp_title']]


			self.df = load_data(self.ps_codes,self.chemicals_to_check).to_pandas()
			self.df = self.df.astype({'Sample Date': 'datetime64[ns]', 'Result': 'float64'},errors='ignore')

		# def convert_concentrations(self):
		# 	dfs['chemical crosswalk'].pipe(lambda df:df.loc[df['GSA'] == name])




	class Analyte:
		def __init__(self, gsa,ps_code,title):
			self.title = title
			self.name = gsa.chemical_names.loc[gsa.chemical_names['pp_title'] == title]['public_name'].values[0]
			self.ps_code = ps_code
			self.gsa = gsa

			self.data = gsa.df.loc[(gsa.df['PS Code'] == ps_code) & (gsa.df['Analyte Name'] == self.name)].reset_index(drop=True)

			try:		
				st.title(f"{self.gsa.name}")
				st.markdown(f"## {self.ps_code}")
				with st.expander("Show Data"):
					if st.checkbox("Show Raw Data"):
						st.dataframe(self.data.sort_values(by='Date',ascending=False))
					else:
						format_flt = lambda s: s if isinstance(s, str) else f"{float(s):.2f}"
						st.dataframe(
							self.data[["Date",'Result',"Units of Measure","MCL"]].sort_values(
								by='Date',ascending=False
								).replace(
									np.nan, 'ND', regex=True
									).style.format(
										{'Result': format_flt,'Date': lambda x: x.strftime('%m/%d/%Y')}
						),use_container_width=True)
				self.plot_fig()
			except Exception as e:
				st.markdown("No data available for this analyte")
				st.markdown(e)

		def plot_fig(self):
			data = self.data

			fig = px.scatter(data, y='Result', x='Sample Date')
			fig.update_layout(
				title_text=f"{self.title}<br><br>{self.ps_code}",
				legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
				xaxis_title="Date",
				yaxis_title="Concentration",
				)
			# add title

			# original California MCL
			MCLs = [i for i in data['MCL'].unique() if i is not None]
			# st.markdown(f"MCL = {MCLs}")
			# st.markdown(f"MCL = {float(MCLs[1])}")
			if len(MCLs) == 1:
				mcl = float(MCLs[0])
			else:
				# st.markdown("Multiple MCLs")
				# mcl = st.selectbox('MCL', MCLs)
				# pick max MCL from str to float
				mcl = float(max([float(x) for x in MCLs]))

			try:
				# find max level for 2015-2021
				filter_data = data.loc[(data['Date'] > '2015-01-01') & (data['Date'] < '2022-01-01')].reset_index(drop=True)
				# st.dataframe(filter_data)

				max_level = filter_data['Result'].max()
				max_date = filter_data.iloc[filter_data['Result'].idxmax()]['Date'].date()
				# st.markdown(max_date)

				st.markdown(f"Max in 2015-2022 = {max_level} on {max_date}")
				fig.add_annotation(x=max_date, y=max_level, text=f"Max in Period = {max_level}", showarrow=True, arrowhead=1)
				fig.update_yaxes(range=[0, max(mcl*1.4,max_level*1.3)])

				# compare historical max to MCL
				if max_level >= mcl:

					st.markdown(f"**Warning: Max level is at or above MCL**")
					new_mcl = max_level * 1.2
					st.markdown(f"Minimum Threshold = {new_mcl:.2f}")
					# fig.add_hline(y=new_mcl, line_dash="dash", annotation_text=f"New MCL = {new_mcl:.2f}", annotation_position="bottom left", line_color="orange")
					# only show this line after 2021
				else:
					new_mcl = mcl

			except Exception as e:
				st.markdown("No max level found")
				st.markdown(e)
				new_mcl = mcl

			
			test_period = ['2015-01-01','2022-01-01']
			check_period = ['2022-01-01','2023-01-01']

			# fig.add_hline(y=float(mcl), line_dash="dash", annotation_text=f"MCL = {mcl}", annotation_position="bottom left", line_color="red")
			fig.add_shape(y0=float(mcl), y1=float(mcl),x0=test_period[0],x1=test_period[1],line_dash="dash",line_color="red")
			fig.add_annotation(x='2016-01-01', y=float(mcl), text=f"California MCL = {mcl}", showarrow=True, arrowhead=1,)
			if mcl == new_mcl:
				fig.add_shape(y0=new_mcl, y1=new_mcl, x0=check_period[0], x1=check_period[1], line_dash="dash", line_color="red")
				fig.add_annotation(x=check_period[0], y=float(new_mcl), text=f"Minimum Threshold (California MCL)= {new_mcl:.2f}", showarrow=True, arrowhead=1,)
			else:
				fig.add_shape(y0=new_mcl, y1=new_mcl, x0=check_period[0], x1=check_period[1], line_dash="dash", line_color="orange")
				fig.add_annotation(x=check_period[0], y=float(new_mcl), text=f"Minimum Threshold (120% Max)= {new_mcl:.2f}", showarrow=True, arrowhead=1,)

			# annotate mcl


			# make scatter points bigger and connect scatter points with lines
			fig.update_traces(mode='lines+markers',marker_size=10,line=dict(width=1),connectgaps=True)
			# connect lines
			# fig.update_traces()
			# make data above MCL red
			fig.update_traces(marker=dict(color=data['Result'].apply(lambda x: 'red' if x >= float(mcl) else 'green')))

			# fig.update_traces(marker=dict(color=data['Result'].apply(lambda x: 'red' if x >= float(mcl) else 'green')))
			
			# fig.add_hline(y=max_level, line_dash="dash", annotation_text=f"Max = {max_level}", annotation_position="bottom right")


			fig.update_xaxes(range=["2015-01-01", "2023-01-01"])

			# add vline at 2021
			fig.add_vline(x="2022-01-01", line_dash="dash", line_color="blue" )
			from datetime import date
			# fig.add_vline(x=date(2021,1,1), line_dash="dash", annotation_text="2021", annotation_position="top right", line_color="blue")

			st.plotly_chart(fig)



			
	dfs = pd.read_excel(data_path.joinpath("GSA_info.xlsx"), sheet_name=None)
	GSAs = [i for i in dfs['public_wells']['GSA'].unique()]
	gsa = GSA(dfs,st.sidebar.selectbox('GSA', GSAs))
	# st.dataframe(gsa.chemical_names)
	ps_code = st.sidebar.selectbox('PS Code',gsa.ps_codes)
	analyte_title = st.sidebar.selectbox('Analyte Name', gsa.chemical_titles)

	A = Analyte(gsa,ps_code,analyte_title)
	# analyte = st.sidebar.selectbox('Analyte Name', G.df['Analyte Name'].unique())

