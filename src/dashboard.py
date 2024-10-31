# dashboard.py

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

def create_dashboard(filepath):
    """Create a Plotly Dash dashboard."""
    # Load data
    data = pd.read_csv(filepath)

    # Initialize the app
    app = dash.Dash(__name__)

    # Layout
    app.layout = html.Div([
        html.H1("Air Quality Dashboard"),
        dcc.Dropdown(
            id='pollutant',
            options=[{'label': col, 'value': col} for col in ['CO(GT)', 'NOx(GT)', 'NO2(GT)']],
            value='CO(GT)',
            clearable=False
        ),
        dcc.Graph(id='time-series-chart'),
        dcc.Slider(
            id='time-slider',
            min=0,
            max=len(data) - 1,
            value=len(data) // 2,
            marks={i: str(i) for i in range(0, len(data), len(data) // 10)},
        )
    ])

    # Callback to update graph
    @app.callback(
        Output('time-series-chart', 'figure'),
        [Input('pollutant', 'value'), Input('time-slider', 'value')]
    )
    def update_graph(pollutant, time_value):
        filtered_data = data.iloc[:time_value]
        fig = px.line(filtered_data, x=filtered_data.index, y=pollutant, title=f'Time Series of {pollutant}')
        return fig

    # Run the server
    return app

if __name__ == '__main__':
    app = create_dashboard("../data/processed/air_cleaned.csv")
    app.run_server(debug=True)