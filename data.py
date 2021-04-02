import pandas as pd
df = pd.read_csv("data/daily_report.csv")

# 총 확진자, 사망자, 완치자
totals_df = df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(
    name="count").rename(columns={'index': 'condition'})


# 나라별 총 확진자, 사망자, 완치자
countries_df = df[["Country_Region", "Confirmed", "Deaths", "Recovered"]].groupby(
    "Country_Region").sum().sort_values(by="Confirmed", ascending=False).reset_index()

# 드롭다운 옵션
dropdown_options = countries_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]


conditions = ["confirmed", "death", "recovered"]


def make_country_df(country):
    def make_df(condition):
        df = pd.read_csv(f"data/{condition}.csv")
        df = df.loc[df["Country/Region"] == "Korea, South"]
        df = df.drop(columns=["Province/State", "Country/Region",
                              "Lat", "Long"]).sum().reset_index(name=condition)
        df = df.rename(columns={"index": "date"})
        return df
    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


def make_global_df():
    def make_df(condition):
        df = pd.read_csv(f"data/{condition}.csv")
        df = df.drop(["Province/State", "Country/Region", "Lat",
                      "Long"], axis=1).sum().reset_index(name=condition)
        df = df.rename(columns={'index': 'date'})
        return df
    final_df = None

    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df
