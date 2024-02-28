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
import locale

# Setup Streamlit layout
st.title('Gatenavn til geo-koordinat')

# Display instructions
st.write("""
Denne appen lar deg utvinne geo-koordinater fra norske gateadresser, basert på data fra Kartverket.

Du trenger en Excel-fil med gateadresser. Disse bør angis på formatet `{gatenavn nr.} ({by/kommune})`, f.eks. **Berberisveien 1 (Stavanger)**.,

Excel-arket må bare ha verdier i én kolonne (A), og du behøver ikke angi kolonnenavn i rad 1.

Etter opplastning vil appen utvinne geo-koordinater og returnere kommaseparerte geo-koordinater for bredde- og lengdegrad.
Det kan ta noe tid for appen å fullføre operasjonen.

Du kan da også laste ned en ny Excel-fil der koordinatene finnes i to nye kolonner.
""")

# File uploader widget
uploaded_file = st.file_uploader("Velg en Excel-fil", type=['xlsx'])

if uploaded_file is not None:
    # Display message indicating that geocoding is in progress
    st.info('Geokoding startet.')
    
    df = pd.read_excel(uploaded_file, header=None, names=['gateadresse'])
    
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'en_US')

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
            lat = float(data['adresser'][0]['representasjonspunkt']['lat'])
            lon = float(['adresser'][0]['representasjonspunkt']['lon'])
            
            # Format the lat and lon to only have 6 decimal places
            lat_formatted = f"{lat:.6f}"
            lon_formatted = f"{lon:.6f}"
        
            return lat_formatted, lon_formatted
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
    st.download_button(label="Last ned Excel-fil",
                       data=output,
                       file_name="output.xlsx",
                       mime="application/vnd.ms-excel")

    # Display DataFrame in Streamlit (optional)
    st.dataframe(df)

# Instructions
else:
    st.write("Vennligst last opp en Excel-fil for å begynne.")
