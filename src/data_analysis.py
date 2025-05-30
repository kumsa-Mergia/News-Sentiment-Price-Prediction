import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class NewsAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.publisher_counts = None

    def load_data(self):
        """
        Loads the CSV file into a pandas DataFrame.
        Handles FileNotFoundError and other potential exceptions during loading.
        """
        try:
            self.df = pd.read_csv(self.filepath)
            print("CSV file loaded successfully.")
        except FileNotFoundError:
            print(f"Error: The file '{self.filepath}' was not found.")
        except Exception as e:
            print(f"An error occurred while loading the CSV file: {e}")

    def textual_lengths(self, df_to_analyze=None): # MODIFIED
        """
        Calculates the length of headlines (number of words) and stores it in a new column.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None:
            print("Error: DataFrame not loaded. Please run load_data() first or provide a DataFrame.")
            return target_df # Return the potentially modified DataFrame

        try:
            # Ensure 'headline' column exists and is string type
            if 'headline' not in target_df.columns:
                print("Error: 'headline' column not found in the DataFrame.")
                return target_df

            target_df['headline_length'] = target_df['headline'].apply(lambda x: len(str(x).split()))
            print("Headline lengths calculated successfully.")
        except Exception as e:
            print(f"An error occurred while calculating textual lengths: {e}")
        return target_df # Return the modified DataFrame

    def descriptive_statistics(self, df_to_analyze=None): # MODIFIED
        """
        Prints descriptive statistics for the 'headline_length' column.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None or 'headline_length' not in target_df.columns:
            print("Error: 'headline_length' data not available. Please run textual_lengths() first.")
            return
        try:
            print("\nDescriptive Statistics for Headline Lengths:")
            print(target_df['headline_length'].describe())
        except Exception as e:
            print(f"An error occurred while generating descriptive statistics: {e}")

    def headline_length_visualization(self, df_to_analyze=None): # MODIFIED
        """
        Generates and displays a histogram of headline lengths.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None or 'headline_length' not in target_df.columns:
            print("Error: 'headline_length' data not available. Please run textual_lengths() first.")
            return
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(target_df['headline_length'], bins=30, kde=True)
            plt.title("Distribution of Headline Lengths")
            plt.xlabel("Number of Words")
            plt.ylabel("Frequency")
            plt.grid(axis='y', alpha=0.75)
            plt.show()
            print("Headline length visualization displayed.")
        except Exception as e:
            print(f"An error occurred during headline length visualization: {e}")

    def articles_per_publisher(self, df_to_analyze=None): # MODIFIED
        """
        Calculates the number of articles per publisher.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None:
            print("Error: DataFrame not loaded. Please run load_data() first or provide a DataFrame.")
            return
        try:
            if 'publisher' not in target_df.columns:
                print("Error: 'publisher' column not found in the DataFrame.")
                return
            self.publisher_counts = target_df['publisher'].value_counts() # Still stores in self.publisher_counts
            print("Articles per publisher calculated successfully.")
        except Exception as e:
            print(f"An error occurred while calculating articles per publisher: {e}")

    # top_publishers and publisher_visualization will still use self.publisher_counts,
    # so ensure articles_per_publisher is run on the correct filtered data first.

    def top_publishers(self):
        """
        Prints the top 10 publishers by the number of articles.
        """
        if self.publisher_counts is None:
            print("Error: Publisher counts not available. Please run articles_per_publisher() first.")
            return
        try:
            print("\nTop 10 Publishers:")
            print(self.publisher_counts.head(10))
        except Exception as e:
            print(f"An error occurred while retrieving top publishers: {e}")

    def publisher_visualization(self):
        """
        Generates and displays a bar plot of the top 10 publishers.
        """
        if self.publisher_counts is None:
            print("Error: Publisher counts not available. Please run articles_per_publisher() first.")
            return
        try:
            plt.figure(figsize=(12, 7))
            self.publisher_counts.head(10).plot(kind='bar')
            plt.title("Top 10 Publishers by Number of Articles")
            plt.xlabel("Publisher")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
            print("Publisher visualization displayed.")
        except Exception as e:
            print(f"An error occurred during publisher visualization: {e}")

    def prepare_dates(self, df_to_analyze=None, date_column='date'): # MODIFIED
        """
        Converts the specified date column to datetime objects and extracts time components.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None:
            print("Error: DataFrame not loaded. Please run load_data() first or provide a DataFrame.")
            return target_df # Return the potentially modified DataFrame
        if date_column not in target_df.columns:
            print(f"Error: '{date_column}' column not found in the DataFrame.")
            return target_df

        try:
            target_df[date_column] = pd.to_datetime(target_df[date_column], errors='coerce')
            # Drop rows where date conversion failed
            target_df.dropna(subset=[date_column], inplace=True)

            target_df['year'] = target_df[date_column].dt.year
            target_df['month'] = target_df[date_column].dt.month
            target_df['day_of_week'] = target_df[date_column].dt.day_name()
            target_df['date_only'] = target_df[date_column].dt.date # For daily trends
            target_df['hour'] = target_df[date_column].dt.hour

            print(f"Date column '{date_column}' processed successfully.")
        except Exception as e:
            print(f"An error occurred while preparing dates: {e}")
        return target_df # Return the modified DataFrame

    def articles_by_day_of_week(self, df_to_analyze=None, date_column='date'): # MODIFIED
        """
        Analyzes and visualizes the number of articles published on each day of the week.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None or 'day_of_week' not in target_df.columns:
            print("Error: Date data not prepared. Please run prepare_dates() first or provide a DataFrame.")
            return
        try:
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            articles_dow = target_df['day_of_week'].value_counts().reindex(day_order)

            plt.figure(figsize=(10, 6))
            sns.barplot(x=articles_dow.index, y=articles_dow.values, hue=articles_dow.index, palette='viridis', legend=False)
            plt.title("Number of Articles by Day of the Week")
            plt.xlabel("Day of the Week")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
            print("Articles by day of week visualization displayed.")
        except Exception as e:
            print(f"An error occurred during day of week analysis: {e}")

    def articles_over_time(self, df_to_analyze=None, resampling_freq='D', date_column='date'): # MODIFIED
        """
        Analyzes and visualizes the number of articles published over time.
        'resampling_freq' can be 'D' for daily, 'W' for weekly, 'M' for monthly.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None or date_column not in target_df.columns:
            print(f"Error: Date column '{date_column}' not available or data not prepared. Please run prepare_dates() first or provide a DataFrame.")
            return

        try:
            df_time = target_df.set_index(date_column)
            articles_over_time = df_time.resample(resampling_freq).size()

            plt.figure(figsize=(14, 7))
            articles_over_time.plot(kind='line')
            plt.title(f"Number of Articles Over Time ({resampling_freq} Frequency)")
            plt.xlabel("Date")
            plt.ylabel("Number of Articles")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            print(f"Articles over time ({resampling_freq} frequency) visualization displayed.")
        except Exception as e:
            print(f"An error occurred during articles over time analysis: {e}")

    def articles_by_month(self, df_to_analyze=None, date_column='date'): # MODIFIED
        """
        Analyzes and visualizes the number of articles published per month.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None or 'month' not in target_df.columns:
            print("Error: Date data not prepared. Please run prepare_dates() first or provide a DataFrame.")
            return
        try:
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']
            target_df['month_name'] = target_df[date_column].dt.month_name()
            articles_by_month = target_df['month_name'].value_counts().reindex(month_order)

            plt.figure(figsize=(12, 6))
            sns.barplot(x=articles_by_month.index, y=articles_by_month.values, hue=articles_by_month.index, palette='cubehelix', legend=False)
            plt.title("Number of Articles by Month")
            plt.xlabel("Month")
            plt.ylabel("Number of Articles")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
            print("Articles by month visualization displayed.")
        except Exception as e:
            print(f"An error occurred during articles by month analysis: {e}")

    def articles_by_hour(self, df_to_analyze=None): # MODIFIED
        """
        Analyzes and visualizes the number of articles published per hour of the day.
        Operates on df_to_analyze if provided, otherwise on self.df.
        """
        target_df = df_to_analyze if df_to_analyze is not None else self.df # Use the provided or self.df

        if target_df is None or 'hour' not in target_df.columns:
            print("Error: 'hour' data not available. Please run prepare_dates() first and ensure your date column has time information.")
            return

        try:
            articles_hourly = target_df['hour'].value_counts().sort_index()

            plt.figure(figsize=(12, 6))
            sns.barplot(x=articles_hourly.index, y=articles_hourly.values, hue=articles_hourly.index, palette='viridis', legend=False)
            plt.title("Number of Articles by Hour of Day")
            plt.xlabel("Hour of Day (24-hour format)")
            plt.ylabel("Number of Articles")
            plt.xticks(range(0, 24)) # Ensure all 24 hours are shown
            plt.grid(axis='y', alpha=0.75)
            plt.tight_layout()
            plt.show()
            print("Articles by hour visualization displayed.")
        except Exception as e:
            print(f"An error occurred during articles by hour analysis: {e}")