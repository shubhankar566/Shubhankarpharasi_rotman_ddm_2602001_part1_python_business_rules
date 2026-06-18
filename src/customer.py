"""
customer.py
-----------
Feature 1: Customer Profile and Financial Summary

This file is responsible for:
- Collecting customer details from the user
- Calculating monthly savings, savings percentage, and EMI-to-income ratio
- Deciding the customer's Risk Category (Low / Medium / High)
- Deciding the customer's Value Category (Low / Medium / High)

Business rules for Risk and Value categories are explained in README.md.
"""

from src import utils


def collect_customer_details():
    """
    Asks the user for all customer details one by one, validating each.
    Returns a dictionary containing all the collected and calculated values.
    This dictionary is reused later by billing, eligibility, and campaign features.
    """
    utils.print_section_header("CUSTOMER DETAILS")

    name = utils.get_non_empty_text("Enter customer name: ")
    age = utils.get_age("Enter customer age: ")
    city = utils.get_non_empty_text("Enter customer city: ")
    monthly_income = utils.get_non_negative_float("Enter monthly income (Rs.): ")
    monthly_expenses = utils.get_non_negative_float("Enter monthly expenses (Rs.): ")
    existing_emi = utils.get_non_negative_float("Enter existing EMI amount (Rs.): ")
    credit_score = utils.get_credit_score("Enter credit score (300-900): ")
    segment = utils.get_customer_segment("Enter customer segment (Standard/Premium/Enterprise): ")

    customer = {
        "name": name,
        "age": age,
        "city": city,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "existing_emi": existing_emi,
        "credit_score": credit_score,
        "segment": segment,
    }

    # Calculate derived financial values right away and store them too,
    # so other features (loan, campaign) can reuse them without recalculating.
    customer["monthly_savings"] = calculate_monthly_savings(customer)
    customer["savings_percentage"] = calculate_savings_percentage(customer)
    customer["emi_to_income_ratio"] = calculate_emi_to_income_ratio(customer)
    customer["risk_category"] = determine_risk_category(customer)
    customer["value_category"] = determine_value_category(customer)

    return customer


def calculate_monthly_savings(customer):
    """
    Monthly Savings = Monthly Income - Monthly Expenses - Existing EMI
    If this goes negative, we still return the actual (negative) number,
    because it is useful information for risk calculation.
    """
    income = customer["monthly_income"]
    expenses = customer["monthly_expenses"]
    emi = customer["existing_emi"]
    return income - expenses - emi


def calculate_savings_percentage(customer):
    """
    Savings Percentage = (Monthly Savings / Monthly Income) * 100
    If income is 0, we avoid a divide-by-zero error and return 0.
    """
    income = customer["monthly_income"]
    if income == 0:
        return 0.0

    savings = customer["monthly_savings"]
    return (savings / income) * 100


def calculate_emi_to_income_ratio(customer):
    """
    EMI-to-Income Ratio = Existing EMI / Monthly Income
    If income is 0, we treat the ratio as 1.0 (i.e. maximum risk),
    since a customer with no income but existing EMI is high risk.
    """
    income = customer["monthly_income"]
    if income == 0:
        return 1.0

    emi = customer["existing_emi"]
    return emi / income


def determine_risk_category(customer):
    """
    BUSINESS RULE for Risk Category (explained in detail in README.md):

    We look at two factors together: EMI-to-income ratio and credit score.

    Low Risk:
        EMI ratio is below EMI_RATIO_LOW_RISK_LIMIT (30%)
        AND credit score is at least CREDIT_SCORE_GOOD (700+)

    Medium Risk:
        EMI ratio is below EMI_RATIO_MEDIUM_RISK_LIMIT (50%)
        AND credit score is at least CREDIT_SCORE_AVERAGE (550+)
        (covers everyone who doesn't qualify as Low Risk but isn't extreme)

    High Risk:
        Anyone who does not meet the above two conditions
        (e.g. high EMI burden, or poor credit score, or both)
    """
    emi_ratio = customer["emi_to_income_ratio"]
    credit_score = customer["credit_score"]

    if emi_ratio < utils.EMI_RATIO_LOW_RISK_LIMIT and credit_score >= utils.CREDIT_SCORE_GOOD:
        return "Low Risk"
    elif emi_ratio < utils.EMI_RATIO_MEDIUM_RISK_LIMIT and credit_score >= utils.CREDIT_SCORE_AVERAGE:
        return "Medium Risk"
    else:
        return "High Risk"


def determine_value_category(customer):
    """
    BUSINESS RULE for Value Category (explained in detail in README.md):

    We use a simple points system based on income and savings percentage,
    then map total points to a value category. This rewards customers
    who both earn well AND save well, rather than just one or the other.

    Points from income:
        +2 points if monthly_income > INCOME_HIGH_VALUE   (1,00,000)
        +1 point  if monthly_income > INCOME_MEDIUM_VALUE (50,000)
        +0 otherwise

    Points from savings percentage:
        +2 points if savings_percentage > SAVINGS_PCT_HIGH_VALUE (30%)
        +1 point  if savings_percentage > SAVINGS_PCT_MEDIUM_VALUE (15%)
        +0 otherwise

    Total points -> Value Category:
        4 points          -> High Value
        2 or 3 points      -> Medium Value
        0 or 1 point       -> Low Value
    """
    income = customer["monthly_income"]
    savings_percentage = customer["savings_percentage"]

    points = 0

    if income > utils.INCOME_HIGH_VALUE:
        points += 2
    elif income > utils.INCOME_MEDIUM_VALUE:
        points += 1

    if savings_percentage > utils.SAVINGS_PCT_HIGH_VALUE:
        points += 2
    elif savings_percentage > utils.SAVINGS_PCT_MEDIUM_VALUE:
        points += 1

    if points == 4:
        return "High Value"
    elif points in (2, 3):
        return "Medium Value"
    else:
        return "Low Value"


def display_customer_summary(customer):
    """
    Prints a clean, formatted summary of the customer's financial profile
    and the risk/value categories calculated for them.
    """
    utils.print_section_header("CUSTOMER FINANCIAL SUMMARY")
    utils.print_line_item("Name", customer["name"])
    utils.print_line_item("Age", customer["age"])
    utils.print_line_item("City", customer["city"])
    utils.print_line_item("Segment", customer["segment"])
    utils.print_line_item("Monthly Income (Rs.)", f"{customer['monthly_income']:.2f}")
    utils.print_line_item("Monthly Expenses (Rs.)", f"{customer['monthly_expenses']:.2f}")
    utils.print_line_item("Existing EMI (Rs.)", f"{customer['existing_emi']:.2f}")
    utils.print_line_item("Credit Score", customer["credit_score"])
    utils.print_line_item("Monthly Savings (Rs.)", f"{customer['monthly_savings']:.2f}")
    utils.print_line_item("Savings Percentage", f"{customer['savings_percentage']:.2f}%")
    utils.print_line_item("EMI-to-Income Ratio", f"{customer['emi_to_income_ratio']:.2f}")
    utils.print_line_item("Risk Category", customer["risk_category"])
    utils.print_line_item("Value Category", customer["value_category"])
