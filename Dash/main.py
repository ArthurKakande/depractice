import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State

app = Dash()

app.layout = html.Div(
    style={'backgroundColor': '#111111', 'color': '#FFFFFF', 'padding': '20px'},
    children=[
        html.H1("Stock Price Dashbaord", style={'textAlign': 'center', 'color': '#FFFFFF'}),
        html.Div([
            html.Label('Enter Stock Ticker Symbol:', style={'color': '#FFFFFF'}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'backgroundColor': '#333333', 'color': '#FFFFFF'})
        ], style={'padding': '10px'}),

        html.Div([
            html.Label('Select Start Date:', style={'color': '#FFFFFF'}),
            dcc.DatePickerSingle(id='start-date-picker', date='2022-01-01')
        ], style={'padding': '10px'}),

        html.Div([
            html.Label('Select End Date:', style={'color': '#FFFFFF'}),
            dcc.DatePickerSingle(id='end-date-picker', date='2023-01-01')
        ], style={'padding': '10px'}),

        html.Div([
            html.Button('Submit', id='submit-button', n_clicks=0, style={'backgroundColor': '#007BFF', 'color': '#FFFFFF'})
        ], style={'padding': '10px', 'textAlign': 'center'}),

        html.Div(id='chart-container', style={'visibility': 'hidden'}, 
                 children=[
                     dcc.Graph(id='candlestick-chart', style={'backgroundColor': '#111111'}),
                 ])
    ]
)

@app.callback(
    [Output('candlestick-chart', 'figure'),
     Output('chart-container', 'style')],
    [Input('submit-button', 'n_clicks')],
    [State('ticker-input', 'value'),
     State('start-date-picker', 'date'),
     State('end-date-picker', 'date')]
)

def update_chart(n_clicks, ticker, start_date, end_date):
    if n_clicks > 0:
        # Fetch stock data
        df = yf.download(ticker, start=start_date, end=end_date)
        #df['date'] = pd.to_datetime(df.index)
        #print(df.index)  # Debugging line to check data
        #print(df['Close'].head())
        #print(df['Close'].isnull().sum())
        #print(df.columns)

        #if df is None or df.empty:
            # Return empty figure and hide chart if no data
         #   return go.Figure(), {'visibility': 'hidden'}
        
        # Create candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df[('Open', ticker)],
                                             high=df[('High', ticker)],
                                             low=df[('Low', ticker)],
                                             close=df[('Close', ticker)])
                                             ])

        #fig.write_image("my_chart.png") # Debugging line to check figure
        
        fig.update_layout(title=f'Candlestick Chart for {ticker}',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)',
                          xaxis_rangeslider_visible=False,
                          template='plotly_dark')
        
        return fig, {'visibility': 'visible'}
    
    return go.Figure(), {'visibility': 'hidden'}

if __name__ == '__main__':
    app.run(debug=True)