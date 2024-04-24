import streamlit as st
import os
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
from util import get_weather_info

df = get_weather_info()
# st.dataframe(df)

st.write('## Rainfall')
st.line_chart(df, y='rainfall')

st.write('## Average rainfall over year')
rainfall_over_year = df[['year', 'rainfall']].groupby('year').sum()
st.bar_chart(rainfall_over_year)

st.write('## Temperature')
st.line_chart(df, y=['tmin', 'tmax'])
