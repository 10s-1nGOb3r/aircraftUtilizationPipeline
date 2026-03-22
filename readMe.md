✈️ Aircraft Utilization Reporting Pipeline
📌 Overview

This project is a data processing pipeline built using Python (Pandas & NumPy) to calculate aircraft utilization metrics from daily flight schedule data.

It transforms raw operational flight data into structured reports across multiple levels:

Daily
Monthly
Yearly
Per Aircraft Type
Per Aircraft Registration

The output is exported into multiple .csv files for reporting and analysis.

📂 Project Structure

project/
│
├── input/
│   └── dfsAcUtil.csv
│
├── output/
│   ├── detailUtilReport.csv
│   ├── utilReportPerDay.csv
│   ├── utilReportPerDayPerAircraft.csv
│   ├── utilReportPerMonth.csv
│   ├── utilReportPerMonthPerAircraft.csv
│   ├── utilReportPerYear.csv
│   ├── utilReportPerYearPerAircraft.csv
│   ├── utilReportPerDayPerRegistration.csv
│   ├── utilReportPerMonthPerRegistration.csv
│   └── utilReportPerYearPerRegistration.csv
│
├── acUtilPipeline.py
│
└── runAcUtilPipeline.bat

📥 Input Data Requirements

The input file must follow the structure from:

AIMS 1.2.1 – Daily Flight Schedule

Required Columns:
DATE → Format: DD/MM/YYYY
FLT → Flight Number
TYPE → Aircraft Type
REG → Aircraft Registration
AC → Aircraft Type Code
DEP → Departure Airport
ARR → Arrival Airport
STD → Scheduled Time Departure
STA → Scheduled Time Arrival
ATD → Actual Time Departure
ATA → Actual Time Arrival
BLOCK → Block Time (HH:MM)

⚙️ Key Features
1. Data Preprocessing
Converts DATE into datetime format
Extracts:
Month Name
Month Number
Year
Converts BLOCK into:
Timedelta
Decimal hours (blockDec)
Handles missing values safely

2. Core Calculations
✈️ Block Hours
blockDec = total seconds / 3600
📊 Aircraft Count
Based on change in REG (registration)
Used to estimate active aircraft per period
📅 Day Count
Identifies unique operational days
⚡ Utilization Formula
Utilization = (Total Block Hours / Total Aircraft Online) / Total Days

📊 Generated Reports
1. Detailed Report
detailUtilReport.csv
Raw enriched dataset
2. Daily Reports
utilReportPerDay.csv
utilReportPerDayPerAircraft.csv
utilReportPerDayPerRegistration.csv
3. Monthly Reports
utilReportPerMonth.csv
utilReportPerMonthPerAircraft.csv
utilReportPerMonthPerRegistration.csv
4. Yearly Reports
utilReportPerYear.csv
utilReportPerYearPerAircraft.csv
utilReportPerYearPerRegistration.csv

⏱️ Time Format Conversion
All utilization and block hours are provided in:
Decimal format → HHh MMm
Example:
5.75 → 5h 45m

🚀 How to Run
1. Install Dependencies
pip install pandas numpy
2. Place Input File
Put your dataset in:
/input/dfsAcUtil.csv
3. Run Script
acUtilPipeline.py
4. Output
All reports will be generated automatically in:
/output/

📈 Use Cases
Fleet utilization monitoring
Airline operational performance tracking
Aircraft productivity analysis
Input for forecasting models (e.g., block hours prediction)
⚠️ Notes & Assumptions
Only scheduled flights should be included unless adjusted
BLOCK must be in HH:MM format
Aircraft count is derived from registration change logic
Missing or invalid block times are treated as 0
🧠 Future Improvements
Add visualization (Matplotlib / Power BI integration)
Support real-time data ingestion
Integrate with ML models (e.g., XGBoost for forecasting)
Add anomaly detection for utilization spikes
