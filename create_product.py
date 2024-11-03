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
with open('format.json', 'r') as file:
    dictionary = json.load(file)
print("Objecttype dictionary:\n", dictionary)


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


errorlist = []

# loop over every file in folder "clean_data"
for file_path in folder_path.iterdir():
    if file_path.is_file():  # Check if it is a file (not a directory)
        print(f"Processing file: {file_path.name}")

        # requirement: only one layer per file
        current = gpd.read_file(f"./{file_path}")

        # Auf Dateiname zugreifen, letztes Wort ist der Objecttype (z.B. lake, pipeline, ...)
        objecttype = file_path.name.split("_")[-1].lower()

        # Im Dict format.json nachschauen ob der geom_type des files für den objecttype erlaubt ist
        if current.geometry.geom_type not in dictionary[objecttype]["geometry"]:
            errorlist.append(file_path.name) # falls nicht: Dateiname in errorlist speichern

        migrate_to_map(current, file_path.name, objecttype)


print(errorlist)
# save the map as hmtl
m.save('pipe_map.html')
