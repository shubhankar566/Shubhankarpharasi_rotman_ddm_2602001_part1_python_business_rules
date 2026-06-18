"""
main.py
-------
Entry point for the Business Rules Console Application.

This file ONLY handles:
- Displaying the menu
- Reading the user's menu choice
- Calling the appropriate functions from the src/ modules

All actual business logic lives inside src/customer.py, src/billing.py,
src/eligibility.py, and src/utils.py, as required by the assignment.
"""

from src import customer
from src import billing
from src import eligibility
from src import utils

# Keeps the most recently entered customer in memory during this run,
# so the Loan Eligibility and Campaign Eligibility menu options can reuse
# the same customer data without asking for it again.
current_customer = None


def show_menu():
    """Displays the main menu options to the user."""
    print("\n" + "#" * 50)
    print("   BUSINESS RULES CONSOLE APPLICATION")
    print("#" * 50)
    print("1. Enter Customer Profile & View Financial Summary")
    print("2. Product Billing Calculator")
    print("3. Loan Eligibility Decision")
    print("4. Campaign Eligibility Check")
    print("5. Exit")
    print("#" * 50)


def handle_customer_profile():
    """Menu option 1: collects customer details and shows the summary."""
    global current_customer
    current_customer = customer.collect_customer_details()
    customer.display_customer_summary(current_customer)


def handle_billing():
    """Menu option 2: runs the full product billing flow."""
    order = billing.collect_product_details()
    bill = billing.calculate_bill(order)
    billing.display_bill_summary(order, bill)


def handle_loan_eligibility():
    """
    Menu option 3: runs the loan eligibility check.
    Requires a customer profile to already exist in this session;
    if not, the user is asked to create one first.
    """
    global current_customer
    if current_customer is None:
        print("\nNo customer profile found in this session.")
        print("Please enter customer details first.")
        current_customer = customer.collect_customer_details()
        customer.display_customer_summary(current_customer)

    requested_loan_amount = eligibility.get_requested_loan_amount()
    decision, reason = eligibility.check_loan_eligibility(current_customer, requested_loan_amount)
    eligibility.display_loan_decision(decision, reason)


def handle_campaign_eligibility():
    """
    Menu option 4: runs the campaign eligibility check.
    Requires a customer profile to already exist in this session;
    if not, the user is asked to create one first.
    """
    global current_customer
    if current_customer is None:
        print("\nNo customer profile found in this session.")
        print("Please enter customer details first.")
        current_customer = customer.collect_customer_details()
        customer.display_customer_summary(current_customer)

    campaign_name, reason = eligibility.check_campaign_eligibility(current_customer)
    eligibility.display_campaign_result(campaign_name, reason)


def get_menu_choice():
    """
    Asks the user for a menu choice and validates that it is
    a whole number between 1 and 5.
    """
    while True:
        raw_value = input("\nEnter your choice (1-5): ").strip()
        try:
            choice = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if choice < 1 or choice > 5:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        return choice


def run():
    """Main program loop. Keeps showing the menu until the user exits."""
    print("Welcome to the Business Rules Console Application.")

    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            handle_customer_profile()
        elif choice == 2:
            handle_billing()
        elif choice == 3:
            handle_loan_eligibility()
        elif choice == 4:
            handle_campaign_eligibility()
        elif choice == 5:
            print("\nThank you for using the Business Rules Console Application. Goodbye!")
            break


if __name__ == "__main__":
    run()
