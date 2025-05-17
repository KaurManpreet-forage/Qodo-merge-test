# utils.py (updated)

def convert_temperature(value, to_unit="celsius"):
    """
    Convert temperature between Fahrenheit and Celsius.
    Supported 'to_unit' values: 'celsius', 'fahrenheit'
    """
    if to_unit == "celsius":
        return (value - 32) * 5 / 9
    elif to_unit == "fahrenheit":
        return (value * 9 / 5) + 32
    else:
        raise ValueError("Invalid unit. Use 'celsius' or 'fahrenheit'.")
