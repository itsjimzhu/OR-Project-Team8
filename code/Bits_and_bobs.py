# Pandas to Numpy conversion code
import pandas as pd
df = pd.DataFrame({"Route 1": [x, y], "Route 2": [i, j]})
df_to_array = df.to_numpy()
array([[x, y], [i, j]])

# Importing CSV files into Pandas
import pandas as pd
df = pd.read_csv('Name_of_data_file.csv')
print(df.to_string()) 

# Importing CSV files into NumPy array
from numpy import genfromtxt
my_data = genfromtxt('Name_of_data_file.csv', delimiter=',')
