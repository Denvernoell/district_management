import streamlit as st
from dashboard_shared import District

def page():
	district = District(
		name='Aliso Water District',
		folder='aliso',
		pages = {
				"Depth To Water":'depth_to_water',
			}
	)

