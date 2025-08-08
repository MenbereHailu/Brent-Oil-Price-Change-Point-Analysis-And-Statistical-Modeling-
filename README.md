# 🌍 **Brent-Oil-Price-Change-Point-Analysis** 🛢️
This project analyzes Brent oil prices using change point detection and statistical modeling to assess how significant political and economic events influence prices. 

## 📊 **It features**:

+ Historical Data Collection 📅
+ ARIMA and Bayesian Methods 📈
+ Exploratory Data Analysis Visualizations 🔍
+ Interactive Dashboard for real-time insights 💻✨
  
# 📊 Methodologies and Statistical Exploration

## 1. Data Analysis Workflow
The analysis follows a structured workflow to ensure a comprehensive understanding of the data and its relationship with significant events. The workflow includes the following steps:

### Data Preprocessing
- **Load and Clean Data**: Ensure proper date formatting and handle any anomalies.
- **Exploratory Data Analysis (EDA)**: Understand the distribution of Brent oil prices and identify potential outliers.

### Event Identification
- **Timeline Creation**: Develop a timeline of key historical events that may have influenced Brent oil prices.
- **Event Mapping**: Map these events to the time series data to facilitate analysis.

---

## 2. Time Series Analysis
To analyze the impact of events on Brent oil prices, we will employ several time series methodologies:

### ARIMA (AutoRegressive Integrated Moving Average)
- Helps understand trends and seasonality in the oil price data.
- Implements model selection criteria like AIC (Akaike Information Criterion) to determine the best-fitting model.

### GARCH (Generalized Autoregressive Conditional Heteroskedasticity)
- Models volatility in oil prices, crucial for understanding periods of instability caused by geopolitical events.

### VAR (Vector Autoregression)
- Assesses the relationship between Brent oil prices and other economic indicators (e.g., GDP, inflation, unemployment rates).
- Captures interdependencies among multiple time series.

---

## 3. Machine Learning Approaches
To refine our predictions and capture complex patterns, we will explore the following machine learning methodologies:

### LSTM (Long Short-Term Memory) Networks
- Effective for time series forecasting, as they can learn long-term dependencies in sequential data.

### Regime-Switching Models
- Utilizes models like Markov-Switching ARIMA to capture different market conditions and regimes that may affect oil prices differently.

---

## 4. Statistical Tests and Validation
To validate the findings, we will use:

### Granger Causality Tests
- Assess whether past values of identified events can predict Brent oil prices, establishing a causal relationship.

### Cointegration Analysis
- Explore long-term relationships between Brent oil prices and other relevant economic indicators.

---

## 5. Visualization Techniques
To effectively communicate results, we will utilize various visualization techniques:

### Time Series Plots
- Visualize Brent oil prices over time with annotations for significant events to demonstrate their impact visually.

### Seasonality Analysis
- Decompose the time series data to highlight seasonal trends and cycles in oil prices.

### Scatter Plots
- Explore the relationship between Brent oil prices and other economic variables, helping to identify correlations.

---

## 6. Areas for Deeper Exploration
Further statistical exploration will include:

### Impact Assessment
- Quantify the magnitude of price changes associated with each significant event, possibly using regression analysis to measure the effect size.

### Sentiment Analysis
- Analyze public sentiment and media coverage of key events to understand their psychological impact on market behavior.

### Scenario Analysis
- Conduct what-if analyses to predict potential future price movements based on varying event scenarios.
  


# 📁 **Project Structure**

```
+---.github
| └── workflows
|   ├──  blank.yml
+---.vscode
| └── settings.json
+---api
| ├── init.py
| └── README.md
+---notebooks
| ├── init.ipynb
| ├── Brent_Oil_Price_Change_Point_Analysis
| ├── Econometric_Analysis.ipynb
| ├── Oil_Price_Prediction.ipynb
| └── README.md
+---scripts
| ├── init.py
| ├── data_preprocessing.py
| ├── data_visualizer.py
| ├── event_analysis.py
| └── README.md
+---src
| ├── init.py
| └── README.md
+---tests
| ├── init.py
| ├── test_data_preprocessing.py
| ├── README.md
| ├── .gitignore
| ├── LICENSE
| ├── README.md
| └── requirements.txt
```