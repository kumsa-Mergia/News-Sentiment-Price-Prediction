import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, Dict


class StockAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the StockAnalyzer with a CSV file.

        Args:
            data_path (str): Path to CSV file with stock data
        """
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Load CSV data with proper column names"""
        try:
            df = pd.read_csv(self.data_path, parse_dates=["Date"])
            df.sort_values("Date", inplace=True)
            df.set_index("Date", inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

    def calculate_technical_indicators(self) -> pd.DataFrame:
        """Calculate basic technical indicators"""
        df = self.data.copy()

        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()

        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        df['RSI'] = 100 - (100 / (1 + rs))

        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        return df

    def plot_stock_data(self, data: pd.DataFrame, indicators: bool = True, volume: bool = True) -> None:
        """Plot stock data with optional indicators and volume"""
        fig = make_subplots(
            rows=2 if volume else 1,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3] if volume else [1]
        )

        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )

        if indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='red')), row=1, col=1)

        if volume and 'Volume' in data.columns:
            fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'), row=2, col=1)

        fig.update_layout(
            title='Stock Price with Technical Indicators',
            xaxis_title='Date',
            yaxis_title='Price',
            template='plotly_white'
        )

        fig.show()
