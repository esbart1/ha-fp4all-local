"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.0.0
File    : test_combine_high_low.py

Tests for combine_high_low()
"""

from helpers.combine_high_low import combine_high_low


def run_tests():
    """Run helper tests."""

    tests = [
        (
            "Low only",
            combine_high_low(None, 123),
            123.0,
        ),
        (
            "High only",
            combine_high_low(10, None),
            10.0,
        ),
        (
            "Both values",
            combine_high_low(2, 50),
            52.0,
        ),
        (
            "Multiplier",
            combine_high_low(2, 50, 1000),
            2050.0,
        ),
        (
            "Both None",
            combine_high_low(None, None),
            None,
        ),
    ]

    for name, result, expected in tests:
        if result == expected:
            print(f"[ OK ] {name}")
        else:
            print(
                f"[FAIL] {name}: "
                f"{result} != {expected}"
            )


if __name__ == "__main__":
    run_tests()