import google.generativeai as genai
import os
from app.config import settings

MOCK_MODE = settings.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE"

if not MOCK_MODE:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(prompt, image_url=None):
    if MOCK_MODE:
        return _mock_response(prompt)
    try:
        if image_url:
            response = model.generate_content([prompt, genai.upload_file(image_url)])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return _mock_response(prompt)

def _mock_response(prompt):
    import json
    lowered = (prompt or "").lower()
    # NOTE: check party/jewelry first — a party venue like "Home" would
    # otherwise match the home branch below.
    if 'party' in lowered or 'guest' in lowered or 'catering' in lowered or 'event type' in lowered:
        return json.dumps([
            {"name": "Swiggy Party Package (10 guests)", "price": 9999, "platform": "Swiggy", "description": "Catering package for 10 guests"},
            {"name": "Amazon Decoration Kit", "price": 2499, "platform": "Amazon", "description": "Balloons, streamers, and party supplies"},
            {"name": "OYO Party Venue Booking", "price": 15999, "platform": "OYO", "description": "Affordable venue for celebrations"}
        ])
    elif 'jewel' in lowered or 'occasion' in lowered or 'necklace' in lowered:
        return json.dumps([
            {"name": "Silver Necklace Set", "price": 2499, "platform": "Amazon", "description": "Elegant silver necklace with pendant"},
            {"name": "Flipkart Gold Plated Earrings", "price": 1999, "platform": "Flipkart", "description": "Classic gold-plated earrings"},
            {"name": "Amazon Gemstone Ring", "price": 3499, "platform": "Amazon", "description": "Beautiful gemstone ring for special occasions"}
        ])
    elif 'home' in lowered or 'interior' in lowered or 'room' in lowered or 'furniture' in lowered:
        return json.dumps([
            {"name": "IKEA KALLAX Shelf Unit", "price": 4999, "platform": "IKEA", "description": "Versatile shelving for living room storage"},
            {"name": "Amazon Basics LED Desk Lamp", "price": 1299, "platform": "Amazon", "description": "Adjustable LED lamp for task lighting"},
            {"name": "Amazon Basics Throw Pillow Set", "price": 899, "platform": "Amazon", "description": "Decorative pillow set for modern style"},
            {"name": "IKEA MARKUS Office Chair", "price": 14999, "platform": "IKEA", "description": "Ergonomic chair for home office"}
        ])
    return json.dumps([
        {"name": "Curated Pick 1", "price": 2499, "platform": "Amazon", "description": "Top-rated pick within your budget"},
        {"name": "Curated Pick 2", "price": 4999, "platform": "IKEA", "description": "Popular value-for-money option"},
        {"name": "Curated Pick 3", "price": 1499, "platform": "Flipkart", "description": "Budget-friendly recommendation"}
    ])

def create_home_prompt(budget, room_type, room_quantity, lights, ceiling_fans, dining_tables, preferences):
    prompt = f"""Act as a budget-savvy home interior designer for India. Give recommendations for the following:
- Budget: \u20b9{budget} (Indian Rupees)
- Room type: {room_type}
- Quantity needed: {room_quantity} rooms
- Lights needed: {lights}
- Ceiling fans needed: {ceiling_fans}
- Dining tables needed: {dining_tables}
- Additional preferences: {preferences}

Provide 3-5 product recommendations across Amazon.in, IKEA India, and Flipkart. For each recommendation include: product name, estimated price in Indian Rupees, platform, and a brief description. Keep total cost within budget. Show all prices in INR (\u20b9) only. Format as structured JSON."""
    return prompt

def create_party_prompt(budget, guest_count, event_type, venue, preferences):
    prompt = f"""Act as a party budget planner for India. Give recommendations for the following:
- Budget: \u20b9{budget} (Indian Rupees)
- Guest count: {guest_count}
- Event type: {event_type}
- Venue: {venue}
- Additional preferences: {preferences}

Allocate budget proportionally across catering (Swiggy/Zomato), decoration, and entertainment (OYO for venues). Provide 3-5 recommendations per category with platform details. Show all prices in Indian Rupees (\u20b9) only. Format as structured JSON."""
    return prompt

def create_jewelry_prompt(budget, occasion, style, outfit_image_url=None):
    prompt = f"""Act as a jewelry style advisor for India. Give recommendations for the following:
- Budget: \u20b9{budget} (Indian Rupees)
- Occasion: {occasion}
- Style preference: {style}

Suggest elegant jewelry pieces from Amazon.in and Flipkart that match the occasion and style. Provide 3-5 recommendations with product name, estimated price in Indian Rupees, platform, and brief description. Show all prices in INR (\u20b9) only. Format as structured JSON."""
    return prompt
