import pandas as pd
df = pd.read_csv("data/daily_report.csv")

# 총 확진자, 사망자, 완치자
totals_df = df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(
    name="count").rename(columns={'index': 'condition'})


# 나라별 총 확진자, 사망자, 완치자
countries_df = df[["Country_Region", "Confirmed", "Deaths", "Recovered"]].groupby(
    "Country_Region").sum().sort_values(by="Confirmed", ascending=False).reset_index()
