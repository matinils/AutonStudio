# Python Module HelperFunctions
import math


def generate_path_string(p1, p2, velocity, heading):
    return f'({p1[0]}, {p1[1]}) to ({p2[0]}, {p2[1]}) going {velocity} in/s at {heading}°'

def generate_turn_string(turn, points):
    return f'Turn to {turn[1]} ° at ({points[turn[0]][0]}, {points[turn[0]][1]})'

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
        y_per_frame = math.sqrt(pixels_per_frame ** 2 / (x_to_y_ratio ** 2 + 1))  # Uses derived formula
        x_per_frame = x_to_y_ratio * y_per_frame
    if point2[1] <= point1[1]:
        y_per_frame *= -1
        x_per_frame *= -1
    if point2[0] > point1[0] and y_per_frame == 0.0:
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


def sort_turns(turns):
    if len(turns) > 0:
        sorted_turns = [turns[0]]
        for t in turns:
            if t is turns[0]:
                continue
            for st in sorted_turns:
                if t[0] < st[0]:
                    sorted_turns.insert(0, t)
                    break
            if not sorted_turns.__contains__(t):
                sorted_turns.append(t)
        return sorted_turns
    return turns


def calculate_rotation_per_frame(points, angle1, angle2, degrees_per_second, frames_per_second):
    deltas = []
    for p in points:
        point_deltas = [[], []]
        delta_angle = float(angle2) - float(angle1)
        degrees_per_frame = degrees_per_second / frames_per_second
        frame_count = abs(int(delta_angle / degrees_per_frame))
        current_angle = float(angle1)
        for i in range(0, frame_count):
            current_angle += degrees_per_frame * math.copysign(1.0, delta_angle)
            # Use clockwise rotation matrix
            point_deltas[0].append(
                p[0] * math.sin(math.radians(current_angle)) + p[1] * math.cos(math.radians(current_angle)))
            point_deltas[1].append(
                p[0] * math.cos(math.radians(current_angle)) - p[1] * math.sin(math.radians(current_angle)))
            # if i == frame_count - 1:  # Account for uneven division of degrees into frames
            # angle2 = float(angle2)
            # point_deltas[0][i] = (p[0]*math.sin(math.radians(angle2-current_angle)) + p[1]*math.cos(math.radians(angle2-current_angle)))
            # point_deltas[1][i] = p[0]*(math.cos(math.radians(angle2-current_angle)) - p[1]*math.sin(math.radians(angle2-current_angle)))
        deltas.append(point_deltas)
    return deltas
