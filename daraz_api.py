import pandas as pd
import random

class DarazAPI:
    def __init__(self):
        self.product_cache = {}
    
    def get_product_data(self, product_id):
        """Return cached or mock product data"""
        if product_id not in self.product_cache:
            self.product_cache[product_id] = self._generate_mock_product(product_id)
        return self.product_cache[product_id]
    
    def search_products(self, keyword, category_id=None, page=1, page_size=10):
        """Return mock search results - FAST version"""
        num_results = page_size
        return pd.DataFrame([self._generate_mock_product(i, keyword) for i in range(num_results)])
    
    def _generate_mock_product(self, idx, keyword="Product"):
        return {
            'product_id': 1000 + idx,
            'name': f"{keyword.capitalize()} {idx+1}",
            'price': round(random.uniform(5.0, 100.0), 2),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'sales': random.randint(100, 5000),
            'seller_id': random.randint(5000, 6000),
            'category_id': random.randint(100, 500)
        }