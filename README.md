Here's the full `README.md` for the repo root — copy everything inside the block:

````markdown
# SE_Lab_PES2UG24CS226

Software Engineering Laboratory — coursework repository.

| | |
|---|---|
| **Name** | Khush Bhardwaj |
| **SRN** | PES2UG24CS226 |
| **Section** | D |
| **Scenario (Labs 1–7)
| **Domain** | Retail, E-Commerce & Finance |
| **Stakeholders** | Diner, Restaurant Manager |

---

## Repository structure

| Folder | Lab | Focus |
|--------|-----|-------|
| `SE_Lab1_PES2UG24CS226` | Lab 1 | Requirements Engineering & UML Use-Case Modelling |
| `SE_Lab2_PES2UG24CS226` | Lab 2 | Agile Backlog Creation & Sprint Simulation in Jira |
| `SE_Lab3_PES2UG24CS226` | Lab 3 | Component Modelling & Architectural Pattern Selection |
| `SE_Lab4_PES2UG24CS226` | Lab 4 | Dino Run Repair Lab — LLM-assisted debugging |
| `SE_Lab5_PES2UG24CS226` | Lab 5 | Static Code Analysis |
| `SE_Lab6_PES2UG24CS226` | Lab 6 | Code and Branch Coverage |
| `SE_Lab7_PES2UG24CS226` | Lab 7 | Fuzzing for Input Validation Bugs |

---

## Lab 1 — Requirements Engineering & UML Use-Case Modelling

Elicited requirements for the Restaurant Table Booking & Pre-Ordering App and modelled
them in UML.

- **Requirements table** — 5 functional and 2 nonfunctional requirements, each with
  priority, measurable acceptance criteria, rationale and peer-review comments.
- **Use-case diagram** — 4 actors (Diner, Restaurant Manager, Payment Gateway,
  Kitchen Display System), 7 use cases, system boundary, one `«include»` and one `«extend»`.
- **Use-case flow** — UC-02 *Book a Table*: main success scenario plus five alternate
  flows covering no availability, hold expiry, concurrent booking, declined payment and
  manager rejection.

Key requirements: FR-001 search availability · FR-002 reserve with a 10-minute hold ·
FR-003 pre-order menu items · FR-004 refundable deposit · FR-005 manager confirms or
rejects · NFR-001 search under 3 s at the 95th percentile with 500 concurrent users ·
NFR-002 no raw card data stored.

## Lab 2 — Agile Backlog Creation & Sprint Simulation in Jira

The Lab 1 requirements turned into an Agile backlog and run through two sprints.

- **4 epics**, **13 user stories** in *As a / I want / So that* form, prioritised and
  estimated on the Fibonacci scale by planning poker — 49 points total.
- **Sprint 1** — 22 points committed, 19 completed, one story carried over.
- **Sprint 2** — 24 points committed, 19 completed.
- **Observed velocity** — about 19 points per one-week sprint, roughly 15% below what
  was committed in both sprints.

Built in Jira as a company-managed Scrum project (space key `RTBPOA`).

## Lab 3 — Component Modelling & Architectural Pattern Selection

Evaluated Layered, Client-Server and Microservices architectures and selected one for
the booking system.

- **Component diagram** — 7 internal components plus 2 external systems, 8
  provided/required interface pairs in ball-and-socket notation, 2 `«use»` dependencies.
- **Written justification** — the three-style comparison, the choice of **Microservices**,
  two scenario-specific reasons, a security advantage and a performance benefit.

Chosen because search traffic spikes independently of payments and must scale on its
own, and because a payment-gateway outage must not stop diners booking tables.

## Lab 4 — Dino Run Repair Lab

A single-file Pygame endless runner with one deliberate bug and three unimplemented
features, repaired with an LLM as a pair-programming partner.

- **Bug fixed** — the high score never saved. The comparison after a collision was
  backwards (`self.high_score > current` instead of `current > self.high_score`), so on a
  fresh install the record was never written, and an existing record would have been
  overwritten by a worse run.
- **`dino_tint()`** — the dino turns blue while airborne and green on the ground.
- **`on_obstacle_passed()`** — a combo counter with a floating "+1", a session best, and
  a reset on each new run.
- **`max_jumps()`** — returns 2, giving a double jump.

`game_original.py` is kept alongside so the "before" behaviour can be recorded.

## Lab 5 — Static Code Analysis

A smart home device controller analysed with Pylint, Bandit and Flake8, then cleaned up.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.80/10 | **10.00/10** |
| Bandit | 1 HIGH, 1 MEDIUM, 2 LOW | 0 HIGH, 0 MEDIUM, 2 LOW (informational) |
| Flake8 | 4 issues | **0 issues** |

Eleven issues documented and fixed, including a `shell=True` command injection, a
hardcoded password, a bind to `0.0.0.0`, and an unhandled `KeyError`.

The functional bug no tool called a bug: a mutable default argument (`settings={}`) made
every device share one settings dictionary, so setting the thermostat to 30 also gave the
ceiling light a temperature. Found by reading the program's output, not the reports.

## Lab 6 — Code and Branch Coverage

A test suite for a highway toll calculator, measured with `pytest-cov`.

```
Name              Stmts   Miss Branch BrPart  Cover
---------------------------------------------------
highway_toll.py      28      0     18      0   100%
```

**43 tests — 100% statement coverage and 100% branch coverage.**

Two things branch coverage caught that statement coverage did not: the `for` loop over
trips never exercised with an empty list, and `round()` using half-to-even, so
`toll_for(3, True, True)` is 178.12 rather than the hand-calculated 178.13.

## Lab 7 — Fuzzing for Input Validation Bugs

The same toll module fuzzed with Hypothesis-generated text and `None`.

The fuzzer crashed all three functions — `AttributeError` on `None`, unpacking errors on
malformed plates, negative tolls from negative trip counts, and out-of-range axle counts
silently classified as vehicles. Each function now validates against a strict ASCII regex
and raises `ValueError`, so every input either returns a sane result or is rejected
cleanly. Regression tests pin each bug the fuzzer found.

---

## Running the code labs

```bash
# Lab 4
pip install pygame
python game.py

# Lab 5
pip install pylint bandit flake8
python smart_home.py
python -m pylint smart_home.py

# Lab 6
pip install pytest pytest-cov
pytest test_highway_toll.py -v --cov=highway_toll --cov-branch --cov-report=term-missing

# Lab 7
pip install pytest hypothesis
pytest test_highway_toll.py -q
```

## Tools used

Draw.io / vector UML · Jira (company-managed Scrum) · Python 3.13 · Pygame · Pylint ·
Bandit · Flake8 · pytest · pytest-cov · Hypothesis
````
