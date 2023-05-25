'''
Data analysis script for Introduction to Engineering Research
Project: Effects of Different VEs on Cognitive Load
Writer: Jan Peter Simons (4368185)
'''

# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

EXECUTE_HERE = False
# Keys: frame;Timestamp;openness_L;openness_R;pupil_diameter_L(mm);pupil_diameter_R(mm);
# 'Control' 'Noise' 'NPC' '4_Combined' 'Second_Task'
############################################

class BlinkRate:
    def __init__(self, participant, th_closed):
        self.participant = participant
        self.condition_names = ['Control','Noise','NPC','4_Combined','Second_Task']
        self.bigfigsize = (10,4)
        self.smallfigsize = (3.3,4)
        self.th_closed = th_closed
        self.no_values = False

    def __repr__(self) -> str:
        return f'Blinkrate object of participant {self.participant}'

    def process_single_dataframe(self, csv_loc):        
        csv_file = pd.read_csv(csv_loc)
        self.length = csv_file.shape[0] - 2 # Removing pupil diameters, to speed up process
        keys = csv_file.columns.tolist()[0].split(";")[:-1]
        self.dataframe = {  keys[0]:[], keys[1]:[],
                            keys[2]:[], keys[3]:[],
                            keys[4]:[], keys[5]:[] }

        for line_nr in range(self.length):
            line = csv_file.iloc[line_nr].squeeze().split(";")[:-1]
            i = 0
            for key in keys:
                if key in ('frame' , 'Timestamp'):
                    self.dataframe[key].append(line[i])
                else:
                    self.dataframe[key].append(float(line[i]))
                i += 1
        # Add time values in seconds
        t = self.timestamps_to_t()
        self.dataframe['t'] = t

    def timestamps_to_t(self): 
        t = [0]
        t_value = 0
        for i in range(self.length):
            if i < self.length - 1:
                now = self.dataframe['Timestamp'][i]
                now_dt = self.timestamp_to_datetime(now)
                next = self.dataframe['Timestamp'][i + 1]
                next_dt = self.timestamp_to_datetime(next)
                delta = (next_dt - now_dt).total_seconds()
                t_value += delta
                t.append(t_value)
        assert len(t) == self.length, "t-vector wrong length"
        duration_stamp = self.timestamp_to_datetime(self.dataframe['Timestamp'][i]) - self.timestamp_to_datetime(self.dataframe['Timestamp'][0])
        self.total_duration = duration_stamp.total_seconds()
        return t
    
    def timestamp_to_datetime(self, timestamp: str):
        a = timestamp.split()
        b = [int(x) for x in a[0].split('-')]
        c = a[1].split(':')
        d = [int(x) for x in c[:-1]]
        e = [int(x) for x in  c[2].split('.')]
        e[1] *= 100
        return dt.datetime(b[0], b[1], b[2], d[0], d[1], e[0], e[1])

    def determine_blink(self):
        assert isinstance(self.dataframe, dict), "Process dataframe first"
        eye_left = np.array(self.dataframe['openness_L'])
        # eye_right = self.dataframe['openness_R'] #Not used for determining blink

        # Find peaks
        blinks_left_idx = np.squeeze(np.where(eye_left <= self.th_closed))
        peak = []
        peaks_idx = []
        for i in range(len(blinks_left_idx)):
            if i == len(blinks_left_idx) - 1:
                peak.append(blinks_left_idx[i])
                peaks_idx.append(peak)
                del peak
            elif blinks_left_idx[i+1] - blinks_left_idx[i] == 1:
                peak.append(blinks_left_idx[i])
            else:
                peak.append(blinks_left_idx[i])
                peaks_idx.append(peak)
                peak = []
        
        self.blink_idx = []
        self.blink_lengths = []
        for peak in peaks_idx:
            # Peaks indexes
            indexed_list = zip(peak, range(len(peak)))
            min_value, _ = min(indexed_list)
            self.blink_idx.append(min_value)
            # Blink lengths
            t = self.dataframe['t']
            blink_length = t[peak[-1]] - t[peak[0]]
            self.blink_lengths.append(blink_length)
        self.avg_blink_length = np.mean(self.blink_lengths)

        # Calculate t_blinks [s]
        self.t_blinks = []
        for idx in self.blink_idx:
            self.t_blinks.append(t[idx])

        # Calculate intervals between blinks
        self.blink_intervals = np.diff(self.t_blinks).tolist() # 1 element shorter than self.t_blinks
        
        # Calculate blink rate -> Two ways to do so!
        self.total_blinks = len(self.blink_idx)
        self.blink_rate = np.mean(self.blink_intervals)                 # 1)
        #self.blink_rate = self.total_duration / self.total_blinks      # 2)
        self.blinks_per_minute = 60 / self.blink_rate

class SingleBlinkRate(BlinkRate): 
    def __init__(self, participant, condition, th_closed):
        super().__init__(participant, th_closed) # super(SingleBlinkRate, self) == super()
        self.participant = participant
        self.condition = condition
        # self.th_closed = th_closed
        self.csv_loc = f'./EyeTracking-data/P{self.participant}/Eyerecording_Test_{self.condition}.csv'
        self.dataframe = None

        print(self)
    def __repr__(self):
        return f'Single BRA -> Object: P{self.participant}, test: {self.condition}'

    # RESULTS
    def plots_test(self, show=True, save=True):
        
        # Checks
        assert isinstance(self.dataframe, dict), "Process dataframe first"
        assert self.blink_idx is not None, "determine_blink first"
        
        # Execute necessary calculations
        self.blink_zeros = np.zeros((self.total_blinks))
        props = dict(boxstyle='round', facecolor='white', alpha=0.8)

        # Plot Eye openess = blinks
        plt.figure(figsize=self.bigfigsize)
        plt.plot(self.dataframe['t'], self.dataframe['openness_L'], self.dataframe['t'], 
                 np.multiply(self.dataframe['openness_R'], -1), self.t_blinks, self.blink_zeros, 'rx')
        plt.title(f'Eye openess\nParticipant {self.participant}, condition: {self.condition}')
        plt.xlabel('Time t [s]')
        plt.ylabel(' ')
        plt.yticks([-1,0,1], labels=['Right\nopen' , 'Closed' , 'Left\nopen'])
        
        text = f'TOTAL BLINKS = {self.total_blinks}\nBlinks / minute = {np.round(self.blinks_per_minute,3)}'
        plt.text(round((self.total_duration + 5), 10)-5,-1, text, verticalalignment = 'bottom', horizontalalignment = 'right' ,bbox = props)
        plt.xlim([0,round((self.total_duration + 5), -1)])
        plt.axhline(y=self.th_closed, color = 'tab:gray', linestyle = '--')
        plt.axhline(y=-self.th_closed, color = 'tab:gray', linestyle = '--')
        plt.legend(['Openness Left', 'Openness Right', 'Blink count', 'Threshold'], loc='upper right')
        if save:
            self.loc_graph_eye_openness = './data_processed/graph_eye_openness.png'
            plt.savefig(self.loc_graph_eye_openness) 
        if show:
            plt.show()
            plt.close()

        # Plot blink durations
        plt.figure(figsize=self.bigfigsize)
        plt.stem(self.t_blinks, self.blink_lengths, linefmt='grey', markerfmt='rx')
        plt.title(f'Blink durations\nParticipant {self.participant}, condition: {self.condition}')
        plt.xlabel('Time t [s]')
        plt.ylabel('Blink durations [s] ')
        plt.xlim([0,round((self.total_duration + 5), -1)])
        text = f'Average blink duration = {np.round(self.avg_blink_length, 4)} s'
        plt.text(round((self.total_duration + 5), 10)-5,max(self.blink_lengths), text, 
                 verticalalignment = 'top', horizontalalignment = 'right' ,bbox = props)
        if save:
            self.loc_graph_blink_duration = './data_processed/graph_blink_duration.png' 
            plt.savefig(self.loc_graph_blink_duration)
        if show:
            plt.show()
            plt.close()
        
        # Boxplot blink_intervals
        plt.figure(figsize = self.smallfigsize)
        plt.boxplot(self.blink_intervals)
        plt.title(f'Blink Intervals [s]\nP{self.participant}, condition: {self.condition}')
        plt.ylabel('Blink Interval [s]')
        plt.xlabel('')
            #Textbox
        mu = np.round(np.mean(self.blink_intervals),2)
        median = np.round(np.median(self.blink_intervals),2)
        sigma = np.round(np.std(self.blink_intervals),2)
        text = f'μ = {mu}\nmed = {median}\nσ = {sigma}'
        plt.text(1.15, median, text, fontsize=7,
        verticalalignment='center_baseline', bbox=props)
        plt.xticks([1], labels=[''])
        plt.tight_layout()
        if save:
            self.loc_boxplot_blinks_interval = './data_processed/boxplot_blinks_interval.png' 
            plt.savefig(self.loc_boxplot_blinks_interval)
        if show:
            plt.show()
            plt.close()
        
        # Boxplot blink durations
        plt.figure(figsize = self.smallfigsize)
        plt.boxplot(self.blink_lengths)
        plt.title(f'Blink durations\nP{self.participant}, condition: {self.condition}')
        plt.ylabel('Blink duration [s]')
        plt.xlabel('')
            #Textbox
        mu = np.round(np.mean(self.blink_lengths),4)
        median = np.round(np.median(self.blink_lengths),4)
        sigma = np.round(np.std(self.blink_lengths),4)
        text = f'μ = {mu}\nmed = {median}\nσ = {sigma}'
        plt.text(1.15, median, text, fontsize=7,
        verticalalignment='center_baseline', bbox=props)
        plt.xticks([1], labels=[''])
        plt.tight_layout()
        if save:
            self.loc_boxplot_blink_durations = './data_processed/boxplot_blink_durations.png' 
            plt.savefig(self.loc_boxplot_blink_durations)
        if show:
            plt.show()
            plt.close()        

    def process_all(self):
        self.process_single_dataframe(self.csv_loc)
        self.determine_blink()
        try:
            a = max(self.blink_lengths)
            self.plots_test(show=False,save=True)
        except ValueError:
            self.no_values = True
            print('NO Values, higher your threshold!')
        

class AllTestsBlinkRate(BlinkRate):
    def __init__(self, participant, th_closed):
        super().__init__(participant, th_closed)        
        self.blink_intervals_all_conditions = []
        self.blink_durations_all_conditions = []
        self.avg_blink_rate_all_conditions = []
        self.avg_blink_duration_all_conditions = []

    def __repr__(self):
        return f'Combined BRA -> Object: P{self.participant}'

    def process_data(self):
        for condition in self.condition_names:
            csv_loc = f'./EyeTracking-data/P{self.participant}/Eyerecording_Test_{condition}.csv'
            self.process_single_dataframe(csv_loc)
            self.determine_blink()

            # Store data of 5 conditions in one list
            self.blink_intervals_all_conditions.append(self.blink_intervals)
            self.blink_durations_all_conditions.append(self.blink_lengths)
            self.avg_blink_rate_all_conditions.append(self.blinks_per_minute)
            self.avg_blink_duration_all_conditions.append(self.avg_blink_length)

    def plots_test(self, show=False, save=True):
        
        # Plot parameters
        colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
        names_small = ['Ctrl','Noise','NPC','Comb','2nd']
        names = ['Control','Noise','NPC','Combined','Second Task']

        # Plot avg blink interval per participant
        plt.figure(figsize=self.smallfigsize)
        plt.bar(names_small, self.avg_blink_rate_all_conditions, color=colors)
        plt.rcParams.update({'font.size': 10})
        plt.ylabel('Blinks / minute [-]')
        plt.title(f'Avg blink rate\nP{self.participant}')
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            self.loc_bar_avg_blinkrate = './data_processed/bar_avg_blinkrate.png'
            plt.savefig(self.loc_bar_avg_blinkrate)
            

        # Plot avg blink durations per participant
        plt.figure(figsize=self.smallfigsize)
        plt.bar(names_small, self.avg_blink_duration_all_conditions, color=colors)
        plt.title(f'Avg blink durations\nP{self.participant}')
        plt.ylabel('Avg blink duration [s]')
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            self.loc_bar_avg_blinkduration = './data_processed/bar_avg_blinkduration.png' 
            plt.savefig(self.loc_bar_avg_blinkduration)
        
        # Boxplots blink_intervals
        plt.figure(figsize=self.bigfigsize)
        plt.boxplot(self.blink_intervals_all_conditions)
        plt.xticks([1,2,3,4,5], names)
        plt.title(f'Blink interval lengths, P{self.participant}, for all conditions')
        plt.ylabel('Blink interval lengths [s]')
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            self.loc_box_blink_intervals = './data_processed/box_blink_intervals.png' 
            plt.savefig(self.loc_box_blink_intervals)
        
        # Boxplots blink_intervals
        plt.figure(figsize=self.bigfigsize)
        plt.boxplot(self.blink_durations_all_conditions)
        plt.xticks([1,2,3,4,5], names)
        plt.title(f'Blink durations, P{self.participant}, for all conditions')
        plt.ylabel('Blink durations [s]')
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            self.loc_box_blink_durations = './data_processed/box_blink_durations.png' 
            plt.savefig(self.loc_box_blink_durations)
            
    
    def process_all(self):
        self.process_data()
        try:
            for blink_lengths in self.blink_intervals_all_conditions:
                a = max(blink_lengths)
            self.plots_test()
        except ValueError:
            self.no_values = True
            print('NO Values, higher your threshold!')


#______________________EXECUTE_HERE_______________________________#
if EXECUTE_HERE:
    # assessment_1 = SingleBlinkRate(14,'Second_Task')
    # assessment_1.process_all(0.5, show=True)
    # ass2 = AllTestsBlinkRate(14, 0.5)
    # ass2.process_all(show=False)
    pass



