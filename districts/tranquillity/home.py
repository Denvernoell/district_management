import streamlit as st
import plotly.graph_objects as go
import pandas as pd

import base64
import io
import webbrowser
from pathlib import Path
import arrow


from dashboard_shared import Table,District
def page():
	district = District(
		name='Tranquillity Irrigation District',
		folder='tranquillity',
		pages = {
				# "test1":'test1',
				# "test2":'test2',
				"Subsidence":'subsidence',
				# "Water Levels":'water_levels',
				# "Water Quality":'water_quality',
				"Depth To Water":'depth_to_water',
				"Well Data":'well_data',
			}
	)

