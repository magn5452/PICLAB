


class Optimizer:

    def __init__(self):
        pass


    def gradient_decent(self, start_point, start_gradient, start_second_gradient, num_iterations = 20, learning_rate = 0.15):
        second_gradient_list = []
        gradient_list = []
        point_list = []
        point_x_list = []
        point_y_list = []
        value_list = []

        second_gradient_list.append(start_second_gradient.copy())
        gradient_list.append(start_gradient.copy())
        point_list.append(start_point.copy())
        point_x_list.append(start_point[0])
        point_y_list.append(start_point[1])
        start_value = self.function_evaluation(start_point)
        value_list.append(start_value.copy())

        max_index = 0

        current_point = start_point.copy()
        current_gradient = start_gradient.copy()
        current_value = start_value.copy()

        for i in range(0, num_iterations):

            new_gradient, new_second_gradient = self.calculate_gradient(max_index, value_list, point_list, gradient_list, second_gradient_list)
            max_index = np.argmax(np.abs(new_gradient))


            new_point = current_point.copy()
            new_point[max_index] = current_point[max_index] - learning_rate * new_gradient[max_index] /
            new_value = self.function_evaluation(new_point)



            gradient_list.append(new_gradient.copy())
            second_gradient_list.append(new_second_gradient.copy())
            point_x_list.append(new_point[0])
            point_y_list.append(new_point[1])
            point_list.append(new_point.copy())
            value_list.append(new_value.copy())

            current_gradient = new_gradient.copy()
            current_point = new_point.copy()
            current_value = new_value.copy()


        return value_list, point_list, gradient_list, second_gradient_list, point_x_list, point_y_list



    def calculate_gradient(self, previous_max_index, value_list, point_list, first_gradient_list, second_gradient_list):
        new_gradient = None
        new_second_gradient = None

        if len(value_list) == 1:
            new_gradient  = first_gradient_list[0].copy()
            new_second_gradient = first_gradient_list[0].copy()
        else:
            previous_second_gradient = second_gradient_list[-2]
            current_second_gradient = second_gradient_list[-2]
            previous_gradient = first_gradient_list[-2]
            current_gradient = first_gradient_list[-1]
            previous_point = point_list[-2]
            current_point = point_list[-1]
            previous_value = value_list[-2]
            current_value = value_list[-1]

            new_gradient = current_gradient.copy()
            new_gradient[previous_max_index] = (current_value - previous_value)/(current_point[previous_max_index] - previous_point[previous_max_index])

            new_second_gradient = current_second_gradient.copy()
            new_second_gradient[previous_max_index] = (new_gradient[previous_max_index] - current_gradient[previous_max_index])/(current_point[previous_max_index] - previous_point[previous_max_index])

        return np.array(new_gradient), np.array(new_second_gradient)

    def forward_gradient(self, x0, x1, f0, f1):
        return  (f0 - f1)/(x0 - x1)



    def function_evaluation(self, point):
        x = point[0]
        y = point[1]
        return self.function_evaluation_coordinate(x,y)

    def function_evaluation_coordinate(self, x,y):
        result = x**2 + y**2
        return result

import numpy as np
import matplotlib.pyplot as plt

start_point = np.array([-1.,-1.])
start_gradient = np.array([1,-1.])
start_second_gradient = np.array([1,-1.])
optimizer = Optimizer()
value_list, point_list, gradient_list, second_gradient_list, point_x_list, point_y_list= optimizer.gradient_decent(start_point, start_gradient, start_second_gradient)
print(value_list)
print(point_list)
print(gradient_list)
print(second_gradient_list)

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x,y)
Z = optimizer.function_evaluation_coordinate(X,Y)

extent = np.min(x), np.max(x), np.min(y), np.max(y)
fig = plt.figure(frameon=True)
plt.imshow(Z, cmap=plt.cm.viridis, alpha=.9, interpolation='bilinear', extent=extent)
plt.plot(point_x_list,point_y_list)
plt.show()