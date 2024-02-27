#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:34:16 2024

@author: joncto
"""

# Importere pakker
import requests
import pandas as pd


# Definere datakilde og laste inn data fra Excel
file_path = './gateadresser.xlsx'
df = pd.read_excel(file_path, header=None, names=['gateadresse'])

# Funksjon for henting av geokoordinater fra GeoNorges API
def get_geocoordinates(adresse):
    base_url = "https://ws.geonorge.no/adresser/v1/sok"  # base URL for Geonorges API
    params = {
        'sok': adresse,  # Bruk 'adresse' parameter her
        'treffPerSide': 1,  # Antall treff per side (antar vi bare ønsker toppresultatet)
        'asciiKompatibel': 'true' # Garanterer at dataene som returneres er ascii-kompatible
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    # Henter ut breddegrad (lat) and lengdegrad (lon)
    try:
        lat = data['adresser'][0]['representasjonspunkt']['lat']
        lon = data['adresser'][0]['representasjonspunkt']['lon']
        return lat, lon
    except (IndexError, KeyError):
        return None, None  # I tilfeller der adressen ikke blir funnet eller responsen ikke er som forventet
    
# print(df.columns)

# Legger til geokoordinater for hver gateadresse i 'latitude' og 'longitude'.
df[['latitude', 'longitude']] = df.apply(lambda row: pd.Series(get_geocoordinates(row['gateadresse'])), axis=1)

# Lagrer oppdatert dataframe til ny Excel-fil
output_file_path = './output.xlsx'
df.to_excel(output_file_path, index=False)

# Lagrer oppdatert dataframe til ny CSV fil
csv_output_file_path = './output.csv'
df.to_csv(csv_output_file_path, index=False)