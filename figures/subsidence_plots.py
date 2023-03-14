"""
Used to create overview graphs of gse over time
- graphs on map of panoche water district
- graphs on one page
"""
# %% [markdown]
# # Imports

# %%
# %pip install matplotlib
from matplotlib import pyplot as plt
from matplotlib import ticker
import pandas as pd
# import xlwings as xw
import os
from IPython.display import display
# %pip install pymupdf
import fitz
from numpy import ceil, floor
import numpy as np

import matplotlib

class Month:
	def __init__(self,date,wb_path,client):
		self.date = date
		self.client=client
		dfs = pd.read_excel(wb_path,sheet_name=None)
		
		# point info
		self.info = dfs['point_info']
		# point data
		self.data = dfs['point_data']
		self.pumping = dfs['pumping_data']
		# point locations on map
		self.locations = dfs['point_locations_for_figure']
		self.locations.index = self.locations['point_id']
		self.locations = self.locations.drop(columns='point_id').dropna(how='all',axis='index')


		# df = S.merge(I,left_on='POINT ID',right_on='POINT ID')
		self.points = [i for i in self.data['point_id'].unique()]

		self.base_figures = f"figures\\base"
		self.created_figures = f"figures\\created\\{date}"


	def rtm(self,number, multiple):
		return multiple * round(number / multiple)


	def plot_height_differences(self):
		plt.style.use('default')		
		# https://www.geeksforgeeks.org/plot-multiple-plots-in-matplotlib/
		rows = 4
		cols = 3
		fig,axs = plt.subplots(4,3,sharex=True)
		
		fig.delaxes(axs[0,0])

		# https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
		
		# Landscape tabular
		fig.set_size_inches(17, 11)
		df = self.data

		row = 0
		
		"""-1 starts in top left"""
		# col = -1
		col = 0

		for i,p in enumerate(self.points):
			col+=1
			if col > cols:
				row+=1
				col=0
			
			
			# i,j = [int(floor(i/rows)),i%cols]
			# print(i,j)

			# P = axs[row,col]
			P = axs[col,row]

			point = df.loc[df['point_id'] == p]
			elevations = point['elevation']
			date = point['date']

			middle = round(self.rtm(np.mean(elevations),.3),0)
			
			cushion = 3
			elevation_bounds = [middle - cushion,middle + cushion]

			label = p

			P.plot(date,elevations,label=label)
			P.set_ylim(elevation_bounds)
			P.set_title(label)
			P.grid()

			P.xaxis.set_major_locator(matplotlib.dates.MonthLocator((1)))
			# matplotlib.dates.MonthLocator(interval=6)

			P.xaxis.set_tick_params(labelsize=12,rotation=45,which='major')
			
			# P.set_xticklabls(P.get_xticklabels(),rotation=45)
			# P.xaxis.set_tick_params(labelsize=12,rotation=45)

		top_plot = axs[0,1]
		bottom_plot = axs[3,1]


		# Title
		fig.text(0.5, 0.93, 'Monument Elevations', ha='center',fontsize=20)
		# X-axis title
		bottom_plot.set_xlabel('Date',fontsize=10)
		# Y axis title
		fig.text(0.07, 0.5, 'Elevation (ft)', va='center', rotation='vertical',fontsize=20)

		# fig.tight_layout()


		fig.savefig(f'{self.created_figures}\\heights_diff_graphs_{self.date}.pdf')



	def make_fig(self,point_name):
		"""Adds gse change over time to overall map"""
		plt.style.use('Solarize_Light2')

		fig,ax = plt.subplots()
		# styles = [i for i in plt.style.available]
		# print(styles[0])
		# plt.style.use('default')
		df = self.data
		point = df.loc[df['point_id'] == point_name]
		dates = point['date']
		elevations = point['elevation']
		ax.plot(dates,elevations,linewidth=4)


		ax.set_title(point_name,fontsize=18)
		ax.set_ylabel('Elevation (ft)',fontsize=18)
		ax.set_xlabel('Date', fontsize=18)


		middle = round(self.rtm(np.mean(elevations),.3),0)		
		cushion = 3
		elevation_bounds = [middle - cushion,middle + cushion]
		ax.set_ylim(elevation_bounds)
		
		# ax.set_ylim(floor(min(elevations)),ceil(max(elevations)))

		fig.set_figheight(5)
		fig.set_figwidth(8)
		ax.yaxis.set_major_formatter('{x:.1f}')
		ax.yaxis.set_tick_params(labelsize=18)


		# ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator((1,7)))
		ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator((1)))
		# matplotlib.dates.MonthLocator(interval=6)

		ax.xaxis.set_tick_params(labelsize=16,rotation=45)
		# ax.set_xticklabels(ax.get_xticklabels(), rotation=40)
		# plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees

		# ax.grid(color='black',linewidth=.5)

		return fig, ax

	def graphs_on_overview(self):
		"""
		Creates individual figures of points and puts them over the map
		"""
		plt.style.use('Solarize_Light2')

		pdf_path = r"TID_Ag_Facilities_20221011.pdf"
		src_pdf=f'{self.base_figures}\\{pdf_path}'
		dst_pdf=f'{self.created_figures}\\subsidence_graphs_on_overview_map_{self.date}.pdf'
		document = fitz.open(src_pdf)
		page = document[0]

		for i in self.points:
			p_fig, p_ax = self.make_fig(i)
			plt.close(p_fig)

			src_img = f'{self.created_figures}\\images\\{i}.png'
			p_fig.tight_layout()
			p_fig.savefig(src_img,dpi=100)
			rect = self.locations.loc[i][['x1','y1','x2','y2']]
			# print(i)
			# print(rect)
			# if rect is not 
			
			"""In to pt"""
			rect = rect * 72
			img_rect = fitz.Rect(rect)
			page.insert_image(img_rect, filename=src_img)

		document.save(dst_pdf)
		document.close()
	
	def elevations_vs_pumping(self):
		plt.style.use('default')
		fig,ax = plt.subplots()
		# Landscape tabular
		fig.set_size_inches(17, 11)
		# fig.set_size_inches(11, 8.5)
		# df = self.data

		"""Subsidence"""
		for p in ["AG-20","AG-24","MW-19B","MW-TW3",]:
			point = point = self.data.loc[self.data['point_id'] == p]
			elevations = point['elevation']
			date = point['date']

			ax.plot(date,elevations,label=p,linewidth=3)

		"""Pumping"""
		# ax2.bar(self.pumping['date'],self.pumping['GW Pumping (AF)'],label='Ground Water Pumping',width=20,color='purple')
		ax2 = ax.twinx()
		ax2.bar(
			self.pumping['plot_date'],
			self.pumping['GW Pumping (AF)'],
			label='Groundwater Pumping',
			width=365,
			color='purple',
			alpha=.25,
			align='edge'
			)
		
		ax.legend(loc='upper right')
		ax2.legend(loc='upper left')

		ax.grid()
		
		ax.set_title('Subsidence Monitoring',fontsize=18)
		ax.set_ylabel('Ground Surface Elevation (ft)',fontsize=18)
		ax.set_xlabel('Date', fontsize=18)

		interval = ax.yaxis.get_data_interval()
		# print(interval)

		
		ax2.set_ylabel('Groundwater Pumping (AF)',fontsize=18)

		
		ax.set_ylim(156,172)
		ax2.set_ylim(0,30_000)
		ax2.yaxis.set_major_locator(ticker.LinearLocator(9))


		# print(ax.yaxis.get_ticklocs())

		# # print(ax2.yaxis.get_ticklocs())
		# # print(l2)
		# l = ax.get_ylim()
		# l2 = ax2.get_ylim()
		# f = lambda x: l2[0] + (x - l[0]) / (l[1] - l[0]) * (l2[1] - l2[0])
		# # ax2.grid(None)

		# ticks = f(ax.get_yticks())
		# # ax2.yaxis.set_major_locator(ticker.FixedLocator(ticks))
		# # print(ticks)
		
		# # l = ax.get_ylim()
		# # l2 = ax2.get_ylim()

		# l = ax.get_ylim()
		# l2 = ax2.get_ylim()
		# f = lambda x: l[0] + (x - l2[0]) / (l2[1] - l2[0]) * (l[1] - l[0])
		# ticks = f(ax2.get_yticks())
		# print(ticks)



		# ax.yaxis.set_major_locator(ticker.FixedLocator(ticks))
		
		# ticks = np.linspace(ax2.get_yticks()[0],ax2.get_yticks()[-1],len(ax.get_yticks()))


		# ax2.set_yticks(
		# 	np.linspace(ax2.get_yticks()[0],
		# 	ax2.get_yticks()[-1],
		# 	len(ax.get_yticks())
		# 	))
		# ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
		ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

		suffix = 'scaled'

		# from mpl_axes_aligner import align

		# # Adjust the plotting range of two y axes
		# org1 = 164  # Origin of first axis
		# org2 =  12_500 # Origin of second axis
		# pos = None  # Position the two origins are aligned

		# align.yaxes(ax, org1, ax2, org2, pos)

		fig.tight_layout()
		fig.savefig(f'{self.created_figures}\\gse_vs_pumping_graphs_{suffix}_{self.date}.pdf')



M = Month(
	date='2022-07',
	# wb_path=r'tranquility_subsidence.xlsx',
	wb_path=r"\\ppeng.com\pzdata\clients\Tranquillity ID-1075\Ongoing-1075\140-District Boundaries\146 Benchmarks - GPS Control\2013-01 Control-Well Survey\tranquility_subsidence_data.xlsx",
	client='Tranquility'
)
# M.locations
# M.plot_height_differences()
# M.graphs_on_overview()
M.elevations_vs_pumping()

# %%