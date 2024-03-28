import dash
from dash import Dash, html,dcc, dash_table
from dash.dependencies import Output, Input
import pandas as pd
import numpy as pn
from collections import OrderedDict
import plotly.express as px
import requests
from bs4 import BeautifulSoup
#<---------- all Dependecies ------------------>

#<----------------- Web Scraping ---------------->
def Scrapper(symbol):
    symbol=symbol.upper()
    url=f'https://www.screener.in/company/{symbol}/consolidated'
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'html.parser')
    PE=soup.find_all("span","value", "number")[3]
    PE=PE.get_text() #PE of the Stock
    soup=soup.find_all('section', id="profit-loss")
    Sales_Growth=pd.read_html(soup[0].prettify())[1].iloc[:,-1].str.replace('%', '').values #SALES GROWTH
    print(Sales_Growth)
    Profit_Growth=pd.read_html(soup[0].prettify())[2].iloc[:,-1].str.replace('%', '').values #PROFIT GROWTH
    print(Profit_Growth)
    soup=BeautifulSoup(r.text, 'html.parser')
    soup=soup.find_all('ul', id="top-ratios")
    for soup in soup:
        no=soup.find_all('span', class_="number")[1]
        Market_Cap=no.get_text()
    soup=BeautifulSoup(r.text, 'html.parser')
    results = soup.findAll("section",attrs={"id":"profit-loss"})
    df = pd.read_html(results[0].table.prettify())
    net_profit = float(df[0].iloc[10,-2])
    Market_Capint=float(Market_Cap.replace(',', ''))
    FY23PE=Market_Capint/net_profit # FY23PE
    results = soup.findAll("section",attrs={"id":"ratios"})
    roce = pd.read_html(results[0].table.prettify())[0].iloc[-1].dropna().iloc[-6:-1].str.replace("%","").astype("float32").values
    ROCE= pn.median(roce)
    
    return PE, FY23PE, ROCE, Sales_Growth, Profit_Growth


def dcf(coc,roce,gdhgp,tgr,fp,hgp):
    tax_rate = 0.25
    coc = coc/100
    roce = roce/100
    roce = roce * (1-tax_rate)
    gdhgp = gdhgp/100
    tgr = tgr/100
    rr1 = gdhgp/roce
    rr2 = tgr/roce
    cap_emp = 100
    prev_cap_emp = 100
    egr = 0
    nopat = 0
    prev_nopat = 0
    investment = 0
    fcf = 0
    disc_factor = 0
    disc_fcf = 0
    disc_fcf_li = []
    init_nopat = 0
    for i in range(hgp+1):
        if(i>0):
            egr = (nopat/prev_nopat) - 1
            prev_nopat = nopat
        
        nopat = cap_emp*roce
        if(i==0):
            init_nopat = nopat
            prev_nopat = nopat
        prev_cap_emp = cap_emp
        investment = nopat * rr1
        cap_emp = cap_emp + investment
        fcf = nopat - investment
        disc_factor = (1/(1+coc))**i
        disc_fcf = fcf * disc_factor
        disc_fcf_li.append(disc_fcf)
    next_egr = 0
    for i in range(hgp+1,hgp+fp+1):
        egr = egr-((gdhgp-tgr)/fp)
        nopat = cap_emp*roce

        investment = (egr/roce)*nopat
        cap_emp = cap_emp + investment
        fcf = nopat - investment
        disc_factor = (1/(1+coc))**i
        disc_fcf = fcf * disc_factor
        disc_fcf_li.append(disc_fcf)
    terminal_nopat = (nopat*(1+tgr))/(coc-tgr)
    terminal_investment = terminal_nopat*rr2
    terminal_fcf = terminal_nopat - terminal_investment
    terminal_disc_factor = disc_factor
    terminal_disc_fcf = terminal_fcf * terminal_disc_factor
    disc_fcf_li.append(terminal_disc_fcf)
    intrinsic_val = sum(disc_fcf_li)
    print(intrinsic_val)
    calc_iPE = intrinsic_val/init_nopat
    return calc_iPE


#----------------------------------------------------------------------------------------------------------------------------------


inputs=dcc.Input(type='text', value='NESTIND', id='Stock_id', style={
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
    {'Sales Growth (%)': 100, 'Time Period':   '10YRS'},
    {'Sales Growth (%)': 200, ' Time Period':  '5YRS' },
    {'Sales Growth (%)': 350, ' Time Period':  '3YRS' },
    {'Sales Growth (%)': 400, '  Time Period': 'TTM'  }
]
datar = [
    {'Profit Growth (%)': 100, 'Time Period':   '10YRS'},
    {'Profit Growth (%)': 200,  'Time Period':  '5YRS' },
    {'Profit Growth (%)': 350,  'Time Period':  '3YRS' },
    {'Profit Growth (%)': 400,   'Time Period': 'TTM'  }
]
figure_left=px.bar(data, x='Sales Growth (%)', y="Time Period",labels=dict(x="Time Period", y="Sales Growth (%)"), orientation='h')
figure_right=px.bar(datar, x='Profit Growth (%)', y="Time Period",labels=dict(x="Time Period", y="Sales Growth (%)"), orientation='h')


table=dash_table.DataTable(
        id='table_data',
        columns=[],
        data=[]
    )
app = Dash(__name__)

calculator=html.Div([
    html.Div([
        html.H1("VALUING CONSISTENT COMPOUNDERS", className="top_heading")
    ]),
    html.H4('Hi there!', className="subhead"),
    html.P('This page will help you calculate intrinsic PE of consistent compounders through growth-RoCE DCF model.', className="subhead"),
    html.P('We then compare this with current PE of the stock to calculate degree of overvaluation.', className="subhead"),
    html.P("NSE/BSE symbol"),
    html.Div([inputs]),
    html.Div([input_slider]),
    html.Div([
        html.P(["Stock Symbol:", html.Span(id='Stock_symbol', className='Stock_symbol', children=[]) ]),
              html.P(["Current PE:", html.Span(id='PE', className='PE', children=[])]),
              html.P(["FY23PE:", html.Span(id='FY23PE', className='FY23PE', children=[])]),
              html.P(["5-yr median pre-tax RoCE:", html.Span(id='ptRoCE', className='ptRoCE', children=[])])
              ], className="scrap_data"),
              html.Div([table]),
    html.Div([dcc.Graph(
        figure=figure_left, id='left-bar'
    ),dcc.Graph(
        figure=figure_right, id='right-bar'
    ) ], id="graphs"),
     html.Div([
        html.P(["Play with inputs to see changes in intrinsic PE and overvaluation:"]),
              html.P(["The calculated intrinsic PE is:", html.Span(id='CIPE', className='CIPE', children=[])]),
              html.P(["Degree of overvaluation:", html.Span(id='DO', className='DO', children=[])]),
              ], className="cal_data"),
    

])
