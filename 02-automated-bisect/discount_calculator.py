def calculate_discount(amount):
    """Calculate the discount based on the purchase amount."""
    HIGH_DISCOUNT_THRESHOLD = 1000

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError("Purchase amount must be numeric.")

    if amount < 0:
        raise ValueError("Purchase amount cannot be negative.")

    if amount >= HIGH_DISCOUNT_THRESHOLD:
        return amount * 0.15
    elif amount >= 500:
        return amount * 0.10
    elif amount >= 100:
        return amount * 0.05
    else:
        return 0.0
