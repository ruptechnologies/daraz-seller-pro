import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Performance tracking
start_time = datetime.now()

# Initialize session state
def init_session_state():
    if 'resources_initialized' not in st.session_state:
        st.session_state.resources_initialized = False
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

# Initialize resources only when needed
def init_resources():
    if not st.session_state.resources_initialized:
        # Simulate resource initialization
        time.sleep(0.5)
        
        # Create mock data
        st.session_state.df = pd.DataFrame({
            'product_id': [1001, 1002, 1003, 1004, 1005],
            'name': ['Wireless Headphones', 'Bluetooth Speaker', 'Phone Charger', 'Yoga Mat', 'Water Bottle'],
            'price': [25.99, 18.50, 8.99, 15.75, 12.49],
            'rating': [4.5, 4.2, 4.0, 4.7, 4.3],
            'sales': [1500, 980, 3200, 2100, 4500],
            'category_id': [301, 302, 303, 304, 305]
        })
        
        # Simple AI model
        class SimpleAI:
            def predict_price(self, product_data):
                # Simple price prediction: average of similar products
                similar = st.session_state.df[
                    (st.session_state.df['category_id'] == product_data['category_id']) &
                    (st.session_state.df['product_id'] != product_data['product_id'])
                ]
                if not similar.empty:
                    return similar['price'].mean() * 0.95
                return product_data['price'] * 1.1
            
            def generate_ad_copy(self, product_name, keywords):
                # Simple ad generation without heavy AI
                templates = [
                    f"🔥 HOT DEAL! {product_name} - Best {keywords} on Daraz!",
                    f"Amazing {product_name} - Perfect for {keywords}. Buy now!",
                    f"Special offer: {product_name} - Top quality {keywords}!"
                ]
                return np.random.choice(templates)
        
        st.session_state.ai = SimpleAI()
        st.session_state.resources_initialized = True

# Simplified authentication
def authenticate():
    if not st.session_state.user_authenticated:
        st.title("🚀 Daraz Seller Pro Login")
        
        with st.form("login_form"):
            email = st.text_input("Email", value="seller@example.com")
            password = st.text_input("Password", type="password", value="password")
            
            if st.form_submit_button("Login"):
                st.session_state.user_authenticated = True
                st.rerun()
        st.stop()
    return True

# Dashboard Page - Optimized
def show_dashboard():
    if "dashboard_loaded" not in st.session_state:
        st.session_state.dashboard_loaded = False
    
    st.header("📊 Product Performance Dashboard")
    
    # Product selector
    if not st.session_state.dashboard_loaded:
        selected_product = st.selectbox("Select Product", st.session_state.df['name'])
        st.session_state.selected_product = selected_product
    else:
        selected_product = st.session_state.selected_product
    
    product_data = st.session_state.df[st.session_state.df['name'] == selected_product].iloc[0]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Price", f"${product_data['price']:.2f}")
    col2.metric("Rating", f"{product_data['rating']}/5")
    col3.metric("Sales", f"{product_data['sales']} units")
    
    # Price prediction
    if st.button("Get Price Recommendation", key="price_rec"):
        predicted_price = st.session_state.ai.predict_price(product_data)
        st.subheader(f"💡 AI Price Recommendation: ${predicted_price:.2f}")
    
    # Sales trend - load only when requested
    if st.checkbox("Show Sales Trend", key="show_trend"):
        st.subheader("📈 Sales Trend")
        trend_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Sales': [120, 145, 98, 167, 210]
        })
        st.line_chart(trend_data.set_index('Month'))
    
    st.session_state.dashboard_loaded = True

# Product Research Page - Optimized
def show_research():
    st.header("🔍 Product Research")
    
    keyword = st.text_input("Search Products", key="search_input")
    
    if keyword:
        # Simulate fast search
        time.sleep(0.2)
        
        # Generate mock results
        num_results = 10
        products = []
        for i in range(num_results):
            products.append({
                'product_id': 1000 + i,
                'name': f"{keyword} Product {i+1}",
                'price': round(np.random.uniform(5.0, 100.0), 2),
                'rating': round(np.random.uniform(3.5, 5.0), 1),
                'sales': np.random.randint(100, 5000),
                'category_id': np.random.randint(100, 500)
            })
            
        results = pd.DataFrame(products)
        
        st.dataframe(results.head(5), height=200)
        
        # Show top products
        st.subheader("🏆 Top Products")
        top_products = results.nlargest(2, 'sales')
        for _, row in top_products.iterrows():
            st.write(f"**{row['name']}** - ${row['price']} (🔥 {row['sales']} sales)")
    
    # Gap analysis - load only when requested
    if st.button("Run Market Gap Analysis", key="gap_analysis"):
        st.subheader("💎 Market Opportunities")
        opportunities = [
            {"Category": "Wireless Earbuds", "Demand": "High", "Competition": "Low"},
            {"Category": "Yoga Mats", "Demand": "Medium", "Competition": "Low"},
        ]
        st.table(pd.DataFrame(opportunities))

# Advertising Tools - Optimized
def show_ads():
    st.header("📢 Ad Campaign Generator")
    
    product_name = st.text_input("Product Name", key="ad_product")
    keywords = st.text_input("Target Keywords", key="ad_keywords")
    
    if st.button("Generate Ad Copy", key="generate_ad"):
        if product_name and keywords:
            ad_copy = st.session_state.ai.generate_ad_copy(product_name, keywords)
            st.subheader("✨ Generated Ad Copy")
            st.success(ad_copy)
        else:
            st.warning("Please enter product name and keywords")
    
    # Budget optimizer
    st.subheader("💰 Ad Budget Optimizer")
    budget = st.slider("Total Budget ($)", 50, 1000, 200, key="budget_slider")
    
    allocations = {
        'Facebook': 0.4,
        'Google': 0.3,
        'TikTok': 0.2,
        'Daraz Ads': 0.1
    }
    
    st.write("Recommended Allocation:")
    for platform, percent in allocations.items():
        st.progress(percent)
        st.caption(f"{platform}: ${budget*percent:.2f}")

# Main App Structure
def main():
    st.set_page_config(
        page_title="Daraz Seller Pro",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    authenticate()
    init_resources()
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    pages = {
        "Dashboard": show_dashboard,
        "Product Research": show_research,
        "Advertising Tools": show_ads
    }
    
    for page_name in pages:
        if st.sidebar.button(page_name, key=f"btn_{page_name}"):
            st.session_state.current_page = page_name
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"⚡ Performance optimized")
    st.sidebar.caption(f"Loaded in {(datetime.now() - start_time).total_seconds():.2f}s")
    
    # Show current page
    st.title(f"🚀 Daraz Seller Pro - {st.session_state.current_page}")
    pages[st.session_state.current_page]()
    
    # Add minimal footer
    st.markdown("---")
    st.caption("Daraz Seller Pro v1.0 | Performance Optimized")

if __name__ == "__main__":
    main()