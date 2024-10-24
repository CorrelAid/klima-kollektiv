# create dictionaries for any further data preprocessing step and save them
# content based on assumptions and the code pipe_map.py
# color key can be treated as the default value in any function in create_product.py


# HUHU: instead of single layers for lake areas only one? only differ in color

import numpy as np


layers = {"lake":
            {
                "geometry": "polygon",
                "pane": "polygonesPane",
                "color": "blue",
                "map_style": {  # default styling setting for style_function parameter
                    'color': "blue",
                    'fillColor': "blue",
                    'fillOpacity': 0.8,
                    'fill': True,
                    'weight': 0
                }
            },
            "line":
            {
                "geometry": "polygon",
                "pane": "polygonesPane",
                "color": "darkblue",
                "map_style":  {  # default styling setting for style_function parameter
                    'color': "darkblue",
                    'fillColor': "darkblue",
                    'fillOpacity': 0.8,
                    'fill': True,
                    'weight': 0
                }
            },
            "field":  # future use of further legend areas from the lakes
            {
                "geometry": "polygon",
                "pane": "polygonesPane",
                "color": "yellow",
                "map_style": {  # default styling setting for style_function parameter
                    'color': "yellow",
                    'fillColor': "yellow",
                    'fillOpacity': 0.8,
                    'fill': True,
                    'weight': 0
                }
            },
            "grass":  # future use of further legend areas from the lakes
            {
                "geometry": "polygon",
                "pane": "polygonesPane",
                "color": "green",
                "map_style":  {  # default styling setting for style_function parameter
                    'color': "green",
                    'fillColor': "green",
                    'fillOpacity': 0.8,
                    'fill': True,
                    'weight': 0
                }
            },
            "pipeline":
            {
                "geometry": "lineString",
                "pane": "linesPane",
                "color": "red",
                "map_style": {
                    'color': '#6b6bc9',
                    'weight': 5
                }
            },
            "building":  # verteilbauwerk + pumpbauwerk. HUHU: why type of polygon but put to pane "linesPane"?
            {
                "geometry": "lineString",
                "pane": "linesPane",
                "color": "black",
                "map_style":  {
                    'color': 'black',
                    'weight': 1,
                    'fillColor': 'black',
                    'fillOpacity': 1
                }
            },
            "coordinates":  # contained in the file Rheinwassertransportleitung.kml
            {
                "geometry": "points",
                "pane": "pointsPane",
                "color": "black"
            }
            }


np.save("layers_dict", layers)

