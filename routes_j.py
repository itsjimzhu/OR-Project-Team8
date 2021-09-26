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

def main():


	pass

def route(df):
	""" generates matrix of potential length three routes
	
		Parameters
		----------
		df :    Pandas dataframe
			Should contain read_csv data from Locations file of ten stores (changeable)
			
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
	n = 9
	k = 4
	routes = np.array(
		[
			[1 if i in comb else 0 for i in range(n)]
			for comb in combinations(np.arange(n), k)
		]
	)
 
	# Loop through each route and add as a column to the stores df
	for i in range(len(routes)):
		copy = routes[i,:].T
		stores.insert(1,i,copy)

	return stores

def costs(routes,locations, demands, times):
	""" calculates optimal time cost of each route and returns vector of best time
		If a route is infeasable, the store with the lowest travel time is removed from the route
	
		Parameters
		----------
		routes :     Dataframe from routes function

		locations :     Dataframe of the locations of interest.

		demands : 	Vector of demands at those locations

		times : 	transit times matrix
			
		Returns
		-------
		times :     Dataframe of time cost of each route, or 999999 if route is infeasible due to demand.

		routes : 	Modified dataframe of routes
	"""	

	# Initial costs vector, first col is index 
	nroutes = len(routes.columns)
	costs = np.zeros(nroutes-1)

	# Loop through each route for demand constraint.
	for i in range(nroutes):

		pass

	
	return times, routes
	

	


if __name__ == "__main__":

	N = 7
	df = pd.read_csv("data" + os.sep + "WoolworthsLocations.csv")
	times = pd.read_csv("data" + os.sep + "WoolworthsTravelDurations.csv")
	demands = pd.read_csv("data" + os.sep + "WoolworthsDemands.csv")

	times1 = times.loc[0:8,:]
	demand1 = demands.iloc[[0,1,2,3,4,5,6,7,8],[1]] 	# Substitute vector of simulated demands later
	df1 = df.loc[0:8,:]

	
	routes = route(df1)
	times, routes = costs(routes,df1,demand1,times1)
	pass
	# TODO
	# Function to calculate time cost for each of the routes generated.
	