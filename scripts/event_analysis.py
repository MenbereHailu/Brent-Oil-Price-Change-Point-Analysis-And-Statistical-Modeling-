import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ruptures as rpt
import pymc as pm
import arviz as az
import logging
from datetime import timedelta
from scipy import stats
from matplotlib import rcParams


class BrentOilEventAnalyzer:
    """
    📈 Brent Oil Event Analyzer
    A class for analyzing event-specific changes in Brent oil prices using CUSUM, Bayesian change
    point detection, and statistical methods.

    🛠️ Features:
    - Detect change points in price trends 🛑
    - Bayesian inference for structural shifts 🔍
    - Analyze price movements around key events 📊

    Parameters:
    - price_data (pd.DataFrame): DataFrame with 'Date' as index and 'Price' column.
    - log_file (str): Path to the log file.
    - log_level (logging level): Logging level (default: logging.INFO).
    """

    def __init__(
        self,
        price_data: pd.DataFrame,
        log_file="../logs/brent_oil_analyzer.log",
        log_level=logging.INFO,
    ):
        self.price_data = price_data
        self.logger = self.setup_logging(log_file, log_level)
        self.mean_price = self.price_data["Price"].mean()
        self.logger.info("BrentOilEventAnalyzer initialized.")

    def setup_logging(self, log_file, log_level):
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        if not logger.hasHandlers():
            file_handler = logging.FileHandler(
                log_file, encoding="utf-8"
            )  # Set encoding to utf-8
            file_handler.setLevel(log_level)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger

    def calculate_cusum(self,color='red'):
        """📉 Computes and visualizes the CUSUM of price deviations."""
        try:
            # Set font to one that supports emojis
            rcParams["font.family"] = "sans-serif"
            rcParams["font.sans-serif"] = ["Segoe UI Emoji", "DejaVu Sans"]

            plt.figure(figsize=(12, 6))  
            cusum = (self.price_data["Price"] - self.mean_price).cumsum()
            plt.plot(
                self.price_data.index,
                cusum,
                label="CUSUM of Price Deviations",
                color=color,
            )  
            plt.title(
                "📉 CUSUM Analysis: Brent Oil Price Deviations",
                fontsize=14,
                fontweight="bold",
                color="#333",
            )
            plt.xlabel("📆 Date", fontsize=12)
            plt.ylabel("💰 Cumulative Sum of Deviations (USD)", fontsize=12)
            plt.legend()
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.show()
            self.logger.info("✅ CUSUM plot created successfully.")
        except Exception as e:
            self.logger.error("❌ Error calculating or plotting CUSUM: %s", e)

    def detect_change_point(self, n_bkps=5):
        """🚀 Detects structural changes in oil prices using the ruptures package."""
        try:
            plt.figure(figsize=(12, 6))
            price_df = self.price_data.reset_index()
            price_series = price_df["Price"].values

            algo = rpt.Binseg(model="rbf").fit(price_series)
            change_points = algo.predict(n_bkps=n_bkps)

            change_years = [price_df["Date"].iloc[cp].year for cp in change_points[:-1]]
            print("📌 Detected Change Point Years:", change_years)

            plt.plot(
                price_df["Date"],
                price_df["Price"],
                label="📊 Brent Oil Price",
                color="blue",
            ) 

            for cp in change_points[:-1]:
                year = price_df["Date"].iloc[cp].year
                plt.axvline(
                    price_df["Date"].iloc[cp], color="red", linestyle="--", alpha=0.7
                )
                plt.text(
                    price_df["Date"].iloc[cp],
                    price_df["Price"].iloc[cp],
                    str(year),
                    color="red",
                    fontsize=10,
                )

            plt.title(
                "📉 Brent Oil Prices & Change Points", fontsize=14, fontweight="bold"
            )
            plt.xlabel("📆 Date")
            plt.ylabel("💰 Price (USD)")
            plt.legend()
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.show()
            self.logger.info("✅ Change points detected and plotted successfully.")

        except Exception as e:
            self.logger.error("❌ Error detecting change points: %s", e)

    def bayesian_change_point_detection(self):
        """🔬 Bayesian analysis of structural changes in oil prices using PyMC."""
        try:
            plt.figure(figsize=(12, 6))
            data = self.price_data["Price"].values
            prior_mu = np.mean(data)

            with pm.Model() as model:
                change_point = pm.DiscreteUniform(
                    "change_point", lower=0, upper=len(data) - 1
                )
                mu1 = pm.Normal("mu1", mu=prior_mu, sigma=5)
                mu2 = pm.Normal("mu2", mu=prior_mu, sigma=5)
                sigma1 = pm.HalfNormal("sigma1", sigma=5)
                sigma2 = pm.HalfNormal("sigma2", sigma=5)

                likelihood = pm.Normal(
                    "likelihood",
                    mu=pm.math.switch(change_point >= np.arange(len(data)), mu1, mu2),
                    sigma=pm.math.switch(
                        change_point >= np.arange(len(data)), sigma1, sigma2
                    ),
                    observed=data,
                )

                trace = pm.sample(20, tune=10, chains=2, random_seed=42)
                self.logger.info("✅ Bayesian sampling completed successfully.")

                az.plot_trace(trace)
                plt.show()

                s_posterior = trace.posterior["change_point"].values.flatten()
                change_point_estimate = int(np.median(s_posterior))
                change_point_date = self.price_data.index[change_point_estimate]

                print(f"🕵️‍♂️ Estimated Change Point Date: {change_point_date}")
                self.logger.info(
                    "📌 Estimated change point date: %s", change_point_date
                )

                return change_point_date
        except Exception as e:
            self.logger.error("❌ Error in Bayesian change point analysis: %s", e)

    def _get_prices_around_event(self, event_date, days_before=30, days_after=30):
        """Helper function to get prices around a given event date."""
        before_date = event_date - timedelta(days=days_before)
        after_date = event_date + timedelta(days=days_after)
        prices_around_event = self.price_data[(self.price_data.index >= before_date) & (self.price_data.index <= after_date)]
        return prices_around_event


    def analyze_price_changes_around_events(self, key_events):
        """Analyzes and plots price changes around specific events."""
        results = []

        for event, date in key_events.items():
            try:
                event_date = pd.to_datetime(date)
                prices_around_event = self._get_prices_around_event(event_date, days_before=180, days_after=180)

                # Calculate percentage changes at different intervals
                change_1m = self._calculate_percentage_change(event_date, 30)
                change_3m = self._calculate_percentage_change(event_date, 90)
                change_6m = self._calculate_percentage_change(event_date, 180)

                # Calculate cumulative returns around the event
                cum_return_before = prices_around_event.loc[:event_date].pct_change().add(1).cumprod().iloc[-1] - 1
                cum_return_after = prices_around_event.loc[event_date:].pct_change().add(1).cumprod().iloc[-1] - 1

                results.append({
                    "Event": event,
                    "Date": date,
                    "Change_1M": change_1m,
                    "Change_3M": change_3m,
                    "Change_6M": change_6m,
                    "Cumulative Return Before": cum_return_before['Price'],
                    "Cumulative Return After": cum_return_after['Price']
                })
            except KeyError:
                self.logger.warning("Event %s at %s is out of price data range.", event, date)

        event_impact_df = pd.DataFrame(results)
        self._plot_price_trends_around_events(key_events)
        self._plot_percentage_changes_and_cumulative_returns(event_impact_df)
        t_test_df = self._perform_statistical_analysis(key_events)

        return event_impact_df, t_test_df

    def _calculate_percentage_change(self, event_date, days):
        """Calculates the percentage change in price before and after a given number of days around an event."""
        try:
            price_before = self.price_data.loc[event_date - timedelta(days=days), 'Price']
            price_after = self.price_data.loc[event_date + timedelta(days=days), 'Price']
            return ((price_after - price_before) / price_before) * 100
        except KeyError:
            return None

    def analyze_price_changes_around_events(self, key_events):
        """Analyzes and plots price changes around specific events."""
        results = []

        for event, date in key_events.items():
            try:
                event_date = pd.to_datetime(date)
                prices_around_event = self._get_prices_around_event(event_date, days_before=180, days_after=180)

                # Calculate percentage changes at different intervals
                change_1m = self._calculate_percentage_change(event_date, 30)
                change_3m = self._calculate_percentage_change(event_date, 90)
                change_6m = self._calculate_percentage_change(event_date, 180)

                # Calculate cumulative returns around the event
                cum_return_before = prices_around_event.loc[:event_date].pct_change().add(1).cumprod().iloc[-1] - 1
                cum_return_after = prices_around_event.loc[event_date:].pct_change().add(1).cumprod().iloc[-1] - 1

                results.append({
                    "Event": event,
                    "Date": date,
                    "Change_1M": change_1m,
                    "Change_3M": change_3m,
                    "Change_6M": change_6m,
                    "Cumulative Return Before": cum_return_before['Price'],
                    "Cumulative Return After": cum_return_after['Price']
                })
            except KeyError:
                self.logger.warning("Event %s at %s is out of price data range.", event, date)

        event_impact_df = pd.DataFrame(results)
        self._plot_price_trends_around_events(key_events)
        self._plot_percentage_changes_and_cumulative_returns(event_impact_df)
        t_test_df = self._perform_statistical_analysis(key_events)

        return event_impact_df, t_test_df

    def _calculate_percentage_change(self, event_date, days):
        """Calculates the percentage change in price before and after a given number of days around an event."""
        try:
            price_before = self.price_data.loc[event_date - timedelta(days=days), 'Price']
            price_after = self.price_data.loc[event_date + timedelta(days=days), 'Price']
            return ((price_after - price_before) / price_before) * 100
        except KeyError:
            return None

    def _plot_price_trends_around_events(self, key_events, days_before=180, days_after=180):
        """Plots price trends around specified events."""
        plt.figure(figsize=(14, 8))
        for event, date in key_events.items():
            event_date = pd.to_datetime(date)
            prices_around_event = self._get_prices_around_event(event_date, days_before=days_before, days_after=days_after)
            plt.plot(prices_around_event.index, prices_around_event['Price'], label=f"{event} ({date})")
            plt.axvline(event_date, color='red', linestyle='--', linewidth=0.8)
        
        plt.title("Brent Oil Price Trends Around Key Events")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    def _plot_percentage_changes_and_cumulative_returns(self, event_impact_df):
        """Plots percentage changes and cumulative returns before and after events."""
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))

        # Plot for percentage changes
        sns.barplot(data=event_impact_df.melt(id_vars=["Event", "Date"], 
                                              value_vars=["Change_1M", "Change_3M", "Change_6M"]),
                    x="Event", y="value", hue="variable", ax=axes[0])
        axes[0].set_title("Percentage Change in Brent Oil Prices Before and After Events")
        axes[0].set_ylabel("Percentage Change")
        axes[0].legend(title="Change Period")

        # Plot for cumulative returns
        sns.barplot(data=event_impact_df.melt(id_vars=["Event", "Date"], 
                                              value_vars=["Cumulative Return Before", "Cumulative Return After"]),
                    x="Event", y="value", hue="variable", ax=axes[1])
        axes[1].set_title("Cumulative Returns Before and After Events")
        axes[1].set_ylabel("Cumulative Return")
        axes[1].legend(title="Cumulative Return")

        plt.tight_layout()
        plt.show()

    def _perform_statistical_analysis(self, key_events):
        """Performs a t-test to assess significant price changes before and after events."""
        t_test_results = {}
        for event, date in key_events.items():
            event_date = pd.to_datetime(date)
            try:
                before_prices = self._get_prices_around_event(event_date, days_before=180).loc[:event_date]['Price']
                after_prices = self._get_prices_around_event(event_date, days_after=180).loc[event_date:]['Price']
                t_stat, p_val = stats.ttest_ind(before_prices, after_prices, nan_policy='omit')
                t_test_results[event] = {"t-statistic": t_stat, "p-value": p_val}
            except KeyError:
                self.logger.warning("Event %s at %s is out of price data range.", event, date)

        t_test_df = pd.DataFrame(t_test_results).T
        print(t_test_df)
        return t_test_df