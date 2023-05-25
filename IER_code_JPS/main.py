#!/usr/bin/env python

# Imports other python filess
try:
    import PySimpleGUI as sg
except ImportError as e:
    print(f'Package not installed:\npython -m pip install pysimplegui')
from ui_layout import layout
from data_process import SingleBlinkRate, AllTestsBlinkRate

if __name__ == '__main__':
    
    # Create the window
    window = sg.Window("Blink Rate Assessment", layout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        print(f'Event = {event}\nValues ={values})')
        if event in("Exit",sg.WIN_CLOSED):
            break

        # Load-button tab 1
        if event == "Load Single":
            participant = int(values['-PARTICIPANT-SINGLE-'])
            condition = values['-CONDITION-']
            th_openess = values['-THRESHOLD-1-']
            if condition == 'Combined':
                condition = '4_Combined'
            if condition == 'Second Task':
                condition = 'Second_Task'
            
            assess = SingleBlinkRate(participant, condition, th_openess)
            assess.process_all()
            if assess.no_values == False:        
                window['-IMAGE1-TAB1-'].update(assess.loc_graph_eye_openness)
                window['-IMAGE2-TAB1-'].update(assess.loc_graph_blink_duration)
                window['-IMAGE3-TAB1-'].update(assess.loc_boxplot_blinks_interval)
                window['-IMAGE4-TAB1-'].update(assess.loc_boxplot_blink_durations)
            else:
                sg.popup_error('Threshold too low!', auto_close=True, auto_close_duration=10, font=(40))
        
        if event == "Load Averages":
            participant = int(values['-PARTICIPANT-COMB-'])
            th_openess = values['-THRESHOLD-2-']   
            assess = AllTestsBlinkRate(participant, th_openess)
            assess.process_all()
            if assess.no_values == False:      
                window['-IMAGE1-TAB2-'].update(assess.loc_box_blink_intervals)
                window['-IMAGE2-TAB2-'].update(assess.loc_box_blink_durations)
                window['-IMAGE3-TAB2-'].update(assess.loc_bar_avg_blinkrate)
                window['-IMAGE4-TAB2-'].update(assess.loc_bar_avg_blinkduration)
            else:
                sg.popup_error('Threshold too low!', auto_close=True, auto_close_duration=10, font=(40))
                        
    window.close()
    