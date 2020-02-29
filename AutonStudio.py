import PySimpleGUI as sg
import HelperFunctions as hf
import math
import time

if __name__ == '__main__':

    sg.theme('Dark Blue 3')  # please make your windows colorful

    pathInfo = sg.Text('None', key='-PATH_INFO-', size=[20, 1])

    # Each inch is five pixels
    field = sg.Graph(canvas_size=[720, 720], graph_bottom_left=[0, 0], graph_top_right=[720, 720], background_color='#BAB8B8', key='-FIELD-', enable_events=True)

    main_column = [[sg.Button('Set Start Point', key='-START_POINT_BUTTON-')],
                   [sg.Button('Add Point to Path', key='-ADD_POINT_BUTTON-')],
                   [sg.Button('Add Turn')],
                   [sg.Button('Add Robot Operation')],
                   [sg.Button('Simulate Robot Run', key='-SIMULATE_BUTTON-')],
                   [sg.Text('\nSelect Path to Edit')],
                   [sg.Listbox(values=[], size=(50, 6), key='-PATH_LIST-')],
                   [sg.Button('Edit Path', key='-EDIT_PATH_BUTTON-')],
                   [sg.Text('Selected Path:'), pathInfo],
                   [sg.Text('Start X', key='-START_X_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-START_X_INPUT-'), sg.Text('   Start Y', key='-START_Y_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-START_Y_INPUT-')],
                   [sg.Text('Final X', key='-FINAL_X_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-FINAL_X_INPUT-'), sg.Text('   Final Y', key='-FINAL_Y_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-FINAL_Y_INPUT-')],
                   [sg.Button('Deselect', key='-DESELECT_BUTTON-')]]

    layout = [[field, sg.Column(main_column)],
              [sg.Button('Exit')]]

    window = sg.Window('Window Title', layout)
    window.finalize()

    # Draw lines on the field
    for x in range(1, 6):
        field.draw_line([120*x, 720], [120*x, 0], 'black')
        field.draw_line([0, 120*x], [720, 120*x], 'black')

    # f = open("testFile.txt", "x") This can be used to create a file. Very easy. Nice.

    # Fields used during the loop
    selectingStartPoint = False
    addingPoint = False
    simulating = False
    pathEditUpdated = False
    startPoint_circle = None
    startPoint_line = None
    robot_rectangle = None
    robot_line = None
    point_lines = []
    points = []
    convertedPoints = []
    paths = [None]
    selectedPathNum = None

    window['-START_X_TEXT-'].hide_row()
    window['-FINAL_X_TEXT-'].hide_row()
    window['-DESELECT_BUTTON-'].hide_row()
    while True:  # Event Loop
        event, values = window.read()  # can also be written as event, values = window()

        # Print to console the event and values
        print('Event:')
        print(event)
        print('Values:')
        print(values)
        print()

        # Exit Condition
        if event is None or event == 'Exit':
            break

        # Choose which path to edit
        if event == '-EDIT_PATH_BUTTON-':
            counter = 0
            pathEditUpdated = False
            for p in paths:
                counter += 1
                if len(values['-PATH_LIST-']) > 0 and values['-PATH_LIST-'][0] == p:
                    window['-PATH_INFO-'].update('Path #' + str(counter))
                    selectedPathNum = counter

        if event == '-DESELECT_BUTTON-':
            window['-PATH_INFO-'].update('None')
            window['-START_X_TEXT-'].hide_row()
            window['-FINAL_X_TEXT-'].hide_row()
            window['-DESELECT_BUTTON-'].hide_row()
            selectedPathNum = None

        if selectedPathNum is not None and not pathEditUpdated:
            window['-START_X_TEXT-'].unhide_row()
            window['-FINAL_X_TEXT-'].unhide_row()
            window['-DESELECT_BUTTON-'].unhide_row()
            window['-START_X_INPUT-'].update(value=convertedPoints[selectedPathNum-1][0])
            window['-START_Y_INPUT-'].update(value=convertedPoints[selectedPathNum - 1][1])
            window['-FINAL_X_INPUT-'].update(value=convertedPoints[selectedPathNum][0])
            window['-FINAL_Y_INPUT-'].update(value=convertedPoints[selectedPathNum][1])
            pathEditUpdated = True

        if pathEditUpdated:
            if event == '-START_X_INPUT-':
                points[selectedPathNum - 1][0] = float(hf.clean_coordinates(values['-START_X_INPUT-'])) * 5 + (720/2)
            elif event == '-START_Y_INPUT-':
                points[selectedPathNum - 1][1] = float(hf.clean_coordinates(values['-START_Y_INPUT-'])) * 5 + (720/2)
            elif event == '-FINAL_X_INPUT-':
                points[selectedPathNum][0] = float(hf.clean_coordinates(values['-FINAL_X_INPUT-'])) * 5 + (720/2)
            elif event == '-FINAL_Y_INPUT-':
                points[selectedPathNum][1] = float(hf.clean_coordinates(values['-FINAL_Y_INPUT-'])) * 5 + (720/2)

        # Select start point and draw the circle for it and add it to points
        if event == '-START_POINT_BUTTON-':
            selectingStartPoint = True
        if selectingStartPoint:
            if event == '-FIELD-':
                field.delete_figure(startPoint_circle)
                startPoint_circle = field.draw_circle([values['-FIELD-'][0], values['-FIELD-'][1]], 5)
                if len(points) > 0:
                    points[0] = ([values['-FIELD-'][0], values['-FIELD-'][1]])
                else:
                    points.append([values['-FIELD-'][0], values['-FIELD-'][1]])
                selectingStartPoint = False

        # Select next point and and it to points
        if event == '-ADD_POINT_BUTTON-' and len(points) > 0:
            addingPoint = True
        if addingPoint:
            if event == '-FIELD-':
                points.append([values['-FIELD-'][0], values['-FIELD-'][1]])
                addingPoint = False

        # Add Points to Paths, then display them in the path list
        paths = []
        convertedPoints = hf.convert_coordinates_to_inches(points, pixels_per_inch=5, field_length_inches=144)
        for i in range(1, len(points)):
            paths.append('Path #' + str(i) + ': ' + hf.generate_path(convertedPoints[i-1], convertedPoints[i], 40, 90))
        window['-PATH_LIST-'].update(values=paths)

        # Draw lines between all points
        if len(points) > 0:
            field.delete_figure(startPoint_circle)
            startPoint_circle = field.draw_circle(points[0], 5)
        if len(points) > 1:
            lineColor = 'black'
            if selectedPathNum == 1:
                lineColor = 'yellow'
            field.delete_figure(startPoint_line)
            startPoint_line = field.draw_line(points[0], points[1], color=lineColor, width=2.0)
        for i in range(2, len(points)):
            if len(point_lines) > i-2:
                field.delete_figure(point_lines[i-2])
            lineColor = 'black'
            if selectedPathNum == i:
                lineColor = 'yellow'
            if len(point_lines) < i-1:
                point_lines.append(None)
            point_lines[i-2] = (field.draw_line(points[i-1], points[i], color=lineColor, width=2.0))

        # Simulate the robot running through the path
        if event == '-SIMULATE_BUTTON-':
            simulating = True
        if simulating:
            for i in range(1, len(points)):
                deltas = hf.calculate_movement_per_frame(points[i-1], points[i], inches_per_second=48, frames_per_second=25, pixels_per_inch=5)
                num_movements = math.sqrt((points[i][0] - points[i-1][0])**2 + (points[i][1] - points[i-1][1])**2) / math.hypot(deltas[0], deltas[1])
                x = points[i-1][0]
                y = points[i-1][1]
                for j in range(0, int(num_movements)):
                    start_time = time.time()
                    x += deltas[0]
                    y += deltas[1]
                    field.delete_figure(robot_rectangle)
                    field.delete_figure(robot_line)
                    robot_rectangle = field.draw_rectangle(bottom_right=[x+45, y-45], top_left=[x-45, y+45], line_color='black')
                    robot_line = field.draw_line([x+45, y], [x+10, y], 'blue', width=4.0)
                    window.refresh()
                    sleepTime = 1/25 - (time.time() - start_time)
                    if sleepTime < 0:
                        sleepTime = 0
                    time.sleep(sleepTime)
            simulating = False

        # Draw robot on the field
        if len(points) > 0:
            field.delete_figure(robot_rectangle)
            field.delete_figure(robot_line)
            bRightRobotRect = [points[0][0] + 45, points[0][1] - 45]
            tLeftRobotRect = [points[0][0] - 45, points[0][1] + 45]
            robotLinePoints = [[points[0][0] + 45, points[0][1]], [points[0][0] + 10, points[0][1]]]
            robot_rectangle = field.draw_rectangle(bottom_right=bRightRobotRect, top_left=tLeftRobotRect, line_color='black')
            robot_line = field.draw_line(robotLinePoints[0], robotLinePoints[1], 'blue', width=4.0)

    window.close()


