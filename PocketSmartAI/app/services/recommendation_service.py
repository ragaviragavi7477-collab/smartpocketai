import json
from app.gemini_utils import (
    get_gemini_response,
    create_home_prompt,
    create_party_prompt,
    create_jewelry_prompt,
)

def _normalize(rec):
    if not isinstance(rec, dict):
        return {"name": str(rec)[:200], "price": "N/A", "platform": "N/A", "description": ""}
    return {
        "name": rec.get("name") or rec.get("product_name") or rec.get("item") or rec.get("title") or "Recommended product",
        "price": rec.get("price") or rec.get("estimated_price") or rec.get("cost") or "N/A",
        "platform": rec.get("platform") or rec.get("platform_name") or rec.get("store") or "N/A",
        "description": rec.get("description") or rec.get("description_text") or rec.get("overview") or rec.get("details") or "",
    }


def parse_recommendations(response_text):
    if not response_text:
        return [{"name": "No recommendations generated", "price": "N/A", "platform": "N/A", "description": "Please try again with a different budget."}]
    try:
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        if start != -1 and end > start:
            parsed = json.loads(response_text[start:end])
            if isinstance(parsed, dict):
                parsed = [parsed]
            if isinstance(parsed, list) and parsed:
                return [_normalize(r) for r in parsed]
    except Exception:
        pass
    text = response_text.strip()
    return [{"name": text[:200] if text else "Recommendation", "price": "N/A", "platform": "N/A", "description": ""}]

def get_home_recommendations(data):
    prompt = create_home_prompt(
        data.budget, data.room_type, data.room_quantity,
        data.lights_count, data.ceiling_fans, data.dining_tables, data.preferences
    )
    response_text = get_gemini_response(prompt)
    recommendations = parse_recommendations(response_text)
    return recommendations

def get_party_recommendations(data):
    prompt = create_party_prompt(
        data.budget, data.guest_count, data.event_type, data.venue, data.preferences
    )
    response_text = get_gemini_response(prompt)
    recommendations = parse_recommendations(response_text)
    return recommendations

def get_jewelry_recommendations(data):
    prompt = create_jewelry_prompt(data.budget, data.occasion, data.style)
    response_text = get_gemini_response(prompt, data.outfit_image_url)
    recommendations = parse_recommendations(response_text)
    return recommendations
