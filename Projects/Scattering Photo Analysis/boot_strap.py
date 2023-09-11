import numpy as np
import pandas as pd
import statsmodels.api as sm
from bootstrapped import bootstrapped as bs

# Load the data
data = pd.read_csv('data.csv')
X = data[['x1', 'x2', 'x3']]
y = data['y']


def fit_model(X, y):
    # Add a constant term to the design matrix
    X = sm.add_constant(X)

    # Fit the model
    model = sm.OLS(y, X).fit()

    # Return the coefficients
    return model.params

# Perform bootstrapping
results = bs.bootstrap(X, y, fit_model, num_iterations=1000)

# Extract the standard errors
std_errs = results.get_result().std_err

# Extract the confidence intervals
conf_ints = results.get_result().conf_int(alpha=0.05)

# Extract the p-values
p_values = results.get_result().p_values