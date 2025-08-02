import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

class AIModels:
    def __init__(self):
        self.price_model = None
    
    @st.cache_resource
    def _load_price_model(_self, data):
        """Train and cache price prediction model"""
        X = data[['rating', 'sales', 'category_id']]
        y = data['price']
        model = RandomForestRegressor(n_estimators=50)  # Fewer trees for faster training
        model.fit(X, y)
        return model
    
    def train_price_model(self, data):
        """Train model (cached)"""
        self.price_model = self._load_price_model(data)
    
    def predict_price(self, product_data):
        """Predict optimal price"""
        if not self.price_model:
            return product_data['price'] * 1.1  # Fallback if model not trained
            
        features = np.array([
            [
                product_data['rating'], 
                product_data['sales'], 
                product_data['category_id']
            ]
        ])
        return self.price_model.predict(features)[0]
    
    @st.cache_data(max_entries=100, ttl=300)
    def generate_ad_copy(_self, product_name, keywords):
        """Generate ad copy without heavy AI"""
        templates = [
            f"🔥 HOT DEAL! {product_name} - Best {keywords} on Daraz! Free Shipping!",
            f"Amazing {product_name} - Perfect for {keywords}. Buy now and save!",
            f"Special offer: {product_name} - Top quality {keywords} at lowest prices!"
        ]
        return np.random.choice(templates)
        def forecast_sales(historical_sales, months=3):
    """Simple linear regression forecast"""
    # For demo purposes - replace with real forecasting model
    last_sales = historical_sales[-1]
    return [last_sales * (1 + i * 0.1) for i in range(1, months+1)]