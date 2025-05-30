import sys
import os

# Get the directory of the current script (run_analysis.py)
script_dir = os.path.dirname(__file__)

# Construct the path to the project root (one level up from 'scripts')
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add the 'src' directory to Python's module search path
sys.path.insert(0, os.path.join(project_root, 'src'))

from news_topic_modeler import AnalystHeadlineTopicModeler

modeler = AnalystHeadlineTopicModeler(
    filepath="Data/raw_analyst_ratings/raw_analyst_ratings.csv",
    target_stocks=['MSF', 'AAPL', 'AMZN', 'GOOG', 'GOOGL', 'FB', 'NVDA'],
    n_topics=5)

modeler.run()
