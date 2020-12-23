from google.transit import gtfs_realtime_pb2 # https://developers.google.com/transit/gtfs-realtime/examples/python-sample
import requests
import os

rootdir = os.getcwd()

geojson = {"type" : "FeatureCollection", "features" : []}
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('http://webapps.regionofwaterloo.ca/api/grt-routes/api/vehiclepositions')
feed.ParseFromString(response.content)

for entity in feed.entity:
  feature = {"type" : "Feature",
                 "properties" : {
                   "route": int(entity.vehicle.trip.route_id)
                   },
                 "geometry" : {
                   "type" : "Point",
                   "coordinates" : [entity.vehicle.position.longitude, entity.vehicle.position.latitude]
                   }
                 }
  geojson["features"].append(feature)

geojson = "var myGeoJSON = " + str(geojson)

with open(rootdir + "/data/" + "Data.geojson", "w") as f:
  f.write(str(geojson).replace("\'","\""))



