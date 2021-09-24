import numpy as np
from numpy.core.numeric import NaN
from matplotlib import pyplot as plt
from numpy.lib.function_base import interp
from scipy.interpolate import interp1d
import itertools
from math import comb
from itertools import combinations
import pandas as pd

def main():


    pass

def route(df):
    """ generates matrix of potential length three routes
	
		Parameters
		----------
		df :    Pandas dataframe
            Should contain read_csv data from Locations file of ten stores (changeable)
			
		Returns
        stores :    Pandas dataframe
            First col cis index of store names, remaining columns are possible combinations of stores
		-------
		None
	"""
    

    # Creating a pandas dataframe of possible length 3 routes in a region of N stores.
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

def costs(routes):

    pass

if __name__ == "__main__":
    N = 10
    df = pd.read_csv("WoolworthsLocations.csv")
    df1 = df.loc[0:8,:]
    routes = route(df1)
    pass
    # TODO
    # Function to calculate time cost for each of the routes generated.
    