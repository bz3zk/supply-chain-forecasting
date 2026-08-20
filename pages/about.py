import streamlit as st

st.markdown("""
# About This App

What is this app about anyway? Well, it's basically me being nostalgic about something that I was planning to do (a long time ago),
but never really got around to building.

I read an amazing book called ["Data Science for Supply Chain Forecasting"](https://www.amazon.com/Data-Science-Supply-Chain-Forecasting/dp/3110671107) by Nicolas Vandeput (all credit goes to him), and I was really inspired to build a simple app that would allow me to play around with the concepts in the book.

So, here's a brief overview of the different forecasting models implemented in this app:

### fm01 - Moving Average (MA)
"We predict the demand in June to be the average of March, April and May."

### fm02 - Simple Exponential Smoothing (SES)
[...] is one of the simplest ways of forecast a time series. Just as for a moving average, the basic idea of this model is to assume that the future will be more or less as the (recent) past. The only pattern that this model will be able to learn from demand is its **level**.

* **Level** is the average value around which the demand varies over time. [...] is a smoothed version of the demand.

The **limitations of Exponential Smoothing**:

* It does not project trends (to be solved using **double exponential smoothing**).
* It does not recognize any seasonal pattern (to be solved with **triple exponential smoothing**).
* It cannot (natively) use any external explanatory variables (such as pricing or marketing expenses).

### fm03 - Double Exponential Smoothing (DES)
A major issue of **simple smoothing** is that it can onlty see a level, and is unable to identify and project a **trend**.

* **Trend** [is] the average variation of the time series level between two consecutive periods. Remember that the level is the average value around which the demand varies over time.

[..] for the **simple exponential smoothing** model, we updated the forecast at each period partially based on
1. the **most recent observation** of the demand.
2. the **previous estimation** of the demand (that is the previous forecat).

Similarly, the general idea behind exponential smoothing models is that each demand component (currently, the level and the trend, later the seasonality, as well) will be updated after each period based on two same pieces of information: the last observation and the previous estimation of this component.

The limitations of **double exponential smoothing** 

[...] our model will assume that the trend will go on forever. This might result in some issues for mid- and long-term forecasts. Next to this risk of infinite trend, we still have:
* The lack of seasonality.
* The impossibility to take external information into account (like marketing budget or price variations).

### fm04 - Double Exponential Smoothing with Damping (DESD)

One of the limitations of the double smoothing model is the fact that the trend is assumed to go on forever. In 1985, Gardner and McKenzie proposed in their paper "Forecasting Trends in Time Series" to add a new layer of intelligence to the double exponential model: a **damping factor, phi**, that will exponentially reduce the trend over time. One could say that this new model **forgets** the trend over time. Or that the model remembers only a fraction (*phi*) of the previous estimated trend.

**Limitations** 

Thanks to the damping factor (*phi*), we solved the main limitation of the *double smoothing model*: the trend doesn't go on forever anymore. This damping factor might at first glance seem like a simple idea, but it actually allow us to be much more accurate for mid- and long-term forecasts. Nevertheless, we still miss the ability for our model to recognize a seasonal pattern and apply it in the future. Many supply chains do face seasonality in one way or another, so we need our forecast models to be smart enough to fit these patterns. In order to do so, we will add a third layer of exponential smoothing.

### fm05 - Triple Exponential Smoothing with Multiplicative Seasonality (TESM)
With the first two exponential smoothing models we saw, we learned how to identify the level and the trend of a time series and used these pieces of information to populate our forecast. After that, we added an extra layer of intelligence to the trend by allowing the model to partially forget it over time.

Unfortunately, the simple and double exponential smoothing models do not recognize **seasonal patterns** and therefore cannot extrapolate any seasonal behavior in the future. Seasonal products -with high and low seasons- are common for many supply chains across the globe, as many different factors can cause seasonality. This limitation is thus a real problem for our model.

[To fix this], the idea is that the model will learn **multiplicative seasonal factors** that will be applied to each period inside a full seasonal cycle. **Multiplicative** seasonal factors mean, for example, that the model will know that the demand is increased by 20% in January (compared to the yearly average) but reduced by 30% in February.
""")