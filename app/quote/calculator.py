import random

def calculate_auto_quote(data: dict) -> dict:
    # Deterministic generation mimicking quick estimate logic
    base = 118
    vehicle = data.get("vehicle_details", "2022 Honda Civic").title()
    
    return {
        "insurance_type": "auto",
        "estimated_premium": f"${base} / month",
        "summary": {
            "vehicle": vehicle,
            "coverage": "Standard Reliable",
            "deductible": "$500",
            "liability": "$100k/$300k"
        },
        "notes": "This is a quick estimate based on average rates for this vehicle."
    }

def calculate_home_quote(data: dict) -> dict:
    base = 85
    property_details = data.get("property_details", "Single-family Home").title()
        
    return {
        "insurance_type": "home",
        "estimated_premium": f"${base} / month",
        "summary": {
            "property": property_details,
            "coverage_type": "Comprehensive",
            "deductible": "$1,000",
            "personal_property": "$50k"
        },
        "notes": "Home premium calculated using estimated property details."
    }

def calculate_life_quote(data: dict) -> dict:
    base = 35
    details = data.get("applicant_details", "30 years old, $500k Coverage").title()

    return {
        "insurance_type": "life",
        "estimated_premium": f"${base} / month",
        "summary": {
            "applicant": details,
            "term": "20 Years",
            "coverage": "Standard Life",
        },
        "notes": "Life insurance premium based on general applicant details."
    }

def generate_quote(insurance_type: str, collected_data: dict) -> dict:
    if insurance_type == "auto":
        return calculate_auto_quote(collected_data)
    elif insurance_type == "home":
        return calculate_home_quote(collected_data)
    elif insurance_type == "life":
        return calculate_life_quote(collected_data)
    
    return {"error": "Invalid insurance type for quote generation."}
