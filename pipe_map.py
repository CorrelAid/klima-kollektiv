# CorrelAid for Klima*Kollektiv Karte der Transportleitung, Rohdungstrassen und Zerrstörungspunkte entlang der Trasse
# Sep 27, 2024

# by Tim Appelhans


# run the command below in your console (or the console of your venv)
# pip install -r requirements.txt

import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point, Polygon, MultiPolygon, MultiLineString
from shapely.ops import split, snap
import json


# ---- Visualization ----

# Create a base map
m = folium.Map(location=[51.0, 6.5], zoom_start=10, min_zoom=8)

# Set up custome map panes for points, lines, polygons
folium.map.CustomPane("pointsPane", z_index=330).add_to(m)
folium.map.CustomPane("linesPane", z_index=320).add_to(m)
folium.map.CustomPane("polygonsPane", z_index=310).add_to(m)


# Add `Esri.WorldImagery` tile layer
# (see [Leaflet Provider Demo](https://leaflet-extras.github.io/leaflet-providers/preview/) for a quick preview of various basemaps).

# add Esri World Imagery tile layer
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


hambacher_see = gpd.read_file("../data/hambachersee.gpkg", layer='fid_2')
# hambacher_see = hambacher_see.set_geometry([Polygon(hambacher_see.get_coordinates())])
hambacher_see_manheim = gpd.read_file("../data/hambachersee_manheim.gpkg", layer='fid_1')
# hambacher_see_kerpen = hambacher_see_kerpen.set_geometry([Polygon(hambacher_see_kerpen.get_coordinates())])
hambacher_see_manheim
# hambacher_see.geometry = hambacher_see.geometry.apply(lambda x: Polygon(x.get_coordinates()))


garzweiler_see = gpd.read_file("../data/garzweilersee_wasser.gpkg", layer='garzweilersee_wasser')
# garzweiler_see = garzweiler_see.set_geometry([Polygon(garzweiler_see.get_coordinates())])
inde_see = gpd.read_file("../data/indersee_gp.gpkg", layer='inder_see_wasser')
inde_see = inde_see.set_geometry([Polygon(inde_see.get_coordinates())])

garzweiler_see



hyperscaler_bergheim = gpd.read_file("../data/hyperscaler-bergheim.gpkg")
hyperscaler_bedburg = gpd.read_file("../data/hyperscaler-bedburg.gpkg")
suendenwaeldchen = gpd.read_file("../data/suendenwaeldchen.gpkg")


folium.GeoJson(
    hambacher_see,
    name="Hambacher See",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#4e4eff',
        'fillColor': "#4e4eff",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Hambacher See"
).add_to(m)

folium.GeoJson(
    hambacher_see_manheim,
    name="Hambacher See (Manheim)",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#9c9cff',
        'fillColor': "#9c9cff",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Hambacher See (Manheim) - geplant.<br>\
        Von Abbaggerung bedrohte Fläche, die nur für Sandgewinnung zerstört<br>\
            werden soll und eine hohe Bedeutung für die Biotopvernetzung hat"
).add_to(m)

folium.GeoJson(
    garzweiler_see,
    name="Garzweiler See",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#4e4eff',
        'fillColor': "#4e4eff",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Garzweiler See"
).add_to(m)

folium.GeoJson(
    inde_see,
    name="Inde See",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#4e4eff',
        'fillColor': "#4e4eff",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Inde See"
).add_to(m)


# load GeoPackage file 'transportleitungen_geom' into geodataframe gdf
pipelines = gpd.read_file("../data/transportleitung_geom.gpkg")

# print to inspect the data
pipelines.Name = ["Transportleitung West", "Transportleitung Süd"]
# pipelines


pipelines = pipelines.to_crs("EPSG:4326")  # change CRS to the same as in 'consumer'
pipelines.crs

pt = pipelines[pipelines.Name == "Transportleitung Süd"].get_coordinates().iloc[0]
pt = Point(pt)

print(pt.coords)

# snap(pt, pipelines.geometry.union_all(), tolerance=1)

jnk = split(pipelines.geometry.union_all(), snap(pt, pipelines.geometry.union_all(), tolerance=1))
jnk
jnk = gpd.GeoDataFrame(geometry=[jnk]).explode(column="geometry", )

pipelines_new = jnk.assign(Name=["Bündelungsleitung", "Garzweilerleitung", "Hambachleitung"])


pipelines_new = gpd.GeoDataFrame(pipelines_new).set_crs("EPSG:4326")

daten_pipelines = pd.read_csv("../data/Daten_Pipelines.csv")
daten_pipelines

pipelines_new = pd.merge(pipelines_new, daten_pipelines, on="Name")
pipelines_new.columns


# Add the GeoDataFrame to the map
folium.GeoJson(
    pipelines_new,
    name="Wasserleitungen",  # again, determine the name for the layer toggle
    pane="linesPane",
    style_function=lambda feature: {
        'color': '#6b6bc9',  # nif feature['properties']['Name'] == 'Bündelungsleitung' else '#3f3f3f',
        'weight': 5  # feature['properties']["Leistung (m3/s)"]
    },
    tooltip=folium.GeoJsonTooltip(fields=['Name'], labels=False),
    popup=folium.GeoJsonPopup(fields=['Name', "Strecke", "Länge (km)", "Leistung (m3/s)", "Trassenbreite (m)", "Anzahl der Röhren"])
).add_to(m)


# load GeoPackage file for clearing
clearing = gpd.read_file("../data/rodungstrasse.gpkg")

# print to inspect the data
clearing


# Add the GeoDataFrame to the map
folium.GeoJson(
    data=clearing,
    name="Rodungstrasse",  # again, determine the name for the layer toggle
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': 'brown',
        'weight': 1,
        'fillColor': 'brown',
        'fillOpacity': 0.3
    }, tooltip="Rodungstrasse"
).add_to(m)


# load GeoPackage file 'transportleitungen_geom' into geodataframe gdf
destruction_data = gpd.read_file("../data/Rheinwassertransportleitung.kml")

# polys = destructions[destructions.geom_type=='Polygon']
points = destruction_data[destruction_data.geom_type == 'Point']

destructions_idx = points['Name'].str.contains('Zerstörung')
destructions = points[destructions_idx]

constructions_idx = ~destructions_idx
constructions = points[constructions_idx]

constructions
# print to inspect the data
# polys
# points


folium.GeoJson(
    destructions,
    name="Zerstörungen",  # again, determine the name for the layer toggle
    pane="pointsPane",
    marker=folium.Marker(
        icon=folium.Icon(color='lightgreen', icon='burst', prefix='fa')
    ),
    tooltip=folium.GeoJsonTooltip(fields=['Name'], labels=False)
).add_to(m)


folium.GeoJson(
    constructions,
    name="Baumaßnahmen",  # again, determine the name for the layer toggle
    pane="pointsPane",
    marker=folium.Marker(
        icon=folium.Icon(color='lightred', icon='person-digging', prefix='fa')
    ),
    tooltip=folium.GeoJsonTooltip(fields=['Name'], labels=False)
).add_to(m)


pumpwerk = gpd.read_file("../data/Pumpbauwerk_Ufer.gpkg")
pumpwerk


verteilwerk = gpd.read_file("../data/Verteilbauwerk.gpkg")
verteilwerk


folium.GeoJson(
    pumpwerk,
    name="Pumpbauwerk",  # again, determine the name for the layer toggle
    pane="linesPane",
    style_function=lambda feature: {
        'color': 'black',
        'weight': 1,
        'fillColor': 'black',
        'fillOpacity': 1
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False)
).add_to(m)


folium.GeoJson(
    verteilwerk,
    name="Verteilbauwerk",  # again, determine the name for the layer toggle
    pane="linesPane",
    style_function=lambda feature: {
        'color': 'black',
        'weight': 1,
        'fillColor': 'black',
        'fillOpacity': 1
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False)
).add_to(m)



folium.GeoJson(
    hyperscaler_bergheim,
    name="Hyperscaler Bergheim",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#c51b8a',
        'fillColor': "#c51b8a",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Hyperscaler Bergheim (hoher Wasserverbrauch)"
).add_to(m)


folium.GeoJson(
    hyperscaler_bedburg,
    name="Hyperscaler Bedburg",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#c51b8a',
        'fillColor': "#c51b8a",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Hyperscaler Bedburg (hoher Wasserverbrauch)"
).add_to(m)


folium.GeoJson(
    suendenwaeldchen,
    name="Sündenwäldchen",
    pane="polygonsPane",
    style_function=lambda feature: {
        'color': '#2ca25f',
        'fillColor': "#2ca25f",
        'fillOpacity': 0.8,
        'fill': True,
        'weight': 0
    },
    tooltip="Bedrohte Waldbesetzung"
).add_to(m)



# Add layer control to toggle layers
folium.LayerControl().add_to(m)
# m
m.show_in_browser()

# save the map as hmtl
m.save('results/pipe_map.html')
