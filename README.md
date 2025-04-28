# 📊 PROJECT - Web Server Log Analytics Pipeline

---

An interactive **Streamlit** dashboard to analyze web server log files by date, identify **top contributing IPs** and **peak traffic hours**, and visualize results using **Plotly** charts.

---

## ✨ Screenshots

![Dashboard1](https://github.com/Pu5hk4r/PROJECT-Web-Server-Log-Analytics-Pipline/blob/main/Dashboard1.png)

![Dashboard2](https://github.com/Pu5hk4r/PROJECT-Web-Server-Log-Analytics-Pipline/blob/main/Dashboard2.png)

![Histogram](https://github.com/Pu5hk4r/PROJECT-Web-Server-Log-Analytics-Pipline/blob/main/hist.png)

![Additional Pic](https://github.com/Pu5hk4r/PROJECT-Web-Server-Log-Analytics-Pipline/blob/main/pic.png)

---

## 🚀 Features

- 📂 Upload a server log file (`.txt` or `.log`).
- 📅 Parse logs based on a target date (format: `DD/Mon/YYYY`).
- 🧠 Identify IP addresses generating **85% of the traffic**.
- ⏰ Identify peak hours contributing to **70% of the traffic**.
- 📊 Interactive horizontal bar charts for easy visualization.
- 🗂️ View raw data tables for detailed inspection.

---

## 🛠️ Tech Stack

| Technology             | Usage                                  |
|:------------------------|:--------------------------------------|
| **Python**              | Core programming language             |
| **Streamlit**           | Building interactive web dashboard    |
| **Pandas**              | Data manipulation and analysis        |
| **Plotly**              | Interactive visualizations (bar charts) |
| **re (Regex)**          | Parsing log file entries               |
| **collections.Counter** | Efficient counting of IPs and hours   |

---

## 📈 How It Works

1. **Upload** a server log file (Apache or Nginx style logs).
2. **Enter** a specific date (example: `17/May/2015`).
3. The app will:
   - Parse each line using regular expressions.
   - Filter logs for the selected date.
   - Count the number of requests per IP address and per hour.
4. **Visualize**:
   - Top IPs responsible for 85% of the requests.
   - Peak traffic hours contributing to 70% of the traffic.
5. **Explore** raw tabular data below the charts.

---

## 📋 Sample Log Format Expected

Example log line:
92.168.1.1 - - [17/May/2015:10:05:00] "GET /index.html HTTP/1.1" 200 2326
Regex Pattern Used:
(\d+.\d+.\d+.\d+) - - [(\d{2}/\w{3}/\d{4}):(\d{2})

---


Extracts:

- **IP Address**
- **Date**
- **Hour**

---

## 📄 License

This project is licensed under the **MYOWNWORK**.  
Feel free to use and customize it!

---

## 📌 Future Enhancements

- Employing distributed Computing **HDFS**,**PYSPARK**
- For Advance visulaization **Tableau** , **PowderBI**
- Allow uploading multiple log files at once.
- Use date picker widgets instead of manual text input.
- Add download/export option for analyzed data.
- Improve error handling for incorrect file formats.
- Add trend lines and time series graphs.

---







