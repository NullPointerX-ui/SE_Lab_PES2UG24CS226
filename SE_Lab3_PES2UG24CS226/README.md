# Lab 3 – Component Modelling & Architectural Pattern Selection

## Project Title
**Self-Service Airport Check-In Kiosk System**

## Student Details
- **Name:** Khush Bhardwaj
- **SRN:** PES2UG24CS226
- **Section:** D

## Overview
This lab focuses on modelling the software architecture of a Self-Service Airport Check-In Kiosk using a UML Component Diagram. The system allows passengers to check in independently by scanning their passport or booking reference, selecting or confirming their seats, and receiving their boarding passes and baggage tags.

## Architectural Pattern
**Layered Architecture**

The Layered Architecture pattern was selected because it provides a clear separation of responsibilities, simplifies maintenance, and is suitable for a self-contained kiosk system.

The architecture consists of four layers:

1. **Presentation Layer**
   - User Interface Component
   - Handles passenger interaction through the kiosk touchscreen.

2. **Business Layer**
   - Check-in Manager Component
   - Seat Selection Service Component
   - Manages check-in operations, seat selection, and business logic.

3. **Integration Layer (Hardware & External Services)**
   - Passport / Boarding-Pass Scanner Component
   - Boarding Pass & Bag-Tag Printer Component
   - Handles communication with external hardware devices.

4. **Data Layer**
   - Reservation Database Component
   - Stores and manages passenger reservation and seat information.

## Architectural Justification
Layered Architecture was chosen over Microservices and Client-Server architectures for the following reasons:

- **Separation of Concerns:** Each layer has a clearly defined responsibility, allowing individual components to be modified independently.
- **Simplicity:** The architecture avoids the unnecessary operational complexity of Microservices for a single-purpose physical kiosk.
- **Maintainability:** Hardware components, business logic, and data storage can be updated independently.
- **Security:** All reservation and passenger data requests pass through the Business Layer, preventing direct access from the Presentation Layer.
- **Performance:** Well-defined interfaces allow efficient reservation lookups and hardware operations, helping maintain responsiveness during peak check-in periods.

## UML Component Diagram
The component diagram illustrates the four architectural layers, their respective components, and the interfaces connecting them.

## Tools Used
- **draw.io (diagrams.net):** Used to create the UML Component Diagram.
- **PDF Export:** Used to prepare the component diagram and written justification for submission.
