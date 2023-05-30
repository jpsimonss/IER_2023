#!/usr/bin/env python
'''
User Interface
Made with PySimpleGUI
Author: JP Simons (4368185)'''

# Imports
try:
    import PySimpleGUI as sg
except ImportError as e:
    print(f'Package not installed:\npython -m pip install pysimplegui')

# Parameters
bigfigsize = (900,420)
smallfigsize = (340,420)
font=(15)

# Column definitions
left_column_single = [
    [sg.Text("Select Participant", font=font)],
    [sg.Combo(values=([f'{x}' for x in range(1,25)]), default_value='1', readonly=False, k='-PARTICIPANT-SINGLE-', font=font)],
    [sg.Text("Select Condition", font=font)],
    [sg.OptionMenu(values=('Control', 'Noise', 'NPC', 'Second Task', 'Combined'),default_value='Control', k='-CONDITION-'),],
    [sg.Text("Select Threshold", font=font)],
    [sg.Combo(values=([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]), default_value='0.5', readonly=False, k='-THRESHOLD-1-', font=font)],
    [sg.Text("")],
    [sg.Button("Load Single")]
    ]

middle_column_single = [
    [sg.Text("Eye Openness", font=font)],
    [sg.Image(key='-IMAGE1-TAB1-', size=bigfigsize)],
    [sg.Text("Blink Durations", font=font)],
    [sg.Image(key='-IMAGE2-TAB1-', size=bigfigsize)],
    ]

right_column_single = [
    [sg.Text("Blink interval lengths", font=font)],
    [sg.Image(key='-IMAGE3-TAB1-', size=smallfigsize)],
    [sg.Text("Blink Durations", font=font)],
    [sg.Image(key='-IMAGE4-TAB1-', size=smallfigsize)],
    ]

left_column_combined = [
    [sg.Text("Select Participant", font=font)],
    [sg.Combo(values=([f'{x}' for x in range(1,25)]), default_value='1', readonly=False, k='-PARTICIPANT-COMB-')],
    [sg.Text("Select Threshold", font=font)],
    [sg.Combo(values=([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]), default_value='0.5', readonly=False, k='-THRESHOLD-2-')],
    [sg.Text("")],
    [sg.Button("Load Averages", font=font)]
    ]

middle_column_combined = [
    [sg.Text("Blink Interval Lengths", font=font)],
    [sg.Image(key='-IMAGE1-TAB2-', size=bigfigsize)],
    [sg.Text("Blink durations", font=font)],
    [sg.Image(key='-IMAGE2-TAB2-', size=bigfigsize)],
    ]

right_column_combined = [
    [sg.Text("Average blink interval length", font=font)],
    [sg.Image(key='-IMAGE3-TAB2-', size=smallfigsize)],
    [sg.Text("Average blink duration", font=font)],
    [sg.Image(key='-IMAGE4-TAB2-', size=smallfigsize)],
    ]


# Combine layouts
layout_single = [
    [sg.Column(left_column_single),
    sg.VSeparator(),
    sg.Column(middle_column_single),
    sg.VSeparator(),
    sg.Column(right_column_single)]
]

layout_combined = [
    [sg.Column(left_column_combined),
    sg.VSeparator(),
    sg.Column(middle_column_combined),
    sg.VSeparator(),
    sg.Column(right_column_combined)]
]


layout =    [[sg.TabGroup([[sg.Tab('Single', layout_single),
                            sg.Tab('All conditions', layout_combined)]], 
                            key='-TAB-', expand_x=True, expand_y=True),
            ]]


