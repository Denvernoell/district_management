import streamlit as st
import pandas as pd
import supabase
from importlib import import_module

from dashboard_shared import Components, Table, District

C = Components("P&P")
C.header()

def login_page():
	st.session_state['client'] = supabase.create_client(st.secrets['supabase_url'],st.secrets['supabase_key'])
	with st.form(key='login'):
		email = st.text_input("Email")
		password = st.text_input("Password", type="password")
		# email = st.secrets['test_email']
		# password = st.secrets['test_password']
		submit_button = st.form_submit_button("Log in")

	if submit_button:
		try:
			st.session_state['user'] = st.session_state['client'].auth.sign_in(email=email, password=password)
			# st.success('Logged in')
			st.session_state['Logged In'] = True
			add_sidebar()
			# st.experimental_rerun()
		except:
			st.error('Incorrect username or password')

		# if (user == st.secrets['login_username'] and password == st.secrets['login_password']):

def add_sidebar():
	user_data = Table('user_permissions').df
	user_email = st.session_state['user'].dict()['user']['identities'][0]['identity_data']['email']
	# st.markdown(user_email)
	permissions = user_data.pipe(lambda df: df.loc[df['email'] == user_email]['districts'].iloc[0])
	st.sidebar.markdown(f"Logged in as {user_email}")
	# st.sidebar(f"Logged in as {user_email}")
	st.sidebar.markdown("---")
	# st.sidebar("---")
	# st.markdown(permissions)
	pages = {
		'Aliso Water District':District(
			name='Aliso Water District',
			folder='aliso',
			pages = {
				"Depth To Water":'depth_to_water',
			}
		),
		'Panoche Water District':District(
			name='Panoche Water District',
			folder='panoche',
			pages = {
					"Subsidence":'subsidence',
				}
		),
		'Tranquillity Irrigation District':District(
			name='Tranquillity Irrigation District',
			folder='tranquillity',
			pages = {
					"Subsidence":'subsidence',
					# "Water Levels":'water_levels',
					# "Water Quality":'water_quality',
					"Depth To Water":'depth_to_water',
					"Well Data":'well_data',
					"Well Locations":'well_locations',
				}
		)
		}
	
	if permissions == 'all':
		pages = pages
			
	else:
		pages = {k:v for k,v in pages.items() if k in permissions.split(';')}
	# districts.append('public')

	# st.session_state['district'] = st.sidebar.radio('District', districts.keys())
	district = pages[st.sidebar.radio('Districts', pages.keys())]
	district.homepage()


public_pages,private_pages = st.tabs(['Public','Private'])


with public_pages:
	pages = {
		'Water Rights':District(
			name='Water Rights',
			folder='water_rights',
			pages = {
				"Aliso Diversion Checker":'aliso_diversion_checker',
				"Flood Watch":'flood_watch',
				'Triangle T Diversion Checker':'triangle_t_diversion_checker',
			}
		),
	}
	district = pages[st.sidebar.radio('Districts', pages.keys())]
	district.homepage()

with private_pages:
	if 'Logged In' not in st.session_state:
		st.session_state['Logged In'] = False
	# try:
	if st.session_state['Logged In']:
		# st.success('Logged in')
		add_sidebar()
	else:
		login_page()

# except Exception as e:
# 	st.markdown(e)
	# st.session_state['Logged In'] = False
	# login_page()



# try:
# login_page()
# 	if st.session_state['Logged In']:
# 		# st.success('Logged in')
# 		add_sidebar()
# 	else:
# except Exception as e:
# 	st.markdown(e)
# 	st.session_state['Logged In'] = False
# 	login_page()

C.footer()