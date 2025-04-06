library(leaflet)
library(sf)
library(lwgeom) # for st_split
library(fontawesome)

data_path = "data" # as we assume we are at the project level

# add data layers
# 1. read data
# 1.1. pipelines
pipelines = st_read(file.path(data_path, "transportleitung_geom.gpkg"))
pipelines = st_transform(pipelines, crs = "EPSG:4326")

split_point = st_coordinates(pipelines[2, ])[1, c("X", "Y")] |>
  st_point() |>
  st_sfc(crs = st_crs(pipelines))

pipelines = st_split(pipelines, split_point) |>
  st_collection_extract("LINESTRING")

pipelines$id = NULL
pipelines$Name = c("Bündelungsleitung", "Garzweilerleitung", "Hambachleitung")
rownames(pipelines) = 1:3

daten_pipelines = read.csv(file.path(data_path, "Daten_Pipelines.csv"))
daten_pipelines = setNames(
  daten_pipelines
  , c(
    "Name"
    , "Strecke"
    , "Länge [km]"
    , "Leistung [m3/s]"
    , "Trassenbreite [m]"
    , "Anzahl Röhren"
  )
)

pipelines_new = merge(pipelines, daten_pipelines)

# 1.2. Trasse
clearing = st_read(file.path(data_path, "rodungstrasse.gpkg"))

# 1.3 destruction points
destruction_data = st_read(file.path(data_path, "Rheinwassertransportleitung.kml"))

points = st_collection_extract(destruction_data, 'POINT') |>
  st_zm()

destructions_idx = grep("Zerstörung", points[['Name']])
destructions = points[destructions_idx, ]

constructions = points[-destructions_idx, ]

# 1.4. Pump- u. Verteilerwerk
pumpwerk = st_read(file.path(data_path, "Pumpbauwerk_Ufer.gpkg"))
verteilwerk = st_read(file.path(data_path, "Verteilbauwerk.gpkg"))

# 1.5. Seen
hambacher_see = st_read(file.path(data_path, "hambachersee.gpkg"), layer='fid_2')
hambacher_see_manheim = st_read(file.path(data_path, "hambachersee_manheim.gpkg"), layer='fid_1')
garzweiler_see = st_read(file.path(data_path, "garzweilersee_wasser.gpkg"), layer='garzweilersee_wasser')
inde_see = st_read(file.path(data_path, "indersee_gp.gpkg"), layer='inder_see_wasser')
inde_see = st_cast(inde_see, "POLYGON")

# 1.6. Hyperscaler
hyperscaler_bergheim = st_read(file.path(data_path, "hyperscaler-bergheim.gpkg"))
hyperscaler_bedburg = st_read(file.path(data_path, "hyperscaler-bedburg.gpkg"))
suendenwaeldchen = st_read(file.path(data_path, "suendenwaeldchen.gpkg"))

# 2. add data to map
# 2.1 setup map
# max bounds
max_bounds = list(
  c(47.5, 0.5)
  , c(55, 20)
)

# base map setup
map = leaflet(
  elementId = "kkv-pipe-map"
  , options = leafletOptions(
    minZoom = 6
    , maxZoom = 18
    , maxBounds = max_bounds
  )
) |>
  addTiles(group = "OpenStreetMap") |>
  addProviderTiles("CartoDB.Positron", group = "CartoLight") |>
  addProviderTiles("Esri.WorldImagery", group = "Satellite") |>
  addMapPane("pointsPane", zIndex = 330) |>
  addMapPane("bauwerksPane", zIndex = 325) |>
  addMapPane("linesPane", zIndex = 320) |>
  addMapPane("polygonsPane", zIndex = 310) 

# 2.1. polygon data
# seen
seen = list(
  "Hambacher See" = hambacher_see
  , "Hambacher See (Manheim)" = hambacher_see_manheim
  , "Garzweiler See" = garzweiler_see
  , "Inde See" = inde_see
)

for (i in seq(seen)) {
  map = addPolygons(
    map
    , data = seen[[i]]
    , group = names(seen)[i]
    , fillColor = ifelse(
      names(seen)[i] == "Hambacher See (Manheim)"
      , "#9c9cff"
      , "#4e4eff"
    )
    , fillOpacity = 0.8
    , fill = TRUE
    , weight = 0
    , label = names(seen)[i]
    , options = pathOptions(pane = "polygonsPane")
  )
}

# rodungstrasse
map = addPolygons(
  map
  , data = clearing
  , group = "Rodungstrasse"
  , color = 'brown'
  , weight = 1
  , fillColor = 'brown'
  , fillOpacity = 0.3
  , label = "Rodungstrasse"
  , options = pathOptions(pane = "polygonsPane")
)

# bauwerke
bauwerke = list(
  "Pumpwerk" = pumpwerk
  , "Verteilbauwerk" = verteilwerk
  , "Hyperscaler Bergheim" = hyperscaler_bergheim
  , "Hyperscaler Bedburg" = hyperscaler_bedburg
)

for (i in seq(bauwerke)) {
  map = addPolygons(
    map
    , data = bauwerke[[i]]
    , group = names(bauwerke)[i]
    , color = "#000000"
    , fillColor = "#202530"
    , fillOpacity = 0.9
    , fill = TRUE
    , weight = 2
    , label = names(bauwerke)[i]
    , options = pathOptions(pane = "bauwerksPane")
  )
}

map = addPolygons(
  map
  , data = suendenwaeldchen
  , group = "Sündenwäldchen"
  , fillColor = "#009000"
  , fillOpacity = 0.5
  , fill = TRUE
  , weight = 0
  , label = "Bedrohte Waldbesetzung"
  , options = pathOptions(pane = "bauwerksPane")
)

# 2.2. line data
# pipelines
map = addPolylines(
  map
  , data = pipelines_new
  , group = "Wasserleitungen"
  , color = "#6b6bc9"
  , opacity = 0.9
  , weight = 5
  , label = ~Name
  , popup = leafpop::popupTable(
    pipelines_new
    , zcol = names(pipelines_new)[-ncol(pipelines_new)]
    , row.numbers = FALSE
    , feature.id = FALSE
  )
  , options = pathOptions(pane = "linesPane")
)

# 2.3. point data
# destructions
map = addAwesomeMarkers(
  map
  , data = destructions
  , group = "Zerstörungen"
  , icon = awesomeIcons(
    icon = fa(name = "burst")
    , library = "fa"
    , markerColor = "lightgreen"
    , iconColor = "#ffffff"
  )
  , label = ~Name
)

# constructions
map = addAwesomeMarkers(
  map
  , data = constructions
  , group = "Baumaßnahmen"
  , icon = awesomeIcons(
    icon = fa(name = "person-digging")
    , library = "fa"
    , markerColor = "lightred"
    , iconColor = "#ffffff"
  )
  , label = ~Name
)


map = map |>
  addLayersControl(
    baseGroups = c("Satellite", "OpenStreetMap", "CartoLight")
    , overlayGroups = c(
      names(seen)
      , "Rodungstrasse"
      , names(bauwerke)
      , "Sündenwäldchen"
      , "Wasserleitungen"
      , "Zerstörungen"
      , "Baumaßnahmen"
    )
  )

saveRDS(map, "closeread/r_scrolly_map/map.rds")
