import dash
from dash import Dash, html,dcc, dash_table
from dash.dependencies import Output, Input
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import requests
from bs4 import BeautifulSoup
#<---------- all Dependecies ------------------>

#<----------------- Web Scraping ---------------->
def Scrapper():
    url='https://www.screener.in/company/NESTLEIND/'
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'html.parser')
    PE=soup.find_all("span","value", "number")[3]
    PE=PE.get_text() #PE of the Stock
    soup=soup.find_all('section', id="profit-loss")
    Sales_Growth=pd.read_html(soup[0].prettify())[1].iloc[:,-1].str.replace('%', '').values #SALES GROWTH
    Profit_Growth=pd.read_html(soup[0].prettify())[2].iloc[:,-1].str.replace('%', '').values #PROFIT GROWTH
    soup=soup.find_all('ul', id="top-ratios")
    for soup in soup:
        no=soup.find_all('span', class_="number")[0]
        Market_Cap=no.get_text()

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
data = [
    {'label': '10YRS', 'value': 100},
    {'label': '5YRS', 'value': 200},
    {'label': '3YRS', 'value': 300},
    {'label': 'TTM', 'value': 400}
]
figuare=px.bar(data, x='value', y="label",labels=dict(x="time", y="perioids"), orientation='h')
app = Dash(__name__)

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
    html.Div([
        html.Div(["Stock Symbol:", html.Span(id='Stock_symbol', className='Stock_symbol', children=[]) ]),
              html.Div(["Current PE:", html.Span(id='PE', className='PE', children=[])]),
              html.Div(["FY23PE:", html.Span(id='FY23PE', className='FY23PE', children=[])]),
              html.Div(["5-yr median pre-tax RoCE:", html.Span(id='ptRoCE', className='ptRoCE', children=[])])
              ], className="scrap_data"),
    html.Div([dcc.Graph(
        figure=figuare
    ),dcc.Graph(
        figure=figuare
    ) ], id="graphs"),
     html.Div([
        html.Div(["Play with inputs to see changes in intrinsic PE and overvaluation:"]),
              html.Div(["The calculated intrinsic PE is:", html.Span(id='CIPE', className='CIPE', children=[])]),
              html.Div(["Degree of overvaluation:", html.Span(id='DO', className='DO', children=[])]),
              ], className="cal_data"),
    

])
Scrapper()