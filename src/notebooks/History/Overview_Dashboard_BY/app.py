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

app = dash.Dash(__name__, title='US School Finder', external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
app.config.suppress_callback_exceptions = True

cur_filepath = "unemployment.csv"
unemploy_data = pd.read_csv(cur_filepath)
unemploy_df_all = unemploy_data.melt(var_name='Year',value_name='Unemployment rate(x1000)')

def plot_unemploy_chart(rate_type = 'all', start_year=2011, end_year=2021):
    # if rate_type == 'all':
    #     unemploy_df = unemploy_df_all
    # else:
    #     unemploy_df = unemploy_df_all
    unemploy_df = unemploy_df_all[(unemploy_df_all['Year'].astype(int) >= start_year) & (unemploy_df_all['Year'].astype(int) <= end_year)]
    line = alt.Chart(unemploy_df).mark_line(
        point=alt.OverlayMarkDef(color="blue")
    ).encode(
        x='Year',
        y='Unemployment rate(x1000)',
        tooltip=['Unemployment rate(x1000)']
    ).properties(width=300, height=240)

    return line.interactive().to_html()  
unemploy_chart = html.Iframe(id='unemployment_rate_chart',srcDoc=plot_unemploy_chart(rate_type = 'all', start_year=2011, end_year=2021),style={'width': '100%', 'height': '400px'})

component_UnemploymentRate = dbc.Card([
        # html.Div("School List", style = {"margin": "auto", "width": "822px"}),
        html.H4("Unemployment Rate", style = {"margin": "auto", "width": "98%", "marginTop":"15px", "marginBottom":"0px"}),
        html.Hr(style = {"margin": "10px 10px"}),
        html.Div( 
        [
            # dbc.Col(component_heatmap, width="auto"),
            dbc.Row(
                [
                    dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Div('Start Year', style={"font-size": "small"}),
                                    dcc.Dropdown(id='start_year', options = [x for x in range (2011,2022)], value = 2011)
                                ], width={"size": 5, "offset": 1}),
                                dbc.Col([
                                    html.Div('End Year', style={"font-size": "small"}),
                                    dcc.Dropdown(id='end_year', options = [x for x in range (2011,2022)], value = 2021)
                                ], width=5),
                            ]),
                                
                            unemploy_chart
                        ], width=4, style = {"padding-left": 0, "border-right": "rgb(220 220 220) solid 1px", "height": "360px", "marginTop": "10px"}),
                    dbc.Col([
                        html.Div([
                                html.Div("Hello, There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. "),
                                html.Div("Hello, There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. ", style={"marginTop": "10px"}),
                                html.Div("Hello, There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. There is the place for related information. ", style={"marginTop": "10px"}),
                                html.Div([
                                    dbc.Button(
                                        "Detail",
                                        href="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410037501",
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
            component_UnemploymentRate

        ],style = {"margin": "auto", "width": dashboard_width}
    ),

], style = {"max-width": "2000px"})

# Callback functions for tuition chart
@app.callback(
    Output('unemployment_rate_chart','srcDoc'), # Specifies where the output "goes"
    Input('start_year', 'value'),
    Input('end_year', 'value')
    )
def update_plot(startYear, endYear): #, in_out_state = 1, room_board = 1
   
    newplot = plot_unemploy_chart(rate_type = 'all', start_year=startYear, end_year=endYear)
    return newplot




if __name__ == "__main__":
    app.run_server(host="127.0.0.4", debug=True)
