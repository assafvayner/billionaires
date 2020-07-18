import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from ref import get_encoded_img

class Item:
    """
    Describes an item and contains the necessary properties to add an
    item to the web app
    """
    def __init__(self, line):
        line_split = line.split(sep=",")
        self.id = line_split[0]
        self.name = line_split[1]
        self.price = int(line_split[2])
    
    def __repr__(self):
        """
        to print item as "name, price"
        """
        return self.name + ", " + str(self.price)
    
    def make_div(self):
        """
        makes the UI element designating an item along with a quantity input
        """
        res = dbc.Card([
            dbc.CardImg(src=get_encoded_img("img/" + self.id + ".jpg")),
            dbc.CardBody([
                html.H4([self.name, html.Br(), "price: $" + str(self.price)]),
                dcc.Input(id=self.id, type="number", min = 0, step = 1, value=0)
            ])
        ], style={"width": "33%"})
        return res

def make_items_cards():
    """
    returns list of all Item objects and Div of all item cards with quantity
    input
    """
    items = list()
    # read items from file and make objects
    with open('item_price.csv') as f:
        lines = f.readlines()
        for line in lines:
            items.append(Item(line))
    # make div of item cards
    inp_cards = html.Div([dbc.Row([items[i + j].make_div() for j in range(3)]) \
        for i in range(0, len(items), 3)])
    return items, inp_cards