import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import inventory_manager as inv

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Mall Inventory Management System'),

    # Section: View Products by Category
    html.Div([
        html.H2('Product Catalog'),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': c, 'value': c} for c in inv.view_products_by_category().keys()],
            placeholder="Select a category"
        ),
        html.Div(id='product-list')
    ]),

    # Section: Update Stock (Purchase/Sale)
    html.Div([
        html.H2('Update Stock'),
        dcc.Input(id='product-id', type='text', placeholder='Product ID'),
        dcc.Input(id='quantity', type='number', placeholder='Quantity'),
        dcc.Dropdown(
            id='operation-type',
            options=[
                {'label': 'Purchase', 'value': 'purchase'},
                {'label': 'Sale', 'value': 'sale'}
            ]
        ),
        dcc.Input(id='operator', type='text', placeholder='Operator'),
        html.Button('Submit', id='submit-btn'),
        html.Div(id='update-status')
    ]),
])


@app.callback(
    Output('product-list', 'children'),
    [Input('category-dropdown', 'value')]
)
def display_products(category):
    if category:
        products = inv.view_products_sorted_by_stock(category)
        return html.Ul([html.Li(f"{p['name']}: {p['stock']} in stock") for p in products])
    return "Select a category to view products."


@app.callback(
    Output('update-status', 'children'),
    [Input('submit-btn', 'n_clicks')],
    [Input('product-id', 'value'), Input('quantity', 'value'), Input('operation-type', 'value'),
     Input('operator', 'value')]
)
def update_stock(n_clicks, product_id, quantity, operation_type, operator):
    if n_clicks:
        return inv.update_stock(product_id, quantity, operation_type, operator)
    return ""


if __name__ == '__main__':
    app.run_server(debug=True)
