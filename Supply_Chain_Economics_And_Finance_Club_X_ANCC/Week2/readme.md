# CAIC Summer of Tech (CSoT)
## Week 2 - Parcel Delivery Planner

**By Economics and Finance Club X ANCC**

---

## 📦 Introduction

In Week 2, participants will deepen their understanding of **supply chain systems** by exploring the movement of parcels across a network of interconnected locations. This scenario models real-world challenges in ensuring timely and cost-effective delivery.

Parcels must navigate from **warehouses to recipients** through hubs, depots, and transfer points. Participants will represent these delivery systems as facilities connected by delivery routes.

This week's tasks will focus on:

- 🔍 Determining the **fastest and most efficient** parcel routes.
- 📦 Managing **multiple simultaneous deliveries** under capacity constraints.
- ⏱️ Understanding how **congestion or delays** impact delivery performance.

By evaluating strategies and trade-offs in resource allocation, participants will gain insights into the **complexity and challenges** of real-world logistics.

---

## 1. Background

Efficient parcel delivery planning is critical in today's logistics environment. Customers may prioritize:

- Shortest delivery time (fewest hubs).
- Cheapest delivery cost.
- A balanced trade-off between the two.

The goal is to design **optimal routes** using a set of **delivery legs**, where each leg represents a segment between two hubs.

### Objectives:

- Minimize the **number of transfer hubs**.
- Reduce **total shipping cost**.
- Balance **both time and cost**.

Each hub introduces a **minimum transfer time** due to sorting and rerouting operations.

---

## 2. Modelling

### 2.1 Representation

- **Hubs**: Represented by integers `{1, 2, ..., n}`.
- **Time**: Modeled in **minutes**.
- **Delivery Leg Attributes**:
  - `Leg ID`: Unique integer `{1, 2, ..., m}`
  - `Start Hub`, `Departure Time`
  - `End Hub`, `Arrival Time`
  - `Cost`

### 2.2 Constraints

- ⛔ **Max Capacity**: Each hub can handle **100 delivery legs** arriving or departing.
- ⏳ **Transfer Time**: A package must wait **≥ 20 minutes** before departing on the next leg.

---

## 3. Tasks

Given:

- Source hub **A**
- Destination hub **B**
- Starting time `t1`
- Deadline `t2`

Implement logic to find:

### Route 1: Fewest Legs & Earliest Arrival
- Minimize number of delivery legs.
- Break ties with **earliest arrival**.

### Route 2: Cheapest Route
- Minimize **total delivery cost**, regardless of legs.

### Route 3: Fewest Legs & Cheapest
- Minimize number of legs.
- Among those, choose **lowest cost**.

---

## 4. Requirements

Implement a **Planner module** with:

### Initialization
- Accept a list of delivery legs.
- Remains constant during queries.

### Route-Finding Functions

Each function accepts:  
`start_hub`, `end_hub`, `t1`, `t2`

- `fewest_legs_earliest_route`
- `cheapest_route`
- `fewest_legs_cheapest_route`

Each should return a **chronologically ordered list** of delivery legs.

---

## 5. Complexity

- `initialization`: **O(m)**
- `fewest_legs_earliest_route`: **O(m)**
- `cheapest_route`: **O(m log m)**
- `fewest_legs_cheapest_route`: **O(m log m)**

---

## 6. Notes

- The route output must be an **ordered list**:  
  `route[0], route[1], ...`

---

Happy Planning!
