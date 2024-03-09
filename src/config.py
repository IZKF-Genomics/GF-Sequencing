# Constants for folder paths
FASTQ_FOLDER_PATH = "/data/fastq"
SCIEBO_FOLDER_PATH = "data/sciebo/"

# Mapping dictionaries for sequencing kits and expected clusters
SEQUENCING_KIT_TO_CLUSTERS = {
    'nextseq 500/550 high output kit v2.5 (75 cycles)': '400 mio.',
    'nextseq 500/550 high output kit v2.5 (150 cycles)': '400 mio.',
    'nextseq 500/550 mid output kit v2.5 (300 cycles)': '130 mio.',
    'nextseq 500/550 mid output kit v2.5 (150 cycles)': '130 mio.',
    'miseq reagent kit v3 (150-cycle)': '22–25 million',
    'miseq reagent kit v3 (600-cycles)': '22–25 million',
    'miseq reagent kit v2 (50-cycles)': '12-15 million',
    'miseq reagent kit v2 (300-cycles)': '12-15 million',
    'miseq reagent kit v2 (500-cycles)': '12-15 million',
    'miseq reagent micro kit v2 (300-cycles)': '4 million',
    'miseq reagent nano kit v2 (300-cycles)': '1 million',
    'miseq reagent nano kit v2 (500-cycles)': '1 million',
    'novaseq 6000 s4 reagent kit v1.5 (300 cycles)': '8–10 billion',
    'novaseq 6000 s4 reagent kit v1.5 (200 cycles)': '8–10 billion',
    'novaseq 6000 s4 reagent kit v1.5 (35 cycles)': '8–10 billion',
    'novaseq 6000 s2 reagent kit v1.5 (300 cycles)': '3.3–4.1 billion',
    'novaseq 6000 s2 reagent kit v1.5 (200 cycles)': '3.3–4.1 billion',
    'novaseq 6000 s2 reagent kit v1.5 (100 cycles)': '3.3–4.1 billion',
    'novaseq 6000 s1 reagent kit v1.5 (300 cycles)': '1.3–1.6 billion',
    'novaseq 6000 s1 reagent kit v1.5 (200 cycles)': '1.3–1.6 billion',
    'novaseq 6000 s1 reagent kit v1.5 (100 cycles)': '1.3–1.6 billion',
    'novaseq 6000 sp 500 cycles': '650–800 million',
    'novaseq 6000 sp 300 cycles': '650–800 million',
    'novaseq 6000 sp 200 cycles)': '650–800 million',
    'novaseq 6000 sp 100 cycles': '650–800 million',
    }

SEQUENCING_KIT_TO_MAX_CLUSTERS = {
    'nextseq 500/550 high output kit v2.5 (75 cycles)': 400000000,
    'nextseq 500/550 high output kit v2.5 (150 cycles)': 400000000,
    'nextseq 500/550 mid output kit v2.5 (300 cycles)': 130000000,
    'nextseq 500/550 mid output kit v2.5 (150 cycles)': 130000000,
    'miseq reagent kit v3 (150-cycle)': 25000000,
    'miseq reagent kit v3 (600-cycles)': 25000000,
    'miseq reagent kit v2 (50-cycles)': 15000000,
    'miseq reagent kit v2 (300-cycles)': 15000000,
    'miseq reagent kit v2 (500-cycles)': 15000000,
    'miseq reagent micro kit v2 (300-cycles)': 4000000,
    'miseq reagent nano kit v2 (300-cycles)': 1000000,
    'miseq reagent nano kit v2 (500-cycles)': 1000000,
    'novaseq 6000 s4 reagent kit v1.5 (300 cycles)': 10000000000,
    'novaseq 6000 s4 reagent kit v1.5 (200 cycles)': 10000000000,
    'novaseq 6000 s4 reagent kit v1.5 (35 cycles)': 10000000000,
    'novaseq 6000 s2 reagent kit v1.5 (300 cycles)': 4100000000,
    'novaseq 6000 s2 reagent kit v1.5 (200 cycles)': 4100000000,
    'novaseq 6000 s2 reagent kit v1.5 (100 cycles)': 4100000000,
    'novaseq 6000 s1 reagent kit v1.5 (300 cycles)': 1600000000,
    'novaseq 6000 s1 reagent kit v1.5 (200 cycles)': 1600000000,
    'novaseq 6000 s1 reagent kit v1.5 (100 cycles)': 1600000000,
    'novaseq 6000 sp 500 cycles': 800000000, 
    'novaseq 6000 sp 300 cycles': 800000000,
    'novaseq 6000 sp 200 cycles)': 800000000,
    'novaseq 6000 sp 100 cycles': 800000000,
    }

EXPECTED_READING_PER_SAMPLE_MAPPING = {
    'RNAseq': None,
    'tRNAseq': 50000000,
    'mRNAseq': 30000000, 
    '3mRNAseq': 10000000, 
    'ChIPseq': None, 
    'ATACseq': 50000000, 
    'ampliseq': None, 
    'scRNAseq': None,    
    'scVDJseq': None, 
    'scATACseq': None, 
    'miRNAseq': 10000000, 
    'BWGS': None, 
    'WES': None, 
    'fastq': None, 
    '16S': None, 
    'MAG': None
    }

# Mapping Lowercase application to the GPM naming convention
APPLICATION_MAPPING = {
    'rnaseq': 'RNAseq',
    'trnaseq': 'tRNAseq',
    'mrnaseq': 'mRNAseq', 
    '3mrnaseq': '3mRNAseq', 
    'chipseq': 'ChIPseq', 
    'atacseq': 'ATACseq', 
    'ampliseq': 'ampliseq', 
    'scrnaseq': 'scRNAseq',    
    'scvdjseq': 'scVDJseq', 
    'scatacseq': 'scATACseq', 
    'mirnaseq': 'miRNAseq', 
    'bwgs': 'BWGS', 
    'wes': 'WES', 
    'fastq': 'fastq', 
    '16s': '16S', 
    'mag': 'MAG'
}
