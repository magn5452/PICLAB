import numpy as np
import scipy
from scipy.signal import convolve2d

start_position = np.array([0, 0])
direction = 0
end_position = np.array([1, 3])

end_is_reached = False
while end_is_reached:
    pass


class Turtle():
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.vision_distance = 1
        self.vision_arc_angle = np.pi

    def look(self, points, map_array, resolution=360):
        kernel = np.ones([20, 20]) / (20 * 20)
        smoothed_image_array = convolve2d(map_array, kernel)
        direction_look_array = np.linspace(self.direction - self.vision_arc_angle / 180, self.direction - self.vision_arc_angle / 180, resolution)
        position_look_array = np.array([[self.position + np.cos(direction_look_array)], [self.position + np.sin(direction_look_array)]])
        values_look_array = scipy.interpolate(points, smoothed_image_array,position_look_array)


        return np.amax(values_look_array)

    def move(self, new_position):
        current_position = self.position
        self.angle = np.atan()
        self.position = new_position
