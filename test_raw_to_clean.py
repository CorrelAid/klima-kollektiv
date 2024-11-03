# test 1 if contained layers of a geopackage belong to dictionary layers
# test 2 if contained layers geometric type matches expected geometric type by the layer

# %% test 1
import fiona
import numpy as np
import geopandas as gpd
import fiona  # needs to be installed and add to venv


def test_layers(geopackage_path: str):
    '''
    Takes a string of a path to a geopackage and iterates over every layer to check if the name is
    consistent with the in layers_dict predefined layers.
    '''
    layers = fiona.listlayers(geopackage_path)

    layers_dict = np.load("layers_dict.npy", allow_pickle=True).item()

    all_passed = True
    for layer in layers:

        print(f"Processing layer: {layer}")
        if layer in layers_dict.keys():
            continue
        else:
            print(f"Test failed. Layer {\
                layer} is incorrect.\nAdd new layer to default layer dictionary.")

            print(f'Default layer dictionary contains the layers:\n{\
                  list(layers_dict.keys())}')
            return  # exit the function

    if all_passed:
        print("Test passed.")


# test_layers("INSERT PATH T A GEOPACKAGE")


# %% test 2

# future considerations:
# if multistring but shall be a polygon, transform
# think of distinguishing Multi from Single in geometry type and dictionary


def test_layer_geometry(geopackage_path: str):
    '''
    Takes a string of a path to a geopackage and iterates over every layer to check if the 
    geometry type is consistent with the expected one in the layers_dict predefined layers.
    Requires passed test_layers().
    '''
    layers = fiona.listlayers(geopackage_path)
    layers_dict = np.load("layers_dict.npy", allow_pickle=True).item()

    all_passed = True
    for layer in layers:

        print(f"Processing layer: {layer}")
        gdf = gpd.read_file(geopackage_path, layer=layer)
        layer_geometry = gdf.geom_type.unique()
        layer_type = layer  # given the test above was passed.
        # HUHU distinguish between polygon and multipolygon?
        if layers_dict[layer_type]["geometry"] in layer_geometry:
            continue
        else:
            print(f"Test failed. Layer {\
                layer_type} has geometry type: {layer_geometry}.")

            print(f'Layer of type {layer_type} requires a geometry type of {\
                  layers_dict[layers]["geometry"]}.')
            return  # exit the function

    if all_passed:
        print("Test passed.")


# test_layers_geometry("INSERT PATH T A GEOPACKAGE")

# %% First Testing
test_layers("test_data/hambachersee.gpkg")  # as expected
test_layers("test_data/hambach.gpkg")  # as expected

# %% First Testing
test_layer_geometry("test_data/hambachersee.gpkg")  # as expected
test_layer_geometry("test_data/hambach.gpkg")  # as expected, need of a test case with correct layer type but wrong geometric type
