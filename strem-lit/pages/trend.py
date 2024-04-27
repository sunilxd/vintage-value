import streamlit as st
import os
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt

from util import open_file

fol_path = Path('../data/tn_v1')


crops = list(map(lambda x: x[:-8], os.listdir(fol_path)))

@st.cache_data(show_spinner=False)
def get_dataframe():
    dfs = {}

    bar_text = 'Processing Data'
    bar = st.progress(0, text=bar_text)
    cur = 0

    for crop in crops:
        cur += 1
        bar.progress(cur/len(crops), text=bar_text)
        df = open_file(fol_path / f'{crop}.feather')

        if df.shape[0] < 200:
            dfs[crop] = {'df': None, 'score': 0}
            continue

        dfs[crop] = {}

        average = df['price'].mean()
        std_dev = df['price'].std()
        df['average'] = average
        dfs[crop]['df'] = df
        dfs[crop]['score'] = (df['price'].iloc[-1]-average)/std_dev

    bar.empty()
    return dfs

st.latex(r'''
    Trend Value = \frac{Last Price - Average}{Standard Deviation}
''')

st.latex(r'''
    T(P) = \frac{P_n - \bar{P}}{\sigma(P)}
''')


dfs = get_dataframe()

crops.sort(key= lambda x: dfs[x]['score'], reverse=True)
crops = crops[:10]

# st.write('## Trend')
# trend = pd.DataFrame

for crop in crops:
    st.write('#### **{crop}** {score}'.format(
        crop = crop,
        score = round(dfs[crop]['score'], 2)
    ))

    st.line_chart(dfs[crop]['df'], y=['price', 'average'])
