from scipy.optimize import fsolve
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

#Data Import - Only thing to change when changing data
Name = 'Model'
data_import = np.loadtxt('datapoints.csv',delimiter=',')
hrv_data = data_import[:,0]
resp_data = data_import[:,1]

#Define model and optimization functions
def model(param,resp,stress,exc):
    a = param[0]
    b = param[1]
    c = param[2]

    hrv = ((resp*a/stress)/(b + resp**2 + resp)) + c*exc

    return hrv

def optimize(param,hrv_data,resp_rate,stress_guess,exc_guess):
    
    hrv_model = model(param,resp_rate,stress_guess,exc_guess)
    
    se = (hrv_model-hrv_data)**2
    sse = sum(se)
    return sse

#Initial Guesses  
param_guess = ([210,10,5])
stress_guess = 1
exc_guess = 1

#Use Optimizer function and show results
solution = minimize(optimize,param_guess,args=(hrv_data,resp_data,stress_guess,exc_guess))
print(solution)
print('')
print('A = ',solution.x[0])
print('B = ',solution.x[1])
print('C = ',solution.x[2])
param_opt = ([solution.x[0],solution.x[1],solution.x[2]])

#Save parameters
np.savetxt('parameters.csv',param_opt,delimiter=',')

#Plot Intial, Optimized and Data
initial = model(param_guess,resp_data,stress_guess,exc_guess)
optimized = model(param_opt,resp_data,stress_guess,exc_guess)

plt.figure()
plt.plot(resp_data,initial,'r:',label='Inital Guess')
plt.plot(resp_data,optimized,'b--',label='Optimized Model')
plt.plot(resp_data,hrv_data,'g-',label='Data')
plt.title('Model Parameter Esimation')
plt.xlabel('Respiration Rate (breath/min)')
plt.ylabel('Heart Rate Variability (bpm/min)')
plt.legend()
filename = 'Model_Optimize_' + Name + '.png'
plt.savefig(filename)
plt.show()

