import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def predict_ampl_shape(dataset, time_increment):
    time_min = pd.to_datetime(dataset['datetime'].min())
    time_max = pd.to_datetime(dataset['datetime'].max())
    total_time = (time_max - time_min).total_seconds()

    # Number of time increments
    num_increments = int(total_time // (time_increment * 60) + 1)

    # Length of FFT result (half the number of data points in each increment)
    fft_length = int(0.5 * (time_increment * 60 / 30))

    return (fft_length, num_increments)

def fft_vtec(dataset, gps_site, sat_id, time_from=None, time_to=None):
    """
    This function calculates the FFT of the time series of the TEC (Total Electron Content) values.
    The TEC values are the measurements of the ionospheric electron content.

    Parameters
    ----------
    dataset : pandas.DataFrame
        The dataset containing the data.
    gps_site : str
        The name of the GPS site.
    sat_id : str
        The satellite ID.
    time_from : str, optional
        The start time of the time series. If not provided, the minimum datetime in the dataset is used.
    time_to : str, optional
        The end time of the time series. If not provided, the maximum datetime in the dataset is used.

    Returns
    -------
    frequencies : numpy.ndarray
        The frequencies corresponding to the FFT values.
    amplitudes : numpy.ndarray
        The relative amplitudes of the FFT values.
    """
    # Select the data for the given GPS site and satellite ID
    data = dataset[(dataset['gps_site'] == gps_site) & (dataset['sat_id'] == sat_id)]
    data = data[['datetime', 'tec']]
    data['datetime'] = pd.to_datetime(data['datetime'])

    if time_from is not None and time_to is not None:
        # Select the data for the given time range
        data = data[(data['datetime'] >= time_from) & (data['datetime'] <= time_to)]
    else:
        # Select the min and the max datetime in the dataset
        time_from = data['datetime'].min()
        time_to = data['datetime'].max()

    # ADD FILLING MISSING MEASUREMENTS
    data_interpolated = pd.DataFrame({
        'datetime': pd.date_range(start=time_from, end=time_to, freq='30s')
    })

    data_interpolated = data_interpolated.merge(data, on='datetime', how='left')


    data_interpolated['tec'] = data_interpolated['tec'].interpolate()


    # Extract the TEC values
    tec = data_interpolated['tec'].values

    # Demean the TEC values
    tec = tec - np.mean(tec)

    # Calculate the FFT of the TEC values
    delta_t_fft = np.fft.fft(tec)

    # Calculate the frequencies corresponding to the FFT values
    n = len(tec)
    timestep = (pd.to_datetime(time_to) - pd.to_datetime(time_from)).total_seconds() / n
    frequencies = np.fft.fftfreq(n, d=timestep)

    # Calculate the relative amplitudes of the FFT values
    amplitudes = np.abs(delta_t_fft) / n

    # Return the positive frequencies and the corresponding amplitudes
    return frequencies[:n//2].tolist(), amplitudes[:n//2].tolist()

def fft_development(dataset, gps_site, sat_id, time_increment, time_from, time_to, min_data):
    frequencies = []
    amplitudes = []
    times = []

    data = dataset[(dataset['gps_site'] == gps_site) & (dataset['sat_id'] == sat_id)]

    time_min = data['datetime'].min()
    time_max = data['datetime'].max()

    time_from = pd.to_datetime(time_from)
    time_to = pd.to_datetime(time_to)

    time_min = pd.to_datetime(time_min)
    time_max = pd.to_datetime(time_max)

    timedelta = pd.Timedelta(minutes=time_increment)

    fft_length = int(0.5 * (time_increment * 60 / 30))

    expected_length = time_increment * 2 + 1

    current_time = time_from

    ffts = 0
    while current_time < time_to:
        if  (time_min <= current_time and time_max >= current_time + timedelta
                and (len(data[(data['datetime'] >= current_time) & (data['datetime'] < current_time + timedelta)])
                > min_data * expected_length)):
            freq, ampl = fft_vtec(dataset, gps_site, sat_id, current_time, current_time + timedelta)
            frequencies.append(freq)
            ffts += 1
        else:
            ampl = np.ones(fft_length) * np.nan


        amplitudes.append(ampl)
        times.append(current_time)

        current_time += timedelta

    if ffts == 0:
        return np.nan, np.nan, np.nan, False

    else:
        amplitudes = np.array(amplitudes)
        frequencies = np.array(frequencies)

        for i in range(1, len(frequencies)):
            assert np.array_equal(frequencies[0, :], frequencies[i, :])

        return frequencies[0, :], amplitudes.T, times, True

def multi_fft_development(dataset, time_increment, min_data=0.8):

    gps_sites = dataset['gps_site'].unique()
    sat_ids = dataset['sat_id'].unique()

    amplitudes = [[] for _ in range(len(gps_sites))]
    times = [[] for _ in range(len(gps_sites))]
    frequencies = None

    time_min = dataset['datetime'].min()
    time_max = dataset['datetime'].max()

    for i, gps_site in enumerate(gps_sites):
        for j, sat_id in enumerate(sat_ids):
            # Check if there is a timeseries for this combination of sat and gps
            if len(dataset[(dataset['gps_site'] == gps_site) & (dataset['sat_id'] == sat_id)]) > 0:
                freq, ampl, time, success = fft_development(dataset, gps_site, sat_id, time_increment, time_min, time_max, min_data)
                if success:
                    amplitudes[i].append(ampl)
                    times[i].append(time)
                    if frequencies is None:
                        frequencies = freq
                    else:
                        assert np.allclose(frequencies, freq), 'Frequencies are not the same'
                else:
                    amplitudes[i].append(np.ones(predict_ampl_shape(dataset, time_increment)) * np.nan)
            else:
                amplitudes[i].append(np.ones(predict_ampl_shape(dataset, time_increment)) * np.nan)

    return frequencies, amplitudes, times, gps_sites, sat_ids

def multi_fft_development_plot(frequencies, amplitudes, times, gps_sites, sat_ids, label_time_step=3, label_freq_step=3, event_time=None):
    cmap = plt.get_cmap('viridis')
    fig, axs = plt.subplots(len(sat_ids), len(gps_sites), figsize=(10, 50))
    fig.suptitle('FFT Development', fontsize=16)
    for i, sat_id in enumerate(sat_ids):
        for j, gps_site in enumerate(gps_sites):
            axs[i,j].imshow(amplitudes[j][i], cmap=cmap)
            #axs[i,j].set_title(f'{gps_site} - {sat_id}')

            axs[i,j].set_xticks(np.arange(0, len(times), label_time_step))
            axs[i,j].set_xticklabels([time.strftime('%H:%M') for time in times[::label_time_step]])

            axs[i,j].set_yticks(np.arange(0, len(frequencies), label_freq_step))
            axs[i,j].set_yticklabels([f'{freq:.3f}' for freq in frequencies[::label_freq_step]])

            if event_time is not None:
                try:
                    event_time = pd.to_datetime(event_time)
                    event_index = np.where(np.array(times) == event_time)[0][0]
                    axs[i,j].axvline(event_index, color='red', linestyle='--')
                except:
                    print('Event time not found')

    fig.tight_layout()
    fig.savefig('fft_development.png')

def multi_fft_development_mean(frequencies, amplitudes, times, label_time_step=3, label_freq_step=3, event_time=None):

    # Flatten the first dimension of amplitudes
    amplitudes = np.array(amplitudes)
    amplitudes_shape = np.shape(amplitudes)
    amplitudes = amplitudes.reshape(-1, amplitudes_shape[-2], amplitudes_shape[-1])


    mean_amplitudes = np.nanmean(amplitudes, axis=0)
    std_amplitudes = np.nanstd(amplitudes, axis=0)

    fig, axs = plt.subplots(2, 1, figsize=(20, 6))
    fig.suptitle('Mean and std of FFT', fontsize=16)
    axs[0].imshow(mean_amplitudes, cmap='viridis')
    axs[0].set_title('Mean Amplitude')

    axs[1].imshow(std_amplitudes, cmap='viridis')
    axs[1].set_title('Standard Deviation Amplitude')

    axs[0].set_xticks(np.arange(0, len(times), label_time_step))
    axs[0].set_xticklabels([time.strftime('%H:%M') for time in times[::label_time_step]])
    axs[0].set_yticks(np.arange(0, len(frequencies), label_freq_step))
    axs[0].set_yticklabels([f'{freq:.3f}' for freq in frequencies[::label_freq_step]])


    axs[1].set_xticks(np.arange(0, len(times), label_time_step))
    axs[1].set_xticklabels([time.strftime('%H:%M') for time in times[::label_time_step]])
    axs[1].set_yticks(np.arange(0, len(frequencies), label_freq_step))
    axs[1].set_yticklabels([f'{freq:.3f}' for freq in frequencies[::label_freq_step]])

    if event_time is not None:
        try:
            event_time = pd.to_datetime(event_time)
            event_index = np.where(np.array(times) == event_time)[0][0]
            axs[0].axvline(event_index, color='red', linestyle='--')
            axs[1].axvline(event_index, color='red', linestyle='--')
        except:
            print('Event time not found')

    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Frequency')

    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Frequency')

    axs[0].invert_yaxis()
    axs[1].invert_yaxis()

    fig.tight_layout()
    fig.savefig('fft_mean.png')


def dataset_filter(dataset, time_from, time_to):
    dataset['datetime'] = pd.to_datetime(dataset['datetime'])
    return dataset[(dataset['datetime'] >= time_from) & (dataset['datetime'] <= time_to)]
