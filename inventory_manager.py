import os
import json
from datetime import datetime
from collections import OrderedDict
from dash import html

DATA_DIR = 'data'
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')


# Utility to read/write JSON files
def read_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


# 1. View Products by Category
def view_products_by_category():
    products = read_json(PRODUCTS_FILE)
    categorized_products = {}
    for product_id, details in products.items():
        category = details.get('category')
        if category not in categorized_products:
            categorized_products[category] = []
        categorized_products[category].append(details)
    return categorized_products


# 2. Stock Management (Purchase and Sale)
def update_stock(product_id, product_name, quantity, operation_type, user):
    products = read_json(PRODUCTS_FILE)
    transactions = read_json(TRANSACTIONS_FILE)

    if not (product_id and product_name and quantity and operation_type and user):
        return "Please input more information."

    if product_id not in products:
        return "New product! Please operate product category first."

    if operation_type == "sale" and products[product_id]['stock'] < quantity:
        return "Insufficient stock."

    # Update stock
    if operation_type == "purchase":
        products[product_id]['stock'] += quantity
    elif operation_type == "sale":
        products[product_id]['stock'] -= quantity

    # Record transaction
    transaction = {
        "product_id": product_id,
        "product_name": product_name,
        "operation_type": operation_type,
        "operator": user,
        "timestamp": datetime.now().isoformat(),
        "quantity": quantity
    }
    if not transactions:
        transactions = [transaction]
    else:
        transactions.append(transaction)

    write_json(PRODUCTS_FILE, products)
    write_json(TRANSACTIONS_FILE, transactions)
    return "Stock updated successfully."


# 3. Add or Delete Product (Retain transaction history)
def add_product(product_id, product_name, category, user):
    if not (product_id and product_name and category):
        return "Please input more information."
    products = read_json(PRODUCTS_FILE)
    if product_id in products:
        products[product_id]['name'] = product_name
        write_json(PRODUCTS_FILE, products)
        return "Product information changed successfully."
    products[product_id] = {
        'id': product_id,
        'name': product_name,
        'stock': 0,
        'category': category,
        'user': user
    }
    write_json(PRODUCTS_FILE, products)
    return "Product added successfully."


def delete_product(product_id, user):
    if not product_id:
        return "Please input more product ID."
    products = read_json(PRODUCTS_FILE)
    if product_id in products:
        del products[product_id]
        write_json(PRODUCTS_FILE, products)
        return "Product deleted successfully."
    return "Product not found."


# 4. View Category Products by Stock (Sorted)
def view_products_sorted_by_stock(category):
    products = read_json(PRODUCTS_FILE)
    category_products = [p for p in products.values() if p['category'] == category]

    sorted_products = sorted(category_products, key=lambda x: x['stock'], reverse=True)
    if not sorted_products:
        return html.P(f"No products available in the '{category}' category.")

    # table header
    table_header = html.Thead(html.Tr([
        html.Th("Product ID"),
        html.Th("Product Name"),
        html.Th("Stock"),
        html.Th("Category"),
        html.Th("User")
    ]))

    # table body
    table_body = html.Tbody([
        html.Tr([
            html.Td(product['id']),
            html.Td(product['name']),
            html.Td(product['stock']),
            html.Td(product['category']),
            html.Td(product['user'])
        ]) for product in sorted_products
    ])

    return html.Table([table_header, table_body],
                      style={'width': '100%', 'border': '1px solid black', 'border-collapse': 'collapse'})


# 5. Query Transaction Records
def query_transactions(product_id=None, user=None, start_time=None, end_time=None):
    transactions = read_json(TRANSACTIONS_FILE)
    filtered_transactions = transactions

    if product_id:
        filtered_transactions = [t for t in filtered_transactions if t['product_id'] == product_id]
    if user:
        filtered_transactions = [t for t in filtered_transactions if t['operator'] == user]
    if start_time:
        filtered_transactions = [t for t in filtered_transactions if start_time <= t['timestamp']]
    if end_time:
        filtered_transactions = [t for t in filtered_transactions if t['timestamp'] <= end_time]

    if not filtered_transactions:
        return html.P("No transactions match the criteria.")

    # Build the table header
    table_header = html.Thead(html.Tr([
        html.Th("Product ID"),
        html.Th("Product Name"),
        html.Th("Operation Type"),
        html.Th("Operator"),
        html.Th("Timestamp"),
        html.Th("Quantity")
    ]))

    # Build the table body by iterating over filtered transactions
    table_body = html.Tbody([
        html.Tr([
            html.Td(transaction['product_id']),
            html.Td(transaction['product_name']),
            html.Td(transaction['operation_type']),
            html.Td(transaction['operator']),
            html.Td(transaction['timestamp']),
            html.Td(transaction['quantity'])
        ]) for transaction in filtered_transactions
    ])

    return html.Table([table_header, table_body],
                      style={'width': '100%', 'border': '1px solid black', 'border-collapse': 'collapse'})


# 6. Sales Summary
def sales_summary(start_time, end_time, category=None):
    transactions = read_json(TRANSACTIONS_FILE)
    sales = [t for t in transactions if t['operation_type'] == "sale"]

    if not sales:
        return html.P("No transaction records available.")

    # time filter
    if start_time:
        sales = [t for t in sales if start_time <= t['timestamp']]
    if end_time:
        sales = [t for t in sales if t['timestamp'] <= end_time]

    # category filter
    if category:
        products = read_json(PRODUCTS_FILE)
        sales = [s for s in sales if products[s['product_id']]['category'] == category]

    summary = {}
    for sale in sales:
        product_name = sale['product_name']
        summary[product_name] = summary.get(product_name, 0) + sale['quantity']

    if not summary:
        return html.P("No sales records available for the specified period.")
    summary = OrderedDict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

    # table header
    table_header = html.Thead(html.Tr([
        html.Th("Product Name"),
        html.Th("Total Quantity Sold")
    ]))

    # table body
    table_body = html.Tbody([
        html.Tr([
            html.Td(product_name),
            html.Td(quantity)
        ]) for product_name, quantity in summary.items()
    ])

    return html.Table([table_header, table_body], style={'width': '50%', 'border': '1px solid black', 'border-collapse': 'collapse'})


# 7. Display all products
def display_all_products():
    products = read_json(PRODUCTS_FILE)
    if not products:
        return html.P("No product records available.")

    sorted_products = {}

    # categorize the product
    for product_id, product_info in products.items():
        category = product_info['category']
        if category not in sorted_products:
            sorted_products[category] = []
        sorted_products[category].append(product_info)

    # sort down by stock
    for category in sorted_products:
        sorted_products[category].sort(key=lambda x: x['stock'], reverse=True)

    tables = []

    # particular form for each category
    for category, items in sorted(sorted_products.items()):
        # table header
        table_header = html.Thead(html.Tr([
            html.Th("ID"),
            html.Th("Name"),
            html.Th("Stock"),
            html.Th("User")
        ]))

        # table body
        table_body = html.Tbody([
            html.Tr([
                html.Td(item['id']),
                html.Td(item['name']),
                html.Td(item['stock']),
                html.Td(item['user'])
            ]) for item in items
        ])

        tables.append(html.H3(f"Category: {category}"))
        tables.append(html.Table(
            [table_header, table_body],
            style={'width': '100%', 'border': '1px solid black', 'border-collapse': 'collapse', 'margin-bottom': '20px'}
        ))

    return html.Div(tables)


# 8. Display all transactions
def display_all_transactions():
    transactions = read_json(TRANSACTIONS_FILE)

    if not transactions:
        return html.P("No transaction records available.")

    # sort by timestamp
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'], reverse=True)

    # table header
    table_header = [
        html.Thead(html.Tr([
            html.Th("Product ID"),
            html.Th("Product Name"),
            html.Th("Operation Type"),
            html.Th("Operator"),
            html.Th("Timestamp"),
            html.Th("Quantity")
        ]))
    ]

    # table body
    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(transaction['product_id']),
                html.Td(transaction['product_name']),
                html.Td(transaction['operation_type']),
                html.Td(transaction['operator']),
                html.Td(transaction['timestamp']),
                html.Td(transaction['quantity'])
            ]) for transaction in sorted_transactions
        ])
    ]

    return html.Table(table_header + table_body, style={'width': '100%', 'border': '1px solid black', 'border-collapse': 'collapse'})