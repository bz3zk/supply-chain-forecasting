import streamlit as st

#! Main entry point for the Streamlit App

forecast_page = st.Page("./pages/forecast.py", title="Forecast", icon=":material/chart_data:", default=True)
about_page = st.Page("./pages/about.py", title="About", icon=":material/info:")

st.sidebar.title("Supply Chain Forecasting")

pg = st.navigation([forecast_page, about_page])

st.set_page_config(
    page_title='Supply Chain Forecasting',
    page_icon=':chart_with_upwards_trend:'
)

pg.run()