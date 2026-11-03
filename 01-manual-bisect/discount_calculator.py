def calculate_discount(amount):
    """Calculate the discount based on the purchase amount."""
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError("Purchase amount must be numeric.")

    if amount < 0:
        raise ValueError("Purchase amount cannot be negative.")

    if amount >= 1000:
        return amount * 0.15
    elif amount >= 500:
        return amount * 0.10
    elif amount >= 100:
        return amount * 0.05
    else:
        return 0.0


def main():
    purchase_amount = float(input("Enter purchase amount: "))

    discount = calculate_discount(purchase_amount)
    final_amount = purchase_amount - discount

    print(f"Purchase Amount: ${purchase_amount:.2f}")
    print(f"Discount: ${discount:.2f}")
    print(f"Final Amount: ${final_amount:.2f}")


if __name__ == "__main__":
    main()
