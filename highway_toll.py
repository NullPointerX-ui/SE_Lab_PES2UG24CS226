import re

# Strict input formats. ASCII-only so that inputs such as Arabic-Indic digits,
# "1_0", "+5" or " 5 " (all accepted by a bare int()) are rejected.
_PLATE_RE = re.compile(r"[A-Za-z]{2}-[0-9]{1,2}-[A-Za-z]{1,3}-[0-9]{1,4}")
_TRIP_RE = re.compile(r"([0-9]{1,6})[xX]([0-9]{1,6})")
_AXLE_RE = re.compile(r"[0-9]{1,2}")

MIN_AXLES = 2
MAX_AXLES = 20


def _require_text(value, name):
    """Reject None and non-string input with a clear ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string, got {type(value).__name__}")
    return value.strip()


def parse_plate(plate):
    """Parse a plate such as 'KA-05-AB-1234' into (state, district, number)."""
    plate = _require_text(plate, "plate")
    if not _PLATE_RE.fullmatch(plate):
        raise ValueError(f"invalid plate {plate!r}; expected format KA-05-AB-1234")
    state, district, series, number = plate.split('-')
    return state.upper(), int(district), int(number)


def trip_cost(text):
    """Price 'trips x rate' text such as '3x150' -> 450."""
    text = _require_text(text, "trip text")
    match = _TRIP_RE.fullmatch(text)
    if not match:
        raise ValueError(f"invalid trip text {text!r}; expected format 3x150")
    count, rate = int(match.group(1)), int(match.group(2))
    if count == 0:
        raise ValueError("trip count must be at least 1")
    return count * rate


def axle_class(axles):
    """Classify a vehicle by its axle count ('2' -> car, 3-4 -> truck, 5+ -> heavy)."""
    axles = _require_text(axles, "axle count")
    if not _AXLE_RE.fullmatch(axles):
        raise ValueError(f"invalid axle count {axles!r}; expected a whole number")
    n = int(axles)
    if n < MIN_AXLES or n > MAX_AXLES:
        raise ValueError(f"axle count must be between {MIN_AXLES} and {MAX_AXLES}, got {n}")
    if n == 2:
        return 'car'
    if n <= 4:
        return 'truck'
    return 'heavy'


def main():
    try:
        print("==== Running parse_plate ====")
        user_input = input("Enter a plate (e.g. KA-05-AB-1234): ")
        result = parse_plate(user_input)
        print("State, District and Number:", result)

        print("\n==== Running trip_cost ====")
        user_input = input("Enter trips x rate (e.g. 3x150): ")
        result = trip_cost(user_input)
        print("Trip Cost:", result)

        print("\n==== Running axle_class ====")
        user_input = input("Enter an axle count (e.g. 3): ")
        result = axle_class(user_input)
        print("Vehicle Class:", result)
    except ValueError as err:
        print("Invalid input:", err)


if __name__ == "__main__":
    main()
