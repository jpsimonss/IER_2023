# Blink rate and duration determination
This repository contains the blink-determination software for the dataset 'EyeTracking-data'. It gives the user the opportunity to investigate 
blink-rate and blink-durations of participants of a Virtual Reality tests, through a intuitive GUI.

## 1 Dataset
The dataset contains eye-opennes and pupil-dilation information of 24 participants during five different virtual-reality tests.
The data is stored in one *.csv* file per test. 
To insert this dataset or your own data:

    .
    ├── IER_code_JPS            
    │   ├── EyeTracking-data    # Insert it here
    │   │   ├── P1
    │   │   ├── ...  
    │   │   └── P24     
    │   ├── data_processed     
    │   ├── data_process.py                
    │   ├── ui_layout.py    
    │   └── main.py      


## 2 Installing dependencies
To run *main.py* a version of python 3.4 - 3.12 is needed.
It makes use of *PySimpleGUI*, which can be installed by running:

    python -m pip install pysimplegui

or 

    pip3 install pysimplegui

## 3 Scripts 
The repository contains three Python scripts:
- **data_process.py**
    This file contains three classes: One parent and two children.

    **Parent: BlinkRate:**
    This class has the following functions:
        - Read the desired csv_file of the dataset, and convert it into a python dictionary. 
        - Transfer the csv timestamps to absolute seconds
        - Read the transferred data and determine when the participant blinked
        - Calculate blink-rate and blink-durations 
    
    **Child 1: SingleBlinkRate:**
    An object of this class takes a participant-number and one of the five conditions as input. 
    It returns the desired plots as a *.png* file in the directory *./data_processed*.
    This process can be initiated by making an object of the class and executing function *process_all*.

    **Child 2: AllTestsBlinkRate:**
    An object of this class takes a participant-number as input.
    It then reads the five corresponding *.csv* files of this participant, generates the desired plots and stores them in the
    *./data_processed* directory. The process can be initiatied by executing the function *process_all*.

- **ui_layout.py**
    This script imports PySimpleGUI and stores all the desired layout objects in a single variable called *layout*

- **main.py**
    Run this script to open the GUI.
    It imports the classes from *data_process.py* and the GUI-layout from *ui_layout.py* to:
    - Open the GUI
    - Generate the graphs that are requested by the GUI
    - Display these graphs in the GUI 

## 4 Explanation of the data
The GUI contains two tabs. The *Single* tab and the *All conditions* tab.

### Single
In the left column, a participant, a condition and a threshold can be selected. The default threshold is 0.5
To load the graphs, press **Load Single**. Four graphs will appear. 

In the middle column:
- A graph displaying the eye-openness of both eyes. A red cross indicates when the algorithm indicates it as a blink.
- A graph indicating what the duration [s] of every blink is. 

In the right column:
- A boxplot containing the distribution of the intervals [s] between the blinks.
- A boxplot containing the distribution of the durations of all the blinks.

### All Conditions
In the left column, a participant and threshold can be selected. To load the graphs, press **Load Averages**.
Four graphs appear.

In the middle column:
- A graph showing the distribution of the blink **intervals** of the selected participant in all the five tests.
- A graph showing the distribution of the blink **durations** of the selected participant in all the five tests.

In the right column:
- A bar plot with the average blink rate [blinks/minute] of the selected participant in all the five tests.
- A bar plot with the average blink duration [s] of the selected participant in all the five tests.