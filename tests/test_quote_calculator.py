from app.quote.calculator import calculate_auto_quote, calculate_home_quote, calculate_life_quote

def test_calculate_auto_quote():
    data = {"driver_age": "20", "coverage_level": "Premium"}
    quote = calculate_auto_quote(data)
    
    val = int(quote["estimated_premium"].split(" ")[0].replace("$", ""))
    # Base 100 + 50 (under 25) + 40 (premium) = 190
    assert val == 190

def test_calculate_home_quote():
    data = {"estimated_property_value": "600000"}
    quote = calculate_home_quote(data)
    
    val = int(quote["estimated_premium"].split(" ")[0].replace("$", ""))
    # Base 80 + 60 (> 500k) = 140
    assert val == 140

def test_calculate_life_quote():
    data = {"applicant_age": "55", "health_status": "Fair"}
    quote = calculate_life_quote(data)
    
    val = int(quote["estimated_premium"].split(" ")[0].replace("$", ""))
    # Base 35 + 45 (> 50) + 30 (Fair) = 110
    assert val == 110
