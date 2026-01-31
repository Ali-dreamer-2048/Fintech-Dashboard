# Fintech Dashboard

An interactive web-based Fintech dashboard developed with Streamlit for CityU Year 1 Fintech project (JS1221).  
The tool allows users to analyze stocks and monitor exchange rates with real-time data from Yahoo Finance.

## Features

- **Stock Portfolio Screener**
  - Input multiple stock tickers (e.g., AAPL, TSLA, 0700.HK)
  - Calculate and compare:
    - Annualized Return (%)
    - Annualized Volatility (%)
    - Sharpe Ratio
  - Visualizations:
    - Cumulative Return Trend Over Time (line chart)
    - Return vs Volatility Comparison (dual-axis horizontal bar chart)
    - Risk-Return Scatter Plot (size/color by Sharpe Ratio)

- **FX Rate Checker**
  - Select currency pairs (USD→HKD, CNY→HKD, EUR→HKD, JPY→HKD)
  - Query historical exchange rate trend (customizable days)
  - Display interactive line chart with 30-day Moving Average
  - Show current exchange rate in real-time

## Technologies Used

- Streamlit (web app framework)
- yfinance (real-time financial data)
- Pandas & NumPy (data processing & calculations)
- Plotly (interactive charts & visualizations)

## Installation & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Ali-dreamer-2048/fintech-dashboard.git
   cd fintech-dashboard
   
2.Install dependencies:
Bash
pip install -r requirements.txt

3.Launch the application:
Bash
streamlit run app.py
or Open http://localhost:8501 in your browser.
