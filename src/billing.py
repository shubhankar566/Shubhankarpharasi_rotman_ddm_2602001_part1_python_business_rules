"""
billing.py
----------
Feature 2: Product Billing Calculator

Responsible for:
- Collecting product/order details from the user
- Calculating gross amount, discount, GST, delivery charge, and final amount
- Applying the delivery charge waiver rule when the order value is high enough
"""

from src import utils


def collect_product_details():
    """
    Asks the user for product/order details, validating each input.
    Returns a dictionary with the raw inputs collected.
    """
    utils.print_section_header("PRODUCT BILLING DETAILS")

    product_name = utils.get_non_empty_text("Enter product name: ")
    product_category = utils.get_non_empty_text("Enter product category: ")
    quantity = utils.get_positive_int("Enter quantity: ")
    unit_price = utils.get_non_negative_float("Enter unit price (Rs.): ")
    discount_percentage = utils.get_percentage("Enter discount percentage (0-100): ")
    gst_percentage = utils.get_percentage("Enter GST percentage: ", min_value=0, max_value=100)
    delivery_charge = utils.get_non_negative_float("Enter delivery charge (Rs.): ")

    return {
        "product_name": product_name,
        "product_category": product_category,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_percentage": discount_percentage,
        "gst_percentage": gst_percentage,
        "delivery_charge": delivery_charge,
    }


def calculate_gross_amount(order):
    """Gross Amount = Quantity * Unit Price"""
    return order["quantity"] * order["unit_price"]


def calculate_discount_amount(order, gross_amount):
    """Discount Amount = Gross Amount * (Discount % / 100)"""
    return gross_amount * (order["discount_percentage"] / 100)


def calculate_amount_after_discount(gross_amount, discount_amount):
    """Amount After Discount = Gross Amount - Discount Amount"""
    return gross_amount - discount_amount


def calculate_gst_amount(amount_after_discount, gst_percentage):
    """GST is applied on the amount AFTER discount, not on the gross amount."""
    return amount_after_discount * (gst_percentage / 100)


def determine_delivery_charge(order, amount_before_delivery):
    """
    BUSINESS RULE (Feature 2 additional rule):
    If the final payable amount BEFORE delivery (i.e. amount after discount + GST)
    is above DELIVERY_WAIVER_THRESHOLD, delivery charge is waived (set to 0).
    Otherwise, the delivery charge entered by the user is applied as-is.
    """
    if amount_before_delivery > utils.DELIVERY_WAIVER_THRESHOLD:
        return 0.0
    return order["delivery_charge"]


def calculate_bill(order):
    """
    Runs the full billing calculation pipeline and returns a dictionary
    with every intermediate and final value, so it can be displayed
    and also reused (e.g. for loan eligibility checks on big purchases).
    """
    gross_amount = calculate_gross_amount(order)
    discount_amount = calculate_discount_amount(order, gross_amount)
    amount_after_discount = calculate_amount_after_discount(gross_amount, discount_amount)
    gst_amount = calculate_gst_amount(amount_after_discount, order["gst_percentage"])
    amount_before_delivery = amount_after_discount + gst_amount
    delivery_charge_applied = determine_delivery_charge(order, amount_before_delivery)
    final_payable_amount = amount_before_delivery + delivery_charge_applied

    return {
        "gross_amount": gross_amount,
        "discount_amount": discount_amount,
        "amount_after_discount": amount_after_discount,
        "gst_amount": gst_amount,
        "delivery_charge_applied": delivery_charge_applied,
        "final_payable_amount": final_payable_amount,
    }


def display_bill_summary(order, bill):
    """Prints a clean, formatted bill summary."""
    utils.print_section_header("BILLING SUMMARY")
    utils.print_line_item("Product Name", order["product_name"])
    utils.print_line_item("Product Category", order["product_category"])
    utils.print_line_item("Quantity", order["quantity"])
    utils.print_line_item("Unit Price (Rs.)", f"{order['unit_price']:.2f}")
    utils.print_line_item("Gross Amount (Rs.)", f"{bill['gross_amount']:.2f}")
    utils.print_line_item("Discount Percentage", f"{order['discount_percentage']:.2f}%")
    utils.print_line_item("Discount Amount (Rs.)", f"{bill['discount_amount']:.2f}")
    utils.print_line_item("Amount After Discount (Rs.)", f"{bill['amount_after_discount']:.2f}")
    utils.print_line_item("GST Percentage", f"{order['gst_percentage']:.2f}%")
    utils.print_line_item("GST Amount (Rs.)", f"{bill['gst_amount']:.2f}")

    if bill["delivery_charge_applied"] == 0 and order["delivery_charge"] > 0:
        utils.print_line_item("Delivery Charge", "Rs. 0.00 (Waived - order above threshold)")
    else:
        utils.print_line_item("Delivery Charge Applied (Rs.)", f"{bill['delivery_charge_applied']:.2f}")

    utils.print_line_item("FINAL PAYABLE AMOUNT (Rs.)", f"{bill['final_payable_amount']:.2f}")
