import streamlit as st
import pandas as pd

import base64
import io

import arrow

import geopandas as gpd

from dashboard_shared import Table,Components,export_df
import leafmap.foliumap as leafmap

def main():
	st.markdown('## Subsidence')
	