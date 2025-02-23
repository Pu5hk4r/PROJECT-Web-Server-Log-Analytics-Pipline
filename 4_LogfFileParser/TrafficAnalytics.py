import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Regular expressions to parse the log file
LOG_PATTERN_DAILY = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(\d{2}/\w{3}/\d{4})')
LOG_PATTERN_HOURLY = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(\d{2}/\w{3}/\d{4}):(\d{2})')


# Read and process the log file for daily analysis
def parse_log_file_daily(log_file):
    daily_counter = Counter()

    with open(log_file, 'r') as file:
        for line in file:
            match = LOG_PATTERN_DAILY.search(line)
            if match:
                ip, date = match.groups()
                daily_counter[(date, ip)] += 1

    return daily_counter


# Read and process the log file for hourly analysis
def parse_log_file_hourly(log_file, target_date):
    hourly_counter = Counter()

    with open(log_file, 'r') as file:
        for line in file:
            match = LOG_PATTERN_HOURLY.search(line)
            if match:
                ip, date, hour = match.groups()
                if date == target_date:
                    hourly_counter[hour] += 1

    return hourly_counter


# Convert Counter to DataFrame
def counter_to_dataframe(counter, columns):
    df = pd.DataFrame([{columns[0]: k[0], columns[1]: k[1], 'Occurrences': v} for k, v in counter.items()])
    return df


# Convert hourly Counter to DataFrame
def counter_to_dataframe_hourly(counter):
    df = pd.DataFrame(sorted(counter.items()), columns=['Hour', 'Visitors'])
    df['Hour'] = df['Hour'].astype(int)  # Convert hour to integer for sorting
    return df.sort_values(by='Hour')


# Plot histograms
def plot_histograms(df):
    plt.figure(figsize=(14, 5))

    # Unique IPs per day
    plt.subplot(1, 2, 1)
    ip_per_day = df.groupby('Date')['IP'].nunique()
    sns.barplot(x=ip_per_day.index, y=ip_per_day.values, palette="viridis")
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Unique IPs')
    plt.title('Unique IPs per Day')

    # Requests per IP
    plt.subplot(1, 2, 2)
    ip_counts = df.groupby('IP')['Occurrences'].sum()
    sns.histplot(ip_counts, bins=10, kde=True, color="skyblue")
    plt.xlabel('Requests per IP')
    plt.ylabel('Frequency')
    plt.title('Distribution of Requests per IP')

    plt.tight_layout()
    plt.show()


# Plot hourly histogram
def plot_histogram_hourly(df, target_date):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df['Hour'], y=df['Visitors'], palette="magma")
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Visitors')
    plt.title(f'Hourly Traffic on {target_date}')
    plt.xticks(range(0, 24))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


# Main function
def main():
    log_file = 'log.txt'  # Change this to your log file path
    target_date = '30/Jan/2024'  # Change this to analyze a specific day

    # Daily analysis
    daily_counter = parse_log_file_daily(log_file)
    daily_df = counter_to_dataframe(daily_counter, ['Date', 'IP'])
    print(daily_df.pivot(index='IP', columns='Date', values='Occurrences').fillna(0))
    plot_histograms(daily_df)

    # Hourly analysis
    hourly_counter = parse_log_file_hourly(log_file, target_date)
    hourly_df = counter_to_dataframe_hourly(hourly_counter)

    print(f"\nHourly Traffic on {target_date}")
    print("Hour  | Visitors")
    print("--------------------")
    for _, row in hourly_df.iterrows():
        print(f" {row['Hour']:02}   | {row['Visitors']}")

    plot_histogram_hourly(hourly_df, target_date)


if __name__ == "__main__":
    main()
