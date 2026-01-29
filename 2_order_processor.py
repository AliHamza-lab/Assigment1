# Assignment 2: Order Processing with God Function
# Issues: Single function doing validation, pricing, shipping, payment, inventory, and persistence
# Goal: Extract smaller functions with single responsibilities

from fastapi import FastAPI, HTTPException

app = FastAPI()

orders_db = {}
inventory = {"apple": 100, "banana": 50, "orange": 75}


@app.post("/order")
def process_order(user_id: str, item: str, quantity: int, payment_method: str, shipping_type: str):
    # Validate user
    if not user_id or len(user_id) < 5:
        raise HTTPException(400, "Invalid user")

    # Check inventory
    if item not in inventory:
        raise HTTPException(400, "Item not found")
    if inventory[item] < quantity:
        raise HTTPException(400, "Not enough stock")

    # Calculate price
    prices = {"apple": 1.0, "banana": 0.5, "orange": 0.75}
    subtotal = prices[item] * quantity
    if quantity > 10:
        subtotal = subtotal * 0.9
    if quantity > 50:
        subtotal = subtotal * 0.85

    # Add shipping
    if shipping_type == "express":
        shipping = 15.0
    elif shipping_type == "standard":
        shipping = 5.0
    elif shipping_type == "free":
        if subtotal > 50:
            shipping = 0
        else:
            shipping = 5.0
    else:
        shipping = 5.0

    # Process payment
    if payment_method == "credit":
        fee = subtotal * 0.03
    elif payment_method == "debit":
        fee = 1.0
    elif payment_method == "cash":
        fee = 0
    else:
        raise HTTPException(400, "Invalid payment")

    total = subtotal + shipping + fee

    # Update inventory
    inventory[item] -= quantity

    # Save order
    order_id = f"ORD-{len(orders_db) + 1}"
    orders_db[order_id] = {"user": user_id, "item": item, "total": total}

    return {"order_id": order_id, "total": total}
