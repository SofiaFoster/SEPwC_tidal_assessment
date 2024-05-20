#!/usr/bin/env python3

# Import needed modules
import argparse
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.dates as dates
from datetime import datetime
import uptide

# Read in the tidal data files
def read_tidal_data(filename):
    
# Skip to where data starts (row 12)
    df = pd.read_csv(filename, delim_whitespace=True, header=None, skiprows=11)
    
# Assign column names
    df.rename(columns={0: "Index", 1: "Date", 2: "Time", 3: "Sea Level", 4: "Sea Level B"}, inplace=True)
    
# Concatenate date and time to DateTime
    DateTime = df["Date"] + " " + df["Time"]
    
# Format into a single string
    df["DateTime"] = pd.to_datetime(DateTime, format="%Y/%m/%d %H:%M:%S")

# Set DateTime column as index of DataFrame    
    df.set_index('DateTime', inplace=True)

# Replace values that end in M,N,T with NaN    
    df.replace(to_replace=".*M$",value={'Sea Level':np.nan},regex=True,inplace=True)
    df.replace(to_replace=".*N$",value={'Sea Level':np.nan},regex=True,inplace=True)
    df.replace(to_replace=".*T$",value={'Sea Level':np.nan},regex=True,inplace=True)
 
# Convert data type to float
    df["Sea Level"] = df["Sea Level"].astype(float)    
    
    return df
    

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
    x = dates.date2num(data.index)
    y = data["Sea Level"]
   
# Execute linear regression
    slope, p_value, _, _, _ = stats.linregress(x,y)

    return slope, p_value


def tidal_analysis(data, constituents, start_datetime):


    return 

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
    
    
    


