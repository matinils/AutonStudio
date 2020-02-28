# Python Module HelperFunctions
def generate_path(point1, point2, velocity, heading):
    path = '('
    path += str(point1[0]) + ', ' + str(point1[1]) + ')'
    path += ' to '
    path += str(point2[0]) + ', ' + str(point2[1]) + ')'
    path += ' going '
    path += str(velocity) + 'in/s'
    path += ' at '
    path += str(heading) + '°'
    return path
