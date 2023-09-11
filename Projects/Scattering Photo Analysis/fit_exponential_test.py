from scipy.optimize import curve_fit
import numpy as np


from functions import *

initial_guess = np.array([1, 1])
N = 50
noise = np.random.normal(0, 1.5, N)
x = np.linspace(0, 1, N)
f = 5 * np.exp(-1*x)
y = f + noise

fit_parameters, fit_parameters_cov_var_matrix = curve_fit(exponential_function, x, y, p0=initial_guess)
sigma_f = exponential_function_confidence_bounds_sigma(x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix)

print(fit_parameters)
print(fit_parameters_cov_var_matrix)


plt.figure()
plt.plot(x, y, 'b-', label="Raw data")
plt.plot(x, f, 'k-', label="Real Distribution")

plt.plot(x, exponential_function(x, *fit_parameters), 'r-', label="Fitted Curve")
plt.plot(x, exponential_function(x, *fit_parameters) + sigma_f, 'r--')
plt.plot(x, exponential_function(x, *fit_parameters) - sigma_f, 'r--')

plt.legend()
plt.xlabel('x Length [um]')
plt.ylabel('Mean of blue intensity')

fit_x = x
fit_y = np.log(y)
fit_parameters, fit_parameters_cov_var_matrix = curve_fit(linear_function, fit_x, fit_y, p0=initial_guess)
sigma_f = linear_function_confidence_bounds_sigma(x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix)

print(fit_parameters)
print(fit_parameters_cov_var_matrix)


plt.figure()
plt.plot(x, y, 'b-', label="Raw data")
plt.plot(x, np.log(f), 'k-', label="Real Distribution")

plt.plot(x, linear_function(x, *fit_parameters), 'r-', label="Fitted Curve")
plt.plot(x, linear_function(x, *fit_parameters) + sigma_f, 'r--')
plt.plot(x, linear_function(x, *fit_parameters) - sigma_f, 'r--')

plt.legend()
plt.xlabel('x Length [um]')
plt.ylabel('Mean of blue intensity')


plt.show()

