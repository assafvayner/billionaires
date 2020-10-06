import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import ref
import numpy as np
from item import Item, make_items_cards, make_receipt
import UI

# initialize data
net_worths = ref.get_net_worths()

items, inp_cards = make_items_cards()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.title = 'Billionaires'
app.layout = html.Div(children=[
    UI.title,
    UI.credit,
    UI.intro,
    html.Br(),
    html.Div([
        html.H2('Select billionaire to analyze wealth:'),
        dcc.Dropdown(
            id='billionaire',
            options=ref.billionaire_dropdown_options(net_worths),
            value='Jeff Bezos',
            clearable=False
        )
    ]),
    html.Br(),

    # image of face of billionaire
    html.H2(id='person_info'),

    html.Div([
        html.Div([
            html.H2(id='name'),
            html.Img(id='img')
        ], style={'text-align':'center', 'width':'40%', 'display' : 'inline-block', 'vertical-align':'top'}),

        
        html.Div(make_receipt(items, [0]*9, 'Jeff Bezos', net_worths),
                id='receipt',
                style={'width':'60%', 'display': 'inline-block'})
    ], style={'padding':'20px'}),

    # item cards
    inp_cards,

    html.H3(id='post_purchase')
])

inp_list = [Input(item.id, 'value') for item in items]

# billionaire change events and item quantity change events
# (to be separate potentially)
@app.callback(
    [
     Output('name', 'children'),
     Output('img', 'src'),
     Output('person_info', 'children'),
     Output('post_purchase', 'children'),
     Output('receipt', 'children')
    ],
    [*inp_list, Input('billionaire', 'value')]
)
def update_output(*args):
    res = []
    args = list(args)
    name = args[-1]
    args.pop(-1)
    res.append(name)

    res.append(ref.get_square_image(name, net_worths))
    
    res.append(ref.make_person_intro(name, net_worths))

    inps = np.array([i if isinstance(i, int) else 0 for i in args])
    prices = np.array([item.price for item in items], dtype=int)
    total_cost = np.sum(inps * prices)
    post_purchase = ref.post_purchase(total_cost, name, net_worths)
    res.append(post_purchase)
    receipt = make_receipt(items, inps, name, net_worths)
    res.append(receipt)
    return tuple(res)


if __name__ == '__main__':
    app.run_server(debug=False)