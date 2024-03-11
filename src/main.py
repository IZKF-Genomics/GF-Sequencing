import os
import logging
import pandas as pd
from tqdm import tqdm

# Import utility functions
import utils.utilities as utils
from parsers.fastq_parser import parse_fastq_stats_folder
from parsers.multiqc_parser import parse_multiqc_data
from parsers.sciebo_parser import parse_sciebo_report


# Import constants and configurations
from config import (
    FASTQ_FOLDER_PATH, 
    SEQUENCING_KIT_TO_CLUSTERS, 
    EXPECTED_READING_PER_SAMPLE_MAPPING
)

###############################################################################
#------------------------------ Set Up Logging -------------------------------#
###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='parser.log',
    filemode='w'
)

###############################################################################
#-------------------------------- Main Functions -----------------------------#
###############################################################################

def main():
    """
    Main function to create and save a DataFrame containing statistics for sequencing projects.
    """
    fastq_folders = os.listdir(FASTQ_FOLDER_PATH)
    fastq_dates = [utils.extract_date_from_folder(folder) for folder in fastq_folders]
    fastq_sequencers = [utils.extract_sequencer_from_folder(folder) for folder in fastq_folders]

    # Initialize DataFrame with project data
    df = initialize_dataframe(fastq_folders, fastq_dates, fastq_sequencers)
    df = process_folders(df, fastq_folders)

    # Post-process and clean up DataFrame
    df = postprocess_dataframe(df)
    df.to_csv('r_scripts/sequencing_statistics.csv', index=True)

def initialize_dataframe(folders, dates, sequencers):
    """
    Initialize the DataFrame with basic information from the project folders in a more concise way.

    :param folders: List of folder names representing the project names.
    :param dates: List of dates corresponding to each folder in 'dd.mm.yyyy' format.
    :param sequencers: List of sequencers corresponding to each folder.
    :return: Initialized pandas DataFrame with the folders as the index.
    """
    columns = [
        "Project Name", "Protocol Name", "Date", "Sciebo Found", "Application", "Sequencer",
        "STD in Millions", "CV", "Undetermined Reads Percentage", "Most Common Undetermined Barcode",
        "Most Common Undetermined Barcode Percentage", "Undetermined Distribution String",
        "Read Distribution", "Expected Reading Per Sample", "Number of Samples Above Requirement",
        "Number of Samples Below Requirement", "Sequencing Kit", "Cycles Read 1",
        "Cycles Index 1", "Cycles Read 2", "Cycles Index 2", "Density", "Clusters PF",
        "Yields", "Q 30", "Phix Input", "Phix Output Percent", "Phix Barcode",
        "Name", "Total Read Count in Millions", "Max Cluster", "Phix Output Count"
    ]

    # Use dictionary comprehension to create the initial data dictionary
    data = {col: [None] * len(folders) for col in columns}
    data["Project Name"] = folders
    data["Date"] = dates
    data["Sequencer"] = sequencers

    # Initialize DataFrame with the data dictionary
    df = pd.DataFrame(data)

    # Convert 'Date' column to datetime format and sort DataFrame by 'Date'
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    df.sort_values(by='Date', inplace=True)

    # Set 'Project Name' as index of the DataFrame
    df.set_index('Project Name', inplace=True)

    return df

def process_folders(df, folders):
    """
    Process each (fastq) folder to fill in the DataFrame with detailed statistics.

    :param df: The initialized DataFrame.
    :param folders: List of folder names to process.
    :return: Updated DataFrame with added statistics.
    """
    for folder in tqdm(folders, desc="Processing folders"):
        if not utils.is_valid_folder(folder):
            continue
        update_dataframe_for_folder(df, folder)
    return df

def update_dataframe_for_folder(df, folder):
    """
    Update DataFrame rows for a given folder with detailed statistics.

    :param df: The DataFrame to update.
    :param folder: The folder name corresponding to the DataFrame row to update.
    """
    # Update DataFrame with parsed data from multiple sources
    parse_multiqc_data(df, folder)
    parse_fastq_stats_folder(df, folder)
    parse_sciebo_report(df, folder)

def postprocess_dataframe(df):
    """
    Perform post-processing on the DataFrame to finalize structure and calculations.

    :param df: The DataFrame to post-process.
    :return: The post-processed DataFrame.
    """
    df["Total Read Count in Millions"] = pd.to_numeric(df["Total Read Count in Millions"], errors='coerce').round(2)
    df['Expected Clusters'] = df['Sequencing Kit'].str.lower().map(SEQUENCING_KIT_TO_CLUSTERS)
    utils.calculate_ratios(df)
    utils.adjust_phix_percentages(df)

    # Calculate the number of samples meeting the reads requirement
    df['Expected Reading Per Sample'] = df['Application'].map(EXPECTED_READING_PER_SAMPLE_MAPPING)
    df['Number of Samples Above Requirement'], df['Number of Samples Below Requirement'] = zip(*df.apply(utils.check_read_count, axis=1))

    df.drop(["Max Cluster", "Expected Reading Per Sample", 'Phix Output Count'], axis=1, inplace=True)
    return df


if __name__ == '__main__':
    main()
