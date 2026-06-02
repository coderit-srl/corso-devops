# FastAPI is a modern Python web framework for building REST APIs.
# It automatically generates interactive docs at /docs (Swagger UI).
from fastapi import FastAPI
from pydantic import BaseModel

# We import only the pure logic from converter.py — the API layer stays thin.
from app.converter import celsius_to_fahrenheit, fahrenheit_to_celsius

# Create the FastAPI application instance.
# title, description and version appear in the auto-generated /docs page.
app = FastAPI(
    title="Temperature Converter API",
    description="Convert between Celsius and Fahrenheit",
    version="1.0.0",
)


# Pydantic models define the shape of JSON responses.
# FastAPI validates and serializes them automatically.
class ConversionResult(BaseModel):
    input_value: float   # the value the caller sent
    input_unit: str      # "Celsius" or "Fahrenheit"
    output_value: float  # the converted result
    output_unit: str     # the opposite unit


# Health-check endpoint — used by Koyeb (and any load balancer) to verify
# the container is alive and ready to serve traffic.
@app.get("/health")
def health():
    return {"status": "ok"}


# Path parameter {value} is extracted from the URL and passed to the function.
# Example request:  GET /convert/celsius/100
# Example response: {"input_value": 100, "input_unit": "Celsius", "output_value": 212.0, "output_unit": "Fahrenheit"}
@app.get("/convert/celsius/{value}", response_model=ConversionResult)
def convert_celsius(value: float):
    return ConversionResult(
        input_value=value,
        input_unit="Celsius",
        output_value=celsius_to_fahrenheit(value),
        output_unit="Fahrenheit",
    )


# Same pattern for the reverse direction.
# Example request:  GET /convert/fahrenheit/32
# Example response: {"input_value": 32, "input_unit": "Fahrenheit", "output_value": 0.0, "output_unit": "Celsius"}
@app.get("/convert/fahrenheit/{value}", response_model=ConversionResult)
def convert_fahrenheit(value: float):
    return ConversionResult(
        input_value=value,
        input_unit="Fahrenheit",
        output_value=fahrenheit_to_celsius(value),
        output_unit="Celsius",
    )
