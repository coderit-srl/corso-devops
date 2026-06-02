# pytest discovers and runs any file named test_*.py automatically.
# We test converter.py directly — no HTTP server needed — because the logic lives
# in a separate module with no framework dependency.
import pytest
from app.converter import celsius_to_fahrenheit, fahrenheit_to_celsius


# Grouping tests in classes is optional but keeps related cases together.
class TestCelsiusToFahrenheit:

    def test_freezing_point(self):
        # 0 °C is the most basic known conversion — a good sanity check.
        assert celsius_to_fahrenheit(0) == 32.0

    def test_boiling_point(self):
        # 100 °C → 212 °F is the second universally-known reference point.
        assert celsius_to_fahrenheit(100) == 212.0

    def test_body_temperature(self):
        # 37 °C → 98.6 °F — tests that decimal results are handled correctly.
        assert celsius_to_fahrenheit(37) == 98.6

    def test_negative_value(self):
        # -40 is the unique value where both scales are equal — tests symmetry.
        assert celsius_to_fahrenheit(-40) == -40.0

    def test_return_type(self):
        # Confirms the function always returns a float, never an int.
        assert isinstance(celsius_to_fahrenheit(0), float)


class TestFahrenheitToCelsius:

    def test_freezing_point(self):
        assert fahrenheit_to_celsius(32) == 0.0

    def test_boiling_point(self):
        assert fahrenheit_to_celsius(212) == 100.0

    def test_negative_value(self):
        # Again, -40 is the fixed point — both directions must agree.
        assert fahrenheit_to_celsius(-40) == -40.0

    def test_return_type(self):
        assert isinstance(fahrenheit_to_celsius(32), float)


class TestRoundTrip:

    # @pytest.mark.parametrize runs the same test with multiple inputs.
    # This replaces writing one test function per value.
    @pytest.mark.parametrize("value", [-100, -40, 0, 20, 37, 100])
    def test_celsius_round_trip(self, value):
        # Convert C → F → C: the result must equal the original value.
        # This catches rounding bugs that individual tests might miss.
        assert fahrenheit_to_celsius(celsius_to_fahrenheit(value)) == value
