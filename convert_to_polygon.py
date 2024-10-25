
# translate any MultiLineString layer to a Polygon (so far considering MultiPolygon consists of one shape)
# requires closed shape
# requires nested lists in features key

import pandas as pd
import geopandas as gpd
import json
import fiona
from shapely.geometry import shape


# old geopackage consisting of multiple layers, each a MultiLineString type
layers = fiona.listlayers("raw_data/hambachersee_gp.gpkg")

for layer in layers:

    print(f'\nProcessing layer: {layer}')
    gdf = gpd.read_file("raw_data/hambachersee_gp.gpkg",
                        layer=layer)
    print(f'geometry type: {gdf.geom_type.unique()}')

    if gdf.geom_type.unique() == "MultiPolygon":
        print("done")

    else:
        layer_json = gpd.GeoDataFrame.to_json(gdf)

        # convert JSON formatted string into a Python dictionary
        layer_dic = json.loads(layer_json)
        coordinates = layer_dic['features'][0]["geometry"]["coordinates"]
        # print(f'Coordinates:{coordinates}')

        # check if first and last coordinates are the same
        # condition needs to be checked only once because appending
        #  at the most once always ensures if condition
        if coordinates[0][0] == coordinates[0][-1]:
            print("Closed shape already.")
        else:
            coordinates[0].append(coordinates[0][0])
            print("Shape was closed.")

        # replace old coordinates with new
        # MultiPolygon requires nested list structure for every Polygon
        layer_dic['features'][0]["geometry"]["coordinates"] = [coordinates]

        # change geometry type
        layer_dic['features'][0]["geometry"]["type"] = "MultiPolygon"
        print('Conversion done.')

        # check conversion of dic to json and back
        layer_json = json.dumps(layer_dic)
        layer_dic = json.loads(layer_json)

        # convert back to a gdf
        gdf = gpd.GeoDataFrame.from_features(layer_dic['features'])
        #print(gdf.head())

        print(f'New geometric type of layer {layer}: {gdf.geom_type.unique()}.')

        gdf.to_file("temp_data/hambachersee_gp.gpkg",
                        layer=layer)
# further steps:
# save layer to geopackage back
# adjust function for MultiPolygon cases

#%% read in and check again

layers = fiona.listlayers("temp_data/hambachersee_gp.gpkg")

# should work for Single Polygon cases
for layer in layers:

    print(f'\nProcessing layer: {layer}')
    gdf = gpd.read_file("temp_data/hambachersee_gp.gpkg",
                        layer=layer)
    print(f'geometry type: {gdf.geom_type.unique()}')
