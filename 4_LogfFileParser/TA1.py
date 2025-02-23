import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Regular expression to parse the log file
LOG_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(\d{2}/\w{3}/\d{4})')


# Read and process the log file
def parse_log_file(log_file):
    ip_counter = Counter()

    with open('log.txt', 'r') as file:
        for line in file:
            match = LOG_PATTERN.search(line)
            if match:
                ip, date = match.groups()
                ip_counter[(date, ip)] += 1

    return ip_counter


# Convert Counter to DataFrame
def counter_to_dataframe(counter):
    data = [{'Date': date, 'IP': ip, 'Occurrences': count} for (date, ip), count in counter.items()]
    return pd.DataFrame(data)


# Generate histograms
def plot_histograms(df):
    plt.figure(figsize=(14, 5))

    # Histogram 1: Number of unique IPs per day
    plt.subplot(1, 2, 1)
    ip_per_day = df.groupby('Date')['IP'].nunique()
    sns.barplot(x=ip_per_day.index, y=ip_per_day.values, palette="viridis")
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Unique IPs')
    plt.title('Unique IPs per Day')

    # Histogram 2: Number of requests per IP
    plt.subplot(1, 2, 2)
    ip_counts = df.groupby('IP')['Occurrences'].sum()
    sns.histplot(ip_counts, bins=10, kde=True, color="skyblue")
    plt.xlabel('Requests per IP')
    plt.ylabel('Frequency')
    plt.title('Distribution of Requests per IP')

    plt.tight_layout()
    plt.show()


# Main function
def main():
    log_file = 'pythonProject/4_LogfFileParser/log.txt'
    ip_counter = parse_log_file(log_file)
    df = counter_to_dataframe(ip_counter)

    print(df.pivot(index='IP', columns='Date', values='Occurrences').fillna(0))

    plot_histograms(df)


if __name__ == "__main__":
    main()
