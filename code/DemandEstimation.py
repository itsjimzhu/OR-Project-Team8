import numpy as np
import pandas as pd
import os

FILEPATH = False

if FILEPATH:
    demands = pd.read_csv("code" + os.sep + "data" + os.sep + "WoolworthsDemands.csv", index_col=0)
else:
    demands = pd.read_csv("data" + os.sep + "WoolworthsDemands.csv", index_col=0)

weekDemands = []
saturdayDemands = []

# loop through row
for i in demands.index:

    # new demands for each store
    weekTemp = 0
    saturdayTemp = 0
    cnt = 2

    # loop through columns
    for j in demands.columns:

        # check for saturday
        if (cnt)%7 == 0:
            saturdayTemp += demands[j][i]
        else:
            weekTemp += demands[j][i]

        cnt += 1

    # averages
    weekTemp = weekTemp/20
    saturdayTemp = saturdayTemp/4

    # append for each store
    weekDemands.append(weekTemp)
    saturdayDemands.append(saturdayTemp)

# rounding to whole numbers
weekDemands = np.ceil(weekDemands)
saturdayDemands = np.ceil(saturdayDemands)

# convert to dataframe to store in csv
zero = pd.Series(weekDemands, index=demands.index)
one = pd.Series(saturdayDemands, index=demands.index)

df = pd.DataFrame({'0': zero, '1': one})
df.to_csv('DemandEstimation.csv')
