# DataPreprocessor

## Overview
The `DataPreprocessor` class is designed to load, inspect, and preprocess data from a local CSV file. It provides logging, missing value detection, duplicate checking, and outlier analysis. This script is useful for preparing datasets before analysis or modeling.

## Features
- Loads CSV data and converts date columns to datetime format.
- Logs operations to a file.
- Inspects data structure, missing values, unique values, duplicates, summary statistics, and correlation.
- Detects outliers using the IQR method.

## Installation
Ensure you have Python installed (>=3.7). Then, install the required dependencies:
```pip install pandas ipython```

## Usage
### 1. Initialize and Load Data
```from scripts.data_preprocessing import DataPreprocessor```

# Initialize with the dataset file path
preprocessor = DataPreprocessor(file_path="data/BrentOilPrices.csv")

# Load the data
```data = preprocessor.load_data()```

### 2. Inspect Data
```preprocessor.inspect(data)```

This will display:
- Data dimensions (rows, columns)
- Data types of each column
- Missing values count
- Number of unique values per column
- Duplicate row count
- Summary statistics
- Correlation matrix
- Outlier counts

## Logging
The script logs all actions in `logs/data_preprocessing.log` by default. You can specify a different log file when initializing:
```preprocessor = DataPreprocessor(file_path="BrentOilPrices.csv", log_file="custom_log.log")```

## Directory Structure
```
Brent-Oil-Price-Change-Point-Analysis/
│-- data/
│   ├── BrentOilPrices.csv
│-- logs/
│   ├── data_preprocessing.log
│-- scripts/
│   ├── data_preprocessing.py
│-- tests/
│   ├── test_data_preprocessing.py
```

## Error Handling
- If the CSV file is missing, an error is logged, and an exception is raised.
- If the DataFrame is empty, `inspect()` raises a `ValueError`.

## Contributing
Feel free to submit pull requests to improve functionality, add tests, or optimize performance.

## License
MIT License

