import geopandas as gpd
import os 

def convert_to_uniform_crs(file_path: str):
    """
    Converts the Coordinate Reference System (CRS) of a GeoPackage file to a uniform CRS with EPSG code 4326 (WGS84).
    
    Parameters:
    - file_path (str): The path to the input GeoPackage file, which should contain a valid CRS.
    
    Returns:
    - A GeoDataFrame with the converted CRS.
    """
    try:
        # Load the GeoPackage file
        gdf = gpd.read_file(file_path)
        
        # Check if the CRS is already EPSG:4326
        if gdf.crs.to_epsg() == 4326:
            print("The CRS is already EPSG:4326.")
        
        # Convert to EPSG:4326
        gdf = gdf.to_crs(epsg=4326)
        print("The CRS was successfully converted to EPSG:4326.")
        
        # Save the converted file as a new GeoPackage file
        output_path = f'../temp_data/{os.path.basename(file_path)}'
        gdf.to_file(output_path, driver="GPKG")
        print(f"The file was saved as {output_path}.")
        
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
