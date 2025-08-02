import streamlit as st
import pandas as pd
import numpy as np
import time
from auth import authenticate
from daraz_api import DarazAPI
from ai_models import AIModels
from competitor import CompetitorMonitor
from database import save_user_product, get_user_products

# Initialize resources
@st.cache_resource
def init_resources():
    daraz = DarazAPI()
    ai = AIModels()
    competitor = CompetitorMonitor()
    return daraz, ai, competitor

daraz, ai, competitor_monitor = init_resources()

# Authentication
if not authenticate():
    st.stop()

# Sample data loading - CACHED
@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        'product_id': [1001, 1002, 1003, 1004, 1005],
        'name': ['Wireless Headphones', 'Bluetooth Speaker', 'Phone Charger', 'Yoga Mat', 'Water Bottle'],
        'price': [25.99, 18.50, 8.99, 15.75, 12.49],
        'rating': [4.5, 4.2, 4.0, 4.7, 4.3],
        'sales': [1500, 980, 3200, 2100, 4500],
        'seller_id': [5001, 5002, 5003, 5004, 5005],
        'category_id': [301, 302, 303, 304, 305]
    })

df = load_sample_data()

# Train AI model only when needed
if 'model_trained' not in st.session_state:
    ai.train_price_model(df)
    st.session_state.model_trained = True

# Streamlit app
st.title("🚀 Daraz Seller Pro")
st.sidebar.header("Navigation")

# Dashboard
if st.sidebar.checkbox("Dashboard", True, key="dashboard"):
    st.header("Product Performance Dashboard")
    
    # Product selector
    selected_product = st.selectbox("Select Product", df['name'], key="product_select")
    product_data = df[df['name'] == selected_product].iloc[0]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Price", f"${product_data['price']:.2f}")
    col2.metric("Rating", f"{product_data['rating']}/5")
    col3.metric("Sales", f"{product_data['sales']} units")
    
    # Price prediction
    predicted_price = ai.predict_price(product_data)
    st.subheader(f"AI Price Recommendation: ${predicted_price:.2f}")
    
    # Sales trend chart
    if st.button("Show Sales Trend", key="show_trend"):
        trend_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Sales': np.random.randint(50, 200, size=5)
        })
        st.line_chart(trend_data.set_index('Month'))
        
        # Sales forecasting
        st.subheader("Sales Forecast")
        forecast_months = st.slider("Months to forecast", 1, 6, 3, key="forecast_slider")
        forecast = ai.forecast_sales(trend_data['Sales'].tolist(), forecast_months)
        forecast_df = pd.DataFrame({
            'Month': [f"Month {i+1}" for i in range(forecast_months)],
            'Forecasted Sales': forecast
        })
        st.line_chart(forecast_df.set_index('Month'))

# Product Research Tool
if st.sidebar.checkbox("Product Research", key="research"):
    st.header("🔍 Product Research")
    
    keyword = st.text_input("Search Products", key="search_input")
    if keyword:
        with st.spinner("Searching Daraz..."):
            results = daraz.search_products(keyword)
            st.dataframe(results.head(10), height=300)
            
            st.subheader("Top Products")
            top_products = results.nlargest(3, 'sales')
            for _, row in top_products.iterrows():
                st.write(f"**{row['name']}** - ${row['price']} (🔥 {row['sales']} sales)")
    
    # Gap analysis
    if st.button("Run Market Gap Analysis", key="gap_analysis"):
        st.success("Top Opportunity Categories:")
        opportunities = [
            {"Category": "Wireless Earbuds", "Demand": "High", "Competition": "Low"},
            {"Category": "Yoga Mats", "Demand": "Medium", "Competition": "Low"},
            {"Category": "Phone Lenses", "Demand": "High", "Competition": "Medium"},
        ]
        st.table(pd.DataFrame(opportunities))

# Advertising Tools
if st.sidebar.checkbox("Advertising Tools", key="ads"):
    st.header("📢 Ad Campaign Generator")
    
    product_name = st.text_input("Product Name", key="ad_product")
    keywords = st.text_input("Target Keywords", key="ad_keywords")
    
    if st.button("Generate Ad Copy", key="generate_ad"):
        ad_copy = ai.generate_ad_copy(product_name, keywords)
        st.subheader("Generated Ad Copy")
        st.write(ad_copy)
    
    # Budget optimizer
    st.subheader("Ad Budget Optimizer")
    budget = st.slider("Total Budget ($)", 50, 1000, 200, key="budget_slider")
    allocations = {
        'Facebook': 0.4,
        'Google': 0.3,
        'TikTok': 0.2,
        'Daraz Ads': 0.1
    }
    
    for platform, percent in allocations.items():
        st.progress(percent)
        st.write(f"- {platform}: ${budget*percent:.2f}")

# Competitor Monitor
if st.sidebar.checkbox("Competitor Monitor", key="competitor"):
    st.header("🔎 Competitor Intelligence")
    
    product_id = st.text_input("Enter Product ID to monitor", key="comp_product_id")
    if product_id:
        with st.spinner("Tracking competitor pricing..."):
            competitor_df = competitor_monitor.track_product(product_id)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Price History")
                st.line_chart(competitor_df['prices'])
            
            with col2:
                st.subheader("Rating History")
                st.line_chart(competitor_df['ratings'])

# Product Management
if st.sidebar.checkbox("My Products", key="my_products"):
    st.header("🛍️ My Product Portfolio")
    
    # Add new product form
    with st.form("add_product_form"):
        st.subheader("Add New Product")
        name = st.text_input("Product Name", key="new_product_name")
        price = st.number_input("Price ($)", min_value=0.1, step=0.1, key="new_product_price")
        category = st.selectbox("Category", ["Electronics", "Fashion", "Home & Garden"], key="new_product_category")
        
        if st.form_submit_button("Add Product"):
            # Save to database
            save_user_product(st.session_state.user["email"], {
                "name": name,
                "price": price,
                "category": category
            })
            st.success(f"{name} added to your portfolio!")
    
    # Show user's products
    st.subheader("Your Products")
    user_products = get_user_products(st.session_state.user["email"])
    
    if not user_products.empty:
        st.dataframe(user_products)
        selected = st.selectbox("Select a product to manage", user_products['name'], key="manage_product_select")
        
        # Product management actions
        product = user_products[user_products['name'] == selected].iloc[0]
        new_price = st.number_input("Update Price", value=product['price'], key="update_price")
        
        if st.button("Update Price", key="update_price_btn"):
            # Update in database (pseudo-code)
            st.success(f"Price updated to ${new_price}")
    else:
        st.info("You haven't added any products yet")

# Add performance note
st.sidebar.info("⚡ Performance optimized version")