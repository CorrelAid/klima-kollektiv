# translate any MultiLineString layer to a Polygon
# requires closed shape
# requires nested lists in features key

import pandas as pd
import geopandas as gpd
import json
import fiona
from shapely.geometry import shape

# old geopackage consisting of multiple layers, each a MultiLineString type
# %% single shapes
# works only for single shapes
layers = fiona.listlayers("raw_data/hambachersee_gp.gpkg")

for layer in layers:

    print(f'\nProcessing layer: {layer}')

    print(f'Layers:\n{layers}')
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
        # print(gdf.head())

        print(f'New geometric type of layer {\
              layer}: {gdf.geom_type.unique()}.')

        gdf.to_file("temp_data/hambachersee_gp.gpkg",
                    layer=layer)
# further steps:
# save layer to geopackage back
# adjust function for MultiPolygon cases

# %% read in and check again

layers = fiona.listlayers("temp_data/hambachersee_gp.gpkg")

# should work for Single Polygon cases
for layer in layers:

    print(f'\nProcessing layer: {layer}')
    gdf = gpd.read_file("temp_data/hambachersee_gp.gpkg",
                        layer=layer)
    print(f'geometry type:\n{gdf.geom_type}')

# %% for multiple shapes

print(f'\n**Number of layers: {len(layers)}**')
print(f'\nLayers: {layers}')

for layer in layers:
   
    print(f'\n***Processing layer: {layer}***')
    gdf = gpd.read_file("raw_data/hambachersee_gp.gpkg",
                        layer=layer)
    
    print(f'\nNumber of shapes:{gdf.shape[0]}')
    print(f'\nGeometry type:\n{gdf.geom_type}')


    updated_shapes = []

    for i in range(gdf.shape[0]):
        print(f'\nShape {i+1} processed:')
        if gdf.geom_type[0] == "MultiPolygon":
            print("Done.")
            updated_shapes.append(gdf.iloc[i:i+1])

        else:
            layer_json = (gdf.iloc[i:i+1]).to_json()

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
            new_gdf = gpd.GeoDataFrame.from_features(layer_dic['features'])

        # Add the updated GeoDataFrame to the list
        updated_shapes.append(new_gdf)

    # Concatenate all updated shapes into a single GeoDataFrame
    print(f'\nCreate new layer gdf.')
    new_gdf = gpd.GeoDataFrame(pd.concat(updated_shapes, ignore_index=True))

    print(f'\nNew geometry type of layer {layer}: {new_gdf.geom_type.unique()}.')
    print(f'\nSave updated layer in geopackage.')
    new_gdf.to_file("temp_data/hambachersee_gp.gpkg",
                    layer=layer)


# %% test
layers = fiona.listlayers("temp_data/hambachersee_gp.gpkg")

# should work for also for multiple polygones
for layer in layers:

    print(f'\nTesting layer: {layer}')
    gdf = gpd.read_file("temp_data/hambachersee_gp.gpkg",
                        layer=layer)
    print(f'geometry type:\n{gdf.geom_type}')