import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import json
from dash import Input, Output, State, MATCH, ALL

#data
import pandas as pd
import numpy as np
import altair as alt
from textwrap import wrap

app = dash.Dash(__name__, title='Overview', external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
app.config.suppress_callback_exceptions = True

df_YS = pd.read_csv("population.csv")
df_YS_selected=df_YS.iloc[:, [0,1,3,4,11]]
df_YS_selected = df_YS_selected[df_YS_selected["Statistical Area Classification (SAC)"].isin(["All census subdivisions","Within CMAs","Within CAs","Outside CMAs/CAs"])]
df_YS_selected["content_name"]=df_YS_selected["Population and dwelling counts (3)"].apply(lambda x:x.split(",")[0])
df_YS_selected['content_name'] = df_YS_selected['content_name'].apply(wrap, args=[20])

def func_population(prov_name,area):
    df_sub = df_YS_selected[df_YS_selected["GEO"]==prov_name]
    df_sub1 = df_sub[df_sub["Statistical Area Classification (SAC)"]==area]
    tit = "Population and dwelling counts"
    if prov_name is not None:
        tit = tit + " of "+prov_name
    chart = (
        alt.Chart(df_sub1,title=tit)
        .mark_bar()
        .encode(
            x=alt.X('content_name'),
            y="VALUE",
        ).configure_axis(labelLimit=600,title = "")
        .properties(height=200, width=300))
    return chart.to_html()



pop_chart = html.Iframe(
    id="plot1",
    srcDoc=func_population(prov_name="Canada",area = "All census subdivisions"),
    style={'width': '100%', 'height': '400px'},
)



component_population = dbc.Card([
        # html.Div("School List", style = {"margin": "auto", "width": "822px"}),
        html.H4("Population and dwelling counts", style = {"margin": "auto", "width": "98%", "marginTop":"15px", "marginBottom":"0px"}),
        html.Hr(style = {"margin": "10px 10px"}),
        html.Div(
        [
            # dbc.Col(component_heatmap, width="auto"),
            dbc.Row(
                [
                    dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Div('Province', style={"font-size": "small"}),
                                    dcc.Dropdown(id='pop_dropdown', options = [i for i in df_YS_selected['GEO'].unique()], value = 'Canada')
                                ], width={"size": 8, "offset": 1}),
                                dbc.Col([
                                    html.Div('Area Type', style={"font-size": "small"}),
                                    dcc.Dropdown(id='area', options = [i for i in df_YS_selected['Statistical Area Classification (SAC)'].unique()], value = "All census subdivisions")
                                ], width={"size": 8, "offset": 1}),
                            ]),

                            pop_chart
                        ], width=4, style = {"padding-left": 0, "border-right": "rgb(220 220 220) solid 1px", "height": "360px", "marginTop": "10px"}),
                    dbc.Col([
                        html.Div([
                                html.Div("The data is from Census of Population in 2021. You can choose the provinces and the area types to see the population, total private dwellings and private dwellings occupied by usual residents in 2021."),
                                html.Div("The 2021 Census population counts for a particular geographic area represent the number of Canadians whose usual place of residence is in that area, regardless of where they happened to be on Census Day. Also included are any Canadians who were staying in that area on Census Day and who had no usual place of residence elsewhere in Canada, as well as those considered to be non-permanent residents.", style={"marginTop": "10px"}),
                                html.Div("The dwelling counts refer to total private dwellings and private dwellings occupied by usual residents in Canada.  ", style={"marginTop": "10px"}),
                                html.Div("For the area types, CMA refers to a census metropolitan area, and CA refers to a census agglomeration. A CMA must have a total population of at least 100,000 of which 50,000 or more must live in the core. A CA must have a core population of at least 10,000.", style={"marginTop": "10px"}),

                                html.Div([
                                    dbc.Button(
                                        "Detail",
                                        href="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810001601",
                                        external_link=True,
                                        color="primary",
                                    ),
                                ], style = {"position": "absolute", "bottom":"15px", "right": "20px"}),
                            ], style ={"marginTop": "10px"})

                        ])

                ],style = {"margin": "auto", "width": '100%'}
            ),

        ], style = {"height":"360px", "width": "100%"})

    ],style = {"width":"100%", "height":"450px", "marginTop":"20px"})



dashboard_width = "1250px"

## Layout
app.layout = dbc.Container([

    dbc.Row(
        [
        component_population,

        ],style = {"margin": "auto", "width": dashboard_width}
    ),

], style = {"max-width": "2000px"})

# Callback functions for tuition chart
@app.callback(
    Output('plot1','srcDoc'), # Specifies where the output "goes"
    Input('pop_dropdown', 'value'),
    Input('area','value')
    )
def update_plot(pop_dropdown,area): #, in_out_state = 1, room_board = 1
    newplot = func_population(prov_name=pop_dropdown,area = area)
    return newplot




if __name__ == "__main__":
    app.run_server(host="127.0.0.1", debug=True)
