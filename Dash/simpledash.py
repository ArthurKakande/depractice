import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input, dash_table

# Load the dataset
df = pd.read_csv('housing.csv')

# Initialize the Dash app
app = Dash()

app.layout = [
    html.Div(children='Dashboard'),
    dash_table.DataTable(data=df.to_dict(orient='records'), page_size=20),
    html.Div([
        html.Label('Select Feature:'),
        dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=df.columns[0]  # Default value
        )
    ]),
    dcc.Graph(id='histogram')
]

@app.callback(
    Output('histogram', 'figure'),
    Input('feature-dropdown', 'value')
)

def update_histogram(selected_feature):
    fig = px.histogram(df, x=selected_feature)
    fig.update_layout(title=f'Histogram of {selected_feature}',
                      xaxis_title=selected_feature,
                      yaxis_title='Frequency')
    return fig

if __name__ == '__main__':
    app.run(debug=True)