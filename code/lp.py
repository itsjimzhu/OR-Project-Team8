# imports
from pulp import *


def Kevin():
    # list of A list of all the roll lengths is created
    LenOpts = ["5", "7", "9"]  # list of stores in our case

    # A dictionary of the demand for each roll length is created
    rollDemand = {"5": 150,
                  "7": 200,
                  "9": 300}  # store demand

    # A list of all the patterns is created
    PatternNames = ["A", "B", "C"]  # routes

    # Creates a list of the number of rolls in each pattern for each different roll length
    patterns = [  # A B C
        [0, 2, 2],  # 5
        [1, 1, 0],  # 7
        [1, 0, 1]  # 9
    ]  # route x node in our case (all 1's)

    # The cost of each 20cm long sponge roll used
    cost = 1  # time per route

    # The pattern data is made into a dictionary
    patterns = makeDict([LenOpts, PatternNames], patterns, 0)  # can now reference using strings instead of indexes

    # The problem variables of the number of each pattern to make are created
    vars = LpVariable.dicts("Patt", PatternNames, 0, None, 'Integer')

    # The variable 'prob' is created
    prob = LpProblem("CuttingStockProblem", LpMinimize)

    # The objective function is entered: the total number of large rolls used + the fixed cost of each
    prob += lpSum([vars[i] * cost for i in PatternNames]), "ProductionCost"

    # The demand minimum constraint is entered
    for i in LenOpts:
        prob += lpSum([vars[j] * patterns[i][j] for j in PatternNames]) >= rollDemand[i]

    # The problem data is written to an .lp file
    prob.writeLP("SpongeRollProblem. lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        print(v.name, "-", v.varValue)

    # The optimised objective function value is printed to the screen
    print("Production Costs = ", value(prob.objective))

def real(dataFrame):
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
    Kevin()