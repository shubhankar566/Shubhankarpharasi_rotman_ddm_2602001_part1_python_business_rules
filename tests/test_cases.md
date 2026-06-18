# Test Cases

These test cases were created by manually working through the business
rules defined in `README.md`, and then verified by actually running the
program with these exact inputs to confirm the output matches.

---

### Test Case 1: High income, high savings, strong credit -> Low Risk / High Value
**Feature:** Customer Profile & Financial Summary

**Inputs:**
- Age: 35, City: Bangalore, Monthly Income: 150000, Monthly Expenses: 40000
- Existing EMI: 10000, Credit Score: 780, Segment: Enterprise

**Expected Output:**
- Monthly Savings: Rs. 100000.00
- Savings Percentage: 66.67%
- EMI-to-Income Ratio: 0.07
- Risk Category: Low Risk
- Value Category: High Value

**Reason:** EMI ratio (0.07) is below 0.30 and credit score (780) is above
700, satisfying the Low Risk rule. Income is above Rs. 1,00,000 (+2 points)
and savings % is above 30% (+2 points) = 4 points = High Value.

---

### Test Case 2: Low income, high EMI burden, poor credit -> High Risk / Low Value
**Feature:** Customer Profile & Financial Summary

**Inputs:**
- Age: 40, City: Delhi, Monthly Income: 30000, Monthly Expenses: 20000
- Existing EMI: 18000, Credit Score: 500, Segment: Standard

**Expected Output:**
- Monthly Savings: Rs. -8000.00 (negative)
- Savings Percentage: -26.67%
- EMI-to-Income Ratio: 0.60
- Risk Category: High Risk
- Value Category: Low Value

**Reason:** EMI ratio (0.60) exceeds the Medium Risk limit (0.50), so the
customer automatically falls into High Risk regardless of credit score.
Negative savings percentage and low income give 0 points = Low Value.

---

### Test Case 3: Loan rejected due to age outside allowed range
**Feature:** Loan Eligibility Decision

**Inputs:**
- Age: 65, City: Chennai, Monthly Income: 60000, Existing EMI: 5000
- Credit Score: 750, Requested Loan Amount: 100000

**Expected Output:**
- Decision: Rejected
- Reason: Applicant age (65) is outside the eligible range of 21-60 years.

**Reason:** The loan rule rejects applicants outside 21-60 years old
immediately, before checking any other factor.

---

### Test Case 4: Loan approved - all factors healthy
**Feature:** Loan Eligibility Decision

**Inputs:**
- Age: 35, Monthly Income: 150000, Existing EMI: 10000, Credit Score: 780
- Savings Percentage (calculated): 66.67%, Requested Loan Amount: 1000000

**Expected Output:**
- Decision: Approved
- Reason: Credit score is strong, EMI-to-income ratio is healthy, savings
  percentage is decent, and the requested loan amount is reasonable
  compared to income.

**Reason:** Credit score (780) >= 650, EMI ratio (0.07) <= 0.40, savings %
(66.67%) >= 15%, and loan amount (10,00,000) is within 20x monthly income
(20 x 150000 = 30,00,000). All four approval conditions are satisfied.

---

### Test Case 5: Loan sent to Manual Review due to borderline credit score
**Feature:** Loan Eligibility Decision

**Inputs:**
- Age: 30, Monthly Income: 50000, Monthly Expenses: 25000, Existing EMI: 5000
- Credit Score: 600, Requested Loan Amount: 300000

**Expected Output:**
- Decision: Manual Review Required
- Reason: Credit score (600) is acceptable but not strong enough for
  automatic approval; needs human judgement.

**Reason:** Credit score (600) is above the hard rejection limit (550) but
below the auto-approval limit (650), and the customer is not otherwise
disqualified, so the case goes to manual review.

---

### Test Case 6: Billing - delivery charge waived above threshold
**Feature:** Product Billing Calculator

**Inputs:**
- Product: Laptop, Quantity: 1, Unit Price: 60000
- Discount: 5%, GST: 18%, Delivery Charge entered: 300

**Expected Output:**
- Gross Amount: Rs. 60000.00
- Discount Amount: Rs. 3000.00
- Amount After Discount: Rs. 57000.00
- GST Amount: Rs. 10260.00
- Delivery Charge Applied: Rs. 0.00 (Waived)
- Final Payable Amount: Rs. 67260.00

**Reason:** Amount after discount + GST = 57000 + 10260 = 67260, which is
above the DELIVERY_WAIVER_THRESHOLD constant (Rs. 5000), so the delivery
charge is waived regardless of what the user entered.

---

### Test Case 7: Billing - delivery charge applied below threshold
**Feature:** Product Billing Calculator

**Inputs:**
- Product: Pen, Quantity: 5, Unit Price: 10
- Discount: 0%, GST: 5%, Delivery Charge entered: 50

**Expected Output:**
- Gross Amount: Rs. 50.00
- Discount Amount: Rs. 0.00
- Amount After Discount: Rs. 50.00
- GST Amount: Rs. 2.50
- Delivery Charge Applied: Rs. 50.00
- Final Payable Amount: Rs. 102.50

**Reason:** Amount after discount + GST = 50 + 2.5 = 52.5, which is below
the Rs. 5000 waiver threshold, so the user-entered delivery charge of
Rs. 50 is applied as-is.

---

### Test Case 8: Campaign Eligibility - Premium Upsell Campaign
**Feature:** Campaign Eligibility

**Inputs:** Same customer as Test Case 1 (Enterprise segment, High Value)

**Expected Output:**
- Assigned Campaign: Premium Upsell Campaign

**Reason:** Customer's segment is Enterprise and Value Category is High
Value, which directly satisfies the first (highest priority) campaign rule.

---

### Test Case 9 (Invalid Input): Negative age
**Feature:** Input Validation - Customer Profile

**Input:** Age entered as `-5`

**Expected Output:**
"Invalid input. Age cannot be negative. Please try again." is printed,
and the program asks for age again instead of crashing or accepting -5.

**Reason:** The `get_age()` function in `utils.py` explicitly checks for
`value < 0` and re-prompts the user, satisfying the input validation
requirement.

---

### Test Case 10 (Invalid Input): Credit score outside 300-900 range
**Feature:** Input Validation - Customer Profile

**Input:** Credit Score entered as `950`

**Expected Output:**
"Invalid input. Credit score must be between 300 and 900." is printed,
and the program asks for the credit score again.

**Reason:** The `get_credit_score()` function checks
`value < MIN_CREDIT_SCORE or value > MAX_CREDIT_SCORE` (300/900) and
rejects any value outside this range.

---

### Test Case 11 (Invalid Input): Invalid customer segment text
**Feature:** Input Validation - Customer Profile

**Input:** Segment entered as `FancySegment`

**Expected Output:**
"Invalid input. Segment must be one of: Standard, Premium, Enterprise."
is printed, and the program asks for the segment again.

**Reason:** `get_customer_segment()` only accepts values matching
Standard, Premium, or Enterprise (case-insensitive) and rejects anything
else by looping until valid input is given.

---

### Test Case 12 (Invalid Input): Negative monthly income
**Feature:** Input Validation - Customer Profile

**Input:** Monthly Income entered as `-2000`

**Expected Output:**
"Invalid input. This value cannot be negative. Please try again." is
printed, and the program asks for monthly income again.

**Reason:** `get_non_negative_float()` checks `value < 0` for any
financial field (income, expenses, EMI, unit price) and rejects negative
numbers with a clear message, then re-prompts.

---

### Test Case 13 (Invalid Input): Quantity entered as zero
**Feature:** Input Validation - Product Billing

**Input:** Quantity entered as `0`

**Expected Output:**
"Invalid input. Quantity must be greater than 0. Please try again." is
printed, and the program asks for quantity again.

**Reason:** `get_positive_int()` explicitly requires `value > 0` for
quantity, since an order of zero items does not make sense, and
re-prompts on failure.
