import pandas as pd
import random
import time

class CompetitorMonitor:
    def __init__(self):
        self.competitor_data = {}
    
    def track_product(self, product_id):
        if product_id not in self.competitor_data:
            # Initialize with mock data
            self.competitor_data[product_id] = {
                'prices': [random.uniform(20, 30)],
                'ratings': [random.uniform(4.0, 4.8)],
                'update_times': [time.time()]
            }
        else:
            # Simulate price changes
            last_price = self.competitor_data[product_id]['prices'][-1]
            new_price = last_price * random.uniform(0.95, 1.05)
            self.competitor_data[product_id]['prices'].append(new_price)
            self.competitor_data[product_id]['ratings'].append(
                max(3.0, min(5.0, self.competitor_data[product_id]['ratings'][-1] + random.uniform(-0.1, 0.1)))
            self.competitor_data[product_id]['update_times'].append(time.time())
        
        return pd.DataFrame(self.competitor_data[product_id])