# Define the required fields for each insurance product

AUTO_FIELDS = {
    "vehicle_details": "What is the year, make, and model of your vehicle?",
}

HOME_FIELDS = {
    "property_details": "What type of property is this and what is its estimated value? (e.g. Single-family, $300k)",
}

LIFE_FIELDS = {
    "applicant_details": "How old is the applicant and what is the desired coverage amount?",
}

PRODUCT_FIELDS = {
    "auto": AUTO_FIELDS,
    "home": HOME_FIELDS,
    "life": LIFE_FIELDS,
}

def get_next_missing_field(insurance_type: str, collected_data: dict) -> str | None:
    """Returns the key of the next missing field, or None if all are collected."""
    fields = PRODUCT_FIELDS.get(insurance_type, {})
    for key in fields.keys():
        if key not in collected_data or not collected_data[key]:
            return key
    return None

def get_field_prompt(insurance_type: str, field_key: str) -> str:
    return PRODUCT_FIELDS.get(insurance_type, {}).get(field_key, "Please provide the requested detail.")
