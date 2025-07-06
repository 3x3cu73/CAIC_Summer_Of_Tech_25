# 🚁 Alice’s Delivery Sprint

Alice the delivery drone must deliver packages across a city to maximize her total reward, based on delivery times and decreasing rewards.

---

## 🧠 Problem Statement

Alice starts from the hub at coordinates **(0, 0)** and must deliver to **n** locations. Each location has:

- Coordinates: **(x, y)**
- A **reward** value `v`
- A **Deadline** and an **Expire** time

The **reward** decreases **linearly** from full value at `Deadline` to **0** at `Expire`.

Your task is to compute the **optimal delivery sequence** that **maximizes Alice’s total reward**.

---

## 📝 Input Format

1. An integer `n` — number of delivery locations.  
2. `n` lines of three integers: `x`, `y`, and `v` — location coordinates and full reward.  
3. A float `s` — speed of Alice.  
4. Two floats — `Deadline` and `Expire`.

### 🧱 Constraints

- `1 ≤ n ≤ 10`  
- `0 ≤ x, y, v ≤ 10^6`  
- `0 < s ≤ 10^6`  
- `0 ≤ Deadline < Expire ≤ 10^6`  

---

## 🧾 Output Format

1. An integer `X` — number of locations visited.  
2. A space-separated list of `X` integers — indices (0-based) of visited locations, in order.

---

## 🧮 Scoring

Your score is calculated as:

```
score = (Total reward earned / Total possible reward) × 200
```

---

## 📦 Example

### Input
```
2
3 4 10
6 8 20
1
5 15
```

### Output
```
2
0 1
```

### Explanation

- Alice starts at `(0, 0)`
- She travels to point `0`, then to point `1`
- Reward is calculated based on **arrival time**:
  - If `arrival_time ≤ Deadline` → reward = full `v`  
  - If `arrival_time ≥ Expire` → reward = `0`  
  - Otherwise → reward is linearly interpolated between `v` and `0`  

---

## 💡 Goal

Maximize the **total reward** by choosing the best **subset and order** of delivery locations.
