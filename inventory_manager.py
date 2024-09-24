import json
import os
from datetime import datetime

DATA_DIR = 'data'
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')


# Utility to read/write JSON files
def read_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, 'w') as file:
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
def update_stock(product_id, quantity, operation_type, user):
    products = read_json(PRODUCTS_FILE)
    transactions = read_json(TRANSACTIONS_FILE)

    if product_id not in products:
        return "Product not found."

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
        "product_name": products[product_id]['name'],
        "operation_type": operation_type,
        "operator": user,
        "timestamp": datetime.now().isoformat(),
        "quantity": quantity
    }
    transactions.append(transaction)

    write_json(PRODUCTS_FILE, products)
    write_json(TRANSACTIONS_FILE, transactions)
    return "Stock updated successfully."


# 3. Delete Product (Retain transaction history)
def delete_product(product_id):
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
    return sorted_products


# 5. Query Transaction Records
def query_transactions(product_id=None, operator=None, start_time=None, end_time=None):
    transactions = read_json(TRANSACTIONS_FILE)
    filtered_transactions = transactions

    if product_id:
        filtered_transactions = [t for t in filtered_transactions if t['product_id'] == product_id]
    if operator:
        filtered_transactions = [t for t in filtered_transactions if t['operator'] == operator]
    if start_time and end_time:
        filtered_transactions = [t for t in filtered_transactions if start_time <= t['timestamp'] <= end_time]

    return filtered_transactions


# 6. Sales Summary
def sales_summary(start_time, end_time, category=None):
    transactions = read_json(TRANSACTIONS_FILE)
    sales = [t for t in transactions if t['operation_type'] == "sale" and start_time <= t['timestamp'] <= end_time]

    if category:
        sales = [s for s in sales if read_json(PRODUCTS_FILE)[s['product_id']]['category'] == category]

    summary = {}
    for sale in sales:
        product_name = sale['product_name']
        summary[product_name] = summary.get(product_name, 0) + sale['quantity']

    return summary
