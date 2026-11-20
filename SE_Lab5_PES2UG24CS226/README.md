# SE Lab 5 — Static Code Analysis

**Name:** Khush Bhardwaj
**SRN:** PES2UG24CS226
**Scenario:** Smart Home Device Controller

## Files

| File | Description |
|------|-------------|
| `smart_home.py` | The cleaned controller — 11 issues fixed, Pylint 10.00/10 |
| `issues.md` | Issue table: what each tool found, where, why it matters, how it was fixed |
| `reflection.md` | Answers to the four reflection questions |
| `pylint_report.txt` / `bandit_report.txt` / `flake8_report.txt` | Tool output on the cleaned file |
| `*_report_before.txt` | Tool output on the original file, kept for comparison |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.80/10 | **10.00/10** |
| Bandit | 1 HIGH, 1 MEDIUM, 2 LOW | 0 HIGH, 0 MEDIUM, 2 LOW (informational) |
| Flake8 | 4 issues | **0 issues** |

The functional bug: a mutable default argument (`settings={}`) made every device share one
settings dictionary, so setting the thermostat to 30 also gave the ceiling light a
temperature. The demo printed `Light settings: {'temperature': 30}` for a lamp; it now
prints `Light settings: {}`.

## Reproducing

```bash
python smart_home.py
python -m pylint smart_home.py
python -m bandit -r smart_home.py
python -m flake8 smart_home.py
```
