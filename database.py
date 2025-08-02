import sqlite3
import pandas as pd
import streamlit as st

def init_db():
    conn = sqlite3.connect('daraz_data.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 price REAL,
                 rating REAL,
                 sales INTEGER,
                 category_id INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_products (
                 id INTEGER PRIMARY KEY,
                 user_email TEXT,
                 product_id INTEGER)''')
    
    conn.commit()
    return conn

def save_user_product(user_email, product_id):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO user_products (user_email, product_id) VALUES (?, ?)",
              (user_email, product_id))
    conn.commit()
    conn.close()

def get_user_products(user_email):
    conn = init_db()
    query = f'''
    SELECT p.* 
    FROM products p
    JOIN user_products up ON p.id = up.product_id
    WHERE up.user_email = '{user_email}'
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df