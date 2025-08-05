# -------------------------------------------------
# SnackyBites Survey API - 19 Fields Data Generator
# -------------------------------------------------

from fastapi import FastAPI
from faker import Faker
import random
import uuid
import pandas as pd
from fastapi.responses import FileResponse

# Create FastAPI app
app = FastAPI()

# Initialize Faker
fake = Faker()

# Define possible values
brands = ["SnackyBites", "BurgerLounge", "WrapKing", "FryHouse", "TacoTown"]
product_categories = ["Burger", "Fries", "Wrap", "Drink", "Dessert"]
products = {
    "Burger": ["Cheesy Burger", "Double Patty Burger", "Veggie Delight Burger"],
    "Fries": ["Classic Fries", "Chili Fries", "Curly Fries"],
    "Wrap": ["Chicken Wrap", "Paneer Wrap", "Veggie Wrap"],
    "Drink": ["Cola Blast", "Orange Fizz", "Iced Tea"],
    "Dessert": ["Chocolate Muffin", "Cheesecake Slice", "Ice Cream Cup"]
}
sentiments = ["positive", "negative", "neutral"]
channels = ["Mobile App", "Website", "In-store", "Delivery Partner"]
payment_methods = ["Cash", "Card", "Digital Wallet"]
age_groups = ["18-25", "26-40", "41-60", "60+"]
loyalty_tiers = ["Bronze", "Silver", "Gold", "Platinum"]

# ✅ Root Route
@app.get("/")
def home():
    return {"message": "SnackyBites Survey API is running! Use /get_feedback?n=10 to get data."}

# ✅ Generate fake feedback data
@app.get("/get_feedback")
def get_feedback(n: int = 10, brand: str = None):
    """
    Generates 'n' rows of fake consumer feedback data with 19 fields.
    Optionally filter data by brand using query parameter: /get_feedback?n=5&brand=SnackyBites
    """
    data = []
    for _ in range(n):
        category = random.choice(product_categories)
        feedback = {
            "user_id": str(uuid.uuid4()),  # unique user
            "feedback_id": str(uuid.uuid4()),  # unique feedback
            "brand": brand if brand else random.choice(brands),
            "product_category": category,
            "product_name": random.choice(products[category]),
            "feedback": fake.sentence(nb_words=12),
            "sentiment": random.choice(sentiments),
            "rating": random.randint(1, 5),
            "purchase_amount": round(random.uniform(5.0, 50.0), 2),
            "purchase_date": fake.date_this_year().isoformat(),
            "timestamp": fake.date_time_this_year().isoformat(),
            "location_city": fake.city(),
            "location_state": fake.state(),
            "channel": random.choice(channels),
            "payment_method": random.choice(payment_methods),
            "age_group": random.choice(age_groups),
            "customer_loyalty": random.choice(loyalty_tiers),
            "repeat_customer": random.choice(["Yes", "No"]),
            "delivery_time_minutes": random.randint(10, 60)
        }
        data.append(feedback)
    return {"data": data}

# ✅ Export feedback to CSV
@app.get("/export_feedback")
def export_feedback(rows: int = 100):
    """
    Generates 'rows' number of fake feedback data and exports to a CSV file.
    Access via: /export_feedback?rows=500
    """
    data = [get_feedback(1)["data"][0] for _ in range(rows)]
    df = pd.DataFrame(data)
    file_path = "feedback_data.csv"
    df.to_csv(file_path, index=False)
    return FileResponse(file_path, media_type='text/csv', filename="feedback_data.csv")
