"""
utils.py
--------
This file holds:
1. Constants that are reused across the project (so we don't repeat "magic numbers")
2. Generic, reusable helper functions for getting and validating user input.

Keeping these here means customer.py, billing.py and eligibility.py
can all import from utils.py instead of repeating the same code.
"""

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
# These are fixed values used in business rule calculations.
# Putting them here (instead of hard-coding numbers everywhere)
# makes the program easier to update later.

ALLOWED_SEGMENTS = ["Standard", "Premium", "Enterprise"]

MIN_CREDIT_SCORE = 300
MAX_CREDIT_SCORE = 900

# Feature 1: Risk & Value thresholds
EMI_RATIO_LOW_RISK_LIMIT = 0.30      # EMI/income below this -> low risk territory
EMI_RATIO_MEDIUM_RISK_LIMIT = 0.50   # EMI/income below this -> medium risk territory
CREDIT_SCORE_GOOD = 700
CREDIT_SCORE_AVERAGE = 550

SAVINGS_PCT_HIGH_VALUE = 30          # savings % above this -> contributes to High Value
SAVINGS_PCT_MEDIUM_VALUE = 15        # savings % above this -> contributes to Medium Value
INCOME_HIGH_VALUE = 100000           # monthly income above this -> contributes to High Value
INCOME_MEDIUM_VALUE = 50000          # monthly income above this -> contributes to Medium Value

# Feature 2: Billing
DELIVERY_WAIVER_THRESHOLD = 5000     # if amount after discount+GST crosses this, delivery is free
STANDARD_DELIVERY_CHARGE_CAP = 500   # delivery charge entered by user cannot exceed this (sanity cap)

# Feature 3: Loan eligibility
MIN_AGE_FOR_LOAN = 21
MAX_AGE_FOR_LOAN = 60
MIN_CREDIT_SCORE_FOR_APPROVAL = 650
MIN_CREDIT_SCORE_FOR_REVIEW = 550
MAX_EMI_RATIO_FOR_APPROVAL = 0.40
MAX_LOAN_TO_INCOME_MULTIPLIER = 20   # loan amount should not exceed 20x monthly income for auto-approval


# ---------------------------------------------------------
# INPUT HELPER FUNCTIONS
# ---------------------------------------------------------

def get_non_negative_float(prompt):
    """
    Keeps asking the user for a number until they enter a valid,
    non-negative float. Used for things like income, expenses, EMI, price.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("Invalid input. Please enter a numeric value (e.g. 1500 or 1500.50).")
            continue

        if value < 0:
            print("Invalid input. This value cannot be negative. Please try again.")
            continue

        return value


def get_positive_int(prompt):
    """
    Keeps asking until the user enters a whole number greater than 0.
    Used for things like quantity.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number (e.g. 1, 2, 3).")
            continue

        if value <= 0:
            print("Invalid input. Quantity must be greater than 0. Please try again.")
            continue

        return value


def get_percentage(prompt, min_value=0, max_value=100):
    """
    Keeps asking until the user enters a percentage value within the
    allowed range (default 0 to 100). Used for discount %, GST %.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("Invalid input. Please enter a numeric percentage value.")
            continue

        if value < min_value or value > max_value:
            print(f"Invalid input. Value must be between {min_value} and {max_value}. Please try again.")
            continue

        return value


def get_age(prompt):
    """
    Keeps asking until the user enters a realistic, non-negative age.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number for age.")
            continue

        if value < 0:
            print("Invalid input. Age cannot be negative. Please try again.")
            continue

        if value > 120:
            print("Invalid input. Please enter a realistic age.")
            continue

        return value


def get_credit_score(prompt):
    """
    Keeps asking until the user enters a credit score within the
    valid range defined by MIN_CREDIT_SCORE and MAX_CREDIT_SCORE (300-900).
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number for credit score.")
            continue

        if value < MIN_CREDIT_SCORE or value > MAX_CREDIT_SCORE:
            print(f"Invalid input. Credit score must be between {MIN_CREDIT_SCORE} and {MAX_CREDIT_SCORE}.")
            continue

        return value


def get_customer_segment(prompt):
    """
    Keeps asking until the user enters one of the allowed customer segments.
    Comparison is case-insensitive for user convenience, but the
    returned value is always stored in the standard capitalised form.
    """
    while True:
        raw_value = input(prompt).strip()
        for allowed in ALLOWED_SEGMENTS:
            if raw_value.lower() == allowed.lower():
                return allowed
        print(f"Invalid input. Segment must be one of: {', '.join(ALLOWED_SEGMENTS)}.")


def get_non_empty_text(prompt):
    """
    Keeps asking until the user enters some non-empty text.
    Used for names, city, product name, category, etc.
    """
    while True:
        raw_value = input(prompt).strip()
        if raw_value == "":
            print("Invalid input. This field cannot be empty. Please try again.")
            continue
        return raw_value


def print_section_header(title):
    """Prints a consistent, clean header for each section of output."""
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def print_line_item(label, value):
    """Prints a label-value pair in a clean, aligned format."""
    print(f"{label:<35}: {value}")
