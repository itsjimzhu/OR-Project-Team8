import numpy as np
import pandas as pd
import itertools as it
from pulp import *
import os
import time
from generate_demands import *
import folium
import openrouteservice as ors

PATHFILE = True
#set your key here
myKey = '5b3ce3597851110001cf62488446fbb2ccc14d6695a1cb348f0a6edd'

def visualise(route, routeName, day):
    ''' This function takes a route and visualises it on a map'''
    
    client = ors.Client(key = myKey)
    m = folium.Map(location = [-36.95770671222872, 174.81407132219618], zoom_start=15)

    coords = pd.read_csv("code" + os.sep + "data" + os.sep + "WoolworthsLocations.csv", index_col=2)

    dist_routes = ('Distribution Centre Auckland',) + route + ('Distribution Centre Auckland',)
    coords_list = []
    for store in dist_routes:
        coords_list.append([coords.loc[store,'Long'], coords.loc[store,'Lat']])
    route_directions = client.directions(coordinates = coords_list, profile='driving-hgv', \
        format = 'geojson', validate = False)
    folium.PolyLine(locations=[list(reversed(coord))for coord in route_directions['features'][0]['geometry']['coordinates']]).add_to(m)
    
    for store in dist_routes:
        if coords.loc[store,'Type'] == 'Countdown':
            iconCol = "green"
        elif coords.loc[store,'Type'] == 'FreshChoice':
            iconCol = "red"
        elif coords.loc[store,'Type'] == 'SuperValue':
            iconCol = "blue"
        elif coords.loc[store,'Type'] == 'Countdown Metro':
            iconCol = "orange"
        elif coords.loc[store,'Type'] == 'Distribution Centre':
            iconCol = "black"
        folium.Marker([coords.loc[store,'Lat'],coords.loc[store,'Long']], popup = coords.loc[store].name,\
            icon = folium.Icon(color = iconCol)).add_to(m)
    if PATHFILE:
        savename = "code" + os.sep + "RouteMaps" + os.sep + day + os.sep + routeName + '.html'
    else:
        savename = "RouteMaps" + os.sep + day + os.sep + routeName + '.html'
    m.save(savename)

def visual_all_routes(bestRoutes, day):
    """This function takes a list of routes and generates maps of those routes, saving them to 'day' folder
    
        Parameters:
            -----------
            bestRoutes: List
                list of routes (as list of locations)
            day: str
                'Week' or 'Saturday'
                the type of day that we are running the program for
    """
    for i in range(0,len(bestRoutes)):
        visualise(bestRoutes[i], 'Route_'+str(i+1), day)

if __name__ == "__main__":
    visualise(('Countdown Grey Lynn', 'Countdown Grey Lynn Central'),'Route_1', 'Week')



