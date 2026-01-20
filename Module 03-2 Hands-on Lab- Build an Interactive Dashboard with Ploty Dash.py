# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get payload range
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Dropdown options
launch_sites = [{'label': 'All Sites', 'value': 'All Sites'}]
for site in spacex_df["Launch Site"].unique():
    launch_sites.append({'label': site, 'value': site})

# App layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}
    ),

    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites,
        value='All Sites',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie Chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        }
    ),

    html.Br(),

    # TASK 4: Scatter Plot
    dcc.Graph(id='success-payload-scatter-chart')
])

# TASK 2 Callback: Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'All Sites':
        df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(
            df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        df = spacex_df[spacex_df['Launch Site'] == site]
        df = df['class'].value_counts().reset_index()
        df.columns = ['Launch Outcome', 'Count']
        df['Launch Outcome'] = df['Launch Outcome'].map({1: 'Success', 0: 'Failure'})

        fig = px.pie(
            df,
            values='Count',
            names='Launch Outcome',
            title=f'Total Success vs Failure for {site}'
        )

    return fig

# TASK 4 Callback: Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter_chart(site, payload_range):
    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    if site != 'All Sites':
        df = df[df['Launch Site'] == site]

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs Launch Success'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
