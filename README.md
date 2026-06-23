# Business Rules Console Application

**Assignment:** Part 1 - Python Business Rules Console Application
**Student Name:** Shubhankar Pharasi
**Student ID:** rotman_ddm_2602001

---

## Problem Summary

This is a menu-driven, command-line Python application that helps a
business team evaluate customers, calculate billing amounts, and make
decision recommendations. The program keeps running in a loop, showing a
menu, until the user chooses to exit. The logic is split across multiple
files inside the `src/` folder rather than being written entirely in
`main.py`.

---

## Features Implemented

1. **Customer Profile and Financial Summary** - collects customer details
   and calculates monthly savings, savings percentage, EMI-to-income
   ratio, a Risk Category, and a Value Category.
2. **Product Billing Calculator** - collects product/order details and
   calculates gross amount, discount, GST, delivery charge (with a
   waiver rule), and the final payable amount.
3. **Loan Eligibility Decision** - uses the customer's profile plus a
   requested loan amount to decide Approved / Rejected / Manual Review
   Required, along with a clear reason.
4. **Campaign Eligibility** - assigns the customer to one of four
   marketing campaign groups based on segment, city, savings percentage,
   and value category, with a reason for the assignment.
5. **Input Validation and Error Handling** - every numeric and
   text input is validated. Invalid input never crashes the program;
   instead, an error message is shown and the user is asked to
   re-enter the value.

---

## Business Rules Used

All thresholds mentioned below are defined as constants in
`src/utils.py`, so they can be changed in one place if business
requirements change later.

### 1. Risk Category (in `src/customer.py` -> `determine_risk_category`)

The two factors used are **EMI-to-Income Ratio** and **Credit Score**.

| Risk Category | Condition |
|---|---|
| **Low Risk**    | EMI-to-income ratio < 0.30 **AND** credit score >= 700 |
| **Medium Risk** | EMI-to-income ratio < 0.50 **AND** credit score >= 550 |
| **High Risk**   | Anything that does not satisfy the above two rules |

**Why this rule makes sense:** A customer who spends less than 30% of
their income on existing EMI and has a strong credit history (700+) is
unlikely to default, so they are Low Risk. A customer with a moderate EMI
burden and an average credit score is Medium Risk. Anyone with a heavy
EMI burden (50%+ of income) or a poor credit score is High Risk,
regardless of the other factor, because either condition alone is a
serious red flag.

### 2. Value Category (in `src/customer.py` -> `determine_value_category`)

We use a simple points system based on **Monthly Income** and **Savings
Percentage**, since a genuinely valuable customer should both earn well
and manage their money well (just earning a lot but spending it all is
less valuable to a business than steady savers).

Points from income:
- +2 points if monthly income > Rs. 1,00,000
- +1 point if monthly income > Rs. 50,000
- +0 otherwise

Points from savings percentage:
- +2 points if savings percentage > 30%
- +1 point if savings percentage > 15%
- +0 otherwise

| Total Points | Value Category |
|---|---|
| 4 | High Value |
| 2 or 3 | Medium Value |
| 0 or 1 | Low Value |

### 3. Delivery Charge Waiver (in `src/billing.py` -> `determine_delivery_charge`)

If the amount after discount and GST is above the constant
`DELIVERY_WAIVER_THRESHOLD` (Rs. 5,000), the delivery charge is
automatically waived (set to Rs. 0), regardless of what the user entered.
This rewards larger orders, which is a common real-world e-commerce
practice.

### 4. Loan Eligibility (in `src/eligibility.py` -> `check_loan_eligibility`)

The decision logic is checked in a specific order:

**Step 1 - Hard rejection checks (checked first):**
- Age outside 21-60 years -> **Rejected**
- Monthly income is zero or less -> **Rejected**
- Credit score below 550 -> **Rejected**
- Requested loan amount is extremely large compared to income
  (more than 40x monthly income) -> **Rejected**

**Step 2 - Automatic approval (only if not already rejected):**
All four of these must be true together:
- Credit score >= 650
- EMI-to-income ratio <= 0.40
- Requested loan amount <= 20x monthly income
- Savings percentage >= 15%

If all four hold -> **Approved**.

**Step 3 - Manual Review Required:**
If the applicant was not rejected in Step 1 and did not meet all four
conditions in Step 2, the case is sent for **Manual Review Required**,
with a specific reason pointing out which factor was borderline (e.g.
"Credit score is acceptable, but EMI-to-income ratio is high.").

**Why this rule makes sense:** Clear-cut bad cases (too young/old, no
income, very poor credit, unrealistic loan size) are rejected outright to
save time. Clear-cut good cases are approved automatically. Everything
in between - which is common in the real world - is correctly routed to
a human for manual judgement instead of forcing a black-and-white
decision.

### 5. Campaign Eligibility (in `src/eligibility.py` -> `check_campaign_eligibility`)

Checked in priority order, and the customer is assigned to the **first**
matching group:

1. **Premium Upsell Campaign** - Segment is Premium or Enterprise **AND**
   Value Category is High Value. (Already valuable customers are good
   targets for premium product upselling.)
2. **Loan Offer Campaign** - Customer is not already High Value, but has
   savings percentage >= 15% **AND** lives in a recognised metro city
   (Mumbai, Delhi, Bangalore, Chennai, Kolkata, Hyderabad, Pune).
   (Decent savings + metro presence suggests good loan repayment ability.)
3. **Cashback Campaign** - Segment is Standard **AND** savings percentage
   is below 15%. (Used to encourage more engagement from cost-conscious
   customers who aren't saving much.)
4. **No Campaign** - Anyone who does not match any of the above rules.

---

## File Structure Explanation

```
shubhankarpharasi_260_part1_python_business_rules/
│
├── README.md
├── main.py
├── src/
│   ├── __init__.py
│   ├── customer.py
│   ├── billing.py
│   ├── eligibility.py
│   └── utils.py
├── outputs/
│   ├── sample_output.txt
│   └── screenshots/
└── tests/
    └── test_cases.md
```

**Why the code is split this way:** `utils.py` holds anything reused
everywhere (constants, input validation), so there is no repeated
code across files. `customer.py`, `billing.py`, and `eligibility.py`
each own exactly one feature area's business logic and display logic.
`main.py` stays small and only handles the menu loop and wiring
everything together, as required by the assignment.

---

## How to Run the Program

1. Make sure Python 3 is installed (`python3 --version` to check).
2. Open a terminal in the project's root folder (the one containing
   `main.py`).
3. Run:
   ```
   python3 main.py
   ```
   (On Windows, this may just be `python main.py`)
4. Use the on-screen menu (type 1-5 and press Enter) to navigate
   between features. Choose `5` to exit the program at any time.

No external libraries are required - the program only uses Python's
built-in features.

---

## Sample Input and Output

A complete sample run (and a second run showing invalid input handling)
is available in `outputs/sample_output.txt`. A short excerpt:

```
Enter customer name: Shubhankar Pharasi
Enter customer age: 29
Enter customer city: Mumbai
Enter monthly income (Rs.): 80000
Enter monthly expenses (Rs.): 30000
Enter existing EMI amount (Rs.): 10000
Enter credit score (300-900): 720
Enter customer segment (Standard/Premium/Enterprise): Premium

==================================================
CUSTOMER FINANCIAL SUMMARY
==================================================
Monthly Savings (Rs.)              : 40000.00
Savings Percentage                 : 50.00%
EMI-to-Income Ratio                : 0.12
Risk Category                      : Low Risk
Value Category                     : Medium Value
```

See `tests/test_cases.md` for 13 fully worked test cases with expected
output and the reasoning behind each one.

---

## Screenshots

See `outputs/screenshots/`. (A note inside that folder explains exactly
how to capture and add your own screenshots of the program running.)

---

## Assumptions Made

- Currency is assumed to be Indian Rupees (Rs.), since the assignment
  mentions GST, which is an Indian tax.
- "Monthly Savings" is calculated as `Income - Expenses - Existing EMI`,
  i.e. EMI is treated as a committed monthly outflow, not part of
  "expenses" already.
- If monthly income is entered as 0, Savings Percentage is shown as 0%
  (instead of crashing on a divide-by-zero error), and EMI-to-Income
  Ratio is treated as 1.0 (maximum) since any EMI with zero income is
  effectively unaffordable.
- GST is calculated on the amount **after** discount has been applied,
  not on the original gross amount, which matches how GST is generally
  applied in real billing.
- A fixed list of major Indian metro cities (Mumbai, Delhi, Bangalore /
  Bengaluru, Chennai, Kolkata, Hyderabad, Pune) is used for the "metro
  city" condition in the Campaign Eligibility rule; this list is defined
  as a constant and can be extended.
- The Loan Eligibility and Campaign Eligibility menu options (3 and 4)
  reuse the most recently entered customer profile within the same
  program run. If no customer has been entered yet, the program asks for
  one first instead of crashing or using empty data.
- Age input is capped at a realistic maximum (120) purely as a sanity
  check against typing mistakes (e.g. typing an extra digit).
