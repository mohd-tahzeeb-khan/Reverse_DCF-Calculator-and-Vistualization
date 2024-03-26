from dash import Dash, html, dcc
import dash
from dash.dependencies import Output, Input
app = dash.Dash(__name__)


dropdown=dcc.Dropdown(options=[{
    "label":dcc.Link(children="Home", href="/github"),
    "value":"HOmE"

}, {
    "label":dcc.Link(children="DCF Valuation", href="/github"),
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
    Output('dropdownoption', 'value'), # <- dropdown placeholder gets updated
    Input('dropdownoption', 'value'))
def update_placeholder(value):
    return "PAGES"

if __name__ == '__main__':
    app.run(debug=True)
