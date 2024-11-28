import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PLOTS_PATH = 'plots/'

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
        
    n_points = int((time_to - time_from).total_seconds() / 30) + 1

    # ADD FILLING MISSING MEASUREMENTS
    data_interpolated = pd.DataFrame({
        'datetime': pd.date_range(start=time_from, end=time_to, periods=n_points)
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

    # In `fft_vtec`, replace the frequency calculation
    frequencies = np.fft.fftfreq(n, d=timestep)[:n // 2]

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
    standard_fft_length = fft_length  # Standardize FFT length

    expected_length = time_increment * 2 + 1
    current_time = time_from

    ffts = 0
    while current_time < time_to:
        if (time_min <= current_time and time_max >= current_time + timedelta and
                (len(data[(data['datetime'] >= current_time) & (data['datetime'] < current_time + timedelta)])
                 > min_data * expected_length)):
            freq, ampl = fft_vtec(dataset, gps_site, sat_id, current_time, current_time + timedelta)

            # Standardize frequency and amplitude lengths
            if len(freq) > standard_fft_length:
                freq = freq[:standard_fft_length]
                ampl = ampl[:standard_fft_length]
            elif len(freq) < standard_fft_length:
                freq = np.pad(freq, (0, standard_fft_length - len(freq)), constant_values=np.nan)
                ampl = np.pad(ampl, (0, standard_fft_length - len(ampl)), constant_values=np.nan)

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
            if not np.array_equal(frequencies[0, :], frequencies[i, :]):
                frequencies[i, :] = frequencies[0, :]  # Align to reference

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
    
    
def multi_fft_development_plot(
        frequencies, amplitudes, times, gps_sites, sat_ids, 
        label_time_step=3, label_freq_step=3, event_time=None, name=''):
    cmap = plt.get_cmap('viridis')
    
    # Dynamically set figure size based on the number of subplots
    n_rows = len(sat_ids)
    n_cols = len(gps_sites)
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4), squeeze=False)
    fig.suptitle('FFT Development', fontsize=20, y=1.02)
    
    for i, sat_id in enumerate(sat_ids):
        for j, gps_site in enumerate(gps_sites):
            ax = axs[i, j]
            
            # Validate the dimensions of amplitudes[j][i]
            current_amplitudes = np.array(amplitudes[j][i])
            if current_amplitudes.shape != (len(frequencies), len(times)):
                print(f"Dimension mismatch for amplitudes at {gps_site} - {sat_id}: Expected ({len(frequencies)}, {len(times)}), got {current_amplitudes.shape}")
                continue
            
            # Plot the amplitude using imshow
            im = ax.imshow(
                current_amplitudes, cmap=cmap, aspect='auto',
                extent=[0, len(times), frequencies[0], frequencies[-1]], origin='lower'
            )
            
            # Add titles and axis labels
            ax.set_title(f'{gps_site} - {sat_id}', fontsize=12)
            ax.set_xlabel('Time', fontsize=10)
            ax.set_ylabel('Frequency (Hz)', fontsize=10)
            
            # Adjust x-ticks for time labels
            time_indices = np.arange(0, len(times), label_time_step)
            ax.set_xticks(time_indices)
            ax.set_xticklabels([times[idx].strftime('%H:%M') for idx in time_indices], rotation=45, fontsize=8)
            
            # Adjust y-ticks for frequency labels
            freq_indices = np.linspace(0, len(frequencies) - 1, len(frequencies), dtype=int)[::label_freq_step]
            ax.set_yticks([frequencies[idx] for idx in freq_indices])
            ax.set_yticklabels([f'{frequencies[idx]:.3f}' for idx in freq_indices], fontsize=8)
            
            # Highlight event time if provided
            if event_time is not None:
                try:
                    event_time = pd.to_datetime(event_time)
                    closest_time = min(times, key=lambda t: abs(t - event_time))
                    event_index = times.index(closest_time)
                    ax.axvline(event_index, color='red', linestyle='--', label='Event Time')
                    ax.legend(loc='upper right', fontsize=8)
                except ValueError:
                    print(f"Event time '{event_time}' not found in times.")
            
            # Add color bar
            cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.8)
            cbar.set_label('Amplitude', fontsize=10)
            cbar.ax.tick_params(labelsize=8)
    
    # Adjust layout to prevent overlap
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save the figure
    plot_filename = f'{PLOTS_PATH}fft_development_{name}.png'
    fig.savefig(plot_filename)
    
    plt.show()


def multi_fft_development_mean(frequencies, amplitudes, times, label_time_step=3, label_freq_step=3, event_time=None, name=''):
    # Flatten the first dimension and compute mean/std
    amplitudes = np.array(amplitudes)
    amplitudes = amplitudes.reshape(-1, amplitudes.shape[-2], amplitudes.shape[-1])
    mean_amplitudes = np.nanmean(amplitudes, axis=0)
    std_amplitudes = np.nanstd(amplitudes, axis=0)

    # Create subplots for mean and standard deviation
    fig, axs = plt.subplots(2, 1, figsize=(20, 8), sharex=True, sharey=True)
    fig.suptitle('Mean and Standard Deviation of FFT', fontsize=16)

    # Ensure that `extent` correctly maps the array to the frequencies and time
    extent = [0, len(times), frequencies[0], frequencies[-1]]

    # Plot mean amplitudes
    im1 = axs[0].imshow(mean_amplitudes, cmap='viridis', aspect='auto', extent=extent, origin='lower')
    axs[0].set_title('Mean Amplitude', fontsize=14)
    cbar1 = fig.colorbar(im1, ax=axs[0], orientation='vertical')
    cbar1.set_label('Amplitude', fontsize=10)

    # Plot standard deviation amplitudes
    im2 = axs[1].imshow(std_amplitudes, cmap='viridis', aspect='auto', extent=extent, origin='lower')
    axs[1].set_title('Standard Deviation Amplitude', fontsize=14)
    cbar2 = fig.colorbar(im2, ax=axs[1], orientation='vertical')
    cbar2.set_label('Amplitude Std Dev', fontsize=10)

    # Set x and y ticks
    time_indices = np.arange(0, len(times), label_time_step)
    freq_indices = np.linspace(0, len(frequencies) - 1, len(frequencies), dtype=int)[::label_freq_step]

    for ax in axs:
        ax.set_xticks(time_indices)
        ax.set_xticklabels([times[idx].strftime('%H:%M') for idx in time_indices], rotation=45, fontsize=8)
        ax.set_yticks([frequencies[i] for i in freq_indices])
        ax.set_yticklabels([f'{frequencies[i]:.3f}' for i in freq_indices], fontsize=8)
        ax.set_xlabel('Time (HH:MM)', fontsize=12)
        ax.set_ylabel('Frequency (Hz)', fontsize=12)

    # Highlight event time
    if event_time is not None:
        try:
            event_time = pd.to_datetime(event_time)
            closest_time = min(times, key=lambda t: abs(t - event_time))
            event_index = times.index(closest_time)
            for ax in axs:
                ax.axvline(event_index, color='red', linestyle='--', label='Event Time')
            axs[0].legend(loc='upper right', fontsize=10)
        except ValueError:
            print(f"Event time '{event_time}' not found in times.")

    # Adjust layout and save
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    plot_filename = f'{PLOTS_PATH}fft_mean_{name}.png'
    fig.savefig(plot_filename)
    plt.show()


def dataset_filter(dataset, time_from, time_to):
    dataset['datetime'] = pd.to_datetime(dataset['datetime'])
    return dataset[(dataset['datetime'] >= time_from) & (dataset['datetime'] <= time_to)]
