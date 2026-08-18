import streamlit as st
import numpy as np
import altair as alt
import pandas as pd

from models import get_forecast

@st.cache_data
def get_data():
    d = np.random.randint(1,50,20).tolist()
    # p = np.random.randint(3,8)
    # d = [28, 19, 18, 13, 19, 16, 19, 18, 13, 16, 16, 11, 18, 15, 13, 15, 13, 11, 13, 10, 12] #! Uncomment for static values
    df = get_forecast(d, extra_periods=4, n=3)
    df.index.name = 'Period'
    
    return df, d

dataframe, d_list = get_data()

st.markdown(f"""
    ### Statistical Forecasting
    
    Forecasting using several statistical models (no ML yet).
""")

nearest = alt.selection_point(nearest=True, on='pointerover', fields=['y'], empty=False)

chart = alt.Chart(dataframe.reset_index()).transform_fold(
        ['Demand','fm01','fm02'],
        as_=['model','value']
    ).mark_line(interpolate='basis').encode(
    x='Period:Q',
    y='value:Q',
    color='model:N',
)

selectors = alt.Chart(dataframe.reset_index()).transform_fold(
        ['Demand','fm01','fm02'],
        as_=['model','value']
    ).mark_point().encode(
    y='value:Q',
    opacity=alt.value(0),
).add_params(
    nearest
)
when_near = alt.when(nearest)

points = chart.mark_point().encode(
    opacity=when_near.then(alt.value(1)).otherwise(alt.value(0))
)

text = chart.mark_text(align='left', dx=5, dy=-5).encode(
    text=when_near.then('value:Q').otherwise(alt.value(' '))
)

rules = alt.Chart(dataframe.reset_index()).transform_fold(
        ['Demand','fm01','fm02'],
        as_=['model','value']
    ).mark_rule(color='gray').encode(
        x='Period:Q'
). transform_filter(
    nearest        
)

st.altair_chart(
    alt.layer(
        chart, selectors
    ).properties(
        width=600, height=300
    )
)

st.markdown(f"""
    ### Demand and Forecast Values
    Randomly generated demand values for the last 20 periods. The forecast is based on these values.""")

st.dataframe(dataframe, hide_index=True)
