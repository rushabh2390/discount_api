class Data:
    unused_discount = []
    used_discount = []
    users = {"admin@example.com": {
        "username": "Admin",
        "password": "$2b$12$xBKj2hTLP.1Adci6ujCtzeeOazCg5gSZUKQtoBo06AESD4E0jf.H.",  # admin
        "fullname": "Administrator",
        "email": "admin@example.com",
        "date_of_birth": "2000-03-02",
        "is_admin_user": True,
        "is_staff_user": True
    }}
    items = [
        {"id": 1, "name": "Laptop", "category": "Electronics",
            "price": 1200.00, "inventory": 10},
        {"id": 2, "name": "Smartphone", "category": "Electronics",
            "price": 800.00, "inventory": 25},
        {"id": 3, "name": "Headphones", "category": "Electronics",
            "price": 150.00, "inventory": 50},
        {"id": 4, "name": "T-Shirt", "category": "Clothing",
            "price": 25.00, "inventory": 100},
        {"id": 5, "name": "Jeans", "category": "Clothing",
            "price": 60.00, "inventory": 75},
        {"id": 6, "name": "Running Shoes", "category": "Clothing",
            "price": 90.00, "inventory": 60},
        {"id": 7, "name": "Cookbook", "category": "Books",
            "price": 30.00, "inventory": 30},
        {"id": 8, "name": "Novel", "category": "Books",
            "price": 15.00, "inventory": 80},
        {"id": 9, "name": "Textbook", "category": "Books",
            "price": 50.00, "inventory": 20},
        {"id": 10, "name": "Coffee Maker", "category": "Appliances",
            "price": 75.00, "inventory": 40},
        {"id": 11, "name": "Toaster", "category": "Appliances",
            "price": 40.00, "inventory": 90},
        {"id": 12, "name": "Blender", "category": "Appliances",
            "price": 65.00, "inventory": 55},
        {"id": 13, "name": "Gaming Mouse", "category": "Electronics",
            "price": 50.00, "inventory": 70},
        {"id": 14, "name": "Keyboard", "category": "Electronics",
            "price": 80.00, "inventory": 45},
        {"id": 15, "name": "Monitor", "category": "Electronics",
            "price": 250.00, "inventory": 35},
        {"id": 16, "name": "Dress", "category": "Clothing",
            "price": 85.00, "inventory": 50},
        {"id": 17, "name": "Socks", "category": "Clothing",
            "price": 10.00, "inventory": 200},
        {"id": 18, "name": "Gardening Tools Set",
            "category": "Home & Garden", "price": 120.00, "inventory": 20},
        {"id": 19, "name": "Desk Lamp", "category": "Home & Garden",
            "price": 35.00, "inventory": 65},
        {"id": 20, "name": "Pillows", "category": "Home & Garden",
            "price": 45.00, "inventory": 80}
    ]
    orders = []
    payments = []
    max_id = 21

data = Data()
