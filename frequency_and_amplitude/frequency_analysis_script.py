import pandas as pd
from tornado.gen import multi

from frequency_analysis_functions import *
import matplotlib.pyplot as plt
import numpy as np

dataset_tohoku = pd.read_csv('Data/tohoku_filtered_data.csv')

time_from = '2011-03-11 03:46:00'
time_to = '2011-03-11 07:46:59'

min_data = 0.7

event_time = "2011-03-11 05:46:00"

dataset_tohoku_f = dataset_filter(dataset_tohoku, time_from, time_to)
gps_sites = dataset_tohoku_f['gps_site'].unique()

frequencies, amplitudes, times, gps_sites, sat_ids = multi_fft_development(dataset_tohoku_f,
                                                                           20, min_data = min_data)
multi_fft_development_plot(frequencies, amplitudes, times[0][0], gps_sites, sat_ids,
                           label_time_step=25, label_freq_step=4, event_time=event_time)

multi_fft_development_mean(frequencies, amplitudes, times[0][0], label_time_step=10, label_freq_step=2, event_time=event_time)