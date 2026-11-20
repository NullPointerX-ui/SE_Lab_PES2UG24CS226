"""Lab 6: Code and Branch Coverage for the Highway Toll Calculator.

Name: Khush Bhardwaj      SRN: PES2UG24CS226
Scenario: L6_L7_36 Highway Toll Calculator

Run with:
    pytest test_highway_toll.py -v
    pytest --cov=highway_toll --cov-branch --cov-report=term-missing
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice

# Example test cases:
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# ---------------------------------------------------------------------------
# toll_for: the guard clause  (if axles < 2)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("axles", [1, 0, -1, -10])
def test_toll_for_rejects_fewer_than_two_axles(axles):
    """Below the minimum axle count the function must refuse, not price."""
    with pytest.raises(ValueError):
        toll_for(axles, False, False)


def test_toll_for_accepts_exactly_two_axles():
    """Boundary: 2 is the lowest accepted axle count."""
    assert toll_for(2, False, False) == 100


# ---------------------------------------------------------------------------
# toll_for: base rate lookup  (if axles in BASE_TOLL / else 400)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("axles, expected", [(2, 100), (3, 150), (4, 250)])
def test_base_toll_from_table(axles, expected):
    """Every axle count listed in BASE_TOLL takes the table branch."""
    assert toll_for(axles, False, False) == expected


@pytest.mark.parametrize("axles", [5, 6, 10, 18])
def test_base_toll_falls_back_to_flat_rate(axles):
    """Any axle count above the table takes the else branch: a flat 400."""
    assert toll_for(axles, False, False) == 400


# ---------------------------------------------------------------------------
# toll_for: peak surcharge  (if is_peak)
# ---------------------------------------------------------------------------

def test_peak_adds_twenty_five_percent():
    assert toll_for(2, True, False) == 125.0


def test_off_peak_charges_the_base_rate():
    assert toll_for(2, False, False) == 100


def test_peak_applies_to_the_flat_rate_too():
    assert toll_for(5, True, False) == 500.0


# ---------------------------------------------------------------------------
# toll_for: FASTag discount  (if has_fastag -> if axles == 2 / else)
# ---------------------------------------------------------------------------

def test_fastag_gives_two_axle_vehicles_ten_percent():
    """Two axles take the inner if: 100 * 0.90."""
    assert toll_for(2, False, True) == 90.0


@pytest.mark.parametrize("axles, expected", [(3, 142.5), (4, 237.5), (5, 380.0)])
def test_fastag_gives_larger_vehicles_five_percent(axles, expected):
    """More than two axles takes the inner else: base * 0.95."""
    assert toll_for(axles, False, True) == expected


def test_no_fastag_means_no_discount():
    assert toll_for(3, False, False) == 150


# ---------------------------------------------------------------------------
# toll_for: both multipliers together, and the rounding
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "axles, expected",
    [
        (2, 112.5),    # 100 * 1.25 * 0.90
        (3, 178.12),   # 150 * 1.25 * 0.95 = 178.125, rounded half-to-even
        (4, 296.88),   # 250 * 1.25 * 0.95 = 296.875, rounded half-to-even
        (5, 475.0),    # 400 * 1.25 * 0.95
    ],
)
def test_peak_and_fastag_combine(axles, expected):
    assert toll_for(axles, True, True) == expected


def test_result_is_rounded_to_two_decimals():
    """round(x, 2) must never leave more than two decimal places."""
    value = toll_for(3, True, True)
    assert value == round(value, 2)


# ---------------------------------------------------------------------------
# toll_charge: the exemption branch  (if vehicle in EXEMPT)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("vehicle", ["ambulance", "fire_engine"])
def test_exempt_vehicles_pay_nothing(vehicle):
    """Both exempt vehicles are free whatever the axles, hour or tag."""
    assert toll_charge(vehicle, 2, False, False) == 0
    assert toll_charge(vehicle, 6, True, True) == 0


@pytest.mark.parametrize("vehicle", ["car", "truck", "bus", "AMBULANCE", ""])
def test_non_exempt_vehicles_are_charged(vehicle):
    """Anything not in EXEMPT falls through to toll_for (the match is
    case-sensitive, so 'AMBULANCE' is charged)."""
    assert toll_charge(vehicle, 2, False, False) == 100


def test_toll_charge_passes_its_arguments_through():
    assert toll_charge("truck", 3, True, True) == toll_for(3, True, True)


def test_toll_charge_propagates_invalid_axle_count():
    """A non-exempt vehicle with a bad axle count still raises."""
    with pytest.raises(ValueError):
        toll_charge("car", 1, False, False)


# ---------------------------------------------------------------------------
# pass_advice: the three outcomes, and the empty-loop branch
# ---------------------------------------------------------------------------

def test_pass_advice_recommends_buying_when_trips_cost_more():
    """4 off-peak two-axle trips = 400 > a 300 pass."""
    trips = [(False, False)] * 4
    assert pass_advice(trips, 2, 300) == "buy_pass"


def test_pass_advice_says_either_when_the_costs_match():
    """3 off-peak two-axle trips = 300, exactly the pass price."""
    trips = [(False, False)] * 3
    assert pass_advice(trips, 2, 300) == "either"


def test_pass_advice_recommends_paying_per_trip_when_cheaper():
    """2 off-peak two-axle trips = 200 < a 300 pass."""
    trips = [(False, False)] * 2
    assert pass_advice(trips, 2, 300) == "pay_per_trip"


def test_pass_advice_with_no_trips_skips_the_loop():
    """Branch coverage: the for-loop must also be exercised zero times.
    No trips cost nothing, so a pass priced above zero is never worth it."""
    assert pass_advice([], 2, 300) == "pay_per_trip"


def test_pass_advice_with_no_trips_and_a_free_pass():
    """Boundary: cost 0 against a price of 0 is the 'either' branch."""
    assert pass_advice([], 2, 0) == "either"


def test_pass_advice_mixes_peak_and_fastag_trips():
    """A realistic week: the running total must add each trip's own price."""
    trips = [(True, True), (False, False), (True, False), (False, True)]
    expected = (
        toll_for(2, True, True)
        + toll_for(2, False, False)
        + toll_for(2, True, False)
        + toll_for(2, False, True)
    )
    assert expected == pytest.approx(427.5)
    assert pass_advice(trips, 2, 500) == "pay_per_trip"
    assert pass_advice(trips, 2, 400) == "buy_pass"


def test_pass_advice_propagates_invalid_axle_count():
    with pytest.raises(ValueError):
        pass_advice([(False, False)], 1, 300)
