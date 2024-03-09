import pandas as pd
import numpy as np
import os 
import logging

from config import FASTQ_FOLDER_PATH

# get the logger for the current module
logger = logging.getLogger(__name__)

def parse_multiqc_data(df, fastq_folder_name):
    multiqc_bcl2fastq_bysample_path = os.path.join(FASTQ_FOLDER_PATH, fastq_folder_name, "multiqc", "multiqc_data", "multiqc_bcl2fastq_bysample.txt")
    if not os.path.exists(multiqc_bcl2fastq_bysample_path):
        return  

    df_by_sample = pd.read_csv(multiqc_bcl2fastq_bysample_path, sep='\t')
    
    count_total_reads = df_by_sample['total'].sum()
    count_undetermined_reads = df_by_sample.loc[df_by_sample['Sample'] == 'undetermined', 'total'].iloc[0]
    undertermined_read_percentage = round(count_undetermined_reads / count_total_reads * 100, 1)

    read_counts = df_by_sample['total']
    std_deviation = np.std(read_counts)
    std_deviation_millions = round(std_deviation / 1e6, 2)
    mean_value = np.mean(read_counts)
    cv_percentage = round((std_deviation / mean_value) * 100, 1)

    percentages = np.round((read_counts / count_total_reads) * 100, decimals=1)
    distribution_string = '-'.join(map(str, percentages))

    # Update DataFrame directly
    df.loc[fastq_folder_name, 'STD in Millions'] = std_deviation_millions
    df.loc[fastq_folder_name, 'CV'] = cv_percentage
    df.loc[fastq_folder_name, 'Undetermined Reads Percentage'] = undertermined_read_percentage
    df.loc[fastq_folder_name, 'Read Distribution'] = distribution_string
    df.loc[fastq_folder_name, 'Total Read Count in Millions'] = count_total_reads / 1e6