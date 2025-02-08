#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 09:09:10 2025

@author: Seshu K Guddanti
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
import base64
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Initialize Dash app
app = Dash(__name__)

def calculate_investment(monthly_contribution, annual_return, years):
    months = years * 12
    monthly_return = (1 + annual_return / 100) ** (1/12) - 1
    contributions = np.zeros(months)
    total_values = np.zeros(months)
    total = 0
    
    for i in range(months):
        total = (total + monthly_contribution) * (1 + monthly_return)
        contributions[i] = (i + 1) * monthly_contribution
        total_values[i] = total
    
    return contributions, total_values

def generate_plot(monthly_contribution, annual_return, years):
    years_range = np.arange(1, years + 1)
    contributions, total_values = calculate_investment(monthly_contribution, annual_return, years)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years_range, contributions[::12], label='Total Contributions', linestyle='dashed', color='blue')
    ax.plot(years_range, total_values[::12], label='Cumulative Value', color='green')
    ax.set_xlabel('Years')
    ax.set_ylabel('Dollars')
    ax.set_title('Investment Growth Over Time')
    ax.legend()
    ax.grid(True)
    
    # Format y-axis for large numbers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x:,.0f}'))
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url

app.layout = html.Div([
    html.H1("Investment Growth Over Time"),
    dcc.Slider(
        id='monthly_contribution',
        min=0, max=5000, step=100, value=500,
        marks={i: f'${i}' for i in range(0, 5001, 1000)},
        tooltip={"placement": "bottom", "always_visible": True},
    ),
    dcc.Slider(
        id='annual_return',
        min=0, max=20, step=0.5, value=7,
        marks={i: f'{i}%' for i in range(0, 21, 5)},
        tooltip={"placement": "bottom", "always_visible": True},
    ),
    dcc.Slider(
        id='years',
        min=1, max=40, step=1, value=10,
        marks={i: f'{i} yrs' for i in range(1, 41, 5)},
        tooltip={"placement": "bottom", "always_visible": True},
    ),
    html.Img(id='investment_graph')
])

@app.callback(
    Output('investment_graph', 'src'),
    [Input('monthly_contribution', 'value'),
     Input('annual_return', 'value'),
     Input('years', 'value')]
)
def update_graph(monthly_contribution, annual_return, years):
    return f'data:image/png;base64,{generate_plot(monthly_contribution, annual_return, years)}'

if __name__ == '__main__':
    app.run_server(debug=True)
