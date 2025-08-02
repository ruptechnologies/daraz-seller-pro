import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
DARAZ_API_BASE_URL = "https://api.daraz.com"
DARAZ_API_KEY = os.getenv("DARAZ_API_KEY")
DARAZ_USER_ID = os.getenv("DARAZ_USER_ID")
class DarazAPI:
    def __init__(self):
        self.base_url = DARAZ_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {DARAZ_API_KEY}",
            "Content-Type": "application/json"
        }
    def get_product_details(self, product_id):
        """Get product details by product ID"""
        endpoint = f"/product/get?product_id={product_id}&user_id={DARAZ_USER_ID}"
        response = requests.get(self.base_url + endpoint, headers=self.headers)
        return response.json()
    def search_products(self, keyword, category_id=None, page=1, page_size=10):
        """Search products by keyword and optional category"""
        endpoint = f"/product/search?keyword={keyword}&page={page}&page_size={page_size}"
        if category_id:
            endpoint += f"&category_id={category_id}"
        response = requests.get(self.base_url + endpoint, headers=self.headers)
        return response.json()
daraz_api = DarazAPI()
@app.route('/api/search', methods=['GET'])
def search_products():
    keyword = request.args.get('keyword')
    category_id = request.args.get('category_id')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    results = daraz_api.search_products(keyword, category_id, page, page_size)
    return jsonify(results)
@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product_details = daraz_api.get_product_details(product_id)
    return jsonify(product_details)
if __name__ == '__main__':
    app.run(debug=True, port=5001)