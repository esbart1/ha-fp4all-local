"""
FP4All Local for Home Assistant


Helper to combine High/Low counter values.
"""

def combine_high_low(
    high,
    low,
    multiplier=1,
):
    """Combine high and low values."""

    if high is None and low is None:
        return None

    if high is None:
        high = 0

    if low is None:
        low = 0

    return (float(high) * multiplier) + float(low)