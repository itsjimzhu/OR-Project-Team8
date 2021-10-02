import numpy as np
import pandas as pd
import itertools as it
from pulp import *
import os

def vehicleRoutingProblem(demand, max):
    """ solve a vehicle routing problem for specific demands and a maximum route size.
            Parameters:
            -----------
            demand : int
                specifies which set of demands (Weekday or Saturday).

            col : int
                the maximum amount of stores per route.

            Returns:
            --------


            Notes:
            ------
            This is a wrapper for all other functions in this file.
    """
    # instantiation of tracking variables
    bestRoutes = []
    bestTimes = []
    totalTime = 0

    # read in demands
    demands = readDemands(demand)

    # loop through each region
    regions = ["North", "City", "East", "SouthEast", "South", "West", "NorthWest"]
    for i in regions:
        # select correct region
        region = selectRegion(i)

        # generate and cull routes
        routes = routeGeneration(region, max)
        routes = checkDemands(routes, demands)

        # convert route vectors to store lists
        routeNames = routeLocations(routes)

        # instantiate cost vector
        costV = []
        orderV = []

        # loop through routeNames
        for r in routeNames:
            # permutate routes
            permutations = permutateRoute(r)

            cost = 9999999999
            # loop through permutations
            for p in permutations:
                # find cost of permutation
                # TODO add pallet unloading to costRoutes() function, 450 * number of pallets.
                test = costRoutes(p,demands)

                # store lowest permutation and best order
                if (test < cost):
                    cost = test
                    order = p

            # append lowest cost and best order to vector
            costV.append(cost)
            orderV.append(order)

        # convert vectors to series
        mapping = pd.Series(orderV, index=routes.columns)
        costs = pd.Series(costV, index=routes.columns)

        # select best combination of routes
        prob = routeSelection(routes, costs, i)

        # loop through problem variables
        check = 0
        for v in prob.variables():
            # only do used routes
            if (v.varValue != 0):
                # convert problem variable regions to correct index format
                str = v.name.split("_", 1)[1].replace("_", " ")

                # check each store is satisfied
                check += 1 * len(mapping.loc[str])

                # keeping for nice outputs
                bestRoutes.append(mapping.loc[str])
                bestTimes.append(costs.loc[str])

        # output regions solution
        print(i, " ", check, '/', len(routes.index), "\t cumulative total time for region:", value(prob.objective))

        # calculate total time
        totalTime += value(prob.objective)

    # nice output of best routes
    print(" ")
    cnt = 0
    for map in bestRoutes:
        for j in range(len(map)):
            print(map[j], "-->", end=" ")
        print("time for route:", bestTimes[cnt])
        cnt += 1

    # output of total time
    print("\t cumulative total time for all regions", totalTime, " in seconds")
    print("\t Total cost of all routes", 225*totalTime/3600, "$")
    return


def readDemands(col):
    """ Reads in demands from a csv file and return correct set.
            Parameters:
            -----------
            col : int
                specifies which set of demands (Weekday or Saturday).


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
    # this is currently hard coded
    demands = pd.read_csv("code" + os.sep + "data" + os.sep + "WoolworthsDemands.csv", index_col=0)
    demands = demands["6/14/2021"]
    return demands

    #return pd.read_csv("data" +os.sep +"DemandEstimation.csv", index_col=0)[:][col]


def selectRegion(region):
    """ return correct set of stores according to specified regions.
            Parameters:
            -----------
            region : string
                specifies which region.


            Returns:
            --------
            storeNames : pandas Series
                series of storesNames according to a region.


            Notes:
            ------
            The format of the csv is:
                         ... Area ...

            Store 1      ... [North] ...
            Store 2      ... [City] ...
            Store 3      ... [South] ...
            Store 4      ... [NorthWest] ...
    """
    areas = pd.read_csv("code" + os.sep + "data" + os.sep + "WoolworthsLocationsDivisions.csv", index_col=2)
    return areas[areas["Area"]==region]


def routeGeneration(region, choose):
    """ Generate routes of choose! {4,3,2,1} according to a region.
            Parameters:
            -----------
            region : pandas DataFrame
                Stores within this region.

            choose : int
                Max amount of stores per route.


            Returns:
            --------
            routesF : DataFrame
                Series of storesNames according to a region.


            Notes:
            ------

        """

    # get amount of stores in this region
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

    # instantiate an empty dataframe
    routesF = pd.DataFrame()

    # loop through each route
    for i in range(len(routes)):

        # transpose and convert routes to series and then append to frame
        copy = pd.Series(routes[i, :].T, index=region.index)
        routesF.insert(i, "Route " + str(i), copy)

    return routesF


def checkDemands(routes, demands):
    """ checks total demand for a set of routes and removes all greater than 26.
            Parameters:
            -----------
            routes : pandas DataFrame
                combination of routes for a selection of stores.

            demands : pandas DataFrame
                Series of demand value indexed with stores.


            Returns:
            --------
            routes : DataFrame
                culled combination of routes for a selection of stores.
    """

    # loop through all routes
    for route in routes:

        # if total demand of route is greater than 26
        if routes[route].dot(demands[routes.index]) > 26:
            # drop current route
            routes.drop(route, inplace=True, axis=1)

    return routes


def routeLocations(routes):
    """ converts the route DataFrame to a list of lists.
            Parameters:
            -----------
            routes : pandas DataFrame
                combination of routes for a selection of stores.


            Returns:
            --------
            routeNames : list of lists
                list of lists containing only the stores within each route.
    """
    # instantiate route names list
    routeNames = []

    #loop through all routes
    for i in routes.columns:

        # convert binary value to a list of store
        temp = [j if routes[i][j] == 1 else 0 for j in routes.index]
        temp = list(filter(lambda a: a != 0, temp))

        # append the route name list
        routeNames.append(temp)

    return routeNames


def permutateRoute(route):
    """ generates permutations of each route.
            Parameters:
            -----------
            route : list
                list containing only the stores within route.


            Returns:
            --------
            permutations : object(tuple)
                permutations of stores within route.


            Notes:
            ------
            Assuming unidirectional so ABCD == DCBA
    """
    return it.permutations(route)


def costRoutes(route, demands):
    """ cost routes according to store order.
            Parameters:
            -----------
            route : tuple
                combination of stores.
            demands : 
                Series of demand information


            Returns:
            --------
            cost : int
                final cost of a route


            Notes:
            ------
            We don't need an unidirectional average even though the times are directional
            During simulation we will generate values that range over both directions times

                   t1 -- t2
            simt1------------simt2
        <---------------------------->
                   continuum
    """
    cost = 0

    # Crate unloading time
    for store in range(len(route)):
        cost += 450 * demands[route[store]]

    # insert origin node at start and end
    route = ('Distribution Centre Auckland',) + route + ('Distribution Centre Auckland',)

    # read in time DataFrame with storeName indexing
    time = pd.read_csv("code" + os.sep + "data" +os.sep +"WoolworthsTravelDurations.csv", index_col=0)

    # loop from 1 through length of route list
    for i in range(1, len(route)):
        # add time between current and previous node
        cost += time[route[i]][route[i-1]]

    # Can't have routes longer than 4 hours
    # TODO: BUT - after implementing randomness we can allow for longer routes at greater cost.
    if (cost > 14400):
        cost = 99999

    return cost


def routeSelection(routesFrame, timeFrame, region):
    """ Select the best combination of routes that satisfy each store
            Parameters:
            -----------
            routesFrame : Pandas DataFrame
                collection of routes for each store.

            timeFrame : Pandas Series
                contains the time associated with each route.

            region: string
                specifies the current region


            Returns:
            --------
            prob : object
                object containing everything regarding to the lp solution


            Notes:
            ------
            This function uses an integer linear program to solve for the best selection of routes

            The routeFrame format is:
                                    R1,R2,R3,R4,R5

            Store 1                 [1, 1, 1, 0, 1]
            Store 2                 [0, 0, 1, 1, 0]
            Store 3                 [1, 0, 0, 1, 1]
            Store 4                 [0, 1, 1, 0, 1]

            The timeFrame format is:
            Time per route [100, 36, 57, 69]
    """
    # create problem and variables
    prob = LpProblem(region, LpMinimize)
    vars = LpVariable.dicts(region, routesFrame.columns, 0, None, 'Integer')

    # objective constraints
    prob += lpSum([vars[i] * timeFrame[i] for i in timeFrame.index]), "Time"

    # route constraints
    for i in routesFrame.index:
        prob += lpSum([vars[j] * routesFrame[j][i] for j in routesFrame.columns]) == 1

    # truck constraint
    prob += lpSum([vars[i] for i in routesFrame.columns]) <= 30

    # The problem data is written to an .lp file
    # prob.writeLP("VehicleRoutingProblem.lp")

    # The problem is solved using PuLP's choice of Solver, msg=0 to suppress output
    prob.solve(PULP_CBC_CMD(msg=0))

    # TODO: 225$ cost per hour, BUT - after implementing randomness we can allow for longer routes at greater cost.
    # Check the CostRoutes() function

    return prob


if __name__ == "__main__":
    vehicleRoutingProblem(0, 3)