import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,"input","dfsAcUtil.csv")
save_at = os.path.join(script_dir, "output", "detailUtilReport.csv")
save_at2 = os.path.join(script_dir, "output", "utilReportPerDay.csv")

df = pd.read_csv(file_path,sep=";")

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

df2 = df.groupby(["DATE"]).agg(
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
    df2[new_col] = hours.astype(str) + ":" + minutes.astype(str).str.zfill(2)

df.to_csv(save_at,sep=";",index=False)
df2.to_csv(save_at2,sep=";",index=False)