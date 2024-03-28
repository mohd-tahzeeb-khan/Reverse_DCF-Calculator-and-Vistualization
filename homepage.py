from dash import Dash, html, dcc
import dash
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
from Cal_Graph import calculator, Scrapper, dcf
from app import server as application
app = dash.Dash(__name__)
server=app.server

global navigationbar
dropdown=dcc.Dropdown(options=[{
    "label":dcc.Link(children="Home", href="/"),
    "value":"HOME"

}, {
    "label":dcc.Link(children="DCF Valuation", href="/DCF"),
    "value":"DCF"

},],placeholder="PAGES",
id="dropdownoption", className="dropdownoption")

textline=html.Div([
    html.H4("This site provides interactive tools to valuate and analyze stocks through Reverse DCF model. Check the navigation bar for more.")
], id="textline")

navigationbar=html.Div([
    html.Div([
        html.H3("Reverse DCF")], className="Heading-text"), 
        html.Div([dropdown],id="attachdropdown")], id="Navbar",)

app.layout = html.Div([navigationbar, textline])

@app.callback(
    Output('dropdownoption', 'placeholder'),
    Input('dropdownoption', 'value'))
def update_placeholder(value):
    return "PAGES"

@app.callback(
        [Output('Stock_symbol', 'children'),Output('PE', 'children'),Output('FY23PE', 'children'),Output('ptRoCE', 'children'),Output('table_data', 'columns'), Output('table_data', 'data'), Output('left-bar', 'figure'), Output('right-bar', 'figure')],
        [Input('dropdownoption', 'value'), Input('Stock_id', 'value')]
)
def data(data, symbol):
    a=Scrapper(symbol)
    data=[{" ":"Sales Growth","10 yrs":a[3][0],"5yrs":a[3][1],"3yrs":a[3][2],"TTM":a[3][3]},{" ":"Profit growth","10 yrs":a[4][0],"5yrs":a[4][1],"3yrs":a[4][2],"TTM":a[4][3]}]
    coloum=[{'name':" ",'id':" "},{'name':"10 yrs",'id':'10 yrs'},{'name':"5yrs",'id':'5yrs'},{'name':"3yrs",'id':'3yrs'},{'name':"TTM",'id':'TTM'}]
    #fig = px.bar(x=[,,,],y=["10 yrs","5 yrs","3 yrs","TTM"],orientation="h",labels=dict(x="Sales Growth (%)",y="Time Period"))
    datagraph_left = [
    {'Sales Growth (%)':int(a[3][0]) , 'Time Period':'10YRS'},
    {'Sales Growth (%)':int(a[3][1]) , 'Time Period':'5YRS'  },
    {'Sales Growth (%)':int(a[3][2]) , 'Time Period':'3YRS'  },
    {'Sales Growth (%)':int(a[3][3]) , 'Time Period':'TTM'  }
]
    datagraph_right = [
    {'Profit Growth (%)':int(a[4][0]) , 'Time Period':'10YRS'},
    {'Profit Growth (%)':int(a[4][1]) , 'Time Period':'5YRS'  },
    {'Profit Growth (%)':int(a[4][2]) , 'Time Period':'3YRS'  },
    {'Profit Growth (%)':int(a[4][3]) , 'Time Period':'TTM'  }
]
    updated=px.bar(datagraph_left, x='Sales Growth (%)', y='Time Period', orientation='h', labels=dict(x="TimePeriod", y="Sales Growth (%)"))
    updated_right=px.bar(datagraph_right, x='Profit Growth (%)', y='Time Period', orientation='h', labels=dict(x="Time Period", y="Profit Growth (%)"))
    return symbol.upper(),a[0], round(a[1],2), a[2],coloum, data, updated, updated_right


@app.callback(
    Output('textline', 'children'),
    Input('dropdownoption', 'value')
)
def render_content(page):
    print(page)
    if page=='HOME':
        return textline
    else:
        return calculator
@app.callback(
    [Output('CIPE', 'children'),Output('DO', 'children')],
    [Input('coc', 'value'),Input('ReCO', 'value'),Input('gdhgp', 'value'),Input('hgp', 'value'),Input('fd', 'value'),Input('tgr', 'value'), Input('PE', 'children'),Input('FY23PE', 'children'),Input('ptRoCE', 'children')])
def icalculator(inputcoc, inputreco, inputgdhgp, inputhgp, inputfd, inputtgr, pe, fy23pe, ptroce):
    b=dcf(inputcoc,inputreco,inputgdhgp,inputtgr,inputfd,inputhgp)
    
    peconvert=float(pe)
    fy23peconvert=float(fy23pe)
    cipeconvert=float(b)
    if(peconvert<fy23peconvert):
        do=peconvert/cipeconvert
        do=do-1
        do=do*100
    
    else:
        do=fy23peconvert/cipeconvert
        do=do-1
        do*100
    do=round(do)
    do=str(do)
    do=do + " % "
    return round(b,2),do

if __name__ == '__main__':
    application.run()
