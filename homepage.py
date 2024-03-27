from dash import Dash, html, dcc
import dash
from dash.dependencies import Output, Input
from Cal_Graph import calculator
app = dash.Dash(__name__)

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
    Output('dropdownoption', 'placeholder'), # <- dropdown placeholder gets updated
    Input('dropdownoption', 'value'))
def update_placeholder(value):
    return "PAGES"

@app.callback(
        Output('Stock_data', 'children'),
        Input('dropdownoption', 'value')
)
def data(data):
    return 'This is tahzeeb"s logic'

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
if __name__ == '__main__':
    app.run(debug=True)
