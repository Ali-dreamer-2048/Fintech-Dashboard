import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Fintech Dashboard", layout="wide")

# Main title
st.title("Fintech Dashboard - Stock Screener & FX Checker")

# Tabs
tab1, tab2 = st.tabs(["Stock Portfolio Screener", "FX Rate Checker"])

# Tab 1: Stock Portfolio Screener
with tab1:
    st.header("Stock Portfolio Screener")

    tickers_input = st.text_input(
        "Enter stock tickers (comma-separated, e.g., 0700.HK, AAPL, TSLA)",
        value="AAPL, MSFT, TSLA"
    )
    tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.today())

    if st.button("Start Screening", key="stock_screen_button") and tickers:
        if start_date >= end_date:
            st.error("Start date must be earlier than end date")
        else:
            with st.spinner("Downloading stock data..."):
                try:
                    raw_data = yf.download(tickers, start=start_date, end=end_date, progress=False)

                    # Safely extract Adjusted Close
                    if isinstance(raw_data.columns, pd.MultiIndex):
                        adj_close = raw_data['Adj Close'] if 'Adj Close' in raw_data.columns.levels[0] else raw_data['Close']
                    else:
                        adj_close = raw_data['Adj Close'] if 'Adj Close' in raw_data.columns else raw_data['Close']

                    if adj_close.empty or len(adj_close) < 2:
                        st.warning("Insufficient data. Please check tickers or date range.")
                    else:
                        returns = adj_close.pct_change().dropna()
                        ann_ret = returns.mean() * 252 * 100
                        ann_vol = returns.std() * np.sqrt(252) * 100
                        sharpe = np.where(ann_vol > 1e-6, ann_ret / ann_vol, 0)

                        df = pd.DataFrame({
                            'Ticker': ann_ret.index,
                            'Annualized Return (%)': ann_ret.round(2),
                            'Annualized Volatility (%)': ann_vol.round(2),
                            'Sharpe Ratio': sharpe.round(2)
                        }).set_index('Ticker')

                        # Performance table
                        st.subheader("Performance Metrics")
                        st.dataframe(
                            df.sort_values('Sharpe Ratio', ascending=False).style.format("{:.2f}").background_gradient(cmap='RdYlGn', subset=['Sharpe Ratio']),
                            use_container_width=True
                        )

                        # Chart 1: Cumulative Return (Top priority)
                        st.subheader("Cumulative Return Trend Over Time")
                        cum_returns = (1 + returns).cumprod() * 100 - 100
                        fig_cum = px.line(
                            cum_returns,
                            title="Cumulative Return Trend Over Time",
                            labels={'value': 'Cumulative Return (%)', 'index': 'Date'},
                            height=500
                        )
                        fig_cum.update_layout(
                            hovermode="x unified",
                            template="plotly_white",
                            legend_title="Ticker"
                        )
                        st.plotly_chart(fig_cum, use_container_width=True)

                        # Chart 2: Enhanced Return vs Volatility (Dual-axis horizontal bar)
                        st.subheader("Return vs Volatility Comparison")
                        fig_dual = go.Figure()

                        # Return bars (left axis)
                        fig_dual.add_trace(go.Bar(
                            y=df.index,
                            x=df['Annualized Return (%)'],
                            name='Annualized Return (%)',
                            orientation='h',
                            marker_color=np.where(df['Annualized Return (%)'] >= 0, 'royalblue', 'tomato'),
                            text=df['Annualized Return (%)'].round(2).astype(str) + '%',
                            textposition='auto',
                            width=0.35  # 更細的柱子
                        ))

                        # Volatility line (right axis)
                        fig_dual.add_trace(go.Scatter(
                            y=df.index,
                            x=df['Annualized Volatility (%)'],
                            name='Annualized Volatility (%)',
                            mode='lines+markers+text',
                            text=df['Annualized Volatility (%)'].round(1).astype(str) + '%',
                            textposition='middle right',
                            line=dict(color='orange', width=2, dash='dot'),
                            marker=dict(size=10, symbol='circle', color='orange'),
                            yaxis='y2'
                        ))

                        fig_dual.update_layout(
                            title="Return vs Volatility by Ticker",
                            xaxis_title="Annualized Return (%)",
                            yaxis_title="Ticker",
                            yaxis2=dict(
                                title="Annualized Volatility (%)",
                                overlaying='y',
                                side='right'
                            ),
                            height=500,
                            barmode='overlay',
                            template="plotly_white",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            bargap=0.1
                        )

                        st.plotly_chart(fig_dual, use_container_width=True)

                        # Chart 3: Risk-Return Scatter
                        st.subheader("Risk-Return Scatter Plot")
                        df['Sharpe Color'] = df['Sharpe Ratio']
                        fig_scatter = px.scatter(
                            df.reset_index(),
                            x='Annualized Volatility (%)',
                            y='Annualized Return (%)',
                            size='Sharpe Ratio',
                            color='Sharpe Color',
                            hover_name='Ticker',
                            title="Risk vs Return (Size/Color by Sharpe Ratio)",
                            labels={'Sharpe Color': 'Sharpe Ratio'},
                            color_continuous_scale='RdYlGn_r',
                            height=500
                        )
                        fig_scatter.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
                        st.plotly_chart(fig_scatter, use_container_width=True)

                except Exception as e:
                    st.error(f"Data download failed: {str(e)}")

# Tab 2: FX Rate Checker
with tab2:
    st.header("FX Rate Checker")

    currency_options = {
        "USD → HKD": "USDHKD=X",
        "CNY → HKD": "CNYHKD=X",
        "EUR → HKD": "EURHKD=X",
        "JPY → HKD": "JPYHKD=X"
    }
    selected = st.selectbox("Select Currency Pair", list(currency_options.keys()))
    pair = currency_options[selected]

    days = st.slider("Show Past Days", min_value=30, max_value=365, value=180)

    if st.button("Query Exchange Rate", key="fx_query_button"):
        with st.spinner("Downloading exchange rate data..."):
            try:
                data = yf.download(pair, period=f"{days}d", progress=False, auto_adjust=True)

                # Safely extract Close or Adj Close (no debug info)
                if isinstance(data.columns, pd.MultiIndex):
                    close_col = data.get(('Close', pair), data.get(('Adj Close', pair)))
                else:
                    close_col = data['Close'] if 'Close' in data.columns else data.get('Adj Close', data.iloc[:, -1])

                close_col = close_col.dropna()

                if close_col.empty:
                    st.warning(f"No valid data for {pair}.")
                else:
                    current = float(close_col.iloc[-1])

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=close_col.index,
                        y=close_col.values,
                        mode='lines',
                        name=f"{selected} Rate",
                        line=dict(color='royalblue', width=2)
                    ))

                    ma_30 = close_col.rolling(window=30).mean()
                    fig.add_trace(go.Scatter(
                        x=ma_30.index,
                        y=ma_30.values,
                        mode='lines',
                        name="30-Day MA",
                        line=dict(color='orange', width=1, dash='dash')
                    ))

                    fig.update_layout(
                        title=f"{selected} Exchange Rate Trend",
                        xaxis_title="Date",
                        yaxis_title="Exchange Rate",
                        hovermode="x unified",
                        template="plotly_white"
                    )

                    st.plotly_chart(fig, use_container_width=True)
                    st.metric(label=f"Current Rate ({selected})", value=f"{current:.4f} HKD")

            except Exception as e:
                st.error(f"Download failed: {str(e)}")

# Footer
