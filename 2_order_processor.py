from fastapi import FastAPI, HTTPException

app = FastAPI()

# Mock Databases
orders_db = {}
inventory = {"apple": 100, "banana": 50, "orange": 75}
PRICES = {"apple": 1.0, "banana": 0.5, "orange": 0.75}

# --- Helper Functions (Responsibilities) ---

def validate_user(user_id: str):
    if not user_id or len(user_id) < 5:
        raise HTTPException(400, "Invalid user")

def check_stock(item: str, quantity: int):
    if item not in inventory:
        raise HTTPException(400, "Item not found")
    if inventory[item] < quantity:
        raise HTTPException(400, "Not enough stock")

def calculate_subtotal(item: str, quantity: int) -> float:
    price = PRICES[item]
    subtotal = price * quantity
    # Applying discounts
    if quantity > 50:
        subtotal *= 0.85
    elif quantity > 10:
        subtotal *= 0.9
    return subtotal

def get_shipping_cost(shipping_type: str, subtotal: float) -> float:
    if shipping_type == "express":
        return 15.0
    if shipping_type == "free" and subtotal > 50:
        return 0.0
    return 5.0  # Default/Standard shipping

def get_payment_fee(payment_method: str, subtotal: float) -> float:
    fees = {"credit": subtotal * 0.03, "debit": 1.0, "cash": 0.0}
    if payment_method not in fees:
        raise HTTPException(400, "Invalid payment method")
    return fees[payment_method]

# --- Main API Route ---

@app.post("/order")
def process_order(user_id: str, item: str, quantity: int, payment_method: str, shipping_type: str):
    # 1. Validation & Inventory
    validate_user(user_id)
    check_stock(item, quantity)

    # 2. Financial Calculations
    subtotal = calculate_subtotal(item, quantity)
    shipping = get_shipping_cost(shipping_type, subtotal)
    fee = get_payment_fee(payment_method, subtotal)
    
    total = subtotal + shipping + fee

    # 3. State Changes (Inventory & DB)
    inventory[item] -= quantity
    order_id = f"ORD-{len(orders_db) + 1}"
    orders_db[order_id] = {"user": user_id, "item": item, "total": total}

    return {"order_id": order_id, "total": total}