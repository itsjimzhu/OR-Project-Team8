import numpy as np
import pandas as pd
import itertools as it
from pulp import *
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

    return pd.read_csv("data" +os.sep +"DemandEstimation.csv")[:][col]



def selectRegion(region):
    """ Reads in demands from a csv file and return correct set.
            Parameters:
            -----------
            col : int
                used to specify which region.


            Returns:
            --------
            regionNames : List
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

    areas = pd.read_csv("data" + os.sep + "WoolworthsLocationsDivisions.csv")

    return areas[areas["Area"]==region]


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

    stores = region

    # Columns for combos of three stores.
    n = len(stores)

    routes = np.array(
        [
            [1 if i in comb else 0 for i in range(n)]
            for comb in it.combinations(np.arange(n), choose)
        ]
    )
    for j in range(choose - 1, 0, -1):
        routesJ = np.array([
            [1 if i in comb else 0 for i in range(n)]
            for comb in it.combinations(np.arange(n), j)])
        routes = np.concatenate((routes, routesJ), axis=0)

    # Loop through each route and add as a column to the stores df
    for i in range(len(routes)):
        copy = routes[i, :].T
        stores.insert(len(stores.columns), "Route " + str(i), copy)

    return stores


def checkDemands(routes, demands):
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
    for route in routes:
        if route != 'Store':
            if routes[route].dot(demands) > 26:
                routes.drop(route, inplace=True, axis=1)

    return routes


def routeNames():
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
    return it.Permutations(route)


def costRoutes(route):
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
    route.insert(0, "Distribution Centre Auckland")
    route.append("Distribution Centre Auckland")

    # read in data frame with storeName indexing
    time = pd.read_csv("code" +os.sep +"data" +os.sep +"WoolworthsTravelDurations.csv")


    cost = 0

    # loop from 1 through length of route list
    for location in route:
        cost += time[location][location-1]

    return cost


def lp(dataFrame):
    """ interplate two extraction rates to find the total extraction rate, q.
            Parameters:
            -----------
            dataFrame : pandas dataFrame
                Independent variable.

            Returns:
            --------


            Notes:
            ------
            The dataFrame format is:
                                    R1,R2,R3,R4,R5

            Store 1                 [1, 1, 1, 0, 1]
            Store 2                 [0, 0, 1, 1, 0]
            Store 3                 [1, 0, 0, 1, 1]
            Store 4                 [0, 1, 1, 0, 1]
            Time per Route          [100, 36, 57, 69]
    """

    prob = LpProblem("Time", LpMinimize)
    vars = LpVariable.dicts("Route", dataFrame.columns, 0, None, 'Integer')
    prob += lpSum([vars[i] * dataFrame[i][time] for i in dataFrame.columns]), "Time"

    # route constraints
    for i in dataFrame.index[:-2]:
        prob += lpSum([vars[j] * dataFrame[j][i] for j in dataFrame.columns]) == 1

    # truck constraint
    prob += lpSum([vars[i] for i in dataFrame.columns]) <= 60

    # The problem data is written to an .lp file
    prob.writeLP("VehicleRoutingProblem. lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        print(v.name, "-", v.varValue)

    # The optimised objective function value is printed to the screen
    print("Production Costs = ", value(prob.objective))


if __name__ == "__main__":

    #read in demands
    demands = readDemands(0)
    demands = 0;

    # instantiate lp dataframe

    # loop through each region
    regions = ["North", "City", "East", "South", "West", "NorthWest"]
    for i in regions:
        storeNames = selectRegion(i)

        routes = routeGeneration(storeNames, 4)
        routes = checkDemands(routes, demands)

        # convert routes to routeNames

        # loop through routes
        for r in range(routeNames):
            permutations = permutateRoute(r)

            cost = 9999999999
            order = []
            #loop through permutations
            for p in range(p):
                if(costRoutes(p) < p):
                    cost = costRoutes
                    order = p

            # add new cost row to route for this route

        # append to lp dataframe


    # call lp
