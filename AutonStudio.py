import PySimpleGUI as sg

if __name__ == '__main__':

    sg.theme('Dark Blue 3')  # please make your windows colorful

    Path1 = "(0, 0) to (10, 10) going 40in/s at 90°"
    Path2 = "(10, 10) to (10, 20) going 20in/s at 90°"
    Path3 = "(10, 20) to (30, 50) going 40in/s at 90°"
    Paths = [Path1, Path2, Path3]

    pathInfo = sg.Text('None Selected', key='-PATH_INFO-', size=[50, 1])

    col = [[sg.Button('Set Start Point')],
           [sg.Button('Add Point to Path')],
           [sg.Button('Add Turn')],
           [sg.Button('Add Robot Operation')],
           [sg.Text('\nSelect Path to Edit')],
           [sg.Listbox(values=[Path1, Path2, Path3], size=(50, 6), key='-PATH_LIST-')],
           [sg.Button('Edit Path')],
           [sg.Text('Path Being Edited:')],
           [pathInfo]]

    layout = [[sg.Graph(canvas_size=[600, 600], graph_bottom_left=[0, 0], graph_top_right=[600, 600], background_color='#BAB8B8'), sg.Column(col)],
              [sg.Button('Exit')]]

    window = sg.Window('Window Title', layout)

    # f = open("testFile.txt", "x") This can be used to create a file. Very easy. Nice.

    while True:  # Event Loop
        event, values = window.read()  # can also be written as event, values = window()
        if event is None or event == 'Exit':
            break
        for p in Paths:
            if len(values['-PATH_LIST-']) > 0 and values['-PATH_LIST-'][0] == p:
                window['-PATH_INFO-'].update(p)


    window.close()