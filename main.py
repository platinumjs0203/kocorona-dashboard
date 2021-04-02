from data import *
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from builder import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Roboto&display=swap"
]

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

app = dash.Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "font-family": "Roboto, sans-serif"
    },
    children=[
        html.Header(
            style={"textAlign": "center",
                   "paddingTop": "15px", "paddingBottom": "15px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})]
        ),
        html.Div(
            style={"display": "grid",
                   "gap": 30,
                   "gridTemplateColumns": "repeat(3,1fr)",
                   },
            children=[
                html.Div(
                    style={"grid-column-start": "span 2"},
                    children=[dcc.Graph(figure=map_graph)]
                ),
                html.Div(
                    style={},
                    children=[make_table(countries_df)]
                )
            ]
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 30,
                "gridTemplateColumns": "repeat(4, 1fr)"
            },
            children=[
                html.Div(
                    style={},
                    children=[dcc.Graph(figure=bar_graph)]),
                html.Div(
                    style={"grid-column-start": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "color": "#111111"
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ]
                        ),
                        dcc.Graph(id="country-graph")
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output("country-graph", "figure"),
    [Input("country", "value")]
)
def update_graph(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()

    fig = px.line(df, x="date", y=["confirmed", "death", "recovered"],
                  template="plotly_dark",
                  labels={
                      "value": "Cases",
                      "variable": "Condition",
                      "date": "Date"
    },
        hover_data={
        "value": ":,",
        "variable": False
    }
    )
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#3498db"
    fig["data"][2]["line"]["color"] = "#2ecc71"
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
