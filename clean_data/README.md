final cleaned data version from raw data. 
used to create maps or other results for client.

# requirements for cleaned data:
* file format is a geopackage. -> test (Paula)
* contained layers are part of a predefined dictionary of layers (.e.g "see") -> test, new dictionary (Desiree)
    * new dictionary "layers": name {see, acker, line, ..., pipeline, bauwerk, points}, # english layer names!
                           pane: {Polygon, Polygon, Polygon, ...,  MultiLineString, Polygon, Points},
                           colour:{blau, gelb, dunkelblau,..., graublau, schwarz, rot}
    * layers in existing gepoackages must be renamed (Paula, Desiree) 
  * if test fails : name of layers must be adapted or new layer to dictionary and adpation of related steps (Desiree)
* files need to be checked for crs format: crs EPSG:4326 (for region NRW) -> test; new dictionary (Paula)
* layer "type" must be "Polygon" or "Multipolygon" if layer name = etc. -> test  (Paula) if not: error and need for transformation, execute transformation from linestring to polygon (check the geometric type: (Multi)Polygon, (Multi)LineString, Points) (Desiree)
* steps from clean_data to product (Malte)


   * Desiree: dictionary creation, test if geropackage layers have layers on dictionaries, renaming rest
   * Paula: dictionary crs_region, test if file has crs format, test if file is a geopackage, renaming lakes
   * Malte: automatic read in of all files in clean folder, steps for map creation (test clean_data before map creation)

# assumptions for cleaned data:
* single geopackages in the folder clean_data
* geopacke contains layers
