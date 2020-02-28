import PySimpleGUI as sg

if __name__ == '__main__':

    sg.theme('Dark Blue 3')  # please make your windows colorful

    Path1 = "(0, 0) to (10, 10) going 40in/s at 90°"
    Path2 = "(10, 10) to (10, 20) going 20in/s at 90°"
    Path3 = "(10, 20) to (30, 50) going 40in/s at 90°"
    Paths = [Path1, Path2, Path3]


    pathInfo = sg.Text('None Selected', key='-PATH_INFO-', size=[50, 1])

    # Each inch is five pixels
    field = sg.Graph(canvas_size=[720, 720], graph_bottom_left=[0, 0], graph_top_right=[720, 720], background_color='#BAB8B8', key='-FIELD-', enable_events=True)

    col = [[sg.Button('Set Start Point', key='-START_POINT_BUTTON-')],
           [sg.Button('Add Point to Path', key='-ADD_POINT_BUTTON-')],
           [sg.Button('Add Turn')],
           [sg.Button('Add Robot Operation')],
           [sg.Text('\nSelect Path to Edit')],
           [sg.Listbox(values=[Path1, Path2, Path3], size=(50, 6), key='-PATH_LIST-')],
           [sg.Button('Edit Path')],
           [sg.Text('Path Being Edited:')],
           [pathInfo]]

    layout = [[field, sg.Column(col)],
              [sg.Button('Exit')]]

    window = sg.Window('Window Title', layout)

    window.finalize()

    for x in range(1, 6):
        field.draw_line([120*x, 720], [120*x, 0], 'black')
        field.draw_line([0, 120*x], [720, 120*x], 'black')

    # f = open("testFile.txt", "x") This can be used to create a file. Very easy. Nice.

    selectingStartPoint = False
    addingPoint = False;
    startPoint_circle = None
    startPoint_line = None
    points = [None]


    while True:  # Event Loop
        event, values = window.read()  # can also be written as event, values = window()
        print('Event:')
        print(event)
        print('Values:')
        print(values)
        print()
        if event is None or event == 'Exit':
            break

        for p in Paths:
            if len(values['-PATH_LIST-']) > 0 and values['-PATH_LIST-'][0] == p and event == 'Edit Path':
                window['-PATH_INFO-'].update(p)

        if event == '-START_POINT_BUTTON-':
            selectingStartPoint = True

        if selectingStartPoint:
            if event == '-FIELD-':
                field.delete_figure(startPoint_circle)
                startPoint_circle = field.draw_circle([values['-FIELD-'][0], values['-FIELD-'][1]], 5)
                points[0] = ([values['-FIELD-'][0], values['-FIELD-'][1]])
                selectingStartPoint = False

        if event == '-ADD_POINT_BUTTON-':
            addingPoint = True

        if addingPoint:
            if event == '-FIELD-':
                points.append([values['-FIELD-'][0], values['-FIELD-'][1]])
                addingPoint = False

        if len(points) > 1:
            field.delete_figure(startPoint_line)
            startPoint_line = field.draw_line(points[0], points[1], 'black')
        for i in range(2, len(points)):
            field.draw_line(points[i-1], points[i], 'black')




    window.close()