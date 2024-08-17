# CorrelAid for Klima*Kollektiv
# Aug 17, 2024
# by Nicolas Fröhlich, partly based on Florian Detsch and ChatGPT

# install.packages("mapview")
library(sf)
library(mapview)

# ---- Scrape consumers and identify large ones ----

## read geojson of Wasserverbraucher (only run once, please)
consumer_all = sf::read_sf(
  "https://www.klaerwerk-krefeld.org/wasserbuch/utm.php"
)

# save locally as GeoJSON
st_write(consumer_all, "consumer_all.geojson", driver = "GeoJSON")


## create interactive map
mapview::mapview(consumer_all)
consumer_all$size <- as.numeric(consumer_all$size) # set size to data type numeric

## identify large consumers (more than 1 mio m3/a of water granted)
consumer <- consumer_all[
  consumer_all$size > 1000000
  ,
]

mapview::mapview(consumer)

# ---- Spatial subset with bounding box ----

# define coordinates of the rectangle [Köln, Mettmann, Roermond, Aachen]
# using https://boundingbox.klokantech.com/
coords <- matrix(
  c(5.9512135386, 50.7489864309,
    7.0077544451, 50.7489864309,
    7.0077544451, 51.2670019108,
    5.9512135386, 51.2670019108,
    5.9512135386, 50.7489864309), # Close the polygon by repeating the first point
  ncol = 2, byrow = TRUE
)

# Create a polygon from the coordinates
polygon <- st_polygon(list(coords))

# Create a simple features collection object with the polygon and set the CRS to that of the consumer
polygon_sfc <- st_sfc(polygon, crs = st_crs(consumer))

# Find the points that intersect with the polygon
intersects <- st_intersects(consumer, polygon_sfc)

# Convert the list output of st_intersects to a vector of row indices
rows <- sapply(intersects, function(x) any(x))

# Subset consumer to include only points within the rectangle using the row indices
consumer_within <- consumer[rows, ]


# ---- Visualization ----


# display consumer points on the map
map <- mapview(consumer_within, layer.name = "Water consumers > 1 mio m3/a")

# add bounding box polygon with red border
map <- map + mapview(st_as_sf(polygon_sfc), col.regions = "#ffffff00", color = "red", lwd = 2, layer.name = "Bounding Box")

print(map)
