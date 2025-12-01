import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load Data
combined_df = pd.read_csv("combined_future.csv")
total_df = pd.read_csv("total_future.csv")

# App Init
app = Dash(__name__)
app.title = "Sales Forecast Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Sales Forecast Dashboard"),

    html.Div([
        html.Label("Select Forecast Type:"),
        dcc.Dropdown(
            id='forecast-type',
            options=[
                {'label': 'Category-wise Forecast', 'value': 'category'},
                {'label': 'Total Forecast', 'value': 'total'}
            ],
            value='category',
            multi=False
        )
    ], className="dropdown-container"),

    html.Div([
        html.Label("Select Category/Categories:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in combined_df['Category'].unique()],
            value=['Bakery'],
            multi=True
        )
    ], className="dropdown-container"),

    html.Div([
        dcc.Graph(id='forecast-graph')
    ], className="graph-container")
])

# Callback
@app.callback(
    Output('forecast-graph', 'figure'),
    Input('forecast-type', 'value'),
    Input('category-dropdown', 'value')
)
def update_graph(forecast_type, selected_categories):
    if forecast_type == 'category':
        filtered_df = combined_df[combined_df['Category'].isin(selected_categories)]
        fig = px.line(filtered_df, x='Date', y='Forecast', color='Category',
                      title="6-Month Category-wise Weekly Sales Forecast")
    else:
        fig = px.line(total_df, x='Date', y='Forecast',
                      title="6-Month Total Sales Forecast")
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        title_x=0.5
    )
    return fig

# Run
if __name__ == '__main__':
    app.run(debug=True)
