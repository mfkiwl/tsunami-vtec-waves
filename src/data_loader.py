import madrigalWeb.madrigalWeb as mw

# Define the parameters
url = "http://cedar.openmadrigal.org"
output_dir = "/tmp"
user_fullname = "ljbh"
user_email = "knjaldfsf@gasd.com"
user_affiliation = "none"
file_format = "hdf5"
start_year = 2011
start_month = 3
start_day = 11
start_hour = 0
start_min = 0
start_sec = 0
end_year = 2011
end_month = 3
end_day = 12
end_hour = 23
end_min = 59
end_sec = 59
inst = 8000
kindat = 3505

# Initialize the MadrigalData object
madData = mw.MadrigalData(url)

# Get data availability
avail_data = madData.getExperiments(inst, start_year, start_month, start_day, start_hour, start_min, start_sec, end_year, end_month, end_day, end_hour, end_min, end_sec)

# Loop through available data and download
for exp in avail_data:
    print(f"Downloading data for experiment {exp['id']}")
    madData.downloadFile(exp['id'], kindat, output_dir, user_fullname, user_email, user_affiliation, file_format)