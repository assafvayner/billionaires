import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from ref import get_encoded_img

class Item:
    def __init__(self, line):
        line_split = line.split(sep=",")
        self.id = line_split[0]
        self.name = line_split[1]
        self.price = int(line_split[2])
    
    def __repr__(self):
        return self.name + ", " + str(self.price)
    
    def make_div(self):
        res = dbc.Card([
            dbc.CardImg(src=get_encoded_img("img/" + self.id + ".jpg")),
            dbc.CardBody([
                html.H4([self.name, html.Br(), "price: $" + str(self.price)]),
                dcc.Input(id=self.id, type="number", min = 0, step = 1, value=0)
            ])
        ], style={"width": "33%"})
        return res