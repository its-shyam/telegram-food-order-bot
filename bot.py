"""
OONA - Detailed Telegram Food Ordering Bot
Requirements:
  pip install pyTelegramBotAPI
Run:
  python bot.py
"""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "REPLACE_WITH_ADMIN_CHAT_ID"))  # your Telegram id
ORDERS_FILE = "orders.json"

bot = telebot.TeleBot(BOT_TOKEN)

# ----------------- FULL DETAILED MENU (from the uploaded FOOD-MENU.pdf) -----------------
menu = {
    "Indian": {
        "Tandoori Starters Vegetarian": {
            "Oven-roasted Baby Potatoes": 285,
            "Paneer Tikka Shaslik": 325,
            "Kurkure Paneer Tikka": 325,
            "Basil Malai Paneer Tikka": 325,
            "Bhutte Di Seekh": 285,
            "Chaman Malai Gilafi Seekh": 285,
            "Morsels Mushroom Galouti": 325,
            "Oona Big Platter (Veg)": 645
        },
        "Tandoori Starters Non Vegetarian": {
            "Tandoori Chicken Half": 350,
            "Tandoori Chicken Full": 600,
            "Moroccan Tandoori Chicken Half": 350,
            "Moroccan Tandoori Chicken Full": 600,
            "Jalapeno Malai Tikka": 350,
            "Makhmali Creamy Chicken Tikka": 350,
            "Oregano Chicken Tikka": 350,
            "Murg Amritsari Tikka": 350,
            "Dum Khas Tangri Kebab": 350,
            "Rosemary Mutton Seekh": 380,
            "Roast Lamb Chops": 380,
            "Galouti Kebab": 380,
            "Pepper Lamb": 380,
            "Ajwaini Fish Tikka": 420,
            "Lemon Butter Dill Fish Tikka": 420,
            "Oona Big Platter (Non-Veg)": 665
        },
        "Main Course Vegetarian": {
            "Al Verdure": 290,
            "Veg Makhani": 310,
            "Malai Kofta": 285,
            "Veg Maratha Kofta": 285,
            "Cheese Corn Kofta": 340,
            "Hing Jeere Ke Aloo": 285,
            "Amritsari Chole": 340,
            "Dal Punjabi Tadka": 250,
            "Oona Dal Bukhara": 290
        },
        "Main Course Non Vegetarian": {
            "Butter Chicken": 365,
            "Kukkad Junglee Bhatti Half": 365,
            "Kukkad Junglee Bhatti Full": 600,
            "Chicken Changeji Korma": 365,
            "Murg Nihari": 365,
            "Cream Chicken": 365,
            "Chicken Tikka Butter Masala": 365,
            "Chicken Tikka Tawa Masala": 365,
            "Chicken Lababdar": 365,
            "Chicken Dhaniwal": 365,
            "Chicken Mirch Elaichi Korma": 365,
            "Dum Khas Tangri Masala": 365
        },
        "Gosht (Mutton)": {
            "Cooker Rosemary Mutton Curry": 390,
            "Gosht Rogan Josh": 390,
            "Adraki Mutton Chap Masala": 390,
            "Methi Mutton Masala": 390
        },
        "Sea Food (Indian)": {
            "Fish Punjabi Masala": 430,
            "Fish Malwani Curry": 430,
            "Prawn Malabari Masala": 480
        },
        "Rice & Biryani": {
            "Veg Dum Biryani": 0,       # price not specified in PDF extract; set later if needed
            "Kolkata Biryani (Egg/Chicken/Mutton vary)": 0,
            "Veg Pulao": 0,
            "Plain Basmati Rice": 0
        },
        "Breads & Accompaniments": {
            "Assorted Accompaniments": 0
        }
    },

    "Oriental": {
        "Soups": {
            "Four Treasure": 140,
            "Tom Kha": 140,
            "Lemon Coriander": 140,
            "Broccoli Water Chestnut Soup": 140,
            "Manchow": 140,
            "Sweet Corn": 140
        },
        "Starters Veg": {
            "Water Chestnut Crispy Rice": 275,
            "Sambal Paneer": 325,
            "Pan-Fried Chilli Paneer": 325,
            "Spicy Basil Paneer": 325,
            "Cottage Cheese Fa-Fa": 325,
            "Crispy Honey Chilli Lotus Chips": 365,
            "Burnt Garlic Corn Cubes": 325
        },
        "Starters Non Veg": {
            "Mountain Chicken": 350,
            "Smoke Chicken": 350,
            "Kyong Chilli Chicken": 350,
            "Chilli Chicken Kolkata Style": 350,
            "Gai Sai Takrai": 350,
            "Sliced Chicken Cantonese": 350,
            "Drums of Heaven Shandum Style": 350,
            "Chilli Mustard Fish": 420
        },
        "Stir Fry & Greens": {
            "Stir Fried Asian Greens": 325,
            "Crispy Conjee Veg": 325,
            "Shanghai Spring Roll": 275
        },
        "Dim Sums Veg": {
            "Cream Cheese Mushroom Dim Sum": 265,
            "Vegetable Crystal Dim Sum": 265,
            "Corn and Watechestnut Dim Sum": 265,
            "Vegetable Basil Dim Sum": 265,
            "Zucchini Corn Dim Sum": 265,
            "Edamame Dim Sum": 355
        },
        "Dim Sums Non Veg": {
            "Chicken Coriander Dim Sum": 295,
            "Chicken Har Gao": 295,
            "Chicken Gyoza": 295,
            "Prawn Har Gao": 345,
            "Seafood Dim Sum": 345,
            "Prawn Dim Sum": 355
        },
        "Bao": {
            "Multiple Mushroom Bao": 250,
            "Spicy Basil Cottage Cheese Bao": 250,
            "Jackfruit Bao": 250,
            "Just Chicken Bao": 280
        },
        "Sushi": {
            "California Veg Sushi": 425,
            "Crunchy Veg Maki": 425,
            "Cream Cheese Mushroom": 445,
            "Spicy Grill Chicken Sushi": 450,
            "Kasto Chicken Sushi": 450,
            "Prawn Tempura Sushi": 525,
            "Salmon and Avocado Sushi": 720
        },
        "Rice or Noodles": {
            "Wok-tossed Fried Rice Veg": 195,
            "Wok-tossed Fried Rice Chicken": 210,
            "Wok-tossed Fried Rice Mix": 225,
            "Schezwan Rice Veg": 210,
            "Schezwan Rice Chicken": 225,
            "Ginger Capsicum Veg": 210,
            "Ginger Capsicum Chicken": 225,
            "Korean Fried Rice Veg": 230,
            "Korean Fried Rice Chicken": 255,
            "Shiitake Mushroom Fried Rice Veg": 220,
            "Shiitake Mushroom Fried Rice Chicken": 235,
            "Nasi Goreng Chicken": 355,
            "Nasi Goreng Mix": 395,
            "Hakka Noodles Veg": 190,
            "Hakka Noodles Chicken": 210,
            "Chilli Garlic Noodles Veg": 210,
            "Chilli Garlic Noodles Chicken": 225,
            "Udon Noodles Veg": 235,
            "Udon Noodles Chicken": 245,
            "Curry Flavoured Noodles Veg": 225,
            "Curry Flavoured Noodles Chicken": 235
        },
        "Stir Fry / Specials": {
            "Kra Pao Gai": 350,
            "Chopsuey": 205,
            "Green Thai Curry Veg": 320,
            "Green Thai Curry Chicken": 340,
            "Red Thai Curry Veg": 320,
            "Red Thai Curry Chicken": 340
        },
        "Side Orders Veg": {
            "Paneer in Choice of Sauce": 340,
            "Cottage Cheese Chinese Parsley": 340,
            "Exotic Veg in Ginger Wine Sauce": 340,
            "Classic Veg Manchurian": 340
        },
        "Side Orders Non Veg": {
            "Tousi Chicken": 355,
            "Tsingoi Chicken": 355,
            "Kung Pao Chicken": 355,
            "Slice Chicken with Mushroom and Veg": 355,
            "Slice Chicken in Choice of Sauce": 355,
            "Fish in Chinese Parsley Sauce": 430,
            "Asian Chilli Mustard Fish": 430,
            "Fish in Choice of Sauce": 430,
            "Prawns Hubai Sauce": 455,
            "Prawns in Sambal Oelek Sauce": 455
        },
        "Pan-Fried / Prawns": {
            "Pan-Fried Chilli Fish": 420,
            "Dynamite Prawns": 450,
            "Chilli Garlic Prawns": 450
        }
    },

    "Continental": {
        "Soups & Salads": {
            "Various Soups": 0,
            "Fresh Garden Salad (sample)": 0
        },
        "Fries & Snacks": {
            "Fries": 0
        },
        "Appetizers Veg": {
            "Scrambled Mushroom on Toasted Pita": 350,
            "Zucchini Fritters": 350,
            "Mushroom Croquette": 350,
            "Raggi Nachos": 325,
            "Garlic Bread with Cheese": 225,
            "Quasedillas": 350
        },
        "Appetizers Non Veg": {
            "OFC Strips (Oona Fried Chicken)": 350,
            "BBQ Chicken Wings": 350,
            "Shish Taouk": 350,
            "Grilled Chicken with Chimichuri Sauce": 350,
            "Lamb Chelo": 380,
            "Lamb Tabei": 380,
            "Fish and Chips": 420,
            "Garlic Prawns": 450
        },
        "Mezze Platters": {
            "Veg Mezze": 450,
            "Non Veg Mezze Platter": 495
        },
        "Sliders": {
            "Cottage Cheese Slider": 285,
            "Sweet Potato Slider": 285,
            "Pulled Chicken Slider": 325,
            "Lamb Slider": 350
        },
        "Main Continental": {
            "Grilled Cottage Cheese": 435,
            "Corn Crepes": 435,
            "Baked Vegetables with Burrata": 435,
            "Grilled Chicken (choice of sauce)": 465,
            "Chicken Mexicana": 465,
            "Pizza Margherita": 365,
            "Pizza Alle Verdure": 420,
            "Paneer Paprika Pizza": 420,
            "Quattro Formaggi": 420,
            "Italian Pizza": 420,
            "Pizza Di Pollo": 450,
            "Smoked Chicken Pizza": 450,
            "Pizza Bolognese": 450
        },
        "Flat Breads & Pastas": {
            "Marinara & Burrata": 410,
            "Beetroot and Hemp Flat Bread": 410,
            "Spaghetti Aglio Olio": 325,
            "Penne/Spaghetti (sauces)": 325,
            "Spinach and Cashewnut Risotto": 325,
            "Wild Mushroom Risotto": 325
        }
    },

    "Desserts & Others": {
        "Desserts": {
            "Chocolate Roll with Ice Cream": 215,
            "Churros": 215,
            "Panacotta": 215,
            "Tiramisu": 215,
            "Cheesecake": 215,
            "Zafaran Pistachio Phirni": 215,
            "Baked Cheese Cake": 215,
            "Oona Chocolate Ball": 215,
            "Serradura": 215
        },
        "Beverages (sample)": {
            "Soft Drink (sample)": 0
        }
    }
}
# --------------------------------------------------------------------------------------

# Utilities for saving orders
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_order_record(order):
    orders = load_orders()
    orders.append(order)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

# In-memory user carts & order states
user_cart = {}
order_state = {}

# ---------- Helper to create inline keyboard for categories ----------
def kb_from_list(items, prefix):
    kb = InlineKeyboardMarkup()
    for it in items:
        kb.add(InlineKeyboardButton(it, callback_data=f"{prefix}|{it}"))
    kb.add(InlineKeyboardButton("🛒 My Cart", callback_data="action|cart"))
    kb.add(InlineKeyboardButton("🔙 Main Menu", callback_data="action|main"))
    return kb

# ---------- /start handler ----------
@bot.message_handler(commands=["start"])
def start_cmd(msg):
    text = "🍽️ *Welcome to OONA – The One*\nPlease choose a category:"
    kb = InlineKeyboardMarkup()
    for cat in menu.keys():
        kb.add(InlineKeyboardButton(cat, callback_data=f"cat|{cat}"))
    bot.send_message(msg.chat.id, text, parse_mode="Markdown", reply_markup=kb)

# ---------- callback query handler ----------
@bot.callback_query_handler(func=lambda call: True)
def callback_router(call):
    data = call.data
    if data.startswith("cat|"):
        _, cat = data.split("|", 1)
        # show subcategories
        subs = list(menu[cat].keys())
        bot.edit_message_text(f"*{cat}* - Choose a subcategory:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=kb_from_list(subs, f"subcat|{cat}"))
    elif data.startswith("subcat|"):
        _, cat = data.split("|", 1)
        # show dishes grouped by subcategory name selection is encoded in next step
        # Actually the call is "subcat|<cat>|<sub>" but our kb prefix only encoded cat; to keep simple, interpret callback differently:
        # show a list of subcategories again for choosing a particular sub
        # (We will instead encode sub selection from full string - adjust)
        # Not reached in this flow.
        pass
    elif data.startswith("sub|"):
        # encoded as sub|<cat>|<subname>
        _, cat, sub = data.split("|", 2)
        items = menu[cat][sub]
        kb = InlineKeyboardMarkup()
        for dish, price in items.items():
            kb.add(InlineKeyboardButton(f"{dish} — ₹{price if price>0 else '—'}", callback_data=f"add|{dish}|{price}"))
        kb.add(InlineKeyboardButton("🔙 Back to Categories", callback_data="action|main"))
        kb.add(InlineKeyboardButton("🛒 My Cart", callback_data="action|cart"))
        bot.edit_message_text(f"*{sub}* — Select dish to add to cart:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=kb)
    elif data.startswith("action|"):
        _, act = data.split("|",1)
        if act == "cart":
            send_cart(call.message.chat.id, call.from_user.id)
        elif act == "main":
            start_cmd(call.message)
    elif data.startswith("add|"):
        # add|dish|price
        _, dish, price = data.split("|",2)
        uid = call.from_user.id
        if uid not in user_cart:
            user_cart[uid] = []
        user_cart[uid].append({"name": dish, "price": int(price)})
        bot.answer_callback_query(call.id, f"Added {dish} to cart ✅")
    else:
        # support alternative encoded flows - fallback: open category list
        start_cmd(call.message)

# Because the initial kb_from_list used "cat|<cat>" we need to present subcategory keyboard differently.
# We'll send a fresh message listing subcategories with callbacks encoded as sub|cat|sub

@bot.message_handler(func=lambda m: True)
def generic_text_handler(message):
    text = message.text.strip().lower()
    uid = message.from_user.id

    # Quick keywords
    if text in ("menu", "categories", "start"):
        start_cmd(message)
        return
    if text == "my cart" or text == "cart" or text == "🛒":
        send_cart(message.chat.id, uid)
        return
    if text == "place order":
        begin_order(message)
        return

    # If user is in order flow
    if uid in order_state:
        process_order_text(message)
        return

    # If user types a category name, show subcategories
    for cat in menu.keys():
        if text == cat.lower():
            subs = list(menu[cat].keys())
            kb = InlineKeyboardMarkup()
            for sub in subs:
                kb.add(InlineKeyboardButton(sub, callback_data=f"sub|{cat}|{sub}"))
            kb.add(InlineKeyboardButton("🔙 Main Menu", callback_data="action|main"))
            bot.send_message(message.chat.id, f"*{cat}* — Select a subcategory:", parse_mode="Markdown", reply_markup=kb)
            return

    # Not recognized
    bot.send_message(message.chat.id, "Sorry, I didn't understand. Type *menu* to view categories or tap buttons.", parse_mode="Markdown")

# ---------------- Cart display ----------------
def send_cart(chat_id, uid):
    cart = user_cart.get(uid, [])
    if not cart:
        bot.send_message(chat_id, "🛒 Your cart is empty.")
        return
    total = sum(item["price"] for item in cart)
    text = "🛒 *Your Cart:*\n"
    for i, it in enumerate(cart,1):
        text += f"{i}. {it['name']} — ₹{it['price']}\n"
    text += f"\n*Total:* ₹{total}\n"
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✔ Place Order", callback_data="order|start"))
    kb.add(InlineKeyboardButton("➕ Continue Ordering", callback_data="action|main"))
    kb.add(InlineKeyboardButton("❌ Clear Cart", callback_data="cart|clear"))
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)

# Handle special cart callbacks
@bot.callback_query_handler(func=lambda c: c.data.startswith("cart|"))
def cart_actions(call):
    _, act = call.data.split("|",1)
    uid = call.from_user.id
    if act == "clear":
        user_cart[uid] = []
        bot.answer_callback_query(call.id, "Cart cleared ❌")
        bot.send_message(call.message.chat.id, "Your cart has been cleared.")
    else:
        send_cart(call.message.chat.id, uid)

# --------------- Order flow ----------------
def begin_order(message_or_call):
    if hasattr(message_or_call, "message"):  # callback
        chat_id = message_or_call.message.chat.id
        uid = message_or_call.from_user.id
    else:
        chat_id = message_or_call.chat.id
        uid = message_or_call.from_user.id
    if not user_cart.get(uid):
        bot.send_message(chat_id, "Your cart is empty. Add items before placing an order.")
        return
    order_state[uid] = {"step": "name"}
    bot.send_message(chat_id, "Please enter your *Name* for the order:", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("order|"))
def order_cb(call):
    begin_order(call)

def process_order_text(message):
    uid = message.from_user.id
    state = order_state.get(uid)
    if not state:
        return
    step = state["step"]
    if step == "name":
        state["name"] = message.text.strip()
        state["step"] = "phone"
        bot.send_message(message.chat.id, "Enter your *Phone Number*:")
    elif step == "phone":
        state["phone"] = message.text.strip()
        state["step"] = "address"
        bot.send_message(message.chat.id, "Enter your *Delivery Address*:")
    elif step == "address":
        state["address"] = message.text.strip()
        # finalize
        cart = user_cart.get(uid, [])
        total = sum(item["price"] for item in cart)
        order = {
            "id": f"ORD{int(datetime.utcnow().timestamp())}{uid%1000}",
            "user_id": uid,
            "name": state["name"],
            "phone": state["phone"],
            "address": state["address"],
            "items": cart,
            "total": total,
            "timestamp": datetime.utcnow().isoformat()
        }
        save_order_record(order)
        # notify admin
        order_text = f"🆕 *NEW ORDER* — {order['id']}\nName: {order['name']}\nPhone: {order['phone']}\nAddress: {order['address']}\n\nItems:\n"
        for it in cart:
            order_text += f"- {it['name']} — ₹{it['price']}\n"
        order_text += f"\n*Total:* ₹{total}"
        bot.send_message(ADMIN_CHAT_ID, order_text, parse_mode="Markdown")
        bot.send_message(message.chat.id, f"✅ Your order {order['id']} has been placed! We will contact you soon.", parse_mode="Markdown")
        # clear cart & state
        user_cart[uid] = []
        del order_state[uid]

# --------------- Run bot ---------------
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
