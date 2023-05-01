import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import time
from .data_utils import scrape_data

# Import data
try:
    df = scrape_data()
except ValueError:
    df = pd.read_csv('..data/matches.csv')

df['Result'].fillna('D', inplace=True)


# Create app
app = dash.Dash(__name__)
app.title = 'Manchester United Premier League Stats'

# Create figure with go for results
fig = go.Figure()
fig.add_trace(go.Indicator(
    gauge={'axis': {'visible': False}},
    value= df['Result'].value_counts().sum(),
    delta={'reference': df['Result'].value_counts()['W']},
    title="Wins",
    domain={'row': 0, 'column': 0}
))
fig.add_trace(go.Indicator(
    gauge={'axis': {'visible': False}},
    value=df['Result'].value_counts().sum(),
    delta={'reference': df['Result'].value_counts()['D']},
    title="Draws",
    domain={'row': 0, 'column': 1}
))
fig.add_trace(go.Indicator(
    gauge={'axis': {'visible': False}},
    value=df['Result'].value_counts().sum(),
    delta={'reference': df['Result'].value_counts()['L']},
    title="Losses",
    domain={'row': 0, 'column': 2}
))
fig.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    template={'data': {'indicator': [{
        'title': {'text': "Results"},
        'mode': "number+delta+gauge",
        'delta': {'reference': df['Result'].value_counts().sum()},
        'gauge': {'axis': {'visible': False}},
        'domain': {'row': 0, 'column': 0}}]
    }}
)

# Create figure with go for results against opponents
res_opp_df = df.groupby('Opponent')['Result'].value_counts().unstack().fillna(0)
opp_fig = go.Figure()
opp_fig.add_trace(go.Bar(
    x=res_opp_df.index,
    y=res_opp_df['W'],
    name='Wins'
))
opp_fig.add_trace(go.Bar(
    x=res_opp_df.index,
    y=res_opp_df['D'],
    name='Draws'
))
opp_fig.add_trace(go.Bar(
    x=res_opp_df.index,
    y=res_opp_df['L'],
    name='Losses'
))
opp_fig.update_layout(
    barmode='stack',
    title='Results against opponents'
)

# results for each day
day_df = df.groupby('Day')['Result'].value_counts().unstack().fillna(0)
day_fig = go.Figure()
day_fig.add_trace(go.Bar(
    x=day_df.index,
    y=day_df['W'],
    name='Wins'
))
day_fig.add_trace(go.Bar(
    x=day_df.index,
    y=day_df['D'],
    name='Draws'
))
day_fig.add_trace(go.Bar(
    x=day_df.index,
    y=day_df['L'],
    name='Losses'
))
day_fig.update_layout(
    barmode='stack',
    title='Results by day'
)

# probability of each outcome
day_prob_df = df.groupby('Result').size().reset_index(name='counts')
day_prob_df['prob'] = day_prob_df['counts'] / day_prob_df['counts'].sum()
day_prob_df['prob'] = day_prob_df['prob'].apply(lambda x: round(x, 2))

day_prob_fig = go.Figure()
day_prob_fig.add_trace(go.Indicator(
    mode='number',
    value=day_prob_df['prob'][0],
    title='Win',
    domain={'row': 0, 'column': 0}
))
day_prob_fig.add_trace(go.Indicator(
    mode='number',
    value=day_prob_df['prob'][1],
    title='Draw',
    domain={'row': 0, 'column': 1}
))
day_prob_fig.add_trace(go.Indicator(
    mode='number',
    value=day_prob_df['prob'][2],
    title='Loss',
    domain={'row': 0, 'column': 2}
))
day_prob_fig.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    template={'data': {'indicator': [{
        'title': {'text': "Results"},
        'mode': "number",
        'domain': {'row': 0, 'column': 0}}]
    }}
)



# Create app layout
app.layout = html.Div([
    html.H1("MANCHESTER UNITED PREMIER LEAGUE STATS"),

    html.Div([
        html.H3("Results"),
        dcc.Graph(id='results', figure=fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Div([
        html.H3("Results by opponent"),
        dcc.Graph(id='goals', figure=opp_fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Br(),

    html.Div([
        html.H3("Results by day"),
        dcc.Graph(id='day', figure=day_fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Div([
        html.H3("Outcome probability"),
        dcc.Graph(id='day-prob', figure=day_prob_fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'})

])

# Run app and display result inline in the notebook
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8050')