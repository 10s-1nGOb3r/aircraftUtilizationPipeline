import pandas as pd
import numpy as np
import os

#First step as usual, make file directory using os library
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,"input","dfsAcUtil.csv")
save_at = os.path.join(script_dir, "output", "detailUtilReport.csv")
save_at2 = os.path.join(script_dir, "output", "utilReportPerDay.csv")
save_at3 = os.path.join(script_dir, "output", "utilReportPerDayPerAircraft.csv")
save_at4 = os.path.join(script_dir, "output", "utilReportPerMonth.csv")
save_at5 = os.path.join(script_dir, "output", "utilReportPerMonthPerAircraft.csv")
save_at6 = os.path.join(script_dir, "output", "utilReportPerYear.csv")
save_at7 = os.path.join(script_dir, "output", "utilReportPerYearPerAircraft.csv")
save_at8 = os.path.join(script_dir, "output", "utilReportPerDayPerRegistration.csv")
save_at9 = os.path.join(script_dir, "output", "utilReportPerMonthPerRegistration.csv")
save_at10 = os.path.join(script_dir, "output", "utilReportPerYearPerRegistration.csv")

#Read the files on input files
#The required field on AIMS 1.2.1. Daily Flight Schedule such as
#DATE,FLT,TYPE,REG,AC,DEP,ARR
#STD,STA,ATD,ATA,BLOCK
df = pd.read_csv(file_path,sep=";")

#Data formatting on some fields such as
#DATE,FLT,REG,AC,DEP,ARR,BLOCK
#Also some calculated fields are being made such as
#monthName,monthNumber,year,dayCount,blockDec,acCount
df["DATE"] = pd.to_datetime(df["DATE"],format="%d/%m/%Y")
df["monthName"] = df["DATE"].dt.month_name()
df["monthNumber"] = df["DATE"].dt.month
df["year"] = df["DATE"].dt.year
df["dayCount"] = np.where(df["DATE"] != df["DATE"].shift(1),1,0)
df["dayCount"] = df["dayCount"].astype(int)

collection = ["FLT","REG","AC","DEP","ARR","monthName"]
for loop1 in collection:
    df[loop1] = df[loop1].astype(str)

df["BLOCK"] = pd.to_timedelta(df["BLOCK"].astype(str) + ":00",errors="coerce")
df["blockDec"] = df["BLOCK"].dt.total_seconds() / 3600
df["blockDec"] = df["blockDec"].round(2)
df["blockDec"] = df["blockDec"].fillna(0)

df["acCount"] = np.where(df["REG"] != df["REG"].shift(1),1,0)
df["acCount"] = df["acCount"].astype(int)

#Aggregations are being made based on several requirements such as
#Utilization Per Day, Per Month, Per Year
#Utilization Per Aircraft Type Per Day, Per Month, Per Year
#Utilization Per Aircraft Registration Per Day, Per Month, Per Year
df2 = df.groupby(["year","monthNumber","monthName","DATE"]).agg(
    totalBlockDec = ("blockDec","sum"),
    totalAcOnline = ("acCount","sum"),
    totalDay = ("dayCount","sum")
).reset_index()
df2["totalBlockDec"] = df2["totalBlockDec"].astype(float)
df2["totalBlockDec"] = df2["totalBlockDec"].round(2)
df2["utilDec"] = (df2["totalBlockDec"] / df2["totalAcOnline"]) / df2["totalDay"]
df2["utilDec"] = df2["utilDec"].astype(float)
df2["utilDec"] = df2["utilDec"].round(2)
collection2 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection2.items():
    total_minutes = (df2[source_col] * 60).round()
    hours = (total_minutes // 60).astype(int)
    minutes = (total_minutes % 60).astype(int)
    df2[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df3 = df.groupby(["year","monthNumber","monthName","DATE","AC"]).agg(
    totalBlockDec = ("blockDec","sum"),
    totalAcOnline = ("acCount","sum")
).reset_index()
df3["totalBlockDec"] = df3["totalBlockDec"].astype(float)
df3["totalBlockDec"] = df3["totalBlockDec"].round(2)
df3["totalDay"] = np.where(df3["totalBlockDec"] > 0,1,0)
df3["totalDay"] = df3["totalDay"].astype(int)
df3["utilDec"] = (df3["totalBlockDec"] / df3["totalAcOnline"]) / df3["totalDay"]
df3["utilDec"] = df3["utilDec"].astype(float)
df3["utilDec"] = df3["utilDec"].round(2)
collection3 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection3.items():
    total_minutes = (df3[source_col] * 60).round()
    hours = (total_minutes // 60).astype("Int64")
    minutes = (total_minutes % 60).astype("Int64")
    df3[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df4 = df2.groupby(["year","monthNumber","monthName"]).agg(
    totalBlockDec = ("totalBlockDec","sum"),
    totalAcOnline = ("totalAcOnline","mean"),
    totalDay = ("totalDay","sum")
).reset_index()
df4["totalAcOnline"] = df4["totalAcOnline"].astype(int)
df4["totalAcOnline"] = df4["totalAcOnline"].round(0)
df4["totalBlockDec"] = df4["totalBlockDec"].astype(float)
df4["totalBlockDec"] = df4["totalBlockDec"].round(2)
df4["utilDec"] = (df4["totalBlockDec"] / df4["totalAcOnline"]) / df4["totalDay"]
df4["utilDec"] = df4["utilDec"].astype(float)
df4["utilDec"] = df4["utilDec"].round(2)
collection4 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection4.items():
    total_minutes = (df4[source_col] * 60).round()
    hours = (total_minutes // 60).astype("Int64")
    minutes = (total_minutes % 60).astype("Int64")
    df4[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df5 = df3.groupby(["year","monthNumber","monthName","AC"]).agg(
    totalBlockDec = ("totalBlockDec","sum"),
    totalAcOnline = ("totalAcOnline","mean"),
    totalDay = ("totalDay","sum")
).reset_index()
df5["totalAcOnline"] = df5["totalAcOnline"].astype(int)
df5["totalAcOnline"] = df5["totalAcOnline"].round(0)
df5["totalBlockDec"] = df5["totalBlockDec"].astype(float)
df5["totalBlockDec"] = df5["totalBlockDec"].round(2)
df5["utilDec"] = (df5["totalBlockDec"] / df5["totalAcOnline"]) / df5["totalDay"]
df5["utilDec"] = df5["utilDec"].astype(float)
df5["utilDec"] = df5["utilDec"].round(2)
collection5 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection5.items():
    total_minutes = (df5[source_col] * 60).round()
    hours = (total_minutes // 60).astype("Int64")
    minutes = (total_minutes % 60).astype("Int64")
    df5[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df6 = df4.groupby(["year"]).agg(
    totalBlockDec = ("totalBlockDec","sum"),
    totalAcOnline = ("totalAcOnline","mean"),
    totalDay = ("totalDay","sum")
).reset_index()
df6["totalAcOnline"] = df6["totalAcOnline"].astype(int)
df6["totalAcOnline"] = df6["totalAcOnline"].round(0)
df6["totalBlockDec"] = df6["totalBlockDec"].astype(float)
df6["totalBlockDec"] = df6["totalBlockDec"].round(2)
df6["utilDec"] = (df6["totalBlockDec"] / df6["totalAcOnline"]) / df6["totalDay"]
df6["utilDec"] = df6["utilDec"].astype(float)
df6["utilDec"] = df6["utilDec"].round(2)
collection6 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection6.items():
    total_minutes = (df6[source_col] * 60).round()
    hours = (total_minutes // 60).astype("Int64")
    minutes = (total_minutes % 60).astype("Int64")
    df6[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df7 = df5.groupby(["year","AC"]).agg(
    totalBlockDec = ("totalBlockDec","sum"),
    totalAcOnline = ("totalAcOnline","mean"),
    totalDay = ("totalDay","sum")
).reset_index()
df7["totalAcOnline"] = df7["totalAcOnline"].astype(int)
df7["totalAcOnline"] = df7["totalAcOnline"].round(0)
df7["totalBlockDec"] = df7["totalBlockDec"].astype(float)
df7["totalBlockDec"] = df7["totalBlockDec"].round(2)
df7["utilDec"] = (df7["totalBlockDec"] / df7["totalAcOnline"]) / df7["totalDay"]
df7["utilDec"] = df7["utilDec"].astype(float)
df7["utilDec"] = df7["utilDec"].round(2)
collection7 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection7.items():
    total_minutes = (df7[source_col] * 60).round()
    hours = (total_minutes // 60).astype("Int64")
    minutes = (total_minutes % 60).astype("Int64")
    df7[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df8 = df.groupby(["year","monthNumber","monthName","DATE","AC","REG"]).agg(
    totalBlockDec = ("blockDec","sum"),
    totalAcOnline = ("acCount","sum")
).reset_index()
df8["totalBlockDec"] = df8["totalBlockDec"].astype(float)
df8["totalBlockDec"] = df8["totalBlockDec"].round(2)
df8["totalDay"] = np.where(df8["totalBlockDec"] > 0,1,0)
df8["utilDec"] = (df8["totalBlockDec"] / df8["totalAcOnline"]) / df8["totalDay"]
df8["utilDec"] = df8["utilDec"].astype(float)
df8["utilDec"] = df8["utilDec"].round(2)
collection8 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection8.items():
    total_minutes = (df8[source_col] * 60).round()
    hours = (total_minutes // 60).astype(int)
    minutes = (total_minutes % 60).astype(int)
    df8[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df9 = df8.groupby(["year","monthNumber","monthName","AC","REG"]).agg(
    totalBlockDec = ("totalBlockDec","sum"),
    totalAcOnline = ("totalAcOnline","sum")
).reset_index()
df9["totalBlockDec"] = df9["totalBlockDec"].astype(float)
df9["totalBlockDec"] = df9["totalBlockDec"].round(2)
df9["utilDec"] = df9["totalBlockDec"] / df9["totalAcOnline"]
df9["utilDec"] = df9["utilDec"].astype(float)
df9["utilDec"] = df9["utilDec"].round(2)
collection9 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection9.items():
    total_minutes = (df9[source_col] * 60).round()
    hours = (total_minutes // 60).astype(int)
    minutes = (total_minutes % 60).astype(int)
    df9[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"

df10 = df9.groupby(["year","AC","REG"]).agg(
    totalBlockDec = ("totalBlockDec","sum"),
    totalAcOnline = ("totalAcOnline","sum")
).reset_index()
df10["totalBlockDec"] = df10["totalBlockDec"].astype(float)
df10["totalBlockDec"] = df10["totalBlockDec"].round(2)
df10["utilDec"] = df10["totalBlockDec"] / df10["totalAcOnline"]
df10["utilDec"] = df10["utilDec"].astype(float)
df10["utilDec"] = df10["utilDec"].round(2)
collection10 = {
        "utilDec": "utilHR:MM",
        "totalBlockDec": "totalBlockHR:MM"
}
for source_col, new_col in collection10.items():
    total_minutes = (df10[source_col] * 60).round()
    hours = (total_minutes // 60).astype(int)
    minutes = (total_minutes % 60).astype(int)
    df10[new_col] = hours.astype(str) + "h " + minutes.astype(str).str.zfill(2) + "m"
df10 = df10.sort_values(by=["year","AC","utilDec"],ascending=[False,False,False])

#Exporting utilization report into csv files on output folder
df.to_csv(save_at,sep=";",index=False)
df2.to_csv(save_at2,sep=";",index=False)
df3.to_csv(save_at3,sep=";",index=False)
df4.to_csv(save_at4,sep=";",index=False)
df5.to_csv(save_at5,sep=";",index=False)
df6.to_csv(save_at6,sep=";",index=False)
df7.to_csv(save_at7,sep=";",index=False)
df8.to_csv(save_at8,sep=";",index=False)
df9.to_csv(save_at9,sep=";",index=False)
df10.to_csv(save_at10,sep=";",index=False)
