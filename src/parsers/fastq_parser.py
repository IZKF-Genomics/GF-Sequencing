import json
import os
import logging

from config import FASTQ_FOLDER_PATH

# Create a logger for the current module
logger = logging.getLogger(__name__)

def parse_fastq_stats_folder(df, fastq_folder_name):
    """
    Parse FastQ stats from a specified folder and update the DataFrame with the extracted data.

    :param df: The pandas DataFrame to update.
    :param fastq_folder_name: The name of the folder containing FastQ stats.
    """
    stats_json_path = os.path.join(FASTQ_FOLDER_PATH, fastq_folder_name, "Stats", "Stats.json")
    if not os.path.exists(stats_json_path):
        logger.error(f"The path: '{stats_json_path}' does not exist!")
        return

    with open(stats_json_path, 'r') as file:
        stats_data = json.load(file)

    unknown_barcodes = extract_unknown_barcodes(stats_data)
    distribution_string, main_unknown_barcode_percentage = calculate_barcode_percentages(unknown_barcodes)
    phix_output_count, phix_barcode = find_phix_output(unknown_barcodes)

    # Update DataFrame
    df.loc[fastq_folder_name, 'Most Common Undetermined Barcode'] = unknown_barcodes[0][0] if unknown_barcodes else None
    df.loc[fastq_folder_name, 'Undetermined Distribution String'] = distribution_string
    df.loc[fastq_folder_name, 'Most Common Undetermined Barcode Percentage'] = main_unknown_barcode_percentage
    df.loc[fastq_folder_name, 'Phix Output Count'] = phix_output_count
    df.loc[fastq_folder_name, 'Phix Barcode'] = phix_barcode

def extract_unknown_barcodes(stats_data):
    """
    Extract unknown barcodes from stats data.

    :param stats_data: Parsed JSON data containing stats.
    :return: Sorted list of unknown barcodes and their counts.
    """
    unknown_barcodes = {}
    for lane in stats_data.get('UnknownBarcodes', []):
        # Iterate through key-value pairs in each dictionary
        for key, value in lane['Barcodes'].items():
            # Update the combined dictionary, summing up values for duplicate keys
            unknown_barcodes[key] = unknown_barcodes.get(key, 0) + value

    return sorted(unknown_barcodes.items(), key=lambda x: x[1], reverse=True)

def calculate_barcode_percentages(unknown_barcodes):
    """
    Calculate barcode percentages from unknown barcode counts.

    :param unknown_barcodes: List of unknown barcodes and their counts.
    :return: Distribution string and the percentage of the most common unknown barcode.
    """
    if unknown_barcodes is None:
        return None, None

    total_counts = sum(count for _, count in unknown_barcodes)
    percentages = [round((count / total_counts) * 100, 1) for _, count in unknown_barcodes if count != 0]
    distribution_string = '-'.join(map(str, percentages[:15])) # Limit to the top 15 percentages
    if percentages:
        return distribution_string, percentages[0]  
    else: 
        return None, None

def find_phix_output(unknown_barcodes):
    """
    Find PhiX output from the list of unknown barcodes.

    :param unknown_barcodes: List of unknown barcodes and their counts.
    :return: PhiX output count and barcode, if found.
    """
    desired_pattern_no_plus = 'G'
    desired_value_paired_end = 'GGGGGGGGGG+AGATCTCGGT'
    for barcode, value in unknown_barcodes:
        if '+' in barcode and barcode == desired_value_paired_end:
            logger.info(f"Found the pair with '+': {barcode}: {value}")
            return value, barcode
        elif all(char == desired_pattern_no_plus for char in barcode):
            logger.info(f"Found the pair without '+': {barcode}: {value}")
            return value, barcode
    return None, None
