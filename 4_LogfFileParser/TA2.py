import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Regular expression to parse the log file
LOG_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(\d{2}/\w{3}/\d{4}):(\d{2})')

# Read and process the log file
def parse_log_file(log_file, target_date):
    hourly_counter = Counter()

    with open('log.txt', 'r') as file:
        for line in file:
            match = LOG_PATTERN.search(line)
            if match:
                ip, date, hour = match.groups()
                if date == target_date:  # Filter for the given date
                    hourly_counter[hour] += 1

    return hourly_counter

# Convert Counter to DataFrame
def counter_to_dataframe(counter):
    df = pd.DataFrame(sorted(counter.items()), columns=['Hour', 'Visitors'])
    df['Hour'] = df['Hour'].astype(int)  # Convert hour to integer for sorting
    return df.sort_values(by='Hour')

# Generate histogram
def plot_histogram(df, target_date):
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
    log_file = 'server.log'  # Change this to your log file path
    target_date = '30/Jan/2024'  # Change this to analyze a specific day

    hourly_counter = parse_log_file(log_file, target_date)
    df = counter_to_dataframe(hourly_counter)

    # Print the hourly traffic table
    print("\nHourly Traffic on", target_date)
    print("Hour  | Visitors")
    print("--------------------")
    for _, row in df.iterrows():
        print(f" {row['Hour']:02}   | {row['Visitors']}")

    # Plot the histogram
    plot_histogram(df, target_date)

if __name__ == "__main__":
    main()
