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
from typing import Generator


def migrate_to_map(current, file_path, type):
    pane = dictionary[str(type)]["pane"]
    if type == "points_of_interests":
        folium.GeoJson(
            current,
            name=file_path.name,
            pane=pane,
            tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False)
        ).add_to(m)

    else:
        style = dictionary[type]["style_function"]
        folium.GeoJson(
            current,
            name=file_path.name,
            pane=pane,
            style_function=lambda feature: style,
            tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False)
            ).add_to(m)


# Define the folder path
folder_path = Path('./clean_data')

# open json-file
with open('test_dic.json', 'r') as file:
    dictionary = json.load(file)
print(dictionary)


# Create a base map - to be automized with the location and zoom!
m = folium.Map(location=[51.0, 6.5], zoom_start=10, min_zoom=8)

# Set up custome map panes for points, lines, polygons
folium.map.CustomPane("pointsPane", z_index=330).add_to(m)  # type: ignore
folium.map.CustomPane("linesPane", z_index=320).add_to(m)  # type: ignore
folium.map.CustomPane("polygonsPane", z_index=310).add_to(m)  # type: ignore


# add Esri World Imagery tile layer,
# (see [Leaflet Provider Demo](https://leaflet-extras.github.io/leaflet-providers/preview/) for a quick preview of various basemaps).
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri.WorldImagery',
    overlay=False,
    control=True,
    min_zoom=8,
    show=False  # hide layer when opening the map
).add_to(m)
# add grey canvas tile layer
folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    attr='Carto',
    name='Grey Canvas',
    overlay=False,
    control=True,
    min_zoom=8,
    show=True  # hide layer when opening the map
).add_to(m)


# loop over every file in folder "clean_data"
for file_path in folder_path.iterdir():
    if file_path.is_file():  # Check if it is a file (not a directory)
        print(f"Processing file: {file_path.name}")

        # suggest: multiple layers in one file
        for layer in gpd.list_layers(f"./{file_path}"):
            current = gpd.read_file(f"./{file_path}", layer=layer)
            #
            # ---
            # find out which pane the layer has
            # ---
            #
            pane = "pane"
            migrate_to_map(current, file_path.name, layer)


# save the map as hmtl
m.save('pipe_map.html')
