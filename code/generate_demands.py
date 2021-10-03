import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
import itertools as it
from pulp import *
import os
import time

PATHFILE = False

def generate_demands(type = 'Ceil', Saturday = False):
    if PATHFILE:
        initial = pd.read_csv("code" + os.sep + "data" + os.sep + "DemandLongPivot.csv", index_col=0)
    else:
        initial = pd.read_csv("data" + os.sep + "DemandLongPivot.csv", index_col=0)

    initial.set_index('Store')

    if Saturday == True:
        weekend = initial[initial['day']=='Saturday']
        pivoted = weekend.pivot(index = 'Store', columns = 'date', values = 'demand')
        mean = pivoted.mean(axis = 1)
        ceil_mean = mean.apply(np.ceil)
        std = pivoted.std(axis = 1)
        frame = { 'Mean': mean, 'Ceil Mean': ceil_mean, 'Deviation' : std}
        all_data = pd.DataFrame(frame)
    else:
        weekday = initial[initial['day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        pivoted = weekday.pivot(index = 'Store', columns = 'date', values = 'demand')
        mean = pivoted.mean(axis = 1)
        ceil_mean = mean.apply(np.ceil)
        std = pivoted.std(axis = 1)
        frame = { 'Mean': mean, 'Ceil Mean': ceil_mean, 'Deviation' : std}
        all_data = pd.DataFrame(frame)

    if type == 'Ceil':
        return all_data['Ceil Mean']
    elif type == 'Mean':
        return all_data['Mean']
    else:
        random = []
        for store in all_data.index:
            random.append(np.random.normal(all_data['Mean'][store], all_data['Deviation'][store], 1)[0])

    all_data['Random'] = random
    return all_data['Random']

if __name__ == "__main__":
    man = generate_demands(type = 'Deviation')
    print('yes')