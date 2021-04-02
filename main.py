from data import *
import plotly.express as px

# 바 그래프
bar_graph = px.bar(totals_df, x="condition", y="count",
                   template="plotly_dark",
                   title="Total Global Cases",
                   hover_data={"count": ":,"},
                   labels={
                       "condition": "Condition",
                       "count": "Count"
                   }
                   )
bar_graph.update_traces(marker_color=["#f8895a", "#ef5059", "#eed391"])

# 맵 그래프
map_graph = px.scatter_geo(countries_df,
                           size="Confirmed",
                           size_max=40,
                           title="Confirmed By Country",
                           color="Confirmed",
                           color_continuous_scale=px.colors.sequential.Oryel,
                           locations="Country_Region",
                           locationmode="country names",
                           template="plotly_dark",
                           hover_name="Country_Region",
                           hover_data={
                               "Confirmed": ":,",
                               "Deaths": ":,",
                               "Recovered": ":,",
                               "Country_Region": False
                           })
map_graph.update_layout(
    margin=dict(l=10, r=10, t=50, b=0)
)
