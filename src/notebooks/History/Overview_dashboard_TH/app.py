import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import json
from dash import Input, Output, State, MATCH, ALL

component_RCBP_Dscription = dbc.Card([
        # html.Div("School List", style = {"margin": "auto", "width": "822px"}),
        html.H4("Rural Canada Business Profile from 2017 to 2019", style = {"margin": "auto", "width": "98%", "marginTop":"15px", "marginBottom":"0px"}),
        html.Hr(style = {"margin": "10px 10px"}),
        html.Div( 
        [
            # dbc.Col(component_heatmap, width="auto"),
            dbc.Row(
                [
                    #dbc.Col([
                        html.Div([
                                # html.H5("Title"),
                                html.Div("The Rural Canada Business Profiles database (RCBP) provides data on counts and key financial indicators of small and medium sized businesses with a theme classification by rural and urban areas of Canada. The RCBP has a similar methodology to the Financial Performance Data (FPD). In contrast to the FPD, the RCBP notably features a rural and urban breakdown.", style={"marginTop": "10px"}),
                                html.Div("Key terms definition:", style={"marginTop": "10px"}),
                                html.Div("Net profit to equity ratio: This ratio is calculated as (net profit * 100) / (equity). This percentage indicates the profitability of a business. The higher the ratio, the relatively better the profitability. ", style={"marginTop": "10px"}),
                                html.Div("Current debt to equity ratio: This ratio is calculated as (current liabilities * 100) / (equity). This percentage is a measure of liquidity, which indicates a firm’s relative ability to pay its short-term debts. The lower the positive ratio, the more liquid the business. ", style={"marginTop": "0px"}),
                                html.Div("Debt to equity ratio: This ratio is calculated as (total liabilities) / (total equity). This is a solvency ratio that indicates a firm’s ability to pay its long-term debts. The lower the positive ratio, the more solvent the business. ", style={"marginTop": "10px"}),
                                html.Div("Revenue to equity ratio: This ratio is calculated as (total revenue) / (equity). It provides an indication of the economic productivity of capital. ", style={"marginTop": "10px", "font-size": "small"}),
                                htmL.Div("Total Number of Business: The count of businesses in each category", style={"marginTop": "10px", "font-size": "small"})
                                html.Div("Total Revenue: It calculate as number of businesses * average revenue",style={"marginTop": "10px", "font-size": "small"})
                                html.Div("Expense Breakdown: Total expense in different categories",style={"marginTop": "10px", "font-size": "small"})
                                html.Div("Direct Expense: Cost of sales",style={"marginTop": "10px", "font-size": "small"})
                                html.Div("Indirect Expense: Operating expense",style={"marginTop": "10px", "font-size": "small"})
                                html.Div("Net profit: It calculated as total revenue – total expense",style={"marginTop": "10px", "font-size": "small"})
                                #html.Div([
                                    #dbc.Button(
                                        #"Detail",
                                        #href="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410037501",
                                        #external_link=True,
                                        #color="primary",
                                    #),
                                #], style = {"position": "absolute", "bottom":"15px", "right": "20px"}),
                            ], style ={"marginTop": "10px"})
                        
                    #    ])
                    
                ],style = {"margin": "auto", "width": '100%'}
            ),
            
        ], style = {"height":"360px", "width": "100%"})

    ],style = {"width":"100%", "height":"480px", "marginTop":"20px"})



dashboard_width = "1250px"

## Layout
app.layout = dbc.Container([

    dbc.Row(
        [
           component_RCBP_Dscription

        ],style = {"margin": "auto", "width": dashboard_width}
    ),

], style = {"max-width": "2000px"})