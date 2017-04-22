import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import minimize

#Individual Data Settings
SteadyState = 12
High_data = 38
dData = High_data - SteadyState
K = 0.7         #P controller parameter
hrv_point = K * dData

#Data Import - parameters and datapoint
parameters = np.loadtxt('parameters.csv',delimiter=',')

#Define model and optimization functions
def model(resp,hrv,param):
    a = param[0]
    b = param[1]
    c = param[2]
    
    output = (a*resp/(resp**2 + resp + b)) + c - hrv
    return output

output = fsolve(model,5,args=(hrv_point,parameters))
print('Controller Respiration Rate',output)
    
