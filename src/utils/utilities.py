import json
import re
import pandas as pd
from datetime import datetime

from config import  SEQUENCING_KIT_TO_MAX_CLUSTERS

CACHE_FILE_PATH = 'src/utils/sciebo_cache.json'  # Define the path to your cache file

###############################################################################
#------------------------------ Utility Functions ----------------------------#
###############################################################################

def is_valid_folder(folder_name):
    """
    Check if the folder name matches the expected format for sequencing projects.

    :param folder_name: Name of the folder to check.
    :return: True if the folder name is valid, False otherwise.
    """
    return re.match(r'^\d{6}', folder_name) is not None
    
def extract_date_from_folder(folder_name):
    try:
        # Extracting the YYMMDD part from the folder name
        date_str = folder_name[:6]
        # Converting the date string to a datetime object
        date_obj = datetime.strptime(date_str, '%y%m%d')
        # Formatting the datetime object as 'DD.MM.YYYY'
        formatted_date = date_obj.strftime('%d.%m.%Y')
        return formatted_date

    except ValueError:
        # Handle the case where the folder name doesn't match the expected format
        return None

def extract_sequencer_from_folder(folder_name):
    name_array = folder_name.split('_')
    if len(name_array) <= 1 :
        return ""
    instrument_id = name_array[1]
    if instrument_id.startswith("NB501289"):
        return "nextseq500"
    elif instrument_id.startswith("M00818"):
        return "miseq1"
    elif instrument_id.startswith("M04404"):
        return "miseq2"
    elif instrument_id.startswith("A01742"):
        return "novaseq"
    else: 
        return ""
    
def check_read_count(row):
    """ Count above and below requirement samples"""
    samples_above_requirement = 0
    samples_below_requirement = 0
    expected_reading_per_sample = row['Expected Reading Per Sample']
    sample_read_distribution = row['Read Distribution']

    if expected_reading_per_sample is None or sample_read_distribution is None:
        return None, None  # No comparison for 'None' types
    
    sample_read_distribution = [float(x) for x in sample_read_distribution.split('-')]
    # Convert from percenatges to actuall read numbers
    total_read_count = row["Total Read Count in Millions"] * 1000000
    sample_read_distribution = [x * total_read_count for x in sample_read_distribution]
    # Drop undetemined reads
    sample_read_distribution = sample_read_distribution[:-1]

    for sample_reads_count in sample_read_distribution:
        if sample_reads_count < expected_reading_per_sample:
            # Number of Samples Above Requirement increased by 1
            samples_below_requirement += 1  
        elif sample_reads_count >= expected_reading_per_sample:
            # Number of Samples Below Requirement increased by 1
            samples_above_requirement += 1 

    return samples_above_requirement, samples_below_requirement  # No change in counts

def calculate_ratios(df):
    """
    Calculate ratios of total read count to expected clusters and update the DataFrame.

    :param df: The DataFrame to update.
    """
    total_read_count = df['Total Read Count in Millions'] * 1e6
    df['Ratio Total Read Count and Expected Cluster'] = (
        total_read_count /
        df['Sequencing Kit'].str.lower().map(SEQUENCING_KIT_TO_MAX_CLUSTERS)
    ).round(2)

def adjust_phix_percentages(df):
    """
    Adjust Phix input and output percentages in the DataFrame.

    :param df: The DataFrame to adjust.
    """
    total_read_count = df['Total Read Count in Millions'] * 1e6
    df['Phix Output Percent'] = (
        pd.to_numeric(df['Phix Output Count'], errors='coerce') / total_read_count
    ) * 100
    df[['Phix Output Percent', 'Phix Input']] = df[['Phix Output Percent', 'Phix Input']].round(2)

def read_cache():
    try:
        with open(CACHE_FILE_PATH, 'r') as cache_file:
            return json.load(cache_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty dict if the file doesn't exist or is invalid

def write_cache(cache_data):
    with open(CACHE_FILE_PATH, 'w') as cache_file:
        json.dump(cache_data, cache_file, indent=4)
