#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:34:16 2024

@author: joncto
"""

import streamlit as st
import pandas as pd
import requests
pip install openpyxl
import openpyxl
from io import BytesIO

# Setup Streamlit layout
st.title('Gatenavn til geo-koordinat')

# File uploader widget
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=None, names=['gateadresse'])

    def get_geocoordinates(adresse):
        base_url = "https://ws.geonorge.no/adresser/v1/sok"
        params = {
            'sok': adresse,
            'treffPerSide': 1,
            'asciiKompatibel': 'true'
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        try:
            lat = data['adresser'][0]['representasjonspunkt']['lat']
            lon = data['adresser'][0]['representasjonspunkt']['lon']
            return lat, lon
        except (IndexError, KeyError):
            return None, None

    # Process data
    df[['latitude', 'longitude']] = df.apply(lambda row: pd.Series(get_geocoordinates(row['gateadresse'])), axis=1)

    # Convert DataFrame to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
        writer.save()
    output.seek(0)

    # Download link
    st.download_button(label="Download Excel",
                       data=output,
                       file_name="output.xlsx",
                       mime="application/vnd.ms-excel")

    # Display DataFrame in Streamlit (optional)
    st.dataframe(df)

# Instructions
else:
    st.write("Please upload an Excel file to begin.")
