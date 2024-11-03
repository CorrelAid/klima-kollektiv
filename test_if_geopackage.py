import geopandas as gpd
import fiona


def test_if_file_is_geopackage(file_path: str):
    if file_path.endswith(".gpkg"):
        print("File seems to be a geopackage. Checking if the file can be read...")
        try:
            # List layers to check if the file is accessible
            layers = fiona.listlayers(file_path)
            print(f"Layers found: {layers}")
            
            # Attempt to read each layer to verify integrity
            for layer in layers:
                print(f"Testing layer '{layer}'...")
                gpd.read_file(file_path, layer=layer)
            
            return f"{file_path}: Test passed. File is a geopackage with layers: {layers}."
        
        except Exception as e:
            return f"An error occurred while reading the geopackage: {e}"
    
    else:
        return f"{file_path}: File is not a geopackage."
