import PySimpleGUI as sg
import HelperFunctions as hf
import math
import time

if __name__ == '__main__':

    sg.theme('Dark Green')  # please make your windows colorful

    pathInfo = sg.Text('None', key='-PATH_INFO-', size=[20, 1])
    turnInfo = sg.Text('None', key='-TURN_INFO-', size=[20, 1])

    # Each inch is five pixels
    field = sg.Graph(canvas_size=[720, 720], graph_bottom_left=[0, 0], graph_top_right=[720, 720], background_color='#BAB8B8', key='-FIELD-', enable_events=True)

    paths_tab = [[sg.Listbox(values=[], size=(50, 6), key='-PATH_LIST-')],
                   [sg.Button('Edit Path', key='-EDIT_PATH_BUTTON-'), sg.Button('Round All', key='-ROUND_ALL_BUTTON-')],
                   [sg.Text('Selected Path:'), pathInfo],
                   [sg.Text('Start X', key='-START_X_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-START_X_INPUT-'), sg.Text('   Start Y', key='-START_Y_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-START_Y_INPUT-')],
                   [sg.Text('Final X', key='-FINAL_X_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-FINAL_X_INPUT-'), sg.Text('   Final Y', key='-FINAL_Y_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-FINAL_Y_INPUT-')],
                   [sg.Button('Deselect', key='-DESELECT_BUTTON-')]]

    turns_tab = [[sg.Listbox(values=[], size=(50, 6), key='-TURN_LIST-')],
                 [sg.Button('Edit Turn', key='-EDIT_TURN_BUTTON-')],
                 [sg.Text('Selected Turn:'), turnInfo],
                 [sg.Text('Angle', key='-ANGLE_TEXT-'), sg.InputText(enable_events=True, size=[10, 1], key='-ANGLE_INPUT-')]]

    editing_tabGroup = sg.TabGroup(layout=[[sg.Tab(layout=paths_tab, title='Paths'), sg.Tab(layout=turns_tab, title='Turns')]])

    main_column = [[sg.Button('Set Start Point', key='-START_POINT_BUTTON-')],
                   [sg.Button('Add Point', key='-ADD_POINT_BUTTON-')],
                   [sg.Button('Add Turn', key='-ADD_TURN_BUTTON-')],
                   [sg.Button('Add Robot Operation')],
                   [sg.Button('Simulate Robot Run', key='-SIMULATE_BUTTON-')],
                   [sg.Text('\nEdit Menu:')],
                   [editing_tabGroup]]

    layout = [[field, sg.Column(main_column)],
              [sg.Button('Exit')]]

    window = sg.Window('Window Title', layout)
    window.finalize()

    # Draw lines on the field
    for x in range(1, 6):
        field.draw_line([120 * x, 720], [120 * x, 0], 'black')
        field.draw_line([0, 120 * x], [720, 120 * x], 'black')

    # Hide certain elements
    window['-START_X_TEXT-'].hide_row()
    window['-FINAL_X_TEXT-'].hide_row()
    window['-DESELECT_BUTTON-'].hide_row()
    window['-ANGLE_TEXT-'].hide_row()

    # f = open("testFile.txt", "x") This can be used to create a file. Very easy. Nice.

    # Fields used during the loop
    selectingStartPoint = False
    addingPoint = False
    addingTurn = False
    simulating = False
    pathEditUpdated = False
    turnEditUpdated = False
    startPoint_circle = None
    startPoint_line = None
    robot_rectangle = None
    robot_line = None
    point_lines = []
    turn_circles = []
    turnIndicator_circles = []
    turnIndicator_text = []
    points = []
    turns = []
    convertedPoints = []
    paths = [None]
    turnStrings = [None]
    selectedPathNum = None
    selectedTurnNum = None

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

        # Show the entry fields for editing the path
        if selectedPathNum is not None and not pathEditUpdated:
            window['-START_X_TEXT-'].unhide_row()
            window['-FINAL_X_TEXT-'].unhide_row()
            window['-DESELECT_BUTTON-'].unhide_row()
            window['-START_X_INPUT-'].update(value=convertedPoints[selectedPathNum-1][0])
            window['-START_Y_INPUT-'].update(value=convertedPoints[selectedPathNum - 1][1])
            window['-FINAL_X_INPUT-'].update(value=convertedPoints[selectedPathNum][0])
            window['-FINAL_Y_INPUT-'].update(value=convertedPoints[selectedPathNum][1])
            pathEditUpdated = True
        # Change the values of a point based on what was entered into the entry field
        if pathEditUpdated:
            if event == '-START_X_INPUT-':
                points[selectedPathNum - 1][0] = float(hf.clean_coordinates(values['-START_X_INPUT-'])) * 5 + (720/2)
            elif event == '-START_Y_INPUT-':
                points[selectedPathNum - 1][1] = float(hf.clean_coordinates(values['-START_Y_INPUT-'])) * 5 + (720/2)
            elif event == '-FINAL_X_INPUT-':
                points[selectedPathNum][0] = float(hf.clean_coordinates(values['-FINAL_X_INPUT-'])) * 5 + (720/2)
            elif event == '-FINAL_Y_INPUT-':
                points[selectedPathNum][1] = float(hf.clean_coordinates(values['-FINAL_Y_INPUT-'])) * 5 + (720/2)

        # Rounds all the points to the nearest inch
        if event == '-ROUND_ALL_BUTTON-':
            for i in range(0, len(convertedPoints)):
                points[i][0] = round(convertedPoints[i][0]) * 5 + (720/2)
                points[i][1] = round(convertedPoints[i][1]) * 5 + (720 / 2)

        # Deselect the current path
        if event == '-DESELECT_BUTTON-':
            window['-PATH_INFO-'].update('None')
            window['-START_X_TEXT-'].hide_row()
            window['-FINAL_X_TEXT-'].hide_row()
            window['-DESELECT_BUTTON-'].hide_row()
            selectedPathNum = None

        # Choose which turn to edit
        if event == '-EDIT_TURN_BUTTON-':
            counter = 0
            turnEditUpdated = False
            for t in turnStrings:
                counter += 1
                if len(values['-TURN_LIST-']) > 0 and values['-TURN_LIST-'][0] == t:
                    window['-TURN_INFO-'].update('Turn #' + str(counter))
                    selectedTurnNum = counter

        # Show the entry fields for editing the turn
        if selectedTurnNum is not None and not turnEditUpdated:
            window['-ANGLE_TEXT-'].unhide_row()
            window['-ANGLE_INPUT-'].update(value=turns[selectedTurnNum-1][1])
            turnEditUpdated = True
        # Change the angle value of a turn based on what was entered into the entry field
        if turnEditUpdated:
            if event == '-ANGLE_INPUT-':
                turns[selectedTurnNum - 1][1] = float(hf.clean_coordinates(values['-ANGLE_INPUT-']))

        # Select start point and draw the circle for it and add it to points
        if event == '-START_POINT_BUTTON-':
            selectingStartPoint = True
            addingPoint = False
            addingTurn = False
            simulating = False
        if selectingStartPoint:
            if event == '-FIELD-':
                field.delete_figure(startPoint_circle)
                startPoint_circle = field.draw_circle([values['-FIELD-'][0], values['-FIELD-'][1]], 5)
                if len(points) > 0:
                    points[0] = ([values['-FIELD-'][0], values['-FIELD-'][1]])
                else:
                    points.append([values['-FIELD-'][0], values['-FIELD-'][1]])
                selectingStartPoint = False

        # Select next point and and it to list of points
        if event == '-ADD_POINT_BUTTON-' and len(points) > 0:
            addingPoint = True
            selectingStartPoint = False
            addingTurn = False
            simulating = False
        if addingPoint:
            if event == '-FIELD-':
                points.append([values['-FIELD-'][0], values['-FIELD-'][1]])
                addingPoint = False

        # Select a spot to add a turn and add it to list of turns
        if event == '-ADD_TURN_BUTTON-':
            addingTurn = True
            addingPoint = False
            selectingStartPoint = False
            simulating = False
        if addingTurn:
            if len(turn_circles) == 0:
                for i in range(0, len(points)):
                    drawCircle = True
                    for t in turns:
                        if t[0] == i:
                            drawCircle = False
                    if drawCircle:
                        turn_circles.append(field.draw_circle(points[i], 10, fill_color='black'))
            if event == '-FIELD-':
                for i in range(0, len(points)):
                    allowPointToBeSelected = True
                    for t in turns:
                        if t[0] == i:
                            allowPointToBeSelected = False
                    if abs(values['-FIELD-'][0] - points[i][0]) < 10 and abs(values['-FIELD-'][1]) - points[i][1] < 10 and allowPointToBeSelected:
                        angle = sg.PopupGetText('Enter turn angle in degrees', title='Turn Angle Entry')
                        if angle is not None:
                            turns.append([i, hf.clean_coordinates(angle)])
                            addingTurn = False
                        else:
                            sg.PopupAnnoying('ERROR: Please enter a value')
        if not addingTurn:
            if len(turn_circles) > 0:
                for c in turn_circles:
                    field.delete_figure(c)
                turn_circles.clear()

        # Simulate the robot running through the path
        if event == '-SIMULATE_BUTTON-':
            simulating = True
            addingTurn = False
            addingPoint = False
            selectingStartPoint = False
        if simulating:
            for i in range(1, len(points)):
                deltas = hf.calculate_movement_per_frame(points[i-1], points[i], inches_per_second=48, frames_per_second=60, pixels_per_inch=5)
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
                    sleepTime = 1/60 - (time.time() - start_time)
                    if sleepTime < 0:
                        sleepTime = 0
                    time.sleep(sleepTime)
            simulating = False

        # Add points and turns to list of paths and turns, then display them in the path and turn list
        paths = []
        convertedPoints = hf.convert_coordinates_to_inches(points, pixels_per_inch=5, field_length_inches=144)
        for i in range(1, len(points)):
            paths.append('Path #' + str(i) + ': ' + hf.generate_path_string(convertedPoints[i - 1], convertedPoints[i], 40, 90))
        window['-PATH_LIST-'].update(values=paths)
        turnStrings = []
        turns = hf.sort_turns(turns)
        for i in range(0, len(turns)):
            turnStrings.append('Turn #' + str(i+1) + ": " + hf.generate_turn_string(turns[i], convertedPoints))
        window['-TURN_LIST-'].update(values=turnStrings)

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

        # Draw turn indicators
        for i in range(0, len(turns)):
            if len(turnIndicator_circles) > i:
                field.delete_figure(turnIndicator_circles[i])
                field.delete_figure(turnIndicator_text[i])
            if len(turnIndicator_circles) < i + 1:
                turnIndicator_circles.append(None)
                turnIndicator_text.append(None)
            turnIndicator_circles[i] = field.draw_circle(points[turns[i][0]], 5, fill_color='black')
            turnIndicator_text[i] = field.draw_text(text=str(turns[i][1]) + '°', location=[points[turns[i][0]][0]+10, points[turns[i][0]][1]+10], color='dark blue')

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


