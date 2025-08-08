import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import os

class DataVisualizer:
    def __init__(
        self,
        data: pd.DataFrame,
        log_file="../logs/data_visualizer.log",
        log_level=logging.INFO,
    ):
        """
        Initialize the DataVisualizer class with a dataset.

        Parameters:
        - data (pd.DataFrame): The dataset containing 'Date' and 'Price' columns.
        - log_file (str): Path to the log file.
        - log_level (logging level): Logging level (default: logging.INFO).
        """
        self.data = data
        self.logger = self.setup_logging(log_file, log_level)
        self.logger.info("DataVisualizer initialized.")

    def setup_logging(self, log_file, log_level):
        """
        Sets up logging for the visualizer.

        Parameters:
        - log_file (str): The file where logs will be saved.
        - log_level (logging level): The logging level.

        Returns:
        - logging.Logger: Configured logger instance.
        """
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        # Prevent adding multiple handlers in case of multiple class instances
        if not logger.hasHandlers():
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger

    def plot_box(self):
        """Plots a box plot of Brent Oil Prices."""
        try:
            plt.figure(figsize=(8, 4))
            sns.boxplot(data=self.data, y='Price')
            plt.title('Box Plot of Brent Oil Prices')
            plt.ylabel('Price (USD per barrel)')
            plt.show()
            self.logger.info("Box plot displayed successfully.")
        except Exception as e:
            self.logger.error(f"Error in plot_box: {e}")

    def plot_price_over_time(self):
        """Plots Brent Oil Prices over time."""
        try:
            plt.figure(figsize=(10, 4))
            plt.plot(self.data.index, self.data['Price'], label='Brent Oil Price', color='blue')
            plt.title('Brent Oil Prices Over Time')
            plt.xlabel('Date')
            plt.ylabel('Price (USD per barrel)')
            plt.legend()
            plt.show()
            self.logger.info("Price over time plot displayed successfully.")
        except Exception as e:
            self.logger.error(f"Error in plot_price_over_time: {e}")

    def plot_price_distribution(self):
        """Plots the distribution of Brent Oil Prices."""
        try:
            plt.figure(figsize=(10, 4))
            sns.histplot(self.data['Price'], bins=30, kde=True)
            plt.title('Price Distribution')
            plt.xlabel('Price (USD per barrel)')
            plt.ylabel('Frequency')
            plt.show()
            self.logger.info("Price distribution plot displayed successfully.")
        except Exception as e:
            self.logger.error(f"Error in plot_price_distribution: {e}")

    def plot_yearly_average(self):
        """Plots average Brent Oil Prices per year."""
        try:
            df = self.data.copy().reset_index()
            df['Year'] = df['Date'].dt.year
            yearly_avg = df.groupby('Year')['Price'].mean().reset_index()

            plt.figure(figsize=(12, 6))
            sns.barplot(x='Year', y='Price', data=yearly_avg, hue='Year', legend=False, palette='pastel')
            plt.title('Average Yearly Brent Oil Prices')
            plt.xlabel('Year')
            plt.ylabel('Average Price (USD per barrel)')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            plt.tight_layout()
            plt.show()
            self.logger.info("Yearly average price plot displayed successfully.")
        except Exception as e:
            self.logger.error(f"Error in plot_yearly_average: {e}")

    def plot_rolling_volatility(self, window=30):
        """Plots the rolling volatility (standard deviation) of Brent Oil Prices."""
        try:
            self.data['Rolling_Volatility'] = self.data['Price'].rolling(window=window).std()
            plt.figure(figsize=(10, 4))
            plt.plot(self.data.index, self.data['Rolling_Volatility'], color='red', label=f'{window}-Day Rolling Volatility')
            plt.title(f'{window}-Day Rolling Volatility of Brent Oil Prices')
            plt.xlabel('Date')
            plt.ylabel('Volatility (Rolling Standard Deviation)')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            self.logger.info(f"{window}-day rolling volatility plot displayed successfully.")
        except Exception as e:
            self.logger.error(f"Error in plot_rolling_volatility: {e}")
