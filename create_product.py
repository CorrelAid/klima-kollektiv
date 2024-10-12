# CorrelAid for Klima*Kollektiv Karte der Transportleitung, Rohdungstrassen und Zerrstörungspunkte entlang der Trasse
# Oct, 12, 2024

# by Tim Appelhans, Malte Ferber


import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point, Polygon, MultiPolygon, MultiLineString
from shapely.ops import split, snap
import json
from pathlib import Path


# Define the folder path
folder_path = Path('./clean_data')

# loop over every file in folder "clean_data"
for file_path in folder_path.iterdir():
    if file_path.is_file():  # Check if it is a file (not a directory)
        print(f"Processing file: {file_path.name}")
        # Add your file processing code here
