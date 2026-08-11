import pandas as pd
import numpy as np

# ! TODO :
# ! 1 - Build Forecasting Engine
# ! 2 - Test with more than one demand value (e.g., demand for more than one item).
# ! 3 - Complete structure of the project and publish
# ? OPTIONAL : Allow user to upload csv file with demand

def moving_average(d, extra_periods=1, n=3):
    
    # Historical period length
    cols = len(d)
    
    # Append np.nan
    d = np.append(d, [np.nan]*extra_periods)
    
    # Define the forecast array
    f = np.full(cols+extra_periods, np.nan)
    
    # Create all the t+1 forecast until end of historical period
    for t in range(n, cols):
        f[t] = np.mean(d[t-n:t])
    
    # Forecast for all extra periods
    f[t+1:] = np.mean(d[t-n+1:t+1]) 
    
    # !
    # Return a DataFrame with the demand, forecast & error
    # df = pd.DataFrame.from_dict({'Demand':d, 'Forecast':f, 'Error':d-f})
    
    # return df
    # !
    
    return f

def simple_exp_smooth(d, extra_periods=1, alpha=0.4):
    
    # Historical period length
    cols = len(d)
    
    # Append np.nan into the demand array to cover future periods
    d = np.append(d, [np.nan]*extra_periods)
    
    # Forecast array
    f = np.full(cols+extra_periods, np.nan)
    
    # initialization of first forecast
    f[1] = d[0]
    
    # Create all the t+1 forecast until end of historical period
    for t in range(2, cols+1):
        f[t] = alpha*d[t-1]+(1-alpha)*f[t-1]
        
    # Forecast for all extra periods
    for t in range(cols+1, cols+extra_periods):
        # Update the forecast as the previous forecast
        f[t] = f[t-1]
    
    # ! 
    # df = pd.DataFrame.from_dict({'Demand':d, 'Forecast':f, 'Error': d-f})
    
    # return df
    # !
    
    return f
    
def double_exp_smooth(d, extra_periods=1, alpha=0.4, beta=0.4):
    
    # Historical period length
    cols = len(d)
    
    # Append np.nan into the demand array to cover future periods
    d = np.append(d, [np.nan]*extra_periods)
    
    # Creation of the level, trend and forecast arrays
    f, a, b = np.full((3, cols+extra_periods), np.nan)
    
    # Level & Trend initialization
    a[0] = d[0]
    b[0] = d[1] - d[0]
    
    # Create all the t+1 forecast
    for t in range(1, cols):
        f[t] = a[t-1] + b[t-1]
        a[t] = alpha * d[t] + (1-alpha)*(a[t-1] + b[t-1])
        b[t] = beta * (a[t] - a[t-1]) + (1-beta) * b[t-1]
    
    # Forecast for all extra periods
    for t in range(cols, cols+extra_periods):
        f[t] = a[t-1] + b[t-1]
        a[t] = f[t]
        b[t] = b[t-1]
    
    # !
    # df = pd.DataFrame.from_dict({'Demand':d, 'Forecast':f, 'Level':a, 'Trend':b, 'Error':d-f})
    
    # return df
    # !
    
    return f

def double_exp_smooth_damped(d, extra_periods=1, alpha=0.4, beta=0.4, phi=0.9):
    
    # Historical period length
    cols = len(d)
    
    # Append np.nan into the demand array to cover future periods
    d = np.append(d, [np.nan]*extra_periods)
    
    # Creation of the level, trend, and forecast arrays
    f, a, b = np.full((3, cols+extra_periods), np.nan)
    
    # Level & Trend initialization
    a[0] = d[0]
    b[0] = d[1] - d[0]
    
    # Create all the t+1 forecast
    for t in range(1, cols):
        f[t] = a[t-1] + phi * b[t-1]
        a[t] = alpha * d[t] + (1-alpha) * (a[t-1] + phi * b[t-1])
        b[t] = beta * (a[t] - a[t-1]) + (1-beta) * phi * b[t-1]
    
    # Forecast for all extra periods
    for t in range(cols, cols+extra_periods):
        f[t] = a[t-1] + phi * b[t-1]
        a[t] = f[t]
        b[t] = phi * b[t-1]
    
    # !
    # df = pd.DataFrame.from_dict({'Demand':d, 'Forecast':f, 'Level':a, 'Trend':b, 'Error':d-f})
    
    # return df
    # !
    return f

# Seasonal Factor Initialization
def seasonal_factors_mul(s, d, slen, cols):
    for i in range(slen):
        
        # Season average
        s[i] = np.mean(d[i:cols:slen]) 
    
    # Scale all season factors (sum of factors = slen)
    s /= np.mean(s[:slen])
    
    return s

def triple_exp_smooth_mul(d, slen=12, extra_periods=1, alpha=0.4, beta=0.4, phi=0.9, gamma=0.3):
    
    # Historical period length
    cols = len(d)
    
    # Append, np.nan into the demand array to cover future periods
    d = np.append(d, [np.nan]*extra_periods)
    
    # Components initialization
    f, a, b, s = np.full((4, cols+extra_periods), np.nan)
    s = seasonal_factors_mul(s, d, slen, cols)
    
    # Level & Trend initialization
    a[0] = d[0] / s[0]
    b[0] = d[1] / s[1] - d[0] / s[0]
    
    # Create the forecast for the first season
    for t in range(1, slen):
        f[t] = (a[t-1] + phi * b[t-1]) * s[t]
        a[t] = alpha * d[t] / s[t] + (1-alpha) * (a[t-1] + phi * b[t-1])
        b[t] = beta * (a[t] - a[t-1]) + (1-beta) * phi * b[t-1]
    
    # Create all the t+1 forecast
    for t in range(slen, cols):
        f[t] = (a[t-1] + phi * b[t-1]) * s[t-slen]
        a[t] = alpha * d[t] / s[t-slen] + (1-alpha) * (a[t-1] + phi * b[t-1])
        b[t] = beta * (a[t] - a[t-1]) + (1-beta) * phi * b[t-1]
        s[t] = gamma * d[t] / a[t] + (1-gamma) * s[t-slen]
    
    # Forecast for all extra periods
    for t in range(cols, cols+extra_periods):
        f[t] = (a[t-1] + phi * b[t-1]) * s[t-slen]
        a[t] = f[t] / s[t-slen]
        b[t] = phi * b[t-1]
        s[t] = s[t-slen]
    
    # !
    # df = pd.DataFrame.from_dict({'Demand': d, 'Forecast': f, 'Level': a, 'Trend': b, 'Season': s, 'Error': d-f})
    
    # return df
    # !
    
    return f

# Seasonal Factor Initialization
def seasonal_factors_add(s, d, slen, cols):
    for i in range(slen):
        
        # Calculate season average
        s[i] = np.mean(d[i:cols:slen])
    
    # Scale all season factors (sum of factors = 0)
    s -= np.mean(s[:slen])
    
    return s

def triple_exp_smooth_add(d, slen=12, extra_periods=1, alpha=0.4, beta=0.4, phi=0.9, gamma=0.3):
    
    # Historical period length
    cols = len(d)
    
    # Append np.nan into the demand array to cover future periods
    d = np.append(d, [np.nan]*extra_periods)
    
    # Components initialization
    f, a, b, s = np.full((4, cols + extra_periods), np.nan)
    s = seasonal_factors_add(s, d, slen, cols)
    
    # Level & Trend initialization
    a[0] = d[0] - s[0]
    b[0] = (d[1] - s[1]) - (d[0] - s[0])
    
    # Create the forecast for the first season
    for t in range(1, slen):
        f[t] = a[t-1] + phi * b[t-1] + s[t]
        a[t] = alpha * (d[t] - s[t]) + (1-alpha) * (a[t-1] + phi * b[t-1])
        b[t] = beta * (a[t] - a[t-1]) + (1-beta) * phi * b[t-1]
    
    # Create all the t+1 forecast
    for t in range(slen, cols):
        f[t] = a[t-1] + phi * b[t-1] + s[t-slen]
        a[t] = alpha*(d[t] - s[t-slen]) + (1-alpha) * (a[t-1] + phi * b[t-1])
        b[t] = beta * (a[t] - a[t-1]) + (1-beta) * phi * b[t-1]
        s[t] = gamma * (d[t] - a[t]) + (1-gamma) * s[t-slen]
    
    # Forecast for all extra periods
    for t in range(cols, cols+extra_periods):
        f[t] = a[t-1] + phi * b[t-1] + s[t-slen]
        a[t] = f[t] - s[t-slen]
        b[t] = phi * b[t-1]
        s[t] = s[t-slen]
        
    # !
    # df = pd.DataFrame.from_dict({'Demand': d, 'Forecast': f, 'Level':a, 'Trend':b, 'Season': s, 'Error': d-f})
    
    # return df
    # !

def get_forecast(d, extra_periods=1, n=3) -> pd.DataFrame:
    
    fmav = moving_average(d, extra_periods, n)
    fsimsm = simple_exp_smooth(d, extra_periods)
    fdoublesm = double_exp_smooth(d, extra_periods)
    fdoublesmdamp = double_exp_smooth_damped(d, extra_periods)
    ftrismmult = triple_exp_smooth_mul(d, slen=12, extra_periods=extra_periods)
    # ftrismadd = triple_exp_smooth_add(d, slen=12, extra_periods=extra_periods)
    
    d = np.append(d, [np.nan]*extra_periods)
    
    df = pd.DataFrame.from_dict({'Demand':d, 'fm01':fmav, 'fm02':fsimsm ,'fm03':fdoublesm, 'fm04':fdoublesmdamp, 'fm05':ftrismmult})
    
    # print(df)
    
    return df