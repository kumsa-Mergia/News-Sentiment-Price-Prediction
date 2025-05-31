import sys
import os


# Get the directory of the current script (run_analysis.py)
script_dir = os.path.dirname(__file__)

# Construct the path to the project root (one level up from 'scripts')
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add the 'src' directory to Python's module search path
sys.path.insert(0, os.path.join(project_root, 'src'))
# Import the StockAnalyzer class from our custom module
from stock_analyzer import StockAnalyzer

# Dictionary mapping company names to their corresponding CSV file names
stock_files = {
    "APPLE": "AAPL_historical_data.csv",
    "AMAZON": "AMZN_historical_data.csv",
    "GOOGLE": "GOOG_historical_data.csv",
    "META": "META_historical_data.csv",
    "MICROSOFT": "MSFT_historical_data.csv",
    "NVIDIA": "NVDA_historical_data.csv",
    "TESLA": "TSLA_historical_data.csv"
}

# Base directory where yfinance_data folder is located
base_data_dir = "../../Data/yfinance_data/"

def main():
    print("Setup complete. StockAnalyzer class imported.")

    # Loop through each company and its CSV file
    for ticker, filename in stock_files.items():
        print(f"\n==============    {ticker} STOCK ANALYSIS    ==============")
        # Construct the full file path
        full_data_path = os.path.join(base_data_dir, filename)
        
        # Initialize StockAnalyzer with the ticker and the full file path
        analyzer = StockAnalyzer(ticker, full_data_path)
        
        # # Display financial metrics
        analyzer.show_financial_metrics()

    print("\nAll stock analyses complete.")

if __name__ == "__main__":
    main()