import json

import matplotlib.pyplot as plt
from GUI.Functions.functions import *


class Optimize_Piezo:

    def __init__(self, instrument_controller, optimizer, settings_path):
        self.optimize_bool = True
        self.fail_counter = None
        self.settings_path = settings_path
        self.target_detector = None
        self.input_piezo_controller = None
        self.output_piezo_controller = None
        self.instrument_controller = instrument_controller
        self.optimizer = optimizer

        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.iterations = settings_dict["iterations"]
            self.abs_tol = settings_dict["abs_tol"]
            self.fail_limit = settings_dict["fail_limit"]
            self.min_sample_time = settings_dict["min_sample_time"]
            self.max_sample_time = settings_dict["max_sample_time"]

    def optimize(self):

        self.fail_counter = 0
        self.input_piezo_controller = self.instrument_controller.input_piezo_controller
        self.output_piezo_controller = self.instrument_controller.output_piezo_controller
        self.target_detector = self.instrument_controller.get_target_detector()

        initial_point = np.array(
            [self.input_piezo_controller.get_x_voltage_set(), self.input_piezo_controller.get_y_voltage_set(),
             self.input_piezo_controller.get_z_voltage_set(), self.output_piezo_controller.get_x_voltage_set(),
             self.output_piezo_controller.get_y_voltage_set(), self.output_piezo_controller.get_z_voltage_set()])

        current_point = initial_point.copy()
        current_value = self.compute_function_value(current_point)
        best_point = current_point.copy()
        best_value = current_value

        for index in range(self.iterations):
            # Estimate the gradient at the current point
            new_point = self.optimizer.update(self.compute_function_value, current_point, current_value, index,
                                              self.fail_counter)
            new_point[0] = np.clip(new_point[0], 0, 120)
            new_point[1] = np.clip(new_point[1], 0, 120)
            new_point[2] = np.clip(new_point[2], 0, 120)
            new_point[3] = np.clip(new_point[3], 0, 120)
            new_point[4] = np.clip(new_point[4], 0, 120)
            new_point[5] = np.clip(new_point[5], 0, 120)
            new_value = self.compute_function_value(new_point)

            print("New Point: ", new_point)

            # Update the best point if the new point has a lower function value
            if new_value < best_value:
                self.fail_counter = 0
                best_point = new_point
                best_value = new_value
            else:
                if new_value > current_value:
                    print("fail")
                    self.fail_counter = self.fail_counter + 1

            if self.fail_counter >= self.fail_limit:
                print("fail_counter")
                break

            if not self.optimize_bool:
                break

            print("New value: ", new_value, "Best value: ", best_value)

            # Check for convergence based on absolute and relative tolerances
            change = np.linalg.norm(new_value - current_value)
            if change < self.abs_tol:
                print("tolerance")
                break

            current_point = new_point
            current_value = new_value

        self.set_point(best_point)

    def set_point(self, point):
        self.input_piezo_controller.set_xyz_voltage(point[0], point[1], point[2])
        self.output_piezo_controller.set_xyz_voltage(point[3], point[4], point[5])

    def compute_function_value(self, point):
        self.set_point(point)
        plt.pause(self.min_sample_time * (1 - self.fail_counter / self.fail_limit) + self.max_sample_time * (
                self.fail_counter / self.fail_limit))
        res = - power_W_to_dBm(self.target_detector.get_detector_power_get())
        return res

    def set_optimize_bool(self, optimize_bool):
        self.optimize_bool = optimize_bool


class Optimizer_Gradient_Descent:

    def __init__(self, settings_path):
        self.settings_path = settings_path

        self.m = None
        self.v = None
        self.m_hat = None
        self.v_hat = None

    def estimate_gradient(self, function, point, point_value, learning_rate):
        gradient_input_x = self.gradients(function, point, point_value,
                                          np.array([learning_rate[0], 0, 0, 0, 0, 0]))
        gradient_input_y = self.gradients(function, point, point_value,
                                          np.array([0, learning_rate[1], 0, 0, 0, 0]))
        gradient_input_z = self.gradients(function, point, point_value,
                                          np.array([0, 0, learning_rate[2], 0, 0, 0]))
        gradient_output_x = self.gradients(function, point, point_value,
                                           np.array([0, 0, 0, learning_rate[3], 0, 0]))
        gradient_output_y = self.gradients(function, point, point_value,
                                           np.array([0, 0, 0, 0, learning_rate[4], 0]))
        gradient_output_z = self.gradients(function, point, point_value,
                                           np.array([0, 0, 0, 0, 0, learning_rate[5]]))

        first_moment = np.array(
            [gradient_input_x, gradient_input_y, gradient_input_z, gradient_output_x, gradient_output_y,
             gradient_output_z])

        return first_moment

    def gradients(self, function, point, point_value, change):
        dh = np.linalg.norm(change)

        fx = point_value
        fx_h = function(point - change)

        first_order = (fx - fx_h) / (dh)
        return first_order

    def update(self, function, current_point, current_value, index, fail_counter):
        if self.m is None:
            self.m = np.zeros_like(current_point)  # First moment estimate
            self.v = np.zeros_like(current_point)  # Second moment estimate

        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            learning_rate = np.array(settings_dict["learning_rate"])
            gradient_estimation = np.array(settings_dict["gradient_estimation"]) / np.sqrt(fail_counter + 1)
            beta1 = settings_dict["beta1"]
            beta2 = settings_dict["beta2"]
            epsilon = settings_dict["epsilon"]

        gradient = self.estimate_gradient(function, current_point,
                                          current_value, gradient_estimation)

        print("Gradient: ", gradient)
        # Update the first moment estimate
        self.m = beta1 * self.m + (1 - beta1) * gradient
        # Update the second moment estimate
        self.v = beta2 * self.v + (1 - beta2) * gradient ** 2
        # Bias-corrected moment estimates
        self.m_hat = self.m / (1 - beta1 ** (index + 1))
        self.v_hat = self.v / (1 - beta2 ** (index + 1))

        change = learning_rate * self.m_hat / (np.sqrt(self.v_hat) + epsilon)
        new_point = current_point - change
        return new_point


class Optimizer_Coordinate:

    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.second_gradient_list = []
        self.first_gradient_list = []
        self.point_list = []
        self.point_x_list = []
        self.point_y_list = []
        self.value_list = []
        self.max_index_list = []

        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.learning_rate = np.array(settings_dict["single_learning_rate"])

    def estimate_gradient(self):
        new_gradient = None
        new_second_gradient = None

        if len(self.value_list) == 1:
            new_gradient = self.first_gradient_list[0].copy()
            new_second_gradient = self.first_gradient_list[0].copy()
        else:
            current_second_gradient = self.second_gradient_list[-2]
            current_gradient = self.first_gradient_list[-1]
            previous_point = self.point_list[-2]
            current_point = self.point_list[-1]
            previous_value = self.value_list[-2]
            current_value = self.value_list[-1]
            max_index = self.max_index_list[-1]

            new_gradient = current_gradient.copy()
            new_gradient[max_index] = (current_value - previous_value) / (
                    current_point[max_index] - previous_point[max_index])

            new_second_gradient = current_second_gradient.copy()
            new_second_gradient[max_index] = (new_gradient[max_index] - current_gradient[
                max_index]) / (current_point[max_index] - previous_point[max_index])

        return np.array(new_gradient), np.array(new_second_gradient)

    def update(self, function, current_point, current_value, index):
        if len(self.value_list) == 0:
            self.value_list.append(current_value)
            self.point_list.append(current_point * 1.0)
            self.first_gradient_list.append(current_point * 0.1)
            self.second_gradient_list.append(current_point * 0.1)
        new_gradient, new_second_gradient = self.estimate_gradient()
        max_index = np.argmax(np.abs(new_gradient))

        new_point = current_point.copy() * 1.0
        new_point[max_index] = current_point[max_index] - self.learning_rate * new_gradient[max_index]
        new_value = function(new_point)
        self.first_gradient_list.append(new_gradient.copy())
        self.second_gradient_list.append(new_second_gradient.copy())
        self.point_x_list.append(new_point[0])
        self.point_y_list.append(new_point[1])
        self.point_list.append(new_point.copy())
        self.value_list.append(new_value.copy())
        self.max_index_list.append(max_index)

        return new_point

class Optimizer_Seperate_Coordinate:

    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.second_gradient_list = []
        self.first_gradient_list = []
        self.point_list = []
        self.point_x_list = []
        self.point_y_list = []
        self.value_list = []
        self.max_index_list = []

        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.learning_rate = np.array(settings_dict["single_learning_rate"])

        while True:
            pass

    def update(self, function, current_point, current_value, index):
        pass