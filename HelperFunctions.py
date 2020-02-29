# Python Module HelperFunctions
import math
import re


def generate_path_string(point1, point2, velocity, heading):
    path = '('
    path += str(point1[0]) + ', ' + str(point1[1]) + ')'
    path += ' to '
    path += '(' + str(point2[0]) + ', ' + str(point2[1]) + ')'
    path += ' going '
    path += str(velocity) + 'in/s'
    path += ' at '
    path += str(heading) + '°'
    return path


def generate_turn_string(turn, points):
    string = 'Turn to '
    string += str(turn[1]) + '°'
    string += ' at ('
    string += str(points[turn[0]][0]) + ', ' + str(points[turn[0]][1]) + ')'
    return string


def convert_coordinates_to_inches(points, pixels_per_inch, field_length_inches):
    converted_points = []
    for p in points:
        new_point = [None, None]
        new_point[0] = p[0] / pixels_per_inch
        new_point[1] = p[1] / pixels_per_inch
        new_point[0] -= (field_length_inches / 2.0)
        new_point[1] -= (field_length_inches / 2.0)
        new_point[0] = round(new_point[0], 2)
        new_point[1] = round(new_point[1], 2)
        converted_points.append(new_point)
    return converted_points


def convert_coordinates_to_pixels(points, pixels_per_inch, field_length_pixels):
    converted_points = []
    for p in points:
        new_point = [None, None]
        new_point[0] = p[0] * pixels_per_inch
        new_point[1] = p[1] * pixels_per_inch
        new_point[0] += (field_length_pixels / 2.0)
        new_point[1] += (field_length_pixels / 2.0)
        new_point[0] = round(new_point[0], 2)
        new_point[1] = round(new_point[1], 2)
        converted_points.append(new_point)
    return converted_points


def calculate_movement_per_frame(point1, point2, inches_per_second, frames_per_second, pixels_per_inch):
    pixels_per_frame = (inches_per_second * pixels_per_inch) / frames_per_second
    if point2[0] - point1[0] == 0:
        x_per_frame = 0
        y_per_frame = pixels_per_frame
    elif point2[1] - point1[1] == 0:
        x_per_frame = pixels_per_frame
        y_per_frame = 0
    else:
        x_to_y_ratio = (point2[0] - point1[0]) / (point2[1] - point1[1])
        y_per_frame = math.sqrt(pixels_per_frame**2 / (x_to_y_ratio**2 + 1)) # Uses derived formula
        x_per_frame = x_to_y_ratio * y_per_frame
    if point2[1] <= point1[1]:
        y_per_frame *= -1
        x_per_frame *= -1
    return [x_per_frame, y_per_frame]


def clean_coordinates(coord=''):
    string = ''.join(c for c in coord if c.isdigit() or c == '.' or c == '-')
    if len(string) > 0 and (string[0] == '.'):
        string = string[1:-1]
    if len(string) > 0 and (string[-1] == '.' or string[-1] == '-'):
        string = string[0:-1]
    if len(string) == 0:
        string += '0'
    return string

