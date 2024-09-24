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
    return sorted_products


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

    return filtered_transactions


# 6. Sales Summary
def print_summary(summary):
    output = []

    if not summary:
        output.append("No sales data available for the specified period.")
        return "\n".join(output)

    output.append("Sales Summary:")
    output.append("-" * 30)
    output.append(f"{'Product Name':<25} | {'Total Sold':<10}")
    output.append("-" * 30)

    for product_name, total_sold in summary.items():
        output.append(f"{product_name:<25} | {total_sold:<10}")

    output.append("-" * 30)
    output.append("End of Summary.")

    return "\n".join(output)

def sales_summary(start_time, end_time, category=None):
    transactions = read_json(TRANSACTIONS_FILE)
    if not transactions:
        return "No transaction records available."
    sales = [t for t in transactions if t['operation_type'] == "sale" and start_time <= t['timestamp'] <= end_time]

    if category:
        sales = [s for s in sales if read_json(PRODUCTS_FILE)[s['product_id']]['category'] == category]

    summary = {}
    for sale in sales:
        product_name = sale['product_name']
        summary[product_name] = summary.get(product_name, 0) + sale['quantity']

    return print_summary(summary)


# 7. Display all products
def display_all_products():
    products = read_json(PRODUCTS_FILE)  # 假设读取的产品信息是一个字典
    if not products:
        return "No product records available."

    sorted_products = {}

    for product_id, product_info in products.items():
        category = product_info['category']
        if category not in sorted_products:
            sorted_products[category] = []
        sorted_products[category].append(product_info)

    for category in sorted_products:
        sorted_products[category].sort(key=lambda x: x['stock'], reverse=True)

    output = []
    output.append("All Products Information:")
    output.append("-" * 40)

    for category, items in sorted(sorted_products.items()):
        output.append(f"Category: {category}")
        output.append("-" * 40)
        for item in items:
            output.append(f"ID: {item['id']}, Name: {item['name']}, Stock: {item['stock']}, User: {item['user']}")

        output.append("")

    return "\n".join(output)


# 8. Display all transactions
def display_all_transactions():
    transactions = read_json(TRANSACTIONS_FILE)

    if not transactions:
        return "No transaction records available."

    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'], reverse=True)

    output = []
    output.append("All Transactions Information:")
    output.append("-" * 40)

    for transaction in sorted_transactions:
        output.append(f"Product ID: {transaction['product_id']}, "
                      f"Product Name: {transaction['product_name']}, "
                      f"Operation Type: {transaction['operation_type']}, "
                      f"Operator: {transaction['operator']}, "
                      f"Timestamp: {transaction['timestamp']}, "
                      f"Quantity: {transaction['quantity']}")

    return "\n".join(output)