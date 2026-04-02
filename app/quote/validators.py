from datetime import datetime

def validate_collected_data(insurance_type: str, field: str, value: str) -> list[str]:
    """Validates a specific field against deterministic rules."""
    errors = []
    
    # We now accept natural language inputs (e.g. '2022 honda civic')
    # So we only enforce that the value is not empty
    if not value or len(value) < 2:
        errors.append("Please provide more details.")
        
    return errors
