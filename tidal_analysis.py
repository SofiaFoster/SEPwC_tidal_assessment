"""
This module contains functions for reading, processing
and analysing tidal data.
"""

#!/usr/bin/env python3

# Import needed modules
import argparse
import datetime
import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import dates
import pytz
import uptide

# Read in the tidal data files
def read_tidal_data(filename):

    # Skip to where data starts (row 12)
    data_frame = pd.read_csv(filename, delim_whitespace=True, header=None, skiprows=11)

# Assign column names
    data_frame.rename(
        columns={
            0: "Index",
            1: "Date",
            2: "Time",
            3: "Sea Level",
            4: "Sea Level B"
        },
        inplace=True)

# Concatenate date and time to date_time
    date_time = data_frame["Date"] + " " + data_frame["Time"]

# Format into a single string
    data_frame["date_time"] = pd.to_datetime(date_time, format="%Y/%m/%d %H:%M:%S")

# Set date_time column as index of DataFrame
    data_frame.set_index('date_time', inplace=True)

# Replace values that end in M,N,T with NaN
    data_frame.replace(to_replace=".*M$",value={'Sea Level':np.nan},regex=True,inplace=True)
    data_frame.replace(to_replace=".*N$",value={'Sea Level':np.nan},regex=True,inplace=True)
    data_frame.replace(to_replace=".*T$",value={'Sea Level':np.nan},regex=True,inplace=True)

# Convert data type to float
    data_frame["Sea Level"] = data_frame["Sea Level"].astype(float)

    return data_frame


def extract_single_year_remove_mean(year, data):

# Define strings for the start and end of the year
    year_start = str(year) + "-01-01"
    year_end = str(year) + "-12-31"

# Extract data for a specified year
    year_data = data.loc[year_start:year_end].copy()

# Calculate the mean Sea Level
    mean_sea_level = np.mean(year_data["Sea Level"])

# Subtract the mean from Sea Level data
    year_data["Sea Level"] -= mean_sea_level

    return year_data


def extract_section_remove_mean(start, end, data):

# Extract data for a specified section
    section_data = data.loc[start:end].copy()

# Calculate the mean Sea Level
    mean_sea_level = np.mean(section_data["Sea Level"])

# Subtract the mean from Sea Level data
    section_data["Sea Level"] -= mean_sea_level

    return section_data


# Concatenate data2 and data1 to data3
def join_data(data1, data2):

    data3 = pd.concat([data2, data1])

    return data3


def sea_level_rise(data):

# Remove NaN values from data
    data = data.dropna(subset = ["Sea Level"])

# Convert index to datetime
    data.index = pd.to_datetime(data.index)

# Assign data to x and y-axis
    x_value = dates.date2num(data.index)
    y_value = data["Sea Level"]

# Execute linear regression
    slope, p_value, _, _, _ = stats.linregress(x_value,y_value)

    return slope, p_value


def tidal_analysis(data, constituents, start_datetime):

# Make start_datetime timezone-naive
    start_datetime = datetime.datetime(1946, 1, 15, 0, 0, 0)

# Create a tides object with a list of the constituents
    tide = uptide.Tides(constituents)

# Set a start time
    tide.set_initial_time(start_datetime)

# Make data index timezone-naive
    data.index = data.index.tz_localize(None)

# Convert dates to seconds
    seconds_since = (data.index - start_datetime).total_seconds()

# Rewrite for easier use
    sea_level_data = data["Sea Level"].to_numpy()

# Check if sea_level_data is not None
    if sea_level_data is not None and len(sea_level_data) > 0:

# Remove any NaN values
        valid_data = ~pd.isna(sea_level_data)
        sea_level_data = sea_level_data[valid_data]
        seconds_since = seconds_since[valid_data]

# Execute harmonic analysis
        amp, pha = uptide.harmonic_analysis(tide, sea_level_data, seconds_since)

        return amp, pha

    return None, None

def get_longest_contiguous_data(data):


    return

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Sofia Foster"
                     )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose

    read_tidal_data(dirname)
