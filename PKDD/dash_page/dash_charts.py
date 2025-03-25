from dash import Dash, html, dcc, callback, Output, Input
from PKDD.dash_page.sql_queries import CreditScore, CursorAsDataFrame
import plotly.express as px
import dash_bootstrap_components as dbc
from flask import Blueprint
from PKDD import db
from flask import current_app

class DashPage:
    '''
    Page with charts made with Dash. To make style more elegant theres also used dash_bootstrap 
    '''
    def __init__(self):
        super().__init__()
        self.charts = Blueprint('charts', __name__)
        self.regions = ['Prague', 'central Bohemia', 'south Bohemia', 'west Bohemia',
                        'north Bohemia', 'east Bohemia', 'south Moravia', 'north Moravia']

        region_name = ''
        with current_app.app_context():
            self.cursor_df_obj = CursorAsDataFrame(db.session)

            self.df_score_region = self.cursor_df_obj.score_by_region(region_name)
            self.df_trans_region = self.cursor_df_obj.number_of_trans_by_region()
            self.df_by_month = self.cursor_df_obj.number_of_tarns_per_month('1993')

        self.app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],server=current_app,
                         url_base_pathname='/charts/')

        #charts
        self.fg_score_region = px.histogram(self.df_score_region, x='status', y='loan_count',
                                             title="Loan Count by Status", color_discrete_sequence=['#636EFA'])
        self.trans_region = px.histogram(self.df_trans_region, x='region', y='count',
                                            title="Transactions by Region", color_discrete_sequence=['#FFA07A'])
        self.fg_by_month = px.bar(self.df_by_month, x='month', y='count',
                                             title="Transactions per Month", color_discrete_sequence=['#00CC96'])

        #style
        self.fg_score_region.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=18),
            title=dict(x=0.5, xanchor='center', font=dict(size=26))
            )
        self.trans_region.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=18),
            title=dict(x=0.5, xanchor='center', font=dict(size=26))
            )
        self.fg_by_month.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=18),
            title=dict(x=0.5, xanchor='center', font=dict(size=26))
            )

        #layout
        self.app.layout = dbc.Button(
            id='button', 
            children='Home page', 
            className="nav-item nav-link", 
            style={
                'background': 'none',
                'border': 'none',
                'color': 'rgba(255,255,255,.5)',
                'hover': {'color': 'rgba(255,255,255,.75)'}
            }, 
            href='/')
        
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("Statistics based on data from 'PKDD'99 Discovery Challenge Guide to the Financial Data Set",
                                 className="text-center text-info mb-2", style={'font-size': '48px', 'font-family': 'Arial'}), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H5("Made by Karol Grabowski", className="text-center text-secondary mb-4",
                                 style={'font-size': '24px', 'font-family': 'Arial'}), width=12)
            ]),
            dbc.Row([
                dbc.Col(dbc.Select(
                    id='drop_down_region',
                    options=[{'label': name, 'value': name} for name in self.regions],
                    value='Prague',
                    className="mb-4"
                ), width=2)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph_region', figure=self.fg_score_region, className="mb-4"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph_by_account', figure=self.trans_region, className="mb-4"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dbc.Select(
                    id='drop_down_months',
                    options=[{'label': year, 'value': year} for year in ['1993', '1994', '1995', '1996', '1997', '1998']],
                    value='1993',
                    className="mb-4"
                ), width=2)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph_by_month', figure=self.fg_by_month, className="mb-4"), width=12)
            ])
        ], fluid=True, className="p-4 bg-dark text-white")

        self.add_callbacks()


    
    def add_callbacks(self):
        @callback(
            Output('graph_region', 'figure'),
            Input('drop_down_region', 'value'),
        )
        def update_score_region(drop_down):
            df = self.cursor_df_obj.score_by_region(drop_down)
            fig = px.histogram(df, x='status', y='loan_count', title="Loan Count by Status",
                                color_discrete_sequence=['#636EFA'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=18),
                title=dict(x=0.5, xanchor='center', font=dict(size=26))
            )
            return fig

        @callback(
            Output('graph_by_month', 'figure'),
            Input('drop_down_months', 'value'),
        )
        def update_by_month(drop_down):
            df = self.cursor_df_obj.number_of_tarns_per_month(drop_down)
            fig = px.bar(df, x='month', y='count', title="Transactions per Month",
                          color_discrete_sequence=['#00CC96'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=18),
                title=dict(x=0.5, xanchor='center', font=dict(size=26))
            )
            return fig
        


    def __repr__(self):
        return 'DashPage()'


dash_obj = DashPage()
dash_page = dash_obj.app
charts = dash_obj.charts
