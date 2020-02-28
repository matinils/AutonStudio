import PySimpleGUI as sg
import HelperFunctions as hf

if __name__ == '__main__':

    sg.theme('Dark Blue 3')  # please make your windows colorful

    pathInfo = sg.Text('None Selected', key='-PATH_INFO-', size=[50, 1])

    # Each inch is five pixels
    field = sg.Graph(canvas_size=[720, 720], graph_bottom_left=[0, 0], graph_top_right=[720, 720], background_color='#BAB8B8', key='-FIELD-', enable_events=True)

    col = [[sg.Button('Set Start Point', key='-START_POINT_BUTTON-')],
           [sg.Button('Add Point to Path', key='-ADD_POINT_BUTTON-')],
           [sg.Button('Add Turn')],
           [sg.Button('Add Robot Operation')],
           [sg.Text('\nSelect Path to Edit')],
           [sg.Listbox(values=[], size=(50, 6), key='-PATH_LIST-')],
           [sg.Button('Edit Path')],
           [sg.Text('Path Being Edited:')],
           [pathInfo]]

    layout = [[field, sg.Column(col)],
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
    startPoint_circle = None
    startPoint_line = None
    points = []
    paths = [None]

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

        for p in paths:
            if len(values['-PATH_LIST-']) > 0 and values['-PATH_LIST-'][0] == p and event == 'Edit Path':
                window['-PATH_INFO-'].update(p)

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
        for i in range(1, len(points)):
            paths.append('Path #' + str(i) + ': ' + hf.generate_path(points[i-1], points[i], 40, 90))
        window['-PATH_LIST-'].update(values=paths)

        # Draw lines between all points
        if len(points) > 1:
            field.delete_figure(startPoint_line)
            startPoint_line = field.draw_line(points[0], points[1], 'black', width=2.0)
        for i in range(2, len(points)):
            field.draw_line(points[i-1], points[i], 'black', width=2.0)

    window.close()


