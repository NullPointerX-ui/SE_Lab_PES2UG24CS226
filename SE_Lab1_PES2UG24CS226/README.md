# SE Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Name:** Khush Bhardwaj
**SRN:** PES2UG24CS226
**Scenario 36:** Restaurant Table Booking & Pre-Ordering App
**Domain:** Retail, E-Commerce & Finance
**Stakeholders:** Diner, Restaurant Manager

## Deliverables

| File | Description |
|------|-------------|
| `PES2UG24CS226_Lab1_Requirements_Table.pdf` | Five functional and two nonfunctional requirements, each with priority, measurable acceptance criteria, rationale and the peer-critique comments |
| `PES2UG24CS226_Lab1_UseCase_Diagram.pdf` | UML use-case diagram: 4 actors, 7 use cases, system boundary, one «include» and one «extend» |
| `PES2UG24CS226_Lab1_UseCase_Flow.pdf` | Use-case flow for UC-02 *Book a Table* — main success scenario and five alternate flows |

## Summary

**Requirements.** FR-001 search availability, FR-002 reserve a slot with a 10-minute
hold, FR-003 pre-order menu items, FR-004 collect a refundable deposit, FR-005 manager
confirms or rejects a booking. NFR-001 covers search latency under peak load
(< 3 s at the 95th percentile, 500 concurrent users) and NFR-002 covers payment
security (no raw card data stored; tokenised by a PCI-DSS compliant gateway).

**Actors.** Diner, Restaurant Manager, Payment Gateway «external system», Kitchen
Display System «external system».

**Use cases.** UC-01 Search Table Availability, UC-02 Book a Table, UC-03 Pre-Order Menu
Items, UC-04 Make Payment, UC-05 Manage Bookings & Tables, UC-06 Apply Promo Code,
UC-07 Cancel / Modify Booking.

**Relationships.** UC-02 «include» UC-01, because a booking always checks availability
first. UC-03 «include» UC-04, because a pre-order always takes the deposit. UC-06
«extend» UC-04, because a promo code is applied only sometimes.
