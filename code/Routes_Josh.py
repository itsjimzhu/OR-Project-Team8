import numpy as np
from numpy.core.numeric import NaN
from matplotlib import pyplot as plt
from numpy.lib.function_base import interp
from scipy.interpolate import interp1d
import itertools
from math import comb
from itertools import combinations
import pandas as pd
import os

def route(df, k):
	""" generates matrix of potential length three routes
	
		Parameters
		----------
		df : Pandas dataframe
			Should contain read_csv data from Locations file of ten stores (changeable)
        k : integer
                choose n choose k (where n is the number of stores)
			
		Returns
		-------
		stores :    Pandas dataframe
			First col cis index of store names, remaining columns are possible combinations of stores

	"""
	

	# Creating a pandas dataframe of possible length k routes in a region of n stores.
	# The dataframe should have N rows and nC3 (+1) columns
	# Column of store names and idx
	stores = df[['Store']]

	# Columns for combos of three stores.
	n = len(stores)

	routes = np.array(
		[
			[1 if i in comb else 0 for i in range(n)]
			for comb in combinations(np.arange(n), k)
		]
	)
	for j in range(k-1,0,-1):
		routesJ = np.array([
			[1 if i in comb else 0 for i in range(n)]
			for comb in combinations(np.arange(n), j)])
		routes = np.concatenate((routes,routesJ),axis=0)
 
	# Loop through each route and add as a column to the stores df
	for i in range(len(routes)):
		copy = routes[i,:].T
		stores.insert(len(stores.columns),"Route " + str(i),copy)

	return stores

def CheckDemands(Routes, Demands):
	''' calculates demand for each route. If a route is infeasable, the route is removed 
	
	Parameters
	----------
	
		'''
	for Route in Routes:
		if Route != 'Store':
			if Routes[Route].dot(Demands) > 26:
				Routes.drop(Route, inplace= True, axis = 1)

	return Routes
	

if __name__ == "__main__":
	N = 7
	df = pd.read_csv("data" + os.sep + "WoolworthsLocations.csv")
	times = pd.read_csv("data" + os.sep + "WoolworthsTravelDurations.csv")
	demands = pd.read_csv("data" + os.sep + "WoolworthsDemands.csv")
	areas = pd.read_csv("data" + os.sep + "WoolworthsLocationsDivisions.csv")

	AreaSouth = areas[areas["Area"]=="South"]
	# Need to develop some sort of an average function later
	DemandSouth = demands[areas["Area"]=="South"]["6/14/2021"]
	
	RoutesSouth = route(AreaSouth, 4)
	NewRoutesSouth = CheckDemands(RoutesSouth, DemandSouth)

	times.rename(columns={'Unnamed: 0':'Store'}, inplace=True)
	AreaSouthDepo = AreaSouth.append(areas.loc[areas["Type"]=='Distribution Centre'])
	mergedTimes = pd.merge(AreaSouthDepo, times, how = 'inner', on = 'Store')
	SouthTimes = mergedTimes[AreaSouthDepo["Store"]]
	print('yes')
    