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

    demands = pd.read_csv("data" + os.sep + "WoolworthsDemands.csv", index_col=0)
    demands = demands["6/14/2021"]
    return demands

    #return pd.read_csv("data" +os.sep +"DemandEstimation.csv")[:][col]


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

    areas = pd.read_csv("data" + os.sep + "WoolworthsLocationsDivisions.csv", index_col=2)

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

    stores = pd.DataFrame()

    # Columns for combos of three stores.
    n = len(region.index)

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
        copy = pd.Series(routes[i, :].T, index=region.index)
        stores.insert(i, "Route " + str(i), copy)

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
    demands = demands[routes.index]

    for route in routes:
        if routes[route].dot(demands) > 26:
            routes.drop(route, inplace=True, axis=1)

    return routes


def routeLocations(routes):
    """ checks demands of a set of routes and removes all greater than limit.
            Parameters:
            -----------
            route : Data Frame
                routes stored as a dataframe.


            Returns:
            --------
            routeNames : 2D array
                series of storesNames according to a region

    """
    routeNames = []
    for i in routes.columns:
        temp = [j if routes[i][j] == 1 else 0 for j in routes.index]

        temp = list(filter(lambda a: a != 0, temp))
        routeNames.append(temp)


    return routeNames


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
    return it.permutations(route)


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
    route = ('Distribution Centre Auckland',) + route
    route = route + ('Distribution Centre Auckland',)

    # read in data frame with storeName indexing
    time = pd.read_csv("data" +os.sep +"WoolworthsTravelDurations.csv", index_col=0)
    cost = 0

    # loop from 1 through length of route list
    for i in range(1, len(route)):
        cost += time[route[i]][route[i-1]]

    return cost


def lp(routesFrame, timeFrame, i):
    """ interplate two extraction rates to find the total extraction rate, q.
            Parameters:
            -----------
            dataFrame : pandas dataFrame
                Independent variable.

            timeFrame : pandas dataFrame
                Independent variable.

            i: string
                used to specify which region

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
    vars = LpVariable.dicts(i, routesFrame.columns, 0, None, 'Integer')

    prob += lpSum([vars[i] * timeFrame[i] for i in timeFrame.index]), "Time"

    # route constraints
    for i in routesFrame.index:
        prob += lpSum([vars[j] * routesFrame[j][i] for j in routesFrame.columns]) == 1

    # truck constraint
    prob += lpSum([vars[i] for i in routesFrame.columns]) <= 60

    # The problem data is written to an .lp file
    prob.writeLP("VehicleRoutingProblem. lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        if (v.varValue != 0):
            print(v.name, "-", v.varValue)

    # The optimised objective function value is printed to the screen
    print("Total Time = ", value(prob.objective))


if __name__ == "__main__":

    #read in demands
    demands = readDemands(0)

    routeCons = pd.DataFrame()
    timeCons = pd.DataFrame()


    # loop through each region
    regions = ["North", "City", "East", "South", "West", "NorthWest"]
    for i in regions:
        region = selectRegion(i)

        routes = routeGeneration(region, 4)
        routes = checkDemands(routes, demands)

        routeNames = routeLocations(routes)

        # cost vector
        costV = []

        # loop through routes
        for r in routeNames:
            permutations = permutateRoute(r)

            cost = 9999999999

            #loop through permutations
            for p in permutations:

                test = costRoutes(p)
                if(test < cost):
                    cost = test
                    order = p

            # add new cost row to route for this route
            costV.append(cost)

        costs = pd.Series(costV,index=routes.columns)
        #temp = pd.DataFrame({'Time': costs})

        lp(routes, costs, i)

        # append to lp dataframe


    # call lp
