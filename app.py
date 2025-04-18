# app.py
from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os
import json

app = Flask(__name__)

# Load the features configuration from the JSON file if it exists
features_config_path = "features_config.json"

if os.path.exists(features_config_path):
    with open(features_config_path, "r", encoding="utf-8") as file:
        features_config = json.load(file)
else:
    features_config = {
        "features": [
            {"id": 0, "keywords": ["hello", "hi", "hey"], "response": "Hello! How can I help you today?"},
            {"id": 1, "keywords": ["delivery", "arrive"], "response": "Your product is on its way!"},
            {"id": 2, "keywords": ["recommend", "suggest"], "response": "Sure, here are some product recommendations."},
            {"id": 3, "keywords": ["product details", "info"], "response": "Please mention the product name."},
            {"id": 4, "keywords": ["cart", "add to cart", "remove from cart"], "response": "Cart management is enabled."},
            {"id": 5, "keywords": ["track", "order status", "where is my order"], "response": "Please provide your order ID."},
            {"id": 6, "keywords": ["payment", "checkout", "billing"], "response": "Need help with payment? I’m here!"},
            {"id": 7, "keywords": ["support", "help", "customer care"], "response": "Connecting you to customer support."},
            {
                "id": 8,
                "keywords": ["language", "speak"],
                "response": {
                    "en": "Hello! How can I assist you in English?",
                    "es": "¡Hola! ¿Cómo puedo ayudarte en español?",
                    "fr": "Bonjour! Comment puis-je vous aider en français?",
                    "hi": "नमस्ते! मैं आपकी किस प्रकार सहायता कर सकता हूँ?"
                }
            },
            {"id": 9, "keywords": ["ai", "chatgpt", "smart"], "response": "Let me think... 🤖"},
            {"id": 10, "keywords": ["platform", "device", "browser"], "response": "This bot works across all platforms!"},
            {"id": 11, "keywords": ["community", "group"], "response": "Join our WhatsApp community using this link!"}
        ]
    }

products = {
    "1": {"name": "Product A", "price": 100, "description": "High-quality product A"},
    "2": {"name": "Product B", "price": 200, "description": "Premium product B"},
}

orders = {
    "123": {"status": "Shipped", "tracking_id": "XYZ123"},
    "456": {"status": "Delivered", "tracking_id": "ABC456"},
}

def generate_ai_response(message):
    return f"AI Response: {message}"

@app.route("/")
def index():
    return render_template_string(open("templates/chat.html").read())

@app.route("/webhook", methods=["POST"])
def webhook():
    user_message = request.form.get("msg", "").lower()
    response = "Sorry, I didn't understand that. How can I assist you?"

    for feature in features_config["features"]:
        for keyword in feature["keywords"]:
            if keyword in user_message:
                if feature["id"] == 2:
                    recommended_products = ", ".join([products[p]["name"] for p in products])
                    response = f"Recommended products: {recommended_products}"
                elif feature["id"] == 3:
                    product_name = user_message.replace("product", "").strip()
                    found = False
                    for product in products.values():
                        if product_name.lower() in product["name"].lower():
                            response = f"Product: {product['name']}, Price: {product['price']}, Description: {product['description']}"
                            found = True
                            break
                    if not found:
                        response = "Product not found. Please check the product name."
                elif feature["id"] == 5:
                    order_id = user_message.split()[-1]
                    if order_id in orders:
                        order = orders[order_id]
                        response = f"Order Status: {order['status']}, Tracking ID: {order['tracking_id']}"
                    else:
                        response = "Order not found."
                elif feature["id"] == 8:
                    if "hola" in user_message:
                        response = feature["response"]["es"]
                    elif "bonjour" in user_message:
                        response = feature["response"]["fr"]
                    elif "नमस्ते" in user_message:
                        response = feature["response"]["hi"]
                    else:
                        response = feature["response"]["en"]
                elif feature["id"] == 9:
                    ai_message = user_message.replace("ai", "").strip()
                    response = generate_ai_response(ai_message)
                else:
                    response = feature["response"]
                break
    return jsonify(response)
@app.route("/get", methods=["POST"])
def get_response():
    return webhook()

@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    return jsonify(orders.get(order_id, {"error": "Order not found"}))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
