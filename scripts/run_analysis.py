import sys
import os

# Get the directory of the current script (run_analysis.py)
script_dir = os.path.dirname(__file__)

# Construct the path to the project root (one level up from 'scripts')
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add the 'src' directory to Python's module search path
sys.path.insert(0, os.path.join(project_root, 'src'))

# Now you can import directly from 'data_analysis' since 'src' is in sys.path
from data_analysis import NewsAnalyzer

if __name__ == "__main__":
    # Define the data filepath relative to the project root
    data_filepath = os.path.join(project_root, 'Data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')

    analyzer = NewsAnalyzer(data_filepath)

    print("--- Loading Data ---")
    analyzer.load_data()

    if analyzer.df is not None:
        print("\n--- Descriptive Statistics for Headline Lengths ---")
        analyzer.textual_lengths()
        analyzer.descriptive_statistics()
        analyzer.headline_length_visualization()

        print("\n--- Articles per Publisher Analysis ---")
        analyzer.articles_per_publisher()
        analyzer.top_publishers()
        analyzer.publisher_visualization()

        print("\n--- Date-Based Analyses ---")
        analyzer.prepare_dates()
        analyzer.articles_by_day_of_week()
        analyzer.articles_over_time(resampling_freq='D')
        analyzer.articles_by_month()
        analyzer.articles_by_hour()
    else:
        print("\nData could not be loaded. Exiting analysis.")