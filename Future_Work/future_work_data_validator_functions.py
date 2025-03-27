#THESE ARE some of the functions I thought about integrating into the validator.py but didn't have time to. 

def validate_missing_values(item, fields):
    for field in fields:
        if field not in item or item[field] is None:
            logger.warning(f"Missing value for field '{field}' in item '{item.get('name', 'Unknown')}'")
            discrepancy_report.append(f"[MISSING VALUE] '{item.get('name', 'Unknown')}' is missing field '{field}'")


def validate_negative_values(item, field_name):
    value = float(item.get(field_name, 0.0))
    if value < 0:
        logger.warning(f"Negative value found for '{field_name}' in item '{item.get('name', 'Unknown')}'")
        discrepancy_report.append(f"[NEGATIVE VALUE] '{item.get('name', 'Unknown')}' has a negative value of {value}")


def validate_data_type(item, field_name, expected_type=float):
    try:
        value = expected_type(item.get(field_name, 0.0))
    except ValueError:
        logger.warning(f"Incorrect data type for field '{field_name}' in item '{item.get('name', 'Unknown')}'")
        discrepancy_report.append(f"[INVALID DATA TYPE] '{item.get('name', 'Unknown')}' field '{field_name}' has an incorrect data type")


