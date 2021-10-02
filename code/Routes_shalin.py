import numpy as np
import pandas as pd
from itertools import combinations as cb
import os


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

    # read in csv

    # convert col to pandas series, where key is storeNames

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
