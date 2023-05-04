import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import time
from .data_utils import scrape_data, read_static_data

# Import data
try:
    df = scrape_data()
except ValueError:
    df = read_static_data()

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
    title = 'Propotion of Results',
    template={'data': {'indicator': [{
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
    title='Results Distribution by Opponent'
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
    title='Results Distribution by  day'
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
    title = 'Probability of each outcome',
    template={'data': {'indicator': [{
        'mode': "number",
        'domain': {'row': 0, 'column': 0}}]
    }}
)

# venue results 
venue_df = df.groupby('Venue')['Result'].value_counts().unstack().fillna(0)
venue_fig = go.Figure()
venue_fig.add_trace(go.Indicator(
    mode='number',
    value=venue_df['W'][0],
    title='Home wins',
    domain={'row': 0, 'column': 0}
))
venue_fig.add_trace(go.Indicator(
    mode='number',
    value=venue_df['D'][0],
    title='Home draws',
    domain={'row': 0, 'column': 1}
))
venue_fig.add_trace(go.Indicator(
    mode='number',
    value=venue_df['L'][0],
    title='Home losses',
    domain={'row': 0, 'column': 2}
))
venue_fig.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    title = 'Outcomes for home games',
    template={'data': {'indicator': [{
        'mode': "number",
        'domain': {'row': 0, 'column': 0}}]
    }}
)

# away
away_fig = go.Figure()
away_fig.add_trace(go.Indicator(
    mode='number',
    value=venue_df['W'][1],
    title='Away wins',
    domain={'row': 0, 'column': 0}
))
away_fig.add_trace(go.Indicator(
    mode='number',
    value=venue_df['D'][1],
    title='Away draws',
    domain={'row': 0, 'column': 1}
))
away_fig.add_trace(go.Indicator(
    mode='number',
    value=venue_df['L'][1],
    title='Away losses',
    domain={'row': 0, 'column': 2}
))
away_fig.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    title = 'Outcomes for away games',
    template={'data': {'indicator': [{
        'mode': "number",
        'domain': {'row': 0, 'column': 0}}]
    }}
)




# Create app layout
app.layout = html.Div([
    html.H1("MANCHESTER UNITED PREMIER LEAGUE STATS"),

    html.Div([
        dcc.Graph(id='results', figure=fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Div([
        dcc.Graph(id='goals', figure=opp_fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Br(),

    html.Div([
        dcc.Graph(id='day', figure=day_fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Div([
        dcc.Graph(id='day-prob', figure=day_prob_fig)
    ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),

    html.Br(),

    html.Div([
        html.Div([
            dcc.Graph(id='venue', figure=venue_fig)
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='away', figure=away_fig)
        ], style={'width': '49%', 'display': 'inline-block', 'height': '50%'}),
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

])

# Run app and display result inline in the notebook
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8050')