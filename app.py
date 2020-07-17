import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import ref
import numpy as np
from item import Item, make_items_cards

# initialize data
net_worths = ref.get_net_worths()



curr = ""
items, inp_cards = make_items_cards()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div(children=[
    html.H1('Introduction to this website'),
    html.Br(),
    dcc.Dropdown(
        id='billionaire',
        options=ref.billionaire_dropdown_options(net_worths),
        value='Jeff Bezos'
    ),
    html.Br(),

    # image of face of billionaire
    html.Div([
        html.H2(id='name'),
        html.Img(id='img'),
    ], style={"textAlign":"center"}),

    html.P(id='person_info'),
    # item cards
    inp_cards,

    html.P(id='post_purchase')
])

inp_list = [Input(item.id, "value") for item in items]

# billionaire change events and item quantity change events
# (to be separate potentially)
@app.callback(
    [Output('name', 'children'),
     Output('img', 'src'),
     Output('person_info', 'children'),
    Output('post_purchase', 'children')],
    [*inp_list, Input('billionaire', 'value')]
)
def update_output(*args):
    res = []
    name = args[-1]
    res.append(name)

    global curr
    res.append(ref.get_square_image(name, net_worths, curr))
    curr = name
    
    res.append(ref.make_person_intro(name, net_worths))

    [i if isinstance(i, int) else 0 for i in args[0:-1]]
    inps = np.array([i if isinstance(i, int) else 0 for i in args[0:-1]])
    prices = np.array([item.price for item in items], dtype=int)
    total_cost = np.sum(inps * prices)
    res.append(ref.post_purchase(total_cost, name, net_worths))
    
    return tuple(res)


if __name__ == '__main__':
    app.run_server(debug=True)