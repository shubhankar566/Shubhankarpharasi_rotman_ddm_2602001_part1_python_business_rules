"""
eligibility.py
---------------
Feature 3: Loan Eligibility Decision
Feature 4: Campaign Eligibility

This file uses the customer dictionary (built in customer.py) plus a
requested loan amount to decide:
- Loan decision: Approved / Rejected / Manual Review Required (+ reason)
- Campaign group: Premium Upsell / Loan Offer / Cashback / No Campaign (+ reason)
"""

from src import utils


# ---------------------------------------------------------
# FEATURE 3: LOAN ELIGIBILITY
# ---------------------------------------------------------

def get_requested_loan_amount():
    """Asks the user for the loan amount they want to apply for."""
    return utils.get_non_negative_float("Enter requested loan amount (Rs.): ")


def check_loan_eligibility(customer, requested_loan_amount):
    """
    BUSINESS RULE for Loan Eligibility (explained in detail in README.md):

    We check, in order, several disqualifying conditions first
    (these lead to a clear Rejected outcome). If none of those apply,
    we check whether the customer comfortably meets every condition for
    automatic Approval. If they are not clearly rejected and not clearly
    approved, the case goes to Manual Review Required.

    Factors used: age, monthly income, existing EMI, credit score,
    savings percentage, and requested loan amount.

    Returns a tuple: (decision, reason)
    """
    age = customer["age"]
    monthly_income = customer["monthly_income"]
    credit_score = customer["credit_score"]
    savings_percentage = customer["savings_percentage"]
    emi_ratio = customer["emi_to_income_ratio"]

    # --- Hard rejection conditions ---
    if age < utils.MIN_AGE_FOR_LOAN or age > utils.MAX_AGE_FOR_LOAN:
        return (
            "Rejected",
            f"Applicant age ({age}) is outside the eligible range of "
            f"{utils.MIN_AGE_FOR_LOAN}-{utils.MAX_AGE_FOR_LOAN} years.",
        )

    if monthly_income <= 0:
        return ("Rejected", "Applicant has no verifiable monthly income.")

    if credit_score < utils.MIN_CREDIT_SCORE_FOR_REVIEW:
        return (
            "Rejected",
            f"Credit score ({credit_score}) is below the minimum acceptable "
            f"score of {utils.MIN_CREDIT_SCORE_FOR_REVIEW}.",
        )

    if requested_loan_amount > monthly_income * utils.MAX_LOAN_TO_INCOME_MULTIPLIER * 2:
        return (
            "Rejected",
            f"Requested loan amount is far too high compared to monthly income "
            f"(more than {utils.MAX_LOAN_TO_INCOME_MULTIPLIER * 2}x monthly income).",
        )

    # --- Conditions for automatic approval ---
    # All of the following must be true at once for a clean Approved decision.
    good_credit = credit_score >= utils.MIN_CREDIT_SCORE_FOR_APPROVAL
    healthy_emi_ratio = emi_ratio <= utils.MAX_EMI_RATIO_FOR_APPROVAL
    reasonable_loan_size = requested_loan_amount <= monthly_income * utils.MAX_LOAN_TO_INCOME_MULTIPLIER
    decent_savings = savings_percentage >= utils.SAVINGS_PCT_MEDIUM_VALUE

    if good_credit and healthy_emi_ratio and reasonable_loan_size and decent_savings:
        return (
            "Approved",
            f"Credit score ({credit_score}) is strong, EMI-to-income ratio "
            f"({emi_ratio:.2f}) is healthy, savings percentage "
            f"({savings_percentage:.2f}%) is decent, and the requested loan "
            f"amount is reasonable compared to income.",
        )

    # --- Anything else falls into manual review, with a specific reason ---
    if not good_credit:
        return (
            "Manual Review Required",
            f"Credit score ({credit_score}) is acceptable but not strong enough "
            f"for automatic approval; needs human judgement.",
        )

    if not healthy_emi_ratio:
        return (
            "Manual Review Required",
            f"Credit score is acceptable, but EMI-to-income ratio "
            f"({emi_ratio:.2f}) is high.",
        )

    if not reasonable_loan_size:
        return (
            "Manual Review Required",
            "Requested loan amount is high relative to monthly income and "
            "needs manual assessment.",
        )

    return (
        "Manual Review Required",
        f"Savings percentage ({savings_percentage:.2f}%) is on the lower side; "
        f"other factors are acceptable, so this needs manual judgement.",
    )


def display_loan_decision(decision, reason):
    """Prints the loan decision and reason in a clean format."""
    utils.print_section_header("LOAN ELIGIBILITY DECISION")
    utils.print_line_item("Decision", decision)
    utils.print_line_item("Reason", reason)


# ---------------------------------------------------------
# FEATURE 4: CAMPAIGN ELIGIBILITY
# ---------------------------------------------------------

# Cities treated as "metro" cities for campaign targeting purposes.
# This is a simple business rule constant - can be extended easily.
METRO_CITIES = ["mumbai", "delhi", "bangalore", "bengaluru", "chennai", "kolkata", "hyderabad", "pune"]


def check_campaign_eligibility(customer):
    """
    BUSINESS RULE for Campaign Eligibility (explained in detail in README.md):

    Uses customer segment, city, savings percentage, and value category
    to assign exactly one campaign group, checked in priority order:

    1. Premium Upsell Campaign:
       Segment is Premium or Enterprise AND value category is High Value.
       (These are already valuable customers worth upselling premium products.)

    2. Loan Offer Campaign:
       Customer is NOT already High Value, but has decent savings
       percentage (>= SAVINGS_PCT_MEDIUM_VALUE) and lives in a metro city.
       (Good repayment potential + metro presence = good loan offer targets.)

    3. Cashback Campaign:
       Customer has low-to-medium savings percentage but is Standard segment.
       (Used to encourage engagement/spending from cost-conscious customers.)

    4. No Campaign:
       Anyone who does not fit the above rules.

    Returns a tuple: (campaign_name, reason)
    """
    segment = customer["segment"]
    city = customer["city"].strip().lower()
    savings_percentage = customer["savings_percentage"]
    value_category = customer["value_category"]

    is_metro = city in METRO_CITIES

    if segment in ("Premium", "Enterprise") and value_category == "High Value":
        return (
            "Premium Upsell Campaign",
            f"Customer is in the {segment} segment and falls under the "
            f"High Value category, making them a strong fit for premium "
            f"product upselling.",
        )

    if value_category != "High Value" and savings_percentage >= utils.SAVINGS_PCT_MEDIUM_VALUE and is_metro:
        return (
            "Loan Offer Campaign",
            f"Customer has a healthy savings percentage ({savings_percentage:.2f}%) "
            f"and resides in a metro city ({customer['city']}), indicating good "
            f"repayment capacity for a loan offer.",
        )

    if segment == "Standard" and savings_percentage < utils.SAVINGS_PCT_MEDIUM_VALUE:
        return (
            "Cashback Campaign",
            f"Customer is in the Standard segment with a relatively low "
            f"savings percentage ({savings_percentage:.2f}%), so a cashback "
            f"incentive is used to encourage further engagement.",
        )

    return (
        "No Campaign",
        "Customer does not currently match the criteria for any active "
        "marketing campaign.",
    )


def display_campaign_result(campaign_name, reason):
    """Prints the campaign assignment result and reason."""
    utils.print_section_header("CAMPAIGN ELIGIBILITY RESULT")
    utils.print_line_item("Assigned Campaign", campaign_name)
    utils.print_line_item("Reason", reason)
