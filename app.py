import streamlit as st

# Main entry point for the Streamlit App

st.set_page_config(
    page_title='Supply Chain Forecasting',
    page_icon=':chart_with_upwards_trend:'
)

pg = st.navigation([
    st.Page("./pages/charts.py", title="Charts", icon=":material/chart_data:", default=True),
    st.Page("./pages/models.py", title="Models", icon=":material/cognition:"),
    st.Page("./pages/data.py", title="Data", icon=":material/dataset:"),
    st.Page("./pages/about.py", title="About", icon=":material/info:")
    ])

pg.run()