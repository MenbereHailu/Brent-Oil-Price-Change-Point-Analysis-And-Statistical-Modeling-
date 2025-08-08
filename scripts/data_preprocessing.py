import logging
import os
import pandas as pd
from IPython.display import display, Markdown  


class DataPreprocessor:
    def __init__(
        self,
        file_path: str,
        output_dir: str = "../data/",
        output_file: str = "data.csv",
        log_file="../logs/data_preprocessing.log",
        log_level=logging.INFO,
    ):
        """
        Initialize the DataPreprocessor class with the local file path to the dataset.

        Parameters:
        file_path (str): The local file path to the data file.
        output_dir (str): The directory where the data file will be saved.
        output_file (str): The local file name to save the downloaded data.
        log_file (str): The file where logs will be saved.
        log_level (logging level): The level of logging (default is logging.INFO).
        """
        self.file_path = file_path
        self.output_dir = output_dir
        self.output_file = os.path.join(self.output_dir, output_file)
        self.data: pd.DataFrame = None
        self.logger = self.setup_logging(log_file, log_level)

    def setup_logging(self, log_file, log_level):
        """
        Sets up logging for the application.

        Parameters:
        log_file (str): The name of the file to save logs.
        log_level (logging level): The logging level.

        Returns:
        logging.Logger: The configured logger instance.
        """
        # Ensure the directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        # Create a file handler for logging
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # Define the logging format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

        return logger

    def load_data(self) -> pd.DataFrame:
        """
        Load the dataset from the local file path and save it in the specified directory.

        Returns:
        pd.DataFrame: The loaded dataset.
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            self.logger.info(f"Directory checked/created: {self.output_dir}")

            self.logger.info("Loading data from the local file path.")

            self.data = pd.read_csv(self.file_path)

            # Convert Date to Datetime format
            self.data["Date"] = pd.to_datetime(
                self.data["Date"].str.strip(), errors="coerce"
            )

            self.logger.info("Data loaded into DataFrame successfully.")
            return self.data

        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise


    def inspect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Inspect the given DataFrame for structure, completeness, summary statistics,
        correlation, and outlier detection.

        Parameters:
        - df (pd.DataFrame): The DataFrame to inspect.

        Returns:
        - pd.DataFrame: Summary statistics for numeric columns.
        """
        if df.empty:
            raise ValueError("The DataFrame is empty.")

        try:
            # Check and display the dimensions of the DataFrame
            dimensions = df.shape
            display(Markdown(f"### 📏 **Dimensions (rows, columns):** {dimensions}"))
            self.logger.info(f"DataFrame dimensions: {dimensions}")

            # Check and display data types of each column
            data_types = df.dtypes
            display(Markdown("### 📊 **Data Types:**"))
            display(data_types)
            self.logger.info("Displayed data types for each column.")

            # Check for missing values in each column
            missing_values = df.isnull().sum()
            display(Markdown("### ❓ **Missing Values:**"))
            if missing_values.any():
                display(missing_values[missing_values > 0])
                self.logger.warning("Missing values found.")
            else:
                display(Markdown("**No missing values found. ✅**"))
                self.logger.info("No missing values detected.")

            # Check and display the count of unique values for each column
            unique_values = df.nunique()
            display(Markdown("### 🔍 **Unique Values in Each Column:**"))
            display(unique_values)

            # Count the number of duplicate rows
            duplicate_count = df.duplicated().sum()
            display(Markdown(f"### 🚨 **Number of Duplicate Rows: {duplicate_count}**"))
            self.logger.info(f"Duplicate rows found: {duplicate_count}")

            # View duplicate rows if any
            if duplicate_count > 0:
                duplicates = df[df.duplicated()]
                display(Markdown("### 🔄 **Duplicate Rows:**"))
                display(duplicates)

            # Summary statistics for numeric columns
            summary_statistics = df.describe(include='number')
            display(Markdown("### 📈 **Summary Statistics for Numeric Columns:**"))
            display(summary_statistics)

            # Correlation matrix (only for numeric columns)
            correlation_matrix = df.corr()
            display(Markdown("### 🔗 **Correlation Matrix:**"))
            display(correlation_matrix)

            # Outlier detection using IQR for numeric columns only
            numeric_df = df.select_dtypes(include='number')
            Q1 = numeric_df.quantile(0.25)
            Q3 = numeric_df.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_counts = ((numeric_df < lower_bound) | (numeric_df > upper_bound)).sum()
            display(Markdown("### 🚫 **Outlier Counts in Each Numeric Column:**"))
            display(outlier_counts[outlier_counts > 0])

        except Exception as e:
            self.logger.error(f"An error occurred while inspecting the dataset: {e}")
            raise
