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

app = dash.Dash(__name__, title='Overview Dashboard', external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
app.config.suppress_callback_exceptions = True


########
#  DATA
########

def loaddata(filename, rateType):
    cur_filepath = filename
    data = pd.read_csv(cur_filepath)
    df = data.melt(var_name='Year',value_name='Unemployment rate(x1000)')
    df['Rate type'] = rateType
    return df

# unemployment rate data
unemploy_df_all = loaddata("unemployment.csv", "All population")
unemploy_df_metro = loaddata("unemployment_metro.csv", "Metropolitan area and agglomeration")
unemploy_df_nonmetro = loaddata("unemployment_Nonmetro.csv", "Non-metropolitan area and non-agglomeration")
unemploy_df_all = pd.concat([unemploy_df_all,unemploy_df_metro,unemploy_df_nonmetro])

# employment data
employment_filepath = "employment.csv"
employ_data = pd.read_csv(employment_filepath)
employ_df_all = employ_data.melt(id_vars=['Lable'], var_name=['Year'], value_name='employment')

########
#  PLOTS
########

# unemployment rate plot
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
        color = alt.Color('Rate type', legend=alt.Legend(
            orient='none',
            legendX=0, legendY=-65)
        ),
        tooltip=['Unemployment rate(x1000)']
    ).properties(width=300, height=200).configure_legend(labelLimit= 0)

    return line.interactive().to_html()   

# employment plot
def plot_employ_chart(rate_type = 'all', start_year=2011, end_year=2021):
    employ_df = employ_df_all[(employ_df_all['Year'].astype(int) >= start_year) & (employ_df_all['Year'].astype(int) <= end_year)]
    line = alt.Chart(employ_df).mark_line(
        point=alt.OverlayMarkDef(color="blue")
    ).encode(
        x=alt.X('Year', title=None),
        y=alt.Y('employment', title='Employment (x 1000)'),
        color = alt.Color('Lable', legend=alt.Legend(
            orient='none',
            legendX=0, legendY=-65)
        ),
        tooltip=['employment']
    ).properties(width=280, height=240)

    return line.interactive().to_html()  

##################

unemploy_chart = html.Iframe(id='unemployment_rate_chart',srcDoc=plot_unemploy_chart(rate_type = 'all', start_year=2011, end_year=2021),style={'width': '100%', 'height': '400px'})

employ_chart = html.Iframe(id='employment_pop_chart',srcDoc=plot_employ_chart(rate_type = 'all', start_year=2011, end_year=2021),style={'width': '100%', 'height': '400px'})

#####################

####Unemployment

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
                        ], width=4, style = {"padding-left": 0, "border-right": "rgb(220 220 220) solid 1px", "height": "380px", "marginTop": "10px"}),
                    dbc.Col([
                        html.Div([
                                html.H5("Key Indicator: Unemployment Rate"),
                                html.Div("The unemployment rate is the number of unemployed persons expressed as a percentage of the labour force. The unemployment rate for a particular group (age, sex, marital status, etc.) is the number unemployed in that group expressed as a percentage of the labour force for that group. Estimates are percentages, rounded to the nearest tenth.", style={"marginTop": "10px"}),
                                html.Div("For this indicator, rural refers to areas outside of Census Metropolitan Areas and Census Agglomerations. ", style={"marginTop": "10px"}),
                                html.Div("The line chart on the left side shows change of the unemployment rate in selected time period.", style={"marginTop": "10px"}),
                                html.Div("(Default: 2011 to 2021)", style={"marginTop": "0px"}),
                                html.Div("For overview purpose, only 3 unemployment rate types are shown here. You can find more detailed information and apply more filters on the detail page.", style={"marginTop": "10px"}),
                                html.Div("Reference: Statistics Canada. Table 14-10-0375-01  Employment and unemployment rate, annual", style={"marginTop": "10px", "font-size": "small"}),
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

    ],style = {"width":"100%", "height":"480px", "marginTop":"20px"})


####Employment

component_Employment = dbc.Card([
        # html.Div("School List", style = {"margin": "auto", "width": "822px"}),
        html.H4("Employment Population", style = {"margin": "auto", "width": "98%", "marginTop":"15px", "marginBottom":"0px"}),
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
                                    dcc.Dropdown(id='employment_start_year', options = [x for x in range (2011,2022)], value = 2011)
                                ], width={"size": 5, "offset": 1}),
                                dbc.Col([
                                    html.Div('End Year', style={"font-size": "small"}),
                                    dcc.Dropdown(id='employment_end_year', options = [x for x in range (2011,2022)], value = 2021)
                                ], width=5),
                            ]),
                                
                            employ_chart
                        ], width=4, style = {"padding-left": 0, "border-right": "rgb(220 220 220) solid 1px", "height": "380px", "marginTop": "10px"}),
                    dbc.Col([
                        html.Div([
                                html.H5("Key Indicator: Employment"),
                                html.Div("The employment is the number of persons who, during the reference week, worked for pay or profit, or performed unpaid family work or had a job but were not at work due to own illness or disability, personal or family responsibilities, labour dispute, vacation, or other reason. Those persons on layoff and persons without work but who had a job to start at a definite date in the future are not considered employed. Estimates in thousands, rounded to the nearest hundred.", style={"marginTop": "10px"}),
                                html.Div("For this indicator, Rural areas are sparsely populated lands which include small towns, villages and other populated places with less than 1,000 population according to the previous census, as well as remote areas and agricultural lands. Rural areas can be found inside or outside of census metropolitan areas (CMA) or census agglomerations (CA). ", style={"marginTop": "10px"}),
                                html.Div("The line chart on the left side shows the changes of the employment in selected time period.", style={"marginTop": "10px"}),
                                html.Div("(Default: 2011 to 2021)", style={"marginTop": "0px"}),
                                html.Div("For overview purpose, only all population centres and rural areas, Census metropolitan area (CMA) and census agglomerationare (CA), Non-census metropolitan area (Non-CMA) and non-census agglomeration (Non-CA) are shown here. You can find more detailed information and apply more filters on the detail page.", style={"marginTop": "10px"}),
                                html.Div("Reference: Statistics Canada. Table 14-10-0375-01  Employment and unemployment rate, annual", style={"marginTop": "10px", "font-size": "small"}),
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

    ],style = {"width":"100%", "height":"550px", "marginTop":"20px"})







dashboard_width = "1250px"

## Layout
app.layout = dbc.Container([

    dbc.Row(
        [
            component_UnemploymentRate

        ],style = {"margin": "auto", "width": dashboard_width}
    ),

    dbc.Row(
        [
            component_Employment

        ],style = {"margin": "auto", "width": dashboard_width}
    )
], style = {"max-width": "2000px"})

# Callback functions 

# Unemployment rate
@app.callback(
    Output('unemployment_rate_chart','srcDoc'), # Specifies where the output "goes"
    Input('start_year', 'value'),
    Input('end_year', 'value')
    )
def update_plot(startYear, endYear): #, in_out_state = 1, room_board = 1
   
    newplot = plot_unemploy_chart(rate_type = 'all', start_year=startYear, end_year=endYear)
    return newplot

# Employment
@app.callback(
    Output('employment_pop_chart','srcDoc'), # Specifies where the output "goes"
    Input('employment_start_year', 'value'),
    Input('employment_end_year', 'value')
    )
def update_plot(startYear, endYear): #, in_out_state = 1, room_board = 1
   
    newplot = plot_employ_chart(rate_type = 'all', start_year=startYear, end_year=endYear)
    return newplot


if __name__ == "__main__":
    app.run_server(host="127.0.0.1", debug=True)
