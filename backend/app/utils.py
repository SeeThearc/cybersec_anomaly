"""Shared utility helpers."""

import random


def generate_ip() -> str:
    """Return a synthetic private-network IP address."""
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
