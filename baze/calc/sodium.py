"""NIC-Sluchalo (Netopýr) on a sodium-ion cell — a thought of 24 Nov 2026.

The cell's charge against voltage is a typical sloping layered-oxide curve (0 % ~2.50 V, 20 % ~2.95 V, 50 % ~3.25 V,
80 % ~3.55 V, 100 % ~3.90 V) — a chosen cell's own table replaces it. The limits: nPM1300 PS v1.1
(VTERM 3.50/3.55/3.60/3.65 V or 4.00-4.45 V; VSYSPOF down to 2.6 V; its bucks need VSYS >= 2.7 V);
the core board's TMI3113 2.7 V; a 3.3 V rail held only while the cell is above ~3.4 V.
"""
V = [(0, 2.50), (20, 2.95), (50, 3.25), (80, 3.55), (100, 3.90)]


def soc(v):
    for (s0, v0), (s1, v1) in zip(V, V[1:]):
        if v0 <= v <= v1:
            return s0 + (s1 - s0) * (v - v0) / (v1 - v0)
    return 0.0 if v < V[0][1] else 100.0


if __name__ == "__main__":
    cases = [
        ("the cell straight on VSYS, 3.3 V rails held (floor 3.4 V)", 3.40),
        ("the cell straight on VSYS, 3.3 V let sag (floor 3.0 V)", 3.00),
        ("a buck-boost after the charger (floor 2.7 V, the bucks')", 2.70),
        ("a buck-boost after the charger (floor 2.6 V, VSYSPOF's least)", 2.60),
    ]
    for top in (3.65, 3.90):
        print(f"charged to {top:.2f} V ({soc(top):.0f} %):")
        for lab, lo in cases:
            print(f"  {lab:62s} {soc(top) - soc(lo):4.0f} % of the cell")
