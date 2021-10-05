import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
import itertools as it
from pulp import *
import os
import time

if __name__ == "__main__":
    initial = pd.read_csv("code" + os.sep + "data" + os.sep + "DemandLongPivot.csv", index_col=0)
    initial.set_index('Store')
    weekday = initial[initial['day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
    pivoted = weekday.pivot(index = 'Store', columns = 'date', values = 'demand')
    count = 0
    number = 0
    testing_number = 6
    for j in range(len(pivoted.columns)):
        randi = np.random.randint(0,pivoted.shape[0],10000 + testing_number)
        for i in range(10000):
            sums = 0
            for len in range(testing_number):
                sums += pivoted.iloc[randi[i+len],j]
            count += 1
            if sums < 28:
                number += 1
    print(number/count)
    print(number)
    print(count)