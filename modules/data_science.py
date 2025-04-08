import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

def exibir_interface(bb):
    st.subheader("Análise com KMeans")
    df = pd.DataFrame({
        'x': [1, 2, 3, 8, 9, 10],
        'y': [1, 2, 3, 8, 9, 10]
    })
    kmeans = KMeans(n_clusters=2).fit(df)
    df['cluster'] = kmeans.labels_
    st.write(df)
    bb.set("clusters", df)