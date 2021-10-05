import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
import itertools as it
from pulp import *
import os
import time

'''This code simulates random routes of given length and calculates
    what percentage have valid demand '''

if __name__ == "__main__":
    initial = pd.read_csv("code" + os.sep + "data" + os.sep + "DemandLongPivot.csv", index_col=0)
    initial.set_index('Store')
    weekday = initial[initial['day'].isin(['Saturday'])]
    weekday = weekday[weekday['demand']>0]
    pivoted = weekday.pivot(index = 'Store', columns = 'date', values = 'demand')
    count = 0
    number = 0
    daily_sims = 10000
    testing_number = 5
    for j in range(len(pivoted.columns)):
        randi = np.random.randint(0,pivoted.shape[0],daily_sims + testing_number)
        for i in range(daily_sims):
            sums = 0
            for len in range(testing_number):
                sums += pivoted.iloc[randi[i+len],j]
            count += 1
            if sums < 28:
                number += 1
    print('Viable Routes: ' + str(number))
    print('Total Routes Simulated: ' + str(count))
    print('Percentage Valid: ' + str(number/count))