import numpy as np
import matplotlib.pyplot as plt

# Parameters for exponential distribution
decay_param = 2

# Generate exponential data
x = np.arange(0, 10, 0.01)
num_points = len(x)
exponential_data = 10*np.exp(- decay_param * x)

# Parameters for noise
noise_mean = 0
noise_std = 0

# Generate noise
noise = np.random.normal(loc=noise_mean, scale=noise_std, size=num_points)

# Add noise to the exponential data
decay = exponential_data + noise

plt.figure
plt.plot(decay)
# Assuming your time series data is in the 'time_series' variable

x = np.arange(-3, 3, 0.05) + 0.025
y = np.arange(-3, 3, 0.05) + 0.025
[X, Y] = np.meshgrid(x, y)
Z = X + 1j * Y
Z_transform = np.zeros(np.shape(X), dtype=np.cdouble)

for n in range(num_points):
    for i in range(len(x)):
        for j in range(len(y)):
            Z_transform[i][j] += decay[n] * np.exp(Z[i][j]*n)

import matplotlib.pyplot as plt

# Create the surface plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(90, 0)
Z_transform[-100 > np.real(Z_transform)] = np.nan
Z_transform[100 < np.real(Z_transform)] = np.nan
surface = ax.plot_surface(X, Y, np.real(Z_transform), cmap='jet')

# Add colorbar to show magnitude
fig.colorbar(surface)

ax.set_title("Complex 2D Array Magnitude")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlim(0,100)
ax.set_zlabel("Magnitude")



plt.show()