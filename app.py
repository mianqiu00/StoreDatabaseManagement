import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import inventory_manager as inv
from datetime import datetime

today = datetime.now().date().isoformat()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, 'https://fonts.googleapis.com/css?family=Roboto&display=swap'], suppress_callback_exceptions=True)

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Product Catalog Management", id="page-1-link"),
                dbc.DropdownMenuItem("Stock In/Out Management", id="page-2-link"),
                dbc.DropdownMenuItem("Sale Analysis", id="page-3-link"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Products List", id="page-4-link"),
                dbc.DropdownMenuItem("Transactions List", id="page-5-link"),
            ]
        ),
        dbc.NavItem(dbc.NavLink("New page", href="http://127.0.0.1:8050/", target="_blank")),
        html.Div(style={'width': '30px'})
    ],
    brand="Mall Inventory Management System"
)

html1 = dbc.Container([
    dbc.Card([
        dbc.CardHeader(html.H2('Product Catalog Management', className="display-5")),
        dbc.CardBody([

            # Section: Add or Delete a Product
            html.H2('Update Product List'),
            # Inputs in a row with product name field
            html.Div([
                dcc.Input(id='product-id-1', type='text', placeholder='Product ID (Add/Delete)',
                          style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                dcc.Input(id='product-name-1', type='text', placeholder='Product Name (Add)',
                          style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                dcc.Input(id='category-1', type='text', placeholder='Category (Add)',
                          style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                dcc.Input(id='user-1', type='text', placeholder='User (Optional)',
                          style={'width': '22%', 'height': '35px'})
            ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                      'margin-bottom': '15px'}),

            # Operation type dropdown
            dcc.Dropdown(
                id='operation-type-1',
                options=[
                    {'label': 'Add', 'value': 'add'},
                    {'label': 'Delete', 'value': 'delete'}
                ],
                placeholder="Select operation type",
                style={'width': '45%', 'margin-bottom': '15px'}
            ),

            # Submit button
            html.Button('Submit', id='submit-btn-product', style={'margin-bottom': '15px'}),

            # Update status
            html.Div(id='update-product-status'),
            html.Br(),

            # Section: Product Catalog Lookup
            html.Div([
                html.H2('Product Catalog'),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': c, 'value': c} for c in inv.view_products_by_category().keys()],
                    placeholder="Select or input a category"
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=3*1000,
                    n_intervals=0
                ),
            ]),
            html.Br(),
            html.Div(id='product-list')
        ])
    ])
])

html2 = dbc.Container([
    dbc.Card([
        dbc.CardHeader(html.H2('Product Catalog Management', className="display-5")),
        dbc.CardBody([
            # Section: Update Stock (Purchase/Sale)
            html.Div([
                html.H2('Update Stock'),

                # Inputs in a row with product name field
                html.Div([
                    dcc.Input(id='product-id-2', type='text', placeholder='Product ID',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='product-name-2', type='text', placeholder='Product Name',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='quantity-2', type='number', placeholder='Quantity',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='user-2', type='text', placeholder='User',
                              style={'width': '22%', 'height': '35px'})
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'margin-bottom': '15px'}),

                # Operation type dropdown
                dcc.Dropdown(
                    id='operation-type-2',
                    options=[
                        {'label': 'Purchase', 'value': 'purchase'},
                        {'label': 'Sale', 'value': 'sale'}
                    ],
                    placeholder="Select operation type",
                    style={'width': '45%', 'margin-bottom': '15px'}
                ),

                # Submit button
                html.Button('Submit', id='submit-btn-stock', style={'margin-bottom': '15px'}),
                # Update status
                html.Div(id='update-stock-status')
            ]),
            html.Br(),

            # Section: Query Transaction
            html.Div([
                html.H2('Query Transaction'),

                # Inputs in a row with product name field
                html.Div([
                    dcc.Input(id='product-id-3', type='text', placeholder='Product ID (Optional)',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='user-3', type='text', placeholder='User (Optional)',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='start-date-3', type='text', placeholder='YYYY-MM-DD', value=today[:10],
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='start-time-3', type='text', placeholder='HH:MM:SS (Start)', value='00:00:00',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='end-date-3', type='text', placeholder='YYYY-MM-DD', value=today[:10],
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='end-time-3', type='text', placeholder='HH:MM:SS (End)', value='00:00:00',
                              style={'width': '22%', 'height': '35px', 'margin-right': '2%'}),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'margin-bottom': '15px'}),

                # Submit button
                html.Button('Submit', id='submit-btn-transaction', style={'margin-bottom': '15px'}),
                # Update status
                html.Div(id='update-transaction-status')
            ])
        ])
    ])
])

html3 = dbc.Container([
    dbc.Card([
        dbc.CardHeader(html.H2('Sale Analysis', className="display-5")),
        dbc.CardBody([
            # Section: Product Catalog Lookup
            html.Div([
                html.H2('Choose Filter'),
                html.Div([
                    dcc.Dropdown(id='category-4',
                        options=[{'label': c, 'value': c} for c in inv.view_products_by_category().keys()],
                        placeholder="Category (Optional)", style={'width': '90%', 'margin-right': '2%'}),
                    dcc.Input(id='start-date-4', type='text', placeholder='YYYY-MM-DD', value=today[:10],
                              style={'width': '50%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='start-time-4', type='text', placeholder='HH:MM:SS (Start)', value='00:00:00',
                              style={'width': '50%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='end-date-4', type='text', placeholder='YYYY-MM-DD', value=today[:10],
                              style={'width': '50%', 'height': '35px', 'margin-right': '2%'}),
                    dcc.Input(id='end-time-4', type='text', placeholder='HH:MM:SS (End)', value='00:00:00',
                              style={'width': '50%', 'height': '35px', 'margin-right': '2%'}),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'margin-bottom': '15px'}),

                # Submit button
                html.Button('Submit', id='submit-btn-sale', style={'margin-bottom': '15px'}),
                # Update status
                html.Div(id='sale-list')
            ]),
        ])
    ])
])

html4 = dbc.Container([
    dbc.Card([
        dbc.CardHeader(html.H2('Products List', className="display-5")),
        dbc.CardBody([
            # Section: Product Catalog Lookup
            html.Div([
                dcc.Interval(id='refresh-1', interval=3*1000, n_intervals=0),
                # Update status
                html.Div(id='all-product-list')
            ]),
        ])
    ])
])

html5 = dbc.Container([
    dbc.Card([
        dbc.CardHeader(html.H2('Transactions List', className="display-5")),
        dbc.CardBody([
            # Section: Product Catalog Lookup
            html.Div([
                dcc.Interval(id='refresh-2', interval=3*1000, n_intervals=0),
                # Update status
                html.Div(id='all-transaction-list')
            ]),
        ])
    ])
])

app.layout = html.Div([
    html.Link(
        href='https://fonts.googleapis.com/css?family=Roboto&display=swap',  # Import Roboto font from Google Fonts
        rel='stylesheet'
    ),
    navbar,
    html.Div(id="page-content"),
    html.Div(id="prediction-output", style={'display': 'none'})
])


def page_entry1():
    return html1


def page_entry2():
    return html2


def page_entry3():
    return html3


def page_entry4():
    return html4


def page_entry5():
    return html5


@app.callback(
    Output('page-content', 'children'),
    [Input('page-1-link', 'n_clicks'),
     Input('page-2-link', 'n_clicks'),
     Input('page-3-link', 'n_clicks'),
     Input('page-4-link', 'n_clicks'),
     Input('page-5-link', 'n_clicks'),]
)
def display_page(page_1_clicks, page_2_clicks, page_3_clicks, page_4_clicks, page_5_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html1  # Default page1

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "page-1-link":
        return page_entry1()
    elif button_id == "page-2-link":
        return page_entry2()
    elif button_id == "page-3-link":
        return page_entry3()
    elif button_id == "page-4-link":
        return page_entry4()
    elif button_id == "page-5-link":
        return page_entry5()


@app.callback(
    Output('category-dropdown', 'options'),
    Input('interval-component', 'n_intervals')  # 每次间隔触发更新
)
def update_dropdown_options(n_intervals):
    # 获取最新的产品类别并返回给 Dropdown 的 options
    categories = inv.view_products_by_category()
    return [{'label': c, 'value': c} for c in categories.keys()]


@app.callback(
    Output('product-list', 'children'),
    [Input('category-dropdown', 'value')]
)
def display_products(category):
    if category:
        return inv.view_products_sorted_by_stock(category)
    return "Select a category to view products."


@app.callback(
    [Output('product-id-2', 'value'),
     Output('product-name-2', 'value')],
    [Input('product-id-2', 'value'),
     Input('product-name-2', 'value')],
)
def auto_fill_product_fields(product_id, product_name):
    products = inv.read_json(inv.PRODUCTS_FILE)

    # input product_id，automatically find product_name
    if product_id:
        if product_id in products:
            return product_id, products[product_id]['name']
        else:
            return product_id, ''

    # input product_name，automatically find product_id
    elif product_name:
        for p_id, details in products.items():
            if details['name'].lower() == product_name.lower():
                return p_id, product_name
        return '', product_name

    return '', ''


@app.callback(
    Output('update-product-status', 'children'),
    [Input('submit-btn-product', 'n_clicks')],
    [Input('product-id-1', 'value'),
     Input('product-name-1', 'value'),
     Input('category-1', 'value'),
     Input('operation-type-1', 'value'),
     Input('user-1', 'value')]
)
def update_product(n_clicks, product_id, product_name, category, operation_type, user):
    if n_clicks:
        if operation_type == "add":
            return inv.add_product(product_id, product_name, category, user)
        elif operation_type == "delete":
            return inv.delete_product(product_id, user)
    return ""


@app.callback(
    Output('update-stock-status', 'children'),
    [Input('submit-btn-stock', 'n_clicks')],
    [Input('product-id-2', 'value'),
     Input('product-name-2', 'value'),
     Input('quantity-2', 'value'),
     Input('operation-type-2', 'value'),
     Input('user-2', 'value')]
)
def update_stock(n_clicks, product_id, product_name, quantity, operation_type, user):
    if n_clicks:
        if not operation_type:
            return ""
        return inv.update_stock(product_id, product_name, quantity, operation_type, user)
    return ""


def combine_date_and_time(start_date, start_time):
    try:
        date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    except ValueError:
        return None

    try:
        time_obj = datetime.strptime(start_time, '%H:%M:%S').time()
    except ValueError:
        return None

    combined_datetime = datetime.combine(date_obj, time_obj)
    return combined_datetime.isoformat()


@app.callback(
    Output('update-transaction-status', 'children'),
    [Input('submit-btn-transaction', 'n_clicks')],
    [Input('product-id-3', 'value'),
     Input('user-3', 'value'),
     Input('start-date-3', 'value'),
     Input('start-time-3', 'value'),
     Input('end-date-3', 'value'),
     Input('end-time-3', 'value'),]
)
def query_transaction(n_clicks, product_id, user, start_date, start_time, end_date, end_time):
    if n_clicks:
        if start_time:
            start_time = combine_date_and_time(start_date, start_time)
        else:
            start_time = None
        if end_time:
            end_time = combine_date_and_time(end_date, end_time)
        else:
            end_time = None
        if not (product_id or user or start_time or end_time):
            return "Please select at least one filter."
        if start_time and end_time:
            if start_time >= end_time:
                return "Start time must be before end time."
        return inv.query_transactions(product_id, user, start_time, end_time)
    return ""


@app.callback(
    Output('sale-list', 'children'),
    [Input('submit-btn-sale', 'n_clicks')],
    [Input('category-4', 'value'),
     Input('start-date-4', 'value'),
     Input('start-time-4', 'value'),
     Input('end-date-4', 'value'),
     Input('end-time-4', 'value'),]
)
def sales_summary(n_clicks, category, start_date, start_time, end_date, end_time):
    if n_clicks:
        if start_time:
            start_time = combine_date_and_time(start_date, start_time)
        else:
            start_time = None
        if end_time:
            end_time = combine_date_and_time(end_date, end_time)
        else:
            end_time = None
        if start_time and end_time:
            if start_time > end_time:
                return "Start time must be before end time."
        return inv.sales_summary(start_time, end_time, category)
    return ""


@app.callback(
    Output('all-product-list', 'children'),
    [Input('refresh-1', 'n_intervals')]
)
def display_products(n_intervals):
    return inv.display_all_products()


@app.callback(
    Output('all-transaction-list', 'children'),
    [Input('refresh-2', 'n_intervals')]
)
def display_transactions(n_intervals):
    return inv.display_all_transactions()


if __name__ == '__main__':
    app.run_server(debug=True)
