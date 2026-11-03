import sys

try:
    from discount_calculator import calculate_discount
except (ImportError, SyntaxError) as error:
    print(f"UNTESTABLE: {error}")
    sys.exit(125)


def test_high_discount_tier():
    purchase_amount = 600
    expected_discount = 60.0

    actual_discount = calculate_discount(purchase_amount)

    assert actual_discount == expected_discount, (
        f"Expected discount {expected_discount}, got {actual_discount}"
    )


if __name__ == "__main__":
    test_high_discount_tier()
    print("PASS: High discount tier is correct.")
