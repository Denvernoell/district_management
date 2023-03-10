import streamlit as st
import sys
# sys.path.append('..')
from districts.tranquillity.plotly_figures import create_dtw_figure
import plotly.graph_objects as go
import pandas as pd

import base64
import io

import arrow
from dashboard_shared import Table,Components,export_df,month_picker,download_pdf

get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M").format("MMMM YYYY")
add_date = lambda df: df.assign(date = [get_date(y['year'],y['month']) for i,y in df.iterrows()])

def main():
    st.subheader('Depth to water')


    table_name = 'TID_well_depth_to_water_ft'
    df = Table(table_name).df.sort_values(['date'])
    df['date'] = pd.to_datetime(df['date'])


# st.dataframe(df)
# st.markdown(df.dtypes)
# st.markdown(df['date'].min().year)

    # date_range = month_picker(
    #     df['date'].min().year,
    #     df['date'].max().year,
    #     )
    # st.markdown(date_range)

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

    data = df.loc[
        (df['well_id'].isin(wells_to_use))
        # (df['date'] >= date_range[0].naive) &
        # (df['date'] <= date_range[1].naive)
        ]



    # data = data.pipe(add_date)
    pivot = pd.pivot_table(data,values=['dtw_ft'],index=['date'],columns=['well_id']).droplevel(0,axis='columns')
    # if st.button('Graph'):

    figure = create_dtw_figure(data)
    st.plotly_chart(figure)
    import plotly
    def export_figure(figure,name):
        in_to_pt = lambda inch: inch * (1000 / 10.417)
        figure.update_layout(width=in_to_pt(11),height=in_to_pt(8.5))

        figure.write_image(
            f'{name}_{arrow.now().format("YYYYMMDD") }.pdf',
            engine='kaleido',
            scale=1,
            )

    if st.button('Export',use_container_width=True):
        # download_pdf(
        export_figure(figure,'DTW')
            # 'DTW.pdf',
            # 'download DTW figure'

        # )

    # if st.button('Table'):
    to_month_year = lambda y: arrow.get(y).format("MMMM D, YYYY")
    pivot.index = [to_month_year(i) for i in pivot.index]

    st.dataframe(pivot.style.applymap(lambda x: 'color: transparent' if pd.isnull(x) else '').format(formatter="{:.2f}"))
    export_df(pivot,"DTW.xlsx")
