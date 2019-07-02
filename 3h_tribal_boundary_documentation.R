library(rgdal); library(sf); library(sp); library(ggplot2); library(rgeos); library(htmlwidgets); library(shiny)
library(varhandle); library(dplyr); library(leaflet); library(mapview); library(webshot); library(geosphere)
#rm(list=ls())
cat("\014")  
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
#options(error=NULL)
options(error=recover)

# Read shapefiles
tri <- readOGR(dsn = "aiannah shapefiles", layer = "tl_2018_us_aiannh")

# Transform projections
tri <- spTransform(tri, CRS("+init=epsg:4326"))

# Use FIPS codes to mark which polygons are in Indian Country
ind <- subset(tri, CLASSFP == "D1" | CLASSFP == "D2" | CLASSFP == "D3" | CLASSFP == "D0" | CLASSFP == "F1" | CLASSFP == "D5" | CLASSFP == "D8")
ind@data <- tri@data %>% filter(CLASSFP == "D1" | CLASSFP == "D2" | CLASSFP == "D3" | CLASSFP == "D0" | CLASSFP == "F1" | CLASSFP == "D5" | CLASSFP == "D8")
  
# Transform to sf objects
tri_sf <- st_as_sf(tri)
ind_sf <- st_as_sf(ind)

# read in geocoordinates of establisments
est_df <- read.csv("./step_3_work/output/full_retailer_list.csv")  %>% 
  filter(!is.na(Longitude_update)) %>% filter(Longitude_update!=0) %>% filter(IMPAQ_ID>1931)
est_df <- est_df[c('IMPAQ_ID','Longitude_update','Latitude_update','DBA.Name_update')]
dat <- est_df

# overlay with reservation map and return overlapping reservation to csv
coordinates(dat) <- ~ Longitude_update + Latitude_update
proj4string(dat) <- proj4string(ind)
est_df <- cbind(est_df, over(dat, ind))

#write.csv(est_df, file='./output/est_reservations.csv')

# get pics of overlay for documentation

for (i in seq(nrow(dat))) {
#for (i in c(25)) {
  sub_dat <- subset(ind, ind@data$GEOID %in% over(dat[i,], ind)$GEOID)
  print(i)
  if (length(sub_dat@polygons) > 0 ){
    m <- leaflet() %>%
      addPolygons(data=sub_dat,stroke = TRUE,opacity = 0.5,fillOpacity = 0.5, smoothFactor = 0.5,
                  color="blue",weight = 0.5,
                  label=paste('Reservation:',sub_dat@data$NAMELSAD, ' |  Tribe:', sub_dat@data$NAME),
                  labelOptions = labelOptions(noHide=TRUE)) %>%
      addMarkers(lng=coordinates(dat[i,])[1], lat=coordinates(dat[i,])[2], label=paste0(
        'IMPAQ_ID:',dat@data[i,'IMPAQ_ID'],' | DBA Name: ', dat@data[i,'DBA.Name_update']), labelOptions = labelOptions(noHide=TRUE)) %>%
      addTiles()
    mapshot(m, url=paste0("./step_3_work/Tribal Boundary GIS Overlays/", dat@data[i,'IMPAQ_ID'],
                          "_tribe_bound_overlay.html"))
  }
  else {
    nearest <- ind[dist2Line(dat[i,], ind)[,'ID'],]
    #if (min(gDistance(dat[i,], ind , byid=TRUE)) < 1) {
      m <- leaflet() %>%
        addMarkers(lng=coordinates(dat[i,])[1], lat=coordinates(dat[i,])[2], label=paste0(
          'IMPAQ_ID:',dat@data[i,'IMPAQ_ID'],' | DBA Name: ', dat@data[i,'DBA.Name_update']), labelOptions = labelOptions(noHide=TRUE)) %>%
        addTiles() %>%
        addPolygons(data=nearest,stroke = TRUE,opacity = 0.5,fillOpacity = 0.5, smoothFactor = 0.5,
                    color="blue",weight = 0.5,
                    label=paste('Nearest Reservation:',nearest@data$NAMELSAD, ' |  Tribe:', nearest@data$NAME),
                    labelOptions = labelOptions(noHide=TRUE)) 
      mapshot(m, url=paste0("./step_3_work/Tribal Boundary GIS Overlays/", dat@data[i,'IMPAQ_ID'],
                            "_tribe_bound_overlay.html"))
    # }
    # else {
    #   m <- leaflet() %>%
    #     addMarkers(lng=coordinates(dat[i,])[1], lat=coordinates(dat[i,])[2], label=dat@data[i,'IMPAQ_ID'], labelOptions = labelOptions(noHide=TRUE)) %>%
    #     addTiles()
    #   mapshot(m, url=paste0("./output/Tribal Boundary GIS Overlays/", dat@data[i,'IMPAQ_ID'],
    #                         "_tribe_bound_overlay.html"))
    # }
  }
}


