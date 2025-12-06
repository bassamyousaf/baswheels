# scoring.py
import math

def normalize(value, min_v, max_v):
    if max_v == min_v:
        return 0.5
    return (value - min_v) / (max_v - min_v)

def compute_scores(cars, user_prefs, weights):
    """
    cars: list of dicts (each car row)
    user_prefs: dict with keys:
        min_price, max_price, fuel_type (or 'any'), new_used ('new','used','either'),
        purposes (set of purpose strings)
    weights: dict of weights summing to ~1.0 for keys:
        price, fuel, new_used, purpose, trunk, economy, reliability
    Returns list of (car, score, breakdown_dict, explanation_str)
    """
    # Prepare min/max for normalization
    trunk_vals = [float(c.get("trunk_liters") or 0) for c in cars]
    econ_vals = []
    for c in cars:
        fe = c.get("fuel_economy_kmpl")
        if fe is None or fe == "" or float(fe) == 0:
            # for EV with 0 fuel econ, treat as high economy by substitution (choose a cap)
            econ_vals.append(25.0)  # treat EVs as high
        else:
            econ_vals.append(float(fe))
    rel_vals = [float(c.get("reliability_rating") or 3) for c in cars]

    min_trunk, max_trunk = min(trunk_vals), max(trunk_vals)
    min_econ, max_econ = min(econ_vals), max(econ_vals)
    min_rel, max_rel = min(rel_vals), max(rel_vals)

    scored = []
    for c in cars:
        breakdown = {}
        price = float(c.get("price_pkr") or 0)
        # --- budget/price score ---
        min_p, max_p = user_prefs["min_price"], user_prefs["max_price"]
        if min_p <= price <= max_p:
            price_score = 1.0
        else:
            # linear decay: if outside range, measure distance relative to range width
            range_width = max(1, max_p - min_p)
            if price < min_p:
                d = (min_p - price) / range_width
            else:
                d = (price - max_p) / range_width
            price_score = max(0.0, 1.0 - d)  # if too far, it tends to 0
        breakdown["price_score"] = price_score

        # --- fuel type score ---
        pref_fuel = user_prefs["fuel_type"].lower()
        car_fuel = str(c.get("fuel_type") or "").lower()
        if pref_fuel in ("any", "", None):
            fuel_score = 1.0
        elif pref_fuel == car_fuel:
            fuel_score = 1.0
        else:
            # partial credit: hybrid vs petrol/diesel or ev considered alternative
            if car_fuel == "hybrid" and pref_fuel in ("petrol", "diesel"):
                fuel_score = 0.7
            elif car_fuel == "ev" and pref_fuel in ("petrol", "diesel"):
                fuel_score = 0.6
            else:
                fuel_score = 0.0
        breakdown["fuel_score"] = fuel_score

        # --- new/used score ---
        pref_nu = user_prefs["new_used"].lower()
        car_nu = "new" if str(c.get("is_new") or "").lower() in ("yes", "true", "1") else "used"
        if pref_nu == "either":
            new_score = 1.0
        elif pref_nu == car_nu:
            new_score = 1.0
        else:
            new_score = 0.0
        breakdown["new_used_score"] = new_score

        # --- purpose match ---
        user_purposes = set([p.strip().lower() for p in user_prefs.get("purposes", []) if p.strip() != ""])
        car_tags = set([t.strip().lower() for t in str(c.get("suitability_tags") or "").split(",") if t.strip() != ""])
        if len(user_purposes) == 0:
            purpose_score = 1.0
        else:
            matched = len(user_purposes & car_tags)
            purpose_score = matched / len(user_purposes)
        breakdown["purpose_score"] = purpose_score

        # --- trunk score ---
        trunk = float(c.get("trunk_liters") or 0)
        trunk_score = normalize(trunk, min_trunk, max_trunk)
        breakdown["trunk_score"] = trunk_score

        # --- economy score ---
        fe = c.get("fuel_economy_kmpl")
        if fe is None or float(fe) == 0:
            econ_val = 25.0
        else:
            econ_val = float(fe)
        econ_score = normalize(econ_val, min_econ, max_econ)
        breakdown["economy_score"] = econ_score

        # --- reliability score ---
        rel = float(c.get("reliability_rating") or 3.0)
        rel_score = normalize(rel, min_rel, max_rel)
        breakdown["reliability_score"] = rel_score

        # Weighted sum
        total = 0.0
        total += weights.get("price", 0.0) * breakdown["price_score"]
        total += weights.get("fuel", 0.0) * breakdown["fuel_score"]
        total += weights.get("new_used", 0.0) * breakdown["new_used_score"]
        total += weights.get("purpose", 0.0) * breakdown["purpose_score"]
        total += weights.get("trunk", 0.0) * breakdown["trunk_score"]
        total += weights.get("economy", 0.0) * breakdown["economy_score"]
        total += weights.get("reliability", 0.0) * breakdown["reliability_score"]

        score_0_100 = round(total * 100, 2)

        # Explanation text (short)
        positives = []
        negatives = []
        if breakdown["price_score"] > 0.9:
            positives.append("Fits your budget")
        elif breakdown["price_score"] > 0.6:
            positives.append("Close to your budget")
        else:
            negatives.append("Outside preferred budget")

        if breakdown["fuel_score"] >= 0.9:
            positives.append(f"Matches fuel type ({c.get('fuel_type')})")
        elif breakdown["fuel_score"] > 0:
            positives.append(f"Partially matches fuel preferences ({c.get('fuel_type')})")
        else:
            negatives.append(f"Different fuel type ({c.get('fuel_type')})")

        if breakdown["new_used_score"] >= 1.0:
            positives.append(c.get("is_new") and "Is new" or "Is used (as preferred)")
        else:
            negatives.append("New/Used preference mismatch")

        if breakdown["purpose_score"] >= 0.7:
            positives.append("Covers requested purposes")
        elif breakdown["purpose_score"] > 0:
            positives.append("Partially matches your purposes")
        else:
            negatives.append("Does not match requested purposes well")

        if breakdown["trunk_score"] > 0.7:
            positives.append("Good trunk space")
        elif breakdown["trunk_score"] < 0.3:
            negatives.append("Limited trunk space")

        if breakdown["economy_score"] > 0.7:
            positives.append("Good fuel economy")
        elif breakdown["economy_score"] < 0.3:
            negatives.append("Poor fuel economy")

        if breakdown["reliability_score"] > 0.6:
            positives.append("High reliability")
        else:
            negatives.append("Average/Lower reliability")

        explanation = ""
        if positives:
            explanation += "Good: " + "; ".join(positives) + ". "
        if negatives:
            explanation += "Compromises: " + "; ".join(negatives) + "."

        scored.append((c, score_0_100, breakdown, explanation))

    # Sort descending by score
    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored_sorted
