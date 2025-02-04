from dash import Dash, html, dash_table, dcc, callback, Output, Input
from connection import Connection_to_db
from sql_queries import CreditScore
from sql_queries import CursorAsDataFrame
import plotly.express as px
from pandas import DataFrame
# import dash_bootstrap_components as dbc


class FrontPage():
    def __init__(self):
        super().__init__()
        self.dict_names=['Prague', 'central Bohemia', 'south Bohemia', 'west Bohemia', 'north Bohemia', 'east Bohemia', 'south Moravia', 'north Moravia']

        region_name = 'Prague'
        self.cursor_df = CursorAsDataFrame()
        self.df= self.cursor_df.score_by_region(region_name)
         
        self.app = Dash()
        self.fg = px.histogram(self.df, x='status', y='loan_count')
        
        self.app.layout = html.Div([
            html.H2(children="Statistics based on data from 'PKDD'99 Discovery Challenge Guide to the Financial Data Set"),
            dcc.Dropdown(self.dict_names,
                        ['Prague'], id ='drop_down'),
            dash_table.DataTable(data=self.df.to_dict('records'), page_size= 6),
            
            dcc.Graph(id='graph', figure=self.fg)
        ])

        self.add_callbacks()

    def add_callbacks(self):

        @callback(
        Output('graph', 'figure'),
        Input('drop_down', 'value'),
        )
        def update_graph(drop_down):
            df = self.cursor_df.score_by_region(drop_down)
            fig = px.histogram(df, x='status', y='loan_count')
            return fig



if __name__ == '__main__':
    application = FrontPage()
    application.app.run(debug=True)