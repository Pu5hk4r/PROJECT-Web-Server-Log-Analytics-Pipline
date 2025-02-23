import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Regular expression to parse the log file
LOG_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(\d{2}/\w{3}/\d{4}):(\d{2})')

# Read and process the log file
def parse_log_file(log_file, target_date):
    ip_counter = Counter()
    hour_counter = Counter()

    with open('log.txt', 'r') as file:
        for line in file:
            match = LOG_PATTERN.search(line)
            if match:
                ip, date, hour = match.groups()
                if date == target_date:  # Filter for the given date
                    ip_counter[ip] += 1
                    hour_counter[hour] += 1

    return ip_counter, hour_counter

# Function to find contributors to X% of traffic
def get_top_contributors(counter, percentage):
    df = pd.DataFrame(sorted(counter.items(), key=lambda x: x[1], reverse=True), columns=['Key', 'Requests'])
    df['Cumulative'] = df['Requests'].cumsum() / df['Requests'].sum()  # Cumulative percentage
    top_df = df[df['Cumulative'] <= percentage]
    return top_df

# Function to plot bar charts
def plot_bar_chart(df, title, xlabel, ylabel):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df['Requests'], y=df['Key'], palette="plasma")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# Main function
def main():
    log_file = 'server.log'  # Change this to your log file path
    target_date = '17/May/2015'  # Change this to analyze a specific day

    ip_counter, hour_counter = parse_log_file(log_file, target_date)

    # Get top IPs contributing to 85% of traffic
    top_ips = get_top_contributors(ip_counter, 0.85)

    # Get top hours contributing to 70% of traffic
    top_hours = get_top_contributors(hour_counter, 0.70)

    # Print results
    print(f"\nTop IP addresses contributing to 85% of traffic on {target_date}")
    print("IP Address        | Requests")
    print("-----------------------------")
    for _, row in top_ips.iterrows():
        print(f"{row['Key']:16} | {row['Requests']}")

    print(f"\nTop hours contributing to 70% of traffic on {target_date}")
    print("Hour  | Requests")
    print("------------------")
    for _, row in top_hours.iterrows():
        print(f" {row['Key']:02}   | {row['Requests']}")

    # Plot bar charts
    plot_bar_chart(top_ips, f'Top IPs (85% Traffic) on {target_date}', 'Requests', 'IP Address')
    plot_bar_chart(top_hours, f'Top Hours (70% Traffic) on {target_date}', 'Requests', 'Hour')

if __name__ == "__main__":
    main()
