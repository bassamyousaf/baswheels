from tavily import TavilyClient
import re
from dotenv import load_dotenv
import os
 
# Load .env variables
load_dotenv()
TAVILY_API_KEY = os.getenv("TavilyApiKey")
 
# Initialize Tavily client
client = TavilyClient(api_key=TAVILY_API_KEY)
def extract_price(text):
    # PKR price extraction from text (lac, million, crore, PKR, Rs)
    text = text.replace(",", "")
    patterns = [
        r"(\d+\.?\d*)\s*(lac|lakh)", 
        r"(\d+\.?\d*)\s*(million)",
        r"(\d+\.?\d*)\s*(crore)",
        r"[rR][sS]\.?\s*(\d+\.?\d*)",
        r"(\d+\.?\d*)\s*PKR"
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            val = float(m.group(1))
            unit = m.group(2).lower() if len(m.groups()) > 1 else ""

            if "lac" in unit or "lakh" in unit:
                return val * 100000
            if "million" in unit:
                return val * 1000000
            if "crore" in unit:
                return val * 10000000
            return val
    return None


def extract_fuel(text):
    t = text.lower()
    if "hybrid" in t:
        return "hybrid"
    if "electric" in t or "ev" in t:
        return "ev"
    if "diesel" in t:
        return "diesel"
    if "petrol" in t:
        return "petrol"
    return "unknown"


def extract_trunk(text):
    m = re.search(r"(\d+)\s*(liters|l|ltr)", text, re.I)
    if m:
        return int(m.group(1))
    return 350  # default guess


def extract_fuel_economy(text):
    m = re.search(r"(\d+)\s*(km/l|kmpl)", text, re.I)
    if m:
        return float(m.group(1))
    return 12  # default guess


def extract_seats(text):
    m = re.search(r"(\d)\s*seater", text, re.I)
    if m:
        return int(m.group(1))
    return 5


def extract_tags(text):
    tags = []
    t = text.lower()
    if "family" in t or "sedan" in t:
        tags.append("family")
    if "commute" in t or "economy" in t:
        tags.append("commute")
    if "luxury" in t:
        tags.append("luxury")
    if "suv" in t or "7 seater" in t:
        tags.append("roadtrip")
    return ",".join(tags) if tags else "general"


def search_cars_with_tavily(query):
    response = client.search(query=query, max_results=10, include_domains=["pakwheels.com", "olx.com.pk", "carwale.com"])
    
    results = response["results"]
    cars = []

    for r in results:
        title = r.get("title", "")
        desc = r.get("content", "")
        combined = (title + " " + desc)

        price = extract_price(combined)
        fuel = extract_fuel(combined)
        trunk = extract_trunk(combined)
        seats = extract_seats(combined)
        econ = extract_fuel_economy(combined)
        tags = extract_tags(combined)

        cars.append({
            "make_model": title[:50],
            "price_pkr": price or 0,
            "is_new": "yes" if "new" in combined.lower() else "no",
            "fuel_type": fuel,
            "trunk_liters": trunk,
            "seats": seats,
            "fuel_economy_kmpl": econ,
            "suitability_tags": tags,
            "reliability_rating": 3,
            "notes": desc[:200]
        })

    return cars