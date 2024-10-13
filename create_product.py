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


# Create a base map - to be automized with the location and zoom!
m = folium.Map(location=[51.0, 6.5], zoom_start=10, min_zoom=8)

# Set up custome map panes for points, lines, polygons
folium.map.CustomPane("pointsPane", z_index=330).add_to(m)
folium.map.CustomPane("linesPane", z_index=320).add_to(m)
folium.map.CustomPane("polygonsPane", z_index=310).add_to(m)


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
        print(f"{file_path}")
        current = gpd.read_file(f"./{file_path}", layer=file_path.name)

        # adopt this according to dictionary!
        # what are the qualities of a linesPane and a polygonsPane?
        # layer "type" must be "Polygon" or "Multipolygon" if layer name = etc. ->

        if current.geom_type in [Polygon, MultiPolygon]:  # for lakes, buildings etc
            pane = "polygonsPane"
        elif current.geom_type == Point:
            pane = "pointsPane"
        else:
            # elif current.geom_type in [LineString, MultiLineString]:
            pane = "linesPane"


        # for lakes:
        folium.GeoJson(
            current,
            name=file_path.name,
            pane=pane,
            style_function=lambda feature: {
                'color': '#4e4eff',
                'fillColor': "#4e4eff",
                'fillOpacity': 0.8,
                'fill': True,
                'weight': 0
                },
            tooltip=file_path.name
            ).add_to(m)


# save the map as hmtl
m.save('pipe_map.html')

# # --- Just to compare --- #
# # See
# folium.GeoJson(
#     hambacher_see,
#     name="Hambacher See",
#     pane="polygonsPane",
#     style_function=lambda feature: {
#         'color': '#4e4eff',
#         'fillColor': "#4e4eff",
#         'fillOpacity': 0.8,
#         'fill': True,
#         'weight': 0
#     },
#     tooltip="Hambacher See"
# ).add_to(m)

# # Pipeline
# folium.GeoJson(
#     pipelines_new,
#     name="Wasserleitungen",  # again, determine the name for the layer toggle
#     pane="linesPane",
#     style_function=lambda feature: {
#         'color': '#6b6bc9',  # nif feature['properties']['Name'] == 'Bündelungsleitung' else '#3f3f3f',
#         'weight': 5  # feature['properties']["Leistung (m3/s)"]
#     },
#     tooltip=folium.GeoJsonTooltip(fields=['Name'], labels=False),
#     popup=folium.GeoJsonPopup(fields=['Name', "Strecke", "Länge (km)", "Leistung (m3/s)", "Trassenbreite (m)", "Anzahl der Röhren"])
# ).add_to(m)

# # Clearing / Rodungstrasse
# folium.GeoJson(
#     data=clearing,
#     name="Rodungstrasse",  # again, determine the name for the layer toggle
#     pane="polygonsPane",
#     style_function=lambda feature: {
#         'color': 'brown',
#         'weight': 1,
#         'fillColor': 'brown',
#         'fillOpacity': 0.3
#     }, tooltip="Rodungstrasse"
# ).add_to(m)

# # points of interests like constructions, and destructions
# folium.GeoJson(
#     destructions,
#     name="Zerstörungen",  # again, determine the name for the layer toggle
#     pane="pointsPane",
#     marker=folium.Marker(
#         icon=folium.Icon(color='lightgreen', icon='burst', prefix='fa')
#     ),
#     tooltip=folium.GeoJsonTooltip(fields=['Name'], labels=False)
# ).add_to(m)

# # Verteilwerk / Pumpbauwerk
# folium.GeoJson(
#     pumpwerk,
#     name="Pumpbauwerk",  # again, determine the name for the layer toggle
#     pane="linesPane",
#     style_function=lambda feature: {
#         'color': 'black',
#         'weight': 1,
#         'fillColor': 'black',
#         'fillOpacity': 1
#     },
#     tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False)
# ).add_to(m)
