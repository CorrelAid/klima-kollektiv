# test if contained layers of a geopackage belong to dictionary layers
# test if contained layers geometric type matches expected geometric type by the layer

# %%
import numpy as np
import geopandas as gpd
import json
import fiona  # needs to be installed and add to venv



def test_layers(geopackage_path: str):
    '''Takes a string of a path to a geopackage and iterates over every layer to check if the name is consistent with
    the in layers_dict predefined layers.
    '''
    layers = fiona.listlayers(geopackage_path)

    layers_dict = np.load("layers_dict.npy", allow_pickle=True).item()

    all_passed = True
    for layer in layers:
            print(f"Processing layer: {layer}")
            gdf = gpd.read_file(geopackage_path, layer=layer)
            if layer in layers_dict.keys():
                continue
            else:
                print(f"Test failed. Layer {\
                    layer} is incorrect.\nAdd new layer to default layer dictionary.")
                
                print(f'Default layer dictionary contains the layers:\n{list(layers_dict.keys())}')
                return #exit the function

    if all_passed:
            print("Test passed.")


# test_layers("INSERT PATH T A GEOPACKAGE")
