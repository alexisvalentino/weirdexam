from app.quote.validators import validate_auto_field, validate_home_field, validate_life_field

def test_validate_auto_field_year():
    # Future year should fail
    errors = validate_auto_field("vehicle_year", "2050")
    assert len(errors) > 0
    assert "future" in errors[0].lower()

    # Valid year should pass
    errors = validate_auto_field("vehicle_year", "2020")
    assert len(errors) == 0

    # Non-numeric should fail
    errors = validate_auto_field("vehicle_year", "two thousand")
    assert len(errors) > 0

def test_validate_auto_field_age():
    # Underage should fail
    errors = validate_auto_field("driver_age", "12")
    assert len(errors) > 0

    # Valid age should pass
    errors = validate_auto_field("driver_age", "35")
    assert len(errors) == 0

def test_validate_home_field():
    # Negative/Zero value should fail
    errors = validate_home_field("estimated_property_value", "0")
    assert len(errors) > 0
    
    # Valid numeric with characters
    errors = validate_home_field("estimated_property_value", "$350,000")
    assert len(errors) == 0

def test_validate_life_field():
    errors = validate_life_field("applicant_age", "70")
    assert len(errors) > 0 # Over 65 should fail for term life
    
    errors = validate_life_field("applicant_age", "30")
    assert len(errors) == 0
