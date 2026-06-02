# This module contains the pure conversion logic.
# It has NO dependency on FastAPI or any web framework — just plain Python functions.
# This separation makes the logic easy to unit-test in isolation.


def celsius_to_fahrenheit(celsius: float) -> float:
    # Standard formula: multiply by 9/5, then add 32
    return round((celsius * 9 / 5) + 32, 2)  # round to 2 decimal places


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    # Inverse formula: subtract 32 first, then multiply by 5/9
    return round((fahrenheit - 32) * 5 / 9, 2)  # round to 2 decimal places
