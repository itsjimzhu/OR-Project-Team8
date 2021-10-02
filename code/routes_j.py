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
	
	N = 7
	df = pd.read_csv("data" + os.sep + "WoolworthsLocations.csv")
	times = pd.read_csv("data" + os.sep + "WoolworthsTravelDurations.csv")
	demands = pd.read_csv("data" + os.sep + "WoolworthsDemands.csv")
	areas = pd.read_csv("data" + os.sep + "WoolworthsLocationsDivisions.csv")

	times1 = times.loc[0:8,:]
	demand1 = demands.iloc[[0,1,2,3,4,5,6,7,8],[1]] 	# Substitute vector of simulated demands later
	df1 = df.loc[0:8,:]

	
	routes = route(df1)
	times, routes = costs(routes,df1,demand1,times1)
	pass
	# TODO
	# Function to calculate time cost for each of the routes generated.


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
		times :     numpy array of time cost of each route, or 999999 if route is infeasible due to demand.

		routes : 	Modified dataframe of routes to reflect new routes
	"""	

	# Initial costs vector, first col is index 
	nroutes = len(routes.columns)
	costs = np.zeros(nroutes-1)

	# Loop through each route for demand constraint.
	for i in range(nroutes-1):

		# get stores on the route, series -> np.array for SettingWithCopyWarning
		storesvec = pd.Series.to_numpy(routes.loc[:,i])
		
		demand = np.dot(storesvec, demands)

		while (demand > 26):

			# remove one store from that route. TODO implement logic, currently remove first alphabetical store.
			for j in range(len(demands)):
				if (storesvec[j] == 1):
					storesvec[j] = 0
					break
			
			demand = np.dot(storesvec, demands)
			
		# Back to series and overwites, avoids SettingWithCopyWarning
		series = pd.Series(storesvec)
		routes[i] = series

	# Loop through each loop for time calculation.
	for i in range(nroutes-1):
		pass
	
	return times, routes
	

def readDemands(col):
	""" Reads in demands from a csv file and return correct set.
			Parameters:
			-----------
			col : int
				used to specify which set of demands (Weekday or Saturday).


			Returns:
			--------
			StoreDemands : Pandas Series
				series of storesNames matched with a demand value.


			Notes:
			------
			The format of the csv is:
									D1, D2

			Store 1                 [10, 11]
			Store 2                 [5, 7]
			Store 3                 [3, 8]
			Store 4                 [6, 9]

	"""
	demands = pd.read_csv("code" + os.sep + "data" + os.sep + "WoolworthsDemands.csv")

	pass

	# return series


def selectRegion(col):
	""" Reads in demands from a csv file and return correct set.
			Parameters:
			-----------
			col : int
				used to specify which region.


			Returns:
			--------
			region : List
				series of storesNames according to a region


			Notes:
			------
			The format of the csv is:
						 R1, R2, R3

			Store 1      [1, 0, 1]
			Store 2      [0, 0, 0]
			Store 3      [1, 0, 1]
			Store 4      [0, 1, 1]
	"""

	# read in csv

	# loop through col
		# if 1
			# append to list

	# return list


def routeGeneration(region, choose):
	""" Generate routes  of {4,3,2,1} according to a specified region.
			Parameters:
			-----------
			region : list
				Stores within this region.

			choose : int
				How many stores per route.


			Returns:
			--------
			Region : 2d list
				series of storesNames according to a region


			Notes:
			------
			I think we should store the generated routes as a list
			which we can then use as a key for the larger dataframe

			[[s1,s2], [s3,s4], [s1,s4], [s4,s5]]
		"""

	# left blank for now
	# josh codes just need to be slightly adapted


def checkDemands(route, demands):
	""" checks demands of a set of routes and removes all greater than limit.
			Parameters:
			-----------
			route : list
				combination of stores.

			demands : int
				Series of storesNames matched with a demand value.


			Returns:
			--------
			flag : boolean
				series of storesNames according to a region

	"""
	# left blank for now
	# josh codes just need to be slightly adapted


def permutateRoute(route):
	""" cost routes unidirectionaly.
			Parameters:
			-----------
			route : list
				combination of storesNames.


			Returns:
			--------
			permutations : 2d Array
				permutations.


			Notes:
			------

	"""
	# should be easy we googled that permutation function


def costRoutes(list):
	""" cost routes unidirectionaly.
			Parameters:
			-----------
			route : list
				combination of stores.


			Returns:
			--------
			cost : int
				final cost of a route


			Notes:
			------
			We don't need an average even though the times are directional
			because simulation will generate values in a range that include both directions times

	"""
	# insert distribution at start
	# append distribution to end

	# read in duration matrix csv
	# convert to data frame with storeName indexing

	# loop from 1 through length of route list
		# get time at [i][i-1]
		# add to cost

	# return cost

def columnnVector(route):
	""" converts a list of routes to a column vector of all stores.
			Parameters:
			-----------
			route : list
				list of stores names.


			Returns:
			--------
			vector : vector
				final cost of a route


			Notes:
			------

		"""
	# create list of all storeNames
	# use list comprehension to create binary array
	# transpose to column vector

if __name__ == "__main__":
	temp = 0
	# call readDemands
	# instantiate lp dataframe

	# for loop through each region
		# storeNames <- call selectRegion

		# loop through choose
			# routes <- call routeGenerations

			# for loop through routes
				# if checkDemands
					# drop this route

				# permutations <- permutateRoutes

				# loop through permutations
					# call costRoutes

				# keep shortest(lowest time) permutation
				# replace routes[i] with permuatation list (this will store the order for us)(remember to remove distribution nodes)

				# vector <- call column Vector(route)
				# append to lp dataframe


	# call lp

	


if __name__ == "__main__":

	readDemands(0)
	pass