import streamlit as st
import os
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt

from util import open_file, forecast

st.set_page_config(
    page_title="VINTANGE-VALUE"
)


fol_path = Path('../data/tn_v1')

def file_size(file_path):
    return os.stat(fol_path/file_path).st_size

crop = sorted(os.listdir(fol_path), key=file_size, reverse=True)
crop = list(map(lambda x: x[:-8], crop))

st.write('# Crop Page')

crop = st.selectbox('Crop', crop)

df = open_file(fol_path / f'{crop}.feather')
# st.dataframe(df[['price', 'tmin', 'tmax', 'rainfall']], width=800)

st.write('## History')
st.line_chart(df, y='price')

st.write('## Past 6 months')
st.line_chart(df[-100:], y='price')

st.write('## Forecast')
predicted = forecast(df, 20)
one_graph = pd.concat([df, predicted])
st.line_chart(one_graph[-100:], y=['price', 'forcasted'])

st.write('## Average price over years')
price_over_year = df[['year', 'price']].groupby('year').mean()
st.bar_chart(price_over_year, y='price')

# st.write('## Price over years (Inflammation)')
# st.dataframe('')