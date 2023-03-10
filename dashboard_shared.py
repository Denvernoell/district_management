import streamlit as st
import sys

import plotly.graph_objects as go
import pandas as pd

import base64
import io

import arrow
from importlib import import_module

class District:
	def __init__(self,name,folder,pages):
		self.name = name
		self.pages = pages
		self.folder = folder

	def homepage(self):
		st.header(self.name)
		page = self.pages[st.sidebar.radio('Page', list(self.pages.keys()))]
		module = import_module(f'districts.{self.folder}.{page}')
		module.main()
	



class Components:
	def __init__(self,name):
		self.name = name
		st.set_page_config(
			page_title=f"{self.name} Data Management System",
			page_icon="📊",
			layout="wide",
			)
		# self.header()

	def header(self):
		# st.title(f"{self.name} Data Management System")
		st.sidebar.title(f"{self.name} Data Management System")
		# st.markdown("""
        # <style>
        #        .css-18e3th9 {
        #             padding-top: 0rem;
        #             padding-bottom: 0rem;
        #             padding-left: 0rem;
        #             padding-right: 0rem;
        #         }
        #        .css-1d391kg {
        #             padding-top: 3rem;
        #             padding-right: 0rem;
        #             padding-bottom: 3rem;
        #             padding-left: 0rem;
        #         }
        # </style>
        # """, unsafe_allow_html=True)

	def footer(self):
		st.write("---")
		st.markdown(f"[*Provost & Pritchard Consulting Group - 2023*](https://provostandpritchard.com/)")

def month_picker(start_year,end_year):
	year_range = range(start_year,end_year)
	if st.checkbox("Single Month"):
		month = st.selectbox('Month',[arrow.get(f"{i}","M").format('MMMM') for i in range(1,13)])
		year = st.selectbox('Year',year_range)
		return [
			arrow.get(f"{year}-{month}","YYYY-MMMM"),
			arrow.get(f"{year}-{month}","YYYY-MMMM"),
			]
		# return month
	else:
		c1,c2,c3,c4 = st.columns(4)
		with c1:
			start_month = st.selectbox('Start Month',[arrow.get(f"{i}","M").format('MMMM') for i in range(1,13)])
		with c2:
			start_year = st.selectbox('Start Year',year_range,index=0)
		with c3:
			end_month = st.selectbox('End Month',[arrow.get(f"{i}","M").format('MMMM') for i in range(1,13)])
		with c4:
			end_year = st.selectbox('End Year',year_range,index=len(year_range)-1)
		# return [
		# 	arrow.get(f"{start_year}-{start_month}","YYYY-MMMM"),
		# 	arrow.get(f"{end_year}-{end_month}","YYYY-MMMM"),
		# 	]

		# return arrow.get(f"{start_year}-{start_month}","YYYY-M"),arrow.get(f"{end_year}-{end_month}","YYYY-M")						


class User:
	def __init__(self,username,password):
		self.username = username
		self.password = password



# class General:
# 	def __init__():
# 		pass
	




def show_pdf(file_path):
	with open(file_path,"rb") as f:
		base64_pdf = base64.b64encode(f.read()).decode('utf-8')
		pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'		
		st.markdown(pdf_display, unsafe_allow_html=True)


def download_pdf(file_path,file_name,label):
		
	with open(file_path, "rb") as pdf_file:
		PDFbyte = pdf_file.read()

	st.download_button(label=label, 
			data=PDFbyte,
			file_name=f"{file_name}.pdf",
			mime='application/octet-stream')


def convert_date(df,col):
	df[col] = df[col].pipe(pd.to_datetime)
	return df

def export_df(df,file_name,index=True,header=True):
	towrite = io.BytesIO()
	downloaded_file = df.to_excel(towrite, encoding='utf-8', index=index, header=header)
	towrite.seek(0)  # reset pointer
	b64 = base64.b64encode(towrite.read()).decode()  # some strings
	linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Download excel file</a>'
	# return linko
	st.markdown(linko, unsafe_allow_html=True)

# class Plot:
# 	def __init__(self) -> None:
# 		pass

# 	def export(self,fig):
		# fig.write_html("test.html")
		# fig.write_image("test.png")
		# fig.write_image("test.pdf")
		# fig.write_image("test.svg")	
	

class Table:
	# def __init__(self,client,table_name):
	def __init__(self,table_name):
		"""
		client: supabase connection
		table_name: table name of supabase table
		"""
		# self.client = client
		self.client = st.session_state['client']
		
		self.table_name = table_name
		self.refresh()
	
	def __repr__(self) -> str:
		return f"Table Name = {self.table_name}"
	
	def refresh(self):
		self.df = pd.DataFrame(self.client.table(self.table_name).select('*').execute().data)
	
	def append(self,data):
		"""
		data; dict {"client":"Aliso"}
		"""
		self.client.table(self.table_name).insert(data).execute()
		self.refresh()

	def edit(self,data,row,index='index'):
		"""
		data: dict {"client":"Aliso"}
		locator: list ["id",1]
		"""
		self.client.table(self.table_name).update(data).eq(index,row).execute()
		self.refresh()

	def delete(self,row,index='index'):
		"""
		locator: list ["id",1]
		"""
		self.client.table(self.table_name).delete().eq(index,row).execute()
		self.refresh()



# class Table:
# 	# def __init__(self,client,table_name):
# 	def __init__(self,table_name):
# 		"""
# 		client: supabase connection
# 		table_name: table name of supabase table
# 		"""
# 		# self.client = client
# 		self.client = st.session_state['client']
		
# 		self.table_name = table_name
# 		self.refresh()
	
# 	def __repr__(self) -> str:
# 		return f"Table Name = {self.table_name}"
	
# 	def refresh(self):
# 		self.df = pd.DataFrame(self.client.table(self.table_name).select('*').execute().data)
	
# 	def append(self,data):
# 		"""
# 		data; dict {"client":"Aliso"}
# 		"""
# 		self.client.table(self.table_name).insert(data).execute()
# 		self.refresh()

# 	def edit(self,data,locator):
# 		"""
# 		data: dict {"client":"Aliso"}
# 		locator: list ["id",1]
# 		"""
# 		self.client.table(self.table_name).update(data).eq(locator).execute()
# 		self.refresh()

# 	def delete(self,locator):
# 		"""
# 		locator: list ["id",1]
# 		"""
# 		self.client.table(self.table_name).delete().eq(locator).execute()
# 		self.refresh()


# # def get_table(table_name):
# # 	return pd.DataFrame(st.session_state['client'].table(table_name).select('*').execute().data)

# def convert_date(df,col):
# 	df[col] = df[col].pipe(pd.to_datetime)
# 	return df


# def edit_levels():
# 	st.subheader('Wells and Water Levels')

# 	table = Table('date')
# 	st.experimental_data_editor(table.df,use_container_width=True,num_rows='dynamic',key='date_changes',)
# 	changes = st.session_state["date_changes"]
# 	st.write(changes)
# 	if st.button('Save'):
# 		# # st.session_state['client'].table('date').update(st.session_state["date_changes"]).execute()
# 		# for k,v in changes['edited_cells'].items():
# 		# 	row,col = [int(i) for i in k.split(':')]
# 		# 	# row,col = [int(i) for i in k.split(':')]
# 		# 	st.write(f"Changed {row} -> {col}={v}")

# 		# for change in changes['added_rows']:
# 		# 	for i,data in change.items():
# 		# 		for k,v in data.items():
# 		# 			col = int(k)
# 		# 			st.write(f"Added {col}={v}")
		
# 		# for change in changes['deleted_rows']:
# 		# 	for i,row in change.items():
# 		# 		# delete row
# 		# 		st.write(f"Deleted {row}")
		
# 		# st.write(changes['edited_cells'])
# 		st.write(changes['added_rows'])
# 		st.write(changes['deleted_rows'])
# 		st.success('Saved')