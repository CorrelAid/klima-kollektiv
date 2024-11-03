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
    print(f"Adding {type} to map with pane {pane}")
    if type == "points_of_interests":
        folium.GeoJson(
            current,
            name=file_path,
            pane=pane,
            tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False)
        ).add_to(m)

    else:
        style = dictionary[str(type)]["style_function"]
        print('style dict is:', style)
        folium.GeoJson(
            current,
            name=file_path,
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

# Initialize the file counter for gpkg files
file_count = 0

# loop over every file in folder "clean_data"
for file_path in folder_path.iterdir():
    if file_path.is_file():  # Check if it is a file (not a directory)
        print(f"Processing file: {file_path.name}")

        # requirement: only one layer per file
        if file_path.suffix == '.gpkg':
            current = gpd.read_file(f"./{file_path}")
            file_count += 1  # Increment the file counter
        else:
            print(f"Skipping file: {file_path.name}")
            continue

        # Auf Dateiname zugreifen, letztes Wort vor Dateiformat ist der Objecttype (z.B. lake, pipeline, ...)
        objecttype = file_path.name.split(".")[0].split("_")[-1].lower()
        Name = file_path.name.split(".")[0].split("_")[0]

        current['name'] = Name

        print('Has columns:', current.columns)
        print('Layer is of geom_type:', str(current.geometry.geom_type))
        print('Layer is of objecttype:', objecttype)

        # Im Dict format.json nachschauen ob der geom_type des files für den objecttype erlaubt ist
        if objecttype not in dictionary or not current.geometry.geom_type.isin(dictionary[objecttype]["geometry"]).all():
            errorlist.append(file_path.name)  # falls nicht: Dateiname in errorlist speichern

        migrate_to_map(current, file_path.name, objecttype)

print(f"gpkg files processed: {file_count}")

print('Failed files are:', errorlist)

# save the map as hmtl
m.save('pipe_map.html')
print('Map saved as pipe_map.html')
