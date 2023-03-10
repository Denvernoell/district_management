import streamlit as st
from dashboard_shared import District

def page():
	district = District(
		name='Panoche Water District',
		folder='panoche',
		pages = {
				"Subsidence":'subsidence',
			}
	)

