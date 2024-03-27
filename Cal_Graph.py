import dash
from dash import Dash, html,dcc, dash_table
from dash.dependencies import Output, Input
import pandas as pd
from collections import OrderedDict
#<---------- all Dependecies ------------------>


inputs=dcc.Input(type='text', placeholder='NESTIND', id='Stock_id', style={
    #'height':'30px', 
    'border-color':'#000',
    'font-size':'20px', 
    'width':'200px'
})
input_slider=html.Div([
    html.P(["Cost of Capital (CoC): %"]),
    dcc.Slider(min=8,max=16, step=.5,value=12.5, marks={'8':'8', '9':'9', '10':'10', '11':'11','12':'12', '14':'14', '15':'15', '16':'16'} ,id="coc"),
    html.P(["Return on Capital Employed (RoCE): %"]),
    dcc.Slider(10, 100, 10, value=20, id="ReCO"),
    html.P(["Growth during high growth period: $"]), 
    dcc.Slider(8, 20, 2, value=12, id="gdhgp"),
    html.P(["High growth period(years)"]),
    dcc.Slider(10, 24, 2, value=20, id="hgp"), 
    html.P(["Fade period(years):"]),
    dcc.Slider(5, 20, 5, value=15, id="fd"),
    html.P(["Terminal growth rate: %"]),
    dcc.Slider(0, 8, 1, value=20, id="tgr"), 
])


app = Dash(__name__)

data = OrderedDict(
    [
        (["10 YRS", "5 YRS", "3 YRS", "TTM"], ),
        ("Sales Growth", [8,11,13,13]),
        ("Profit Growth", [10, 13, 13, 26])
    ]
)

df = pd.DataFrame(
    OrderedDict([(name) for (name) in data.items()])
)

table = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=2
)
calculator=html.Div([
    html.Div([
        html.H1("VALUING CONSISTENT COMPOUNDERS")
    ]),
    html.H4('Hi there'),
    html.H4('This page will help you calculate intrinsic PE of consistent compounders through growth-RoCE DCF model.'),
    html.H4('We then compare this with current PE of the stock to calculate degree of overvaluation.'),
    html.H3("NSE/BSE symbol", style={
        'color':'#000',
        'padding-bottom':'0px',
        'margin-bottom':'0'
    }),
    html.Div([inputs]),
    html.Div([input_slider]),
    html.Div(id="Stock_data"),
    html.Div([table])

])