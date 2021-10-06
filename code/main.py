
from Routes import *
import time

start_time = time.time()

vehicleRoutingProblem(3)
vehicleRoutingProblem(4, True)

print("Execution time --- %s seconds ---" % (time.time() - start_time))