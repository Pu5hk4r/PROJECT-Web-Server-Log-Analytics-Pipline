import streamlit as st
import pandas as pd
import re
from collections import Counter
import plotly.express as px

# Regular expression to parse the log file
LOG_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(\d{2}/\w{3}/\d{4}):(\d{2})')


def parse_log_file(uploaded_file, target_date):
    ip_counter = Counter()
    hour_counter = Counter()

    for line in uploaded_file.getvalue().decode("utf-8").splitlines():
        match = LOG_PATTERN.search(line)
        if match:
            ip, date, hour = match.groups()
            if date == target_date:
                ip_counter[ip] += 1
                hour_counter[hour] += 1

    return ip_counter, hour_counter


def get_top_contributors(counter, percentage):
    df = pd.DataFrame(sorted(counter.items(), key=lambda x: x[1], reverse=True), columns=['Key', 'Requests'])
    df['Cumulative'] = df['Requests'].cumsum() / df['Requests'].sum()
    return df[df['Cumulative'] <= percentage]


# Streamlit Dashboard
st.title("📊 Web Server Log Analysis Dashboard")

log_file = st.file_uploader("Upload Server Log File", type=["txt", "log"])
target_date = st.text_input("Enter Date (e.g., 17/May/2015)", "17/May/2015")

if log_file and target_date:
    ip_counter, hour_counter = parse_log_file(log_file, target_date)

    if ip_counter and hour_counter:
        top_ips = get_top_contributors(ip_counter, 0.85)
        top_hours = get_top_contributors(hour_counter, 0.70)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Top IPs (85% Traffic) on {target_date}")
            fig1 = px.bar(top_ips, x='Requests', y='Key', orientation='h',
                          title="Top IP Addresses", labels={'Key': 'IP Address'})
            st.plotly_chart(fig1)

        with col2:
            st.subheader(f"Top Hours (70% Traffic) on {target_date}")
            fig2 = px.bar(top_hours, x='Requests', y='Key', orientation='h',
                          title="Top Traffic Hours", labels={'Key': 'Hour'})
            st.plotly_chart(fig2)

        st.subheader("Raw Data")
        st.write(top_ips)
        st.write(top_hours)
