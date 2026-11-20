# SE Lab 6 — Code and Branch Coverage

**Name:** Khush Bhardwaj
**SRN:** PES2UG24CS226
**Scenario:** L6_L7_36 Highway Toll Calculator

## Files

| File | Description |
|------|-------------|
| `highway_toll.py` | The module under test (unchanged) |
| `test_highway_toll.py` | 43 tests covering every statement and every branch |
| `coverage_report.txt` | Saved `pytest --cov` output |

## Result

```
Name              Stmts   Miss Branch BrPart  Cover
---------------------------------------------------
highway_toll.py      28      0     18      0   100%
```

**43 passed — 100% statement coverage and 100% branch coverage.**

## How the branches are covered

| Code | Branches | Tests that reach them |
|------|----------|-----------------------|
| `if axles < 2` | raise / continue | `test_toll_for_rejects_fewer_than_two_axles` (1, 0, -1, -10), `test_toll_for_accepts_exactly_two_axles` (boundary 2) |
| `if axles in BASE_TOLL` | table / flat 400 | `test_base_toll_from_table` (2, 3, 4), `test_base_toll_falls_back_to_flat_rate` (5, 6, 10, 18) |
| `if is_peak` | ×1.25 / skip | `test_peak_adds_twenty_five_percent`, `test_off_peak_charges_the_base_rate` |
| `if has_fastag` | discount / skip | `test_fastag_*`, `test_no_fastag_means_no_discount` |
| `if axles == 2` (inner) | ×0.9 / ×0.95 | `test_fastag_gives_two_axle_vehicles_ten_percent`, `test_fastag_gives_larger_vehicles_five_percent` |
| `if vehicle in EXEMPT` | 0 / charge | `test_exempt_vehicles_pay_nothing`, `test_non_exempt_vehicles_are_charged` |
| `for ... in trips` | loop taken / **not taken** | all `pass_advice` tests, plus `test_pass_advice_with_no_trips_skips_the_loop` for the empty list |
| `cost > pass_price` / `cost == pass_price` / fall-through | all three | `..._recommends_buying`, `..._says_either`, `..._recommends_paying_per_trip` |

Two points worth noting:

- **The empty `trips` list is a branch, not an edge case.** Statement coverage is
  already 100% without it, because the loop body runs in the other tests. Only
  branch coverage shows that "the loop exits without ever running" was untested.
- **`round()` uses half-to-even.** `toll_for(3, True, True)` is 178.125 before
  rounding and comes out as **178.12**, not 178.13. The tests assert the real
  values rather than the hand-calculated ones.

## Reproducing

```bash
pip install pytest pytest-cov
pytest test_highway_toll.py -v --cov=highway_toll --cov-branch --cov-report=term-missing
```
