# GF-Sequencing

This package provides tools for parsing sequencing data, analyzing it, and presenting the results through a comprehensive Shiny application. It's designed to streamline the workflow for bioinformatics data processing and visualization.

## Features

- Data parsing from various formats
- Data analysis and preprocessing
- Visualization of sequencing data
- Shiny app for interactive data exploration

## Getting Started

### Prerequisites

- Python 3.9
- R (version required by Shiny app)
- Conda (recommended for environment management)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Ilya-Fradlin/GF-Sequencing.git
    cd GF-Sequencing
    ```

2. Create a Conda environment:

    ```sh
    conda create --name parser python=3.9
    conda activate parser
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. Run the main script to parse data and generate the DataFrame:

    ```sh
    python src/main.py
    ```

2. Start the Shiny app to visualize the data:

## Shiny App

The included Shiny app provides an interactive interface to explore the sequencing data. Features include:

- Interactive plots and tables
- Data filtering and selection


## License

This project is licensed under the Genomics Facility - Uniklinik Aachen.
