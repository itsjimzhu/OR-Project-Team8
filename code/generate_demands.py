import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
import itertools as it
from pulp import *
import os
import time

PATHFILE = False

def generate_demands(type = 'Ceil', Saturday = False):
    ''' This generates demands for each from the demand data, either in the form random, average or average
        rounded up. It can generate for the week, or for Saturdays
    
        Parameters:
        -----------
        type : string
            string with the label of the type of generation we want - either 'Ceil', 'Mean' or 'Random'
            default set to 'Ceil'
        Saturday : Boolean
            Boolean reflecting whether we want to generate demand for Saturday (else we generate for the weekdays)
            False by default

        Returns:
        --------
        demand : dataframe column
            dataframe column with the generated demand for each location
        
    '''


    if PATHFILE:
        initial = pd.read_csv("code" + os.sep + "data" + os.sep + "DemandLongPivot.csv", index_col=0)
    else:
        initial = pd.read_csv("data" + os.sep + "DemandLongPivot.csv", index_col=0)

    # Set index for the dataframe to be 'Store'
    initial.set_index('Store')

    # Generate demand based on Saturday demand or not
    if Saturday == True:
        # take all the data from days that are saturday
        weekend = initial[initial['day']=='Saturday']
        # pivot so that there is a column for each date
        pivoted = weekend.pivot(index = 'Store', columns = 'date', values = 'demand')
        # take the mean of each row (ie each store)
        mean = pivoted.mean(axis = 1)
        # take the ceiling of the means
        ceil_mean = mean.apply(np.ceil)
        # find the standard deviation of each row (ie each store)
        std = pivoted.std(axis = 1)
        # generate a dictionary with the mean, ceiling and std
        frame = { 'Mean': mean, 'Ceil Mean': ceil_mean, 'Deviation' : std}
        # turn this dictionary into a dataframe
        all_data = pd.DataFrame(frame)
    else:
        # take all the data from days that are weekdays
        weekday = initial[initial['day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        # pivot so that there is a column for each date
        pivoted = weekday.pivot(index = 'Store', columns = 'date', values = 'demand')
        # take the mean of each row (ie each store)
        mean = pivoted.mean(axis = 1)
        # take the ceiling of the means
        ceil_mean = mean.apply(np.ceil)
        # find the standard deviation of each row (ie each store)
        std = pivoted.std(axis = 1)
        # generate a dictionary with the mean, ceiling and std
        frame = { 'Mean': mean, 'Ceil Mean': ceil_mean, 'Deviation' : std}
        # turn this dictionary into a dataframe
        all_data = pd.DataFrame(frame)

    # Return data based on what type we want (ceil, mean or random)
    if type == 'Ceil':
        return all_data['Ceil Mean']
    elif type == 'Mean':
        return all_data['Mean']
    else:
        random = []
        # Loop through each store and generate a random normal value with the mean and deviation we have found for this store
        for store in all_data.index:
            random.append(np.random.normal(all_data['Mean'][store], all_data['Deviation'][store], 1)[0])

    all_data['Random'] = random
    return all_data['Random']

if __name__ == "__main__":
    man = generate_demands(type = 'Deviation')
    print('yes')