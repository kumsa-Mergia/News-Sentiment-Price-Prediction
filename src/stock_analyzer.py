import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import talib
# import pynance # pynance is commented out as we are using a mock for demonstration

# --- Mocking pynance.Stock for demonstration purposes ---
# This mock class simulates the behavior of pynance.Stock by providing
# dummy financial metrics. In a real application, if pynance is installed
# and configured, you would use the actual 'Stock' class.
class MockStock:
    """
    A mock class to simulate pynance.Stock for demonstration.
    Provides dummy financial metrics.
    """
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.name = f"{ticker} Corp."
        self.pe = round(np.random.uniform(15, 35), 2) # Dummy P/E Ratio
        self.eps = round(np.random.uniform(1.5, 5.0), 2) # Dummy EPS
        self.market_cap = f"{round(np.random.uniform(50, 2000), 2)} Billion" # Dummy Market Cap

class StockAnalyzer:
    """
    Analyzes stock data, calculates technical indicators,
    and visualizes the results.
    """
    def __init__(self, ticker: str, data_path: str): # <-- THIS IS THE CRUCIAL LINE
        """
        Initialize the StockAnalyzer with a stock ticker and the path
        to its historical data CSV file.
        """
        self.ticker = ticker
        self.data_path = data_path
        self.data = self._load_data()
        # Use the MockStock for financial metrics.
        # Replace with 'Stock(ticker)' if pynance is installed and configured for real data.
        self.stock = MockStock(ticker)

    def _load_data(self) -> pd.DataFrame:
        """
        Loads stock CSV data from the specified file path.
        Includes error handling for file not found.
        """
        try:
            print(f"Attempting to load data for {self.ticker} from: {self.data_path}")
            df = pd.read_csv(self.data_path, parse_dates=["Date"])
            df.sort_values("Date", inplace=True)
            df.set_index("Date", inplace=True)
            print(f"Data for {self.ticker} loaded successfully.")
            return df
        except FileNotFoundError:
            print(f"Error: CSV file not found at {self.data_path}. Please ensure the path is correct.")
            print(f"Generating dummy data for {self.ticker} as a fallback for demonstration.")
            return self._generate_dummy_data()
        except Exception as e:
            print(f"Error loading data for {self.ticker} from {self.data_path}: {e}")
            print(f"Generating dummy data for {self.ticker} as a fallback for demonstration.")
            return self._generate_dummy_data()

    def _generate_dummy_data(self) -> pd.DataFrame:
        """
        Generates dummy stock OHLCV data as a fallback when actual file loading fails.
        This ensures the rest of the analysis can still run for demonstration.
        """
        print(f"Generating dummy stock data for {self.ticker}...")
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        np.random.seed(hash(self.ticker) % (2**32 - 1)) # Seed based on ticker for varied dummy data

        base_price = np.random.uniform(100, 300)
        price_changes = np.random.normal(0, 2, 100).cumsum()
        close_prices = base_price + price_changes + np.random.uniform(-5, 5, 100)
        open_prices = close_prices + np.random.uniform(-2, 2, 100)
        high_prices = np.maximum(open_prices, close_prices) + np.random.uniform(0, 3, 100)
        low_prices = np.minimum(open_prices, close_prices) - np.random.uniform(0, 3, 100)
        volume = np.random.randint(100000, 500000, 100)

        df = pd.DataFrame({
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': close_prices,
            'Volume': volume
        }, index=dates)
        df = df.apply(lambda x: x.clip(lower=0.1)) # Ensure prices are positive
        return df

    def calculate_indicators(self) -> pd.DataFrame:
        """
        Uses TA-Lib to compute common technical indicators (SMA, RSI, MACD).
        Returns a new DataFrame with the calculated indicators.
        Handles cases where there isn't enough data for certain indicators.
        """
        df = self.data.copy()
        close = df['Close']

        # Check if the DataFrame is empty or has insufficient data
        if df.empty or len(close) < 50: # SMA_50 needs at least 50 periods
            print(f"Warning: Not enough data points ({len(close)}) for {self.ticker} to calculate all indicators.")
            # Initialize indicator columns with NaN if data is insufficient
            df['SMA_20'] = np.nan
            df['SMA_50'] = np.nan
            df['RSI'] = np.nan
            df['MACD'] = np.nan
            df['MACD_signal'] = np.nan
            return df

        df['SMA_20'] = talib.SMA(close, timeperiod=20)
        df['SMA_50'] = talib.SMA(close, timeperiod=50)
        df['RSI'] = talib.RSI(close, timeperiod=14)
        # MACD returns three series: MACD, MACD Signal, and MACD Histogram (not used here)
        df['MACD'], df['MACD_signal'], _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

        return df

    def plot(self, df: pd.DataFrame) -> None:
        """
        Visualizes stock price with candlestick chart, SMA indicators,
        and volume using Plotly.
        """
        if df.empty:
            print(f"Cannot plot for {self.ticker}: DataFrame is empty or failed to load data.")
            return

        # Create subplots: 1 for candlestick/SMA, 1 for volume
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3], # Allocate more space to price chart
                            vertical_spacing=0.05) # Small space between subplots

        # Add Candlestick chart to the first row
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name='Candlestick'), row=1, col=1)

        # Add SMA 20 to the first row, if available and not all NaNs
        if 'SMA_20' in df.columns and not df['SMA_20'].isnull().all():
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20',
                                     line=dict(color='blue', width=1.5)), row=1, col=1)
        # Add SMA 50 to the first row, if available and not all NaNs
        if 'SMA_50' in df.columns and not df['SMA_50'].isnull().all():
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50',
                                     line=dict(color='red', width=1.5)), row=1, col=1)

        # Add Volume bar chart to the second row
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                             marker_color='gray', opacity=0.6), row=2, col=1)

        # Update layout for a cleaner look
        fig.update_layout(
            title=f'{self.ticker} Stock Analysis with Indicators',
            template='plotly_white', # Use a clean white background
            xaxis_rangeslider_visible=False, # Hide the range slider at the bottom
            height=700, # Set a fixed height for the plot
            hovermode='x unified' # Show unified hover information
        )

        # Update y-axis titles
        fig.update_yaxes(title_text='Price', row=1, col=1)
        fig.update_yaxes(title_text='Volume', row=2, col=1)

        fig.show()

    def show_financial_metrics(self):
        """
        Displays key financial metrics using the mocked Stock object.
        In a real application, this would fetch live data from pynance or similar.
        """
        try:
            print(f"\n--- Financial Metrics for {self.ticker} ---")
            print(f"Company Name: {self.stock.name}")
            print(f"P/E Ratio: {self.stock.pe}")
            print(f"EPS: {self.stock.eps}")
            print(f"Market Cap: {self.stock.market_cap}")
        except Exception as e:
            print(f"Error fetching financial metrics: {e}")
            print("Note: Financial metrics are mocked as pynance live data fetching is not available in this environment.")