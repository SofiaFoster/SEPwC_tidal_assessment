#!/usr/bin/env python3

# import the modules you need here
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
import uptide

# Read in the tidal data files
def read_tidal_data(filename):
    
# Skip to where data starts (row 12)
# Assign column names
    df = pd.read_csv(filename, delim_whitespace=True, header=None, skiprows=11, names=["Index", "Date", "Time", "Sea Level", "Sea Level B"])
    
# Concatenate date and time to DateTime
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%Y/%m/%d %H:%M:%S")

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
   
# Extract data for a specified year


# Calculate mean sea level


# Remove the mean from sea level

    return 


def extract_section_remove_mean(start, end, data):


    return 


def join_data(data1, data2):
    
# Concatenate data2 and data1 in a new DataFrame
    data3 = pd.concat([data2, data1])

    return data3



def sea_level_rise(data):

                                                     
    return 

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
    
    
    


