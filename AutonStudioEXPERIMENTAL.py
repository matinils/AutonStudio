import PySimpleGUI as sg
from PySimpleGUI import theme_previewer

import HelperFunctions as hf
import math
import time

if __name__ == '__main__':

    sg.theme('Dark Green')  # please make your windows colorful
    logo = sg.Image('resources/autonStudioLogo.png')

    drive_selection = [sg.Listbox(['Mechanum with Odometry', 'Mechanum without Odometry', 'H-Drive with Odometry',
                                 'H-Drive without Odometry'], enable_events=True, key='-DRIVETRAIN_SELECTION-', size=(25,4))]


    menu_column = [[sg.Text('\n\n')],
                   [sg.Button('Click to Continue to Studio', key='-CONTINUE_BUTTON-')],
                   [sg.Button('Add Configuration', key='-CONFIG_BUTTON-')],
                   drive_selection]

    layout2 = [[sg.Text('Welcome to Auton Studio', text_color='Black', font='Courier 20 bold', justification='center',
                    size=[32,1])], [sg.Text('...where your lazy ass doesn\'t have to write the fucking code, because we already wrote it all for you.', text_color='Black', font='Courier 8', justification='center',
                    size=[72,2])],[logo, sg.Column(menu_column)]]

    title_window = sg.Window('Title Screen', layout2)

     # f = open("testFile.txt", "x") This can be used to create a file. Very easy. Nice.

    # Fields used during the loop
    drivetrain = None
    selectingStartPoint = False
    addingPoint = False
    addingTurn = False
    simulating = False
    pathEditUpdated = False
    turnEditUpdated = False
    startPoint_circle = None
    startPoint_line = None
    robot_rectangle = None
    robot_line1 = None
    robot_line2 = None
    robot_line3 = None
    robot_line4 = None
    robot_point = None
    robot_polygon = None
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
    startHeading = 0.0


    studioWindowActive = False
    while True:
        event0, values0 = title_window.read()

        print(event0)

        if event0 is None or event0 == 'Exit:':
            break

        fieldSave = None
        if not studioWindowActive and event0 == '-CONTINUE_BUTTON-':
            title_window.Hide()
            studioWindowActive = True

            pathInfo = sg.Text('None', key='-PATH_INFO-', size=[20, 1])
            turnInfo = sg.Text('None', key='-TURN_INFO-', size=[20, 1])

            # Each inch is five pixels
            if fieldSave is None:
                field = sg.Graph(canvas_size=[720, 720], graph_bottom_left=[0, 0], graph_top_right=[720, 720],
                            background_color='#BAB8B8', key='-FIELD-', enable_events=True)
            else:
                field = fieldSave



            paths_tab = [[sg.Listbox(values=[], size=(50, 6), key='-PATH_LIST-')],
                         [sg.Button('Edit Path', key='-EDIT_PATH_BUTTON-'),
                          sg.Button('Round All', key='-ROUND_ALL_BUTTON-')],
                         [sg.Text('Selected Path:'), pathInfo],
                         [sg.Text('Start X', key='-START_X_TEXT-'),
                          sg.InputText(enable_events=True, size=[10, 1], key='-START_X_INPUT-'),
                          sg.Text('   Start Y', key='-START_Y_TEXT-'),
                          sg.InputText(enable_events=True, size=[10, 1], key='-START_Y_INPUT-')],
                         [sg.Text('Final X', key='-FINAL_X_TEXT-'),
                          sg.InputText(enable_events=True, size=[10, 1], key='-FINAL_X_INPUT-'),
                          sg.Text('   Final Y', key='-FINAL_Y_TEXT-'),
                          sg.InputText(enable_events=True, size=[10, 1], key='-FINAL_Y_INPUT-')],
                         [sg.Button('Deselect', key='-DESELECT_BUTTON-')]]

            turns_tab = [[sg.Listbox(values=[], size=(50, 6), key='-TURN_LIST-')],
                         [sg.Button('Edit Turn', key='-EDIT_TURN_BUTTON-')],
                         [sg.Text('Selected Turn:'), turnInfo],
                         [sg.Text('Angle', key='-ANGLE_TEXT-'),
                          sg.InputText(enable_events=True, size=[10, 1], key='-ANGLE_INPUT-')]]

            editing_tabGroup = sg.TabGroup(
                layout=[[sg.Tab(layout=paths_tab, title='Paths'), sg.Tab(layout=turns_tab, title='Turns')]])

            main_column = [[sg.Button('Set Start Point', key='-START_POINT_BUTTON-')],
                           [sg.Button('Add Point', key='-ADD_POINT_BUTTON-')],
                           [sg.Button('Add Turn', key='-ADD_TURN_BUTTON-')],
                           [sg.Button('Add Robot Operation')],
                           [sg.Button('Simulate Robot Run', key='-SIMULATE_BUTTON-')],
                           [sg.Text('\nEdit Menu:')],
                           [editing_tabGroup], [sg.Text('\n')], [sg.Button('Clear Field', key='-CLEAR_FIELD_BUTTON-')]]

            layout = [[field, sg.Column(main_column)],
                      [sg.Button('Back', key='-BACK_BUTTON-'), sg.Button('Exit')]]
            studio_window = sg.Window('EXPERIMENTAL GUI', layout)

            studio_window.finalize()

            # Hide certain elements
            studio_window['-START_X_TEXT-'].hide_row()
            studio_window['-FINAL_X_TEXT-'].hide_row()
            studio_window['-DESELECT_BUTTON-'].hide_row()
            studio_window['-ANGLE_TEXT-'].hide_row()

            for z in range (1, 31):
                field.draw_line([24 * z, 720], [24 * z, 0], 'light grey')
                field.draw_line([0, 24 * z], [720, 24 * z], 'light grey')
            for x in range(1, 6):
                field.draw_line([120 * x, 720], [120 * x, 0], 'black')
                field.draw_line([0, 120 * x], [720, 120 * x], 'black')


        while True and studioWindowActive:  # Event Loop
            event1, values1 = studio_window.read()  # can also be written as event, values = window()

            # Print to console the event and values
            print('Event:')
            print(event1)
            print('Values:')
            print(values1)
            print()

            # Exit Condition
            if event1 is None or event1 == 'Exit':
                studio_window.close()
                title_window.close()
                break

            # Back Condition
            if event1 is None or event1 == '-BACK_BUTTON-':
                studioWindowActive = False
                studio_window.Close()
                title_window.UnHide()
                fieldSave = field
                break

            # Clears all field elements and paths
            if event1 == '-CLEAR_FIELD_BUTTON-' and len(points) > 0:
                field.delete_figure(robot_rectangle)
                field.delete_figure(robot_point)
                field.delete_figure(startPoint_circle)
                for tc in turn_circles:
                    field.delete_figure(tc)
                for tic in turnIndicator_circles:
                    field.delete_figure(tic)
                field.delete_figure(startPoint_line)
                for pl in point_lines:
                    field.delete_figure(pl)
                for tit in turnIndicator_text:
                    field.delete_figure(tit)
                points.clear()
                point_lines.clear()
                turn_circles.clear()
                turnIndicator_circles.clear()
                turnIndicator_text.clear()
                turns.clear()
                convertedPoints.clear()
                paths.clear()
                turnStrings.clear()
                fieldSave = None

            # Choose which path to edit
            if event1 == '-EDIT_PATH_BUTTON-':
                counter = 0
                pathEditUpdated = False
                for p in paths:
                    counter += 1
                    if len(values1['-PATH_LIST-']) > 0 and values1['-PATH_LIST-'][0] == p:
                        studio_window['-PATH_INFO-'].update('Path #' + str(counter))
                        selectedPathNum = counter

            # Show the entry fields for editing the path
            if selectedPathNum is not None and not pathEditUpdated:
                studio_window['-START_X_TEXT-'].unhide_row()
                studio_window['-FINAL_X_TEXT-'].unhide_row()
                studio_window['-DESELECT_BUTTON-'].unhide_row()
                studio_window['-START_X_INPUT-'].update(value=convertedPoints[selectedPathNum - 1][0])
                studio_window['-START_Y_INPUT-'].update(value=convertedPoints[selectedPathNum - 1][1])
                studio_window['-FINAL_X_INPUT-'].update(value=convertedPoints[selectedPathNum][0])
                studio_window['-FINAL_Y_INPUT-'].update(value=convertedPoints[selectedPathNum][1])
                pathEditUpdated = True
            # Change the values of a point based on what was entered into the entry field
            if pathEditUpdated:
                if event1 == '-START_X_INPUT-':
                    points[selectedPathNum - 1][0] = float(hf.clean_coordinates(values1['-START_X_INPUT-'])) * 5 + (720 / 2)
                elif event1 == '-START_Y_INPUT-':
                    points[selectedPathNum - 1][1] = float(hf.clean_coordinates(values1['-START_Y_INPUT-'])) * 5 + (720 / 2)
                elif event1 == '-FINAL_X_INPUT-':
                    points[selectedPathNum][0] = float(hf.clean_coordinates(values1['-FINAL_X_INPUT-'])) * 5 + (720 / 2)
                elif event1 == '-FINAL_Y_INPUT-':
                    points[selectedPathNum][1] = float(hf.clean_coordinates(values1['-FINAL_Y_INPUT-'])) * 5 + (720 / 2)

            # Rounds all the points to the nearest inch
            if event1 == '-ROUND_ALL_BUTTON-':
                for i in range(0, len(convertedPoints)):
                    points[i][0] = round(convertedPoints[i][0]) * 5 + (720/2)
                    points[i][1] = round(convertedPoints[i][1]) * 5 + (720 / 2)

            # Deselect the current path
            if event1 == '-DESELECT_BUTTON-':
                studio_window['-PATH_INFO-'].update('None')
                studio_window['-START_X_TEXT-'].hide_row()
                studio_window['-FINAL_X_TEXT-'].hide_row()
                studio_window['-DESELECT_BUTTON-'].hide_row()
                selectedPathNum = None

            # Choose which turn to edit
            if event1 == '-EDIT_TURN_BUTTON-':
                counter = 0
                turnEditUpdated = False
                for t in turnStrings:
                    counter += 1
                    if len(values1['-TURN_LIST-']) > 0 and values1['-TURN_LIST-'][0] == t:
                        studio_window['-TURN_INFO-'].update('Turn #' + str(counter))
                        selectedTurnNum = counter

            # Show the entry fields for editing the turn
            if selectedTurnNum is not None and not turnEditUpdated:
                studio_window['-ANGLE_TEXT-'].unhide_row()
                studio_window['-ANGLE_INPUT-'].update(value=turns[selectedTurnNum - 1][1])
                turnEditUpdated = True
            # Change the angle value of a turn based on what was entered into the entry field
            if turnEditUpdated:
                if event1 == '-ANGLE_INPUT-':
                    turns[selectedTurnNum - 1][1] = float(hf.clean_coordinates(values1['-ANGLE_INPUT-']))

            # Select start point and draw the circle for it and add it to points
            if event1 == '-START_POINT_BUTTON-':
                selectingStartPoint = True
                addingPoint = False
                addingTurn = False
                simulating = False
            if selectingStartPoint:
                if event1 == '-FIELD-':
                    field.delete_figure(startPoint_circle)
                    startPoint_circle = field.draw_circle([values1['-FIELD-'][0], values1['-FIELD-'][1]], 5)
                    if len(points) > 0:
                        points[0] = ([values1['-FIELD-'][0], values1['-FIELD-'][1]])
                    else:
                        points.append([values1['-FIELD-'][0], values1['-FIELD-'][1]])
                    startHeading = float(hf.clean_coordinates(sg.PopupGetText(message='Enter start heading, 0 is straight up, 90 is to the right, -90 is to the left', title='Heading selection')))
                    selectingStartPoint = False

            # Select next point and and it to list of points
            if event1 == '-ADD_POINT_BUTTON-' and len(points) > 0:
                addingPoint = True
                selectingStartPoint = False
                addingTurn = False
                simulating = False
            if addingPoint:
                if event1 == '-FIELD-':
                    points.append([values1['-FIELD-'][0], values1['-FIELD-'][1]])
                    addingPoint = False

            # Select a spot to add a turn and add it to list of turns
            if event1 == '-ADD_TURN_BUTTON-':
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
                if event1 == '-FIELD-':
                    for i in range(0, len(points)):
                        allowPointToBeSelected = True
                        for t in turns:
                            if t[0] == i:
                                allowPointToBeSelected = False
                        if abs(values1['-FIELD-'][0] - points[i][0]) < 10 and abs(values1['-FIELD-'][1]) - points[i][1] < 10 and allowPointToBeSelected:
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
            if event1 == '-SIMULATE_BUTTON-':
                simulating = True
                addingTurn = False
                addingPoint = False
                selectingStartPoint = False
            if simulating:
                prevTurn = None
                robotCBr = [45, -45]  # Bottom right corner and go clockwise
                robotCBl = [-45, -45]
                robotCTl = [-45, 45]
                robotCTr = [45, 45]
                robotPolygonPoints = [robotCBr, robotCBl, robotCTl, robotCTr]
                rot_deltas_final = [[[45], [-45]], [[-45], [-45]], [[-45], [45]], [[45], [45]]]
                if abs(startHeading - 0.0) > 0:
                    rot_deltas_final = hf.calculate_rotation_per_frame(points=robotPolygonPoints, angle1=0.0, angle2=startHeading, degrees_per_second=45, frames_per_second=60)
                for i in range(1, len(points)):
                    deltas = hf.calculate_movement_per_frame(points[i-1], points[i], inches_per_second=48, frames_per_second=60, pixels_per_inch=5)
                    num_movements = math.sqrt((points[i][0] - points[i-1][0])**2 + (points[i][1] - points[i-1][1])**2) / math.hypot(deltas[0], deltas[1])
                    x = points[i-1][0]
                    y = points[i-1][1]
                    for t in turns:
                        if t[0] == i - 1:
                            if prevTurn is None:
                                angle1 = startHeading
                            else:
                                angle1 = prevTurn[1]
                            robotCBr = [45, -45]  # Bottom right corner and go clockwise
                            robotCBl = [-45, -45]
                            robotCTl = [-45, 45]
                            robotCTr = [45, 45]
                            robotPolygonPoints = [robotCBr, robotCBl, robotCTl, robotCTr]
                            rot_deltas = hf.calculate_rotation_per_frame(points=robotPolygonPoints, angle1=angle1, angle2=t[1], degrees_per_second=45, frames_per_second=60)
                            if abs(float(t[1]) - float(angle1)) > 0:
                                rot_deltas_final = rot_deltas.copy()
                            prevTurn = t
                            for j in range(0, len(rot_deltas[0][0])-1):
                                start_time = time.time()
                                field.delete_figure(robot_polygon)
                                field.delete_figure(robot_point)
                                robotCBr = [x + rot_deltas_final[0][0][j], y + rot_deltas_final[0][1][j]]  # Bottom right corner and go clockwise
                                robotCBl = [x + rot_deltas_final[1][0][j], y + rot_deltas_final[1][1][j]]
                                robotCTl = [x + rot_deltas_final[2][0][j], y + rot_deltas_final[2][1][j]]
                                robotCTr = [x + rot_deltas_final[3][0][j], y + rot_deltas_final[3][1][j]]
                                robotPolygonPoints = [robotCBr, robotCBl, robotCTl, robotCTr]
                                robot_polygon = field.draw_polygon(robotPolygonPoints, line_color='black', line_width='3', fill_color='')
                                robotLinePoints = [[((robotCTr[0] + robotCBr[0]) / 2.0), ((robotCTr[1] + robotCBr[1]) / 2.0)], [((robotCTr[0] + robotCBr[0]) / 2.0) - 20, ((robotCTr[1] + robotCBr[1]) / 2.0) - 20]]
                                robot_point = field.draw_point(point=robotLinePoints[0], color='yellow', size=15)
                                studio_window.refresh()
                                sleepTime = 1 / 60 - (time.time() - start_time)
                                if sleepTime < 0:
                                    sleepTime = 0
                                time.sleep(sleepTime)
                    for j in range(0, int(num_movements)):
                        start_time = time.time()
                        x += deltas[0]
                        y += deltas[1]
                        field.delete_figure(robot_polygon)
                        field.delete_figure(robot_point)
                        robotCBr = [x + rot_deltas_final[0][0][-1], y + rot_deltas_final[0][1][-1]]  # Bottom right corner and go clockwise
                        robotCBl = [x + rot_deltas_final[1][0][-1], y + rot_deltas_final[1][1][-1]]
                        robotCTl = [x + rot_deltas_final[2][0][-1], y + rot_deltas_final[2][1][-1]]
                        robotCTr = [x + rot_deltas_final[3][0][-1], y + rot_deltas_final[3][1][-1]]
                        robotPolygonPoints = [robotCBr, robotCBl, robotCTl, robotCTr]
                        robot_polygon = field.draw_polygon(robotPolygonPoints, line_color='black', line_width='3', fill_color='')
                        robotPoint = [((robotCTr[0] + robotCBr[0]) / 2.0), ((robotCTr[1] + robotCBr[1]) / 2.0)]
                        if startHeading == 0 and rot_deltas_final == [[[45], [-45]], [[-45], [-45]], [[-45], [45]], [[45], [45]]]:
                            robotPoint = [((robotCTr[0] + robotCTl[0]) / 2.0), ((robotCTr[1] + robotCTl[1]) / 2.0)]
                        robot_point = field.draw_point(point=robotPoint, color='yellow', size=15)
                        studio_window.refresh()
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
            studio_window['-PATH_LIST-'].update(values=paths)
            turnStrings = []
            turns = hf.sort_turns(turns)
            for i in range(0, len(turns)):
                turnStrings.append('Turn #' + str(i+1) + ": " + hf.generate_turn_string(turns[i], convertedPoints))
            studio_window['-TURN_LIST-'].update(values=turnStrings)



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

            # Draw robot on the field and ensures the robot cannot be magically clipping through
            # the field walls (robot starts touching field wall if outside boundary)
            if len(points) > 0:
                field.delete_figure(robot_polygon)
                field.delete_figure(robot_point)
                robotCBr = [45, -45]  # Bottom right corner and go clockwise
                robotCBl = [-45, -45]
                robotCTl = [-45, 45]
                robotCTr = [45, 45]
                robotPolygonPoints = [robotCBr, robotCBl, robotCTl, robotCTr]
                rot_deltas_final = [[[45], [-45]], [[-45], [-45]], [[-45], [45]], [[45], [45]]]
                if abs(startHeading - 0.0) > 0:
                    rot_deltas_final = hf.calculate_rotation_per_frame(points=robotPolygonPoints, angle1=0.0, angle2=startHeading, degrees_per_second=45, frames_per_second=60)
                robotCBr = [points[0][0] + rot_deltas_final[0][0][-1], points[0][1] + rot_deltas_final[0][1][-1]]  # Bottom right corner and go clockwise
                robotCBl = [points[0][0] + rot_deltas_final[1][0][-1], points[0][1] + rot_deltas_final[1][1][-1]]
                robotCTl = [points[0][0] + rot_deltas_final[2][0][-1], points[0][1] + rot_deltas_final[2][1][-1]]
                robotCTr = [points[0][0] + rot_deltas_final[3][0][-1], points[0][1] + rot_deltas_final[3][1][-1]]
                robotPolygonPoints = [robotCBr, robotCBl, robotCTl, robotCTr]
                robot_polygon = field.draw_polygon(robotPolygonPoints, line_color='black', line_width='3', fill_color='')
                robotPoint = [((robotCTr[0] + robotCBr[0]) / 2.0), ((robotCTr[1] + robotCBr[1]) / 2.0)]
                if startHeading == 0:
                    robotPoint = [((robotCTr[0] + robotCTl[0]) / 2.0), ((robotCTr[1] + robotCTl[1]) / 2.0)]
                robot_point = field.draw_point(point=robotPoint, color='yellow', size=15)

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
                    if len(point_lines) > i - 2:
                        field.delete_figure(point_lines[i - 2])
                    lineColor = 'black'
                    if selectedPathNum == i:
                        lineColor = 'yellow'
                    if len(point_lines) < i - 1:
                        point_lines.append(None)
                    point_lines[i - 2] = (field.draw_line(points[i - 1], points[i], color=lineColor, width=2.0))




    title_window.close()


