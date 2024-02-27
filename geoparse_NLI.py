#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:34:16 2024

@author: joncto
"""

import streamlit as st
import pandas as pd
import requests
import openpyxl
from io import BytesIO

# Setup Streamlit layout
st.title('Gatenavn til geo-koordinat')

# Display instructions
st.write("""
Denne appen lar deg laste opp en Excel-fil med gateadresser. Programmet bruker GeoNorges Swagger API for å parse gateadresser, og returnerer en Excel-fil med kommaseparerte geo-koordinater for bredde- og lengdegrad.

Excel-arket bør bare inneholde én kolonne (A). Adressen bør angis på formatet {gatenavn nr.} ({by/kommune}). F.eks. **Berberisveien 1 (Stavanger)**.

Etter endt operasjon kan du laste ned en Excel-fil med koordinater for hver adresse.

Det kan ta noe tid for appen å fullføre operasjonen.
""")

# File uploader widget
uploaded_file = st.file_uploader("Velg en Excel-fil", type=['xlsx'])

if uploaded_file is not None:
    # Display message indicating that geocoding is in progress
    st.info('Geokoding pågår...')
    
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
        # writer.save()
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
    st.write("Vennligst last opp en Excel-fil for å begynne.")
