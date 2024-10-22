import madrigalWeb.madrigalWeb
import os
import datetime

# Initialize MadrigalData object with the desired Madrigal site URL
madrigal_data = madrigalWeb.madrigalWeb.MadrigalData('http://cedar.openmadrigal.org')

# User information
user_fullname = 'ljbh'
user_email = 'knjaldfsf@gasd.com'
user_affiliation = 'none'

# Date range for the data you want to download
start_date = datetime.datetime(2011, 3, 11, 0, 0, 0)
end_date = datetime.datetime(2011, 3, 12, 23, 59, 59)

# Instrument code and kindat code
instrument_code = 8000
kindat_code = 3505

# Output directory where the files will be saved
output_dir = '/tmp'

# Fetch the list of experiments for the given instrument and date range
experiments = madrigal_data.getExperiments(
    code=instrument_code,
    startyear=start_date.year,
    startmonth=start_date.month,
    startday=start_date.day,
    starthour=start_date.hour,
    startmin=start_date.minute,
    startsec=start_date.second,
    endyear=end_date.year,
    endmonth=end_date.month,
    endday=end_date.day,
    endhour=end_date.hour,
    endmin=end_date.minute,
    endsec=end_date.second
)

# Loop through each experiment and download files with the specified kindat code
for experiment in experiments:
    files = madrigal_data.getExperimentFiles(experiment.id)
    for file in files:
        if file.kindat == kindat_code:
            # Construct the destination file path
            base_filename = os.path.basename(file.name)
            destination_path = os.path.join(output_dir, base_filename)
            # Download the file in HDF5 format
            madrigal_data.downloadFile(
                filename=file.name,
                destination=destination_path,
                user_fullname=user_fullname,
                user_email=user_email,
                user_affiliation=user_affiliation,
                format='hdf5'
            )
            print(f'Downloaded {base_filename} to {destination_path}')
