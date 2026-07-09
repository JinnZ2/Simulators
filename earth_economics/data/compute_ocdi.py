#!/usr/bin/env python3
"""
compute_ocdi.py – Fetches data and computes OCDI and RPI over a historical range.
CC0. Stdlib only. Requires data/fetch_and_compute.py for live data.

Usage:
  python data/compute_ocdi.py --start 1950 --end 2026 --output ocdi_timeseries.csv
  python data/compute_ocdi.py --plot
"""

import argparse
import csv
import math
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# In production, these would be fetched from FRED/BEA via fetch_and_compute.py
# Here we provide a simulated data source that mirrors historical trends.
# Replace the stub values with actual API calls.

def fetch_series(series_id: str, year: int) -> Optional[float]:
    """
    Stub: returns simulated historical data consistent with published trends.
    Replace with actual FRED/BEA API calls in production.
    """
    if series_id == "er":
        # Extraction rate: labor share declining → ER rising
        ls = max(50, 64 - 0.3 * (year - 1950))  # labor share
        return (100 - ls) / 100.0
    elif series_id == "pmi":
        # Maintenance intensity proxy: ratio of depreciation + environmental spend to GDP
        # Declines during extraction-heavy periods
        return max(0.1, 0.6 - 0.005 * (year - 1950))
    elif series_id == "rentier_profits":
        # Financial + IP + land rents as fraction of profits: rising
        return 0.15 + 0.008 * (year - 1980) if year > 1980 else 0.15
    elif series_id == "total_profits":
        return 500 * math.exp(0.04 * (year - 1950))
    elif series_id == "top10_wealth":
        # Top 10% share of wealth: rising
        return 60 + 0.4 * (year - 1980) if year > 1980 else 60
    elif series_id == "median_wage":
        return 2 + 0.06 * (year - 1950)
    elif series_id == "labor_force":
        return 60 + 1.0 * (year - 1950)
    elif series_id == "financial_assets":
        return 5000 * math.exp(0.07 * (year - 1950))
    elif series_id == "gfcf":
        return 200 * math.exp(0.045 * (year - 1950))
    elif series_id == "corp_debt":
        return 1000 * math.exp(0.06 * (year - 1950))
    elif series_id == "tangible_assets":
        return 800 * math.exp(0.04 * (year - 1950))
    elif series_id == "energy_efficiency":
        # GDP per unit energy: improving, but slowing
        return 50 * math.exp(0.02 * (year - 1950))
    return None

def compute_ocdi_components(year: int) -> Dict[str, float]:
    """Compute the five OCDI sub-components for a given year."""
    er = fetch_series("er", year) or 0.5
    pmi = fetch_series("pmi", year) or 0.3
    ocdi_1 = min(2.0, er / pmi if pmi > 0 else 2.0)

    rentier = fetch_series("rentier_profits", year) or 0.15
    ocdi_2 = min(1.0, rentier)

    top10 = fetch_series("top10_wealth", year) or 70
    med_wage = fetch_series("median_wage", year) or 5
    lf = fetch_series("labor_force", year) or 150
    total_wealth = top10 * lf * med_wage * 1000  # rough proxy
    ocdi_3_raw = total_wealth / (med_wage * lf * 1000) if (med_wage * lf) > 0 else 10
    ocdi_3 = min(1.0, ocdi_3_raw / 50)

    fin = fetch_series("financial_assets", year) or 10000
    gfcf = fetch_series("gfcf", year) or 1000
    ocdi_4 = min(1.0, fin / (gfcf * 5)) if gfcf > 0 else 1.0

    debt = fetch_series("corp_debt", year) or 5000
    assets = fetch_series("tangible_assets", year) or 4000
    ocdi_5 = min(1.0, debt / assets) if assets > 0 else 1.0

    ocdi = 0.20 * (ocdi_1 + ocdi_2 + ocdi_3 + ocdi_4 + ocdi_5)

    return {
        "year": year,
        "OCDI_1": round(ocdi_1, 4),
        "OCDI_2": round(ocdi_2, 4),
        "OCDI_3": round(ocdi_3, 4),
        "OCDI_4": round(ocdi_4, 4),
        "OCDI_5": round(ocdi_5, 4),
        "OCDI": round(ocdi, 4),
    }

def compute_rpi(prev_er: float, curr_er: float, prev_eff: float, curr_eff: float) -> float:
    """Compute the Rentier Phase Index (RPI)."""
    d_er = curr_er - prev_er
    d_eff = curr_eff - prev_eff
    if d_eff == 0:
        return float("inf") if d_er > 0 else 0.0
    return d_er / d_eff

def run_historical(start: int, end: int) -> List[Dict[str, float]]:
    """Compute OCDI and RPI for each year in the range."""
    results = []
    prev_er = None
    prev_eff = None
    for yr in range(start, end + 1):
        components = compute_ocdi_components(yr)
        curr_er = fetch_series("er", yr) or 0.5
        curr_eff = fetch_series("energy_efficiency", yr) or 50
        if prev_er is not None and prev_eff is not None:
            components["RPI"] = round(compute_rpi(prev_er, curr_er, prev_eff, curr_eff), 4)
        else:
            components["RPI"] = 0.0
        prev_er, prev_eff = curr_er, curr_eff
        results.append(components)
    return results

def main():
    parser = argparse.ArgumentParser(description="Compute OCDI and RPI over a historical range.")
    parser.add_argument("--start", type=int, default=1950)
    parser.add_argument("--end", type=int, default=2026)
    parser.add_argument("--output", default="ocdi_timeseries.csv")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    results = run_historical(args.start, args.end)

    # Output CSV
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"OCDI timeseries written to {args.output}")

    # Print phase status for latest year
    latest = results[-1]
    ocdi_val = latest["OCDI"]
    rpi_val = latest["RPI"]
    print(f"\nLatest year ({latest['year']}):")
    print(f"  OCDI = {ocdi_val:.4f}")
    print(f"  RPI  = {rpi_val:.4f}")
    if ocdi_val < 0.5:
        phase = "PRODUCTIVE"
    elif ocdi_val < 1.0:
        phase = "JEVONS_REGIME"
    elif ocdi_val < 1.5:
        phase = "RENTIER_PHASE"
    else:
        phase = "LOCKED_IN"
    hysteresis = " (HYSTERESIS)" if rpi_val > 0 and ocdi_val >= 1.0 else ""
    print(f"  Phase: {phase}{hysteresis}")

    # Plot if requested
    if args.plot:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed; skipping plot.")
            return
        yrs = [r["year"] for r in results]
        ocdi_vals = [r["OCDI"] for r in results]
        rpi_vals = [r["RPI"] for r in results]
        fig, ax1 = plt.subplots()
        ax1.plot(yrs, ocdi_vals, 'b-', label="OCDI")
        ax1.axhline(y=0.5, color='green', linestyle='--', alpha=0.5)
        ax1.axhline(y=1.0, color='orange', linestyle='--', alpha=0.5)
        ax1.axhline(y=1.5, color='red', linestyle='--', alpha=0.5)
        ax1.set_ylabel("OCDI", color='b')
        ax2 = ax1.twinx()
        ax2.plot(yrs, rpi_vals, 'r-', alpha=0.5, label="RPI")
        ax2.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
        ax2.set_ylabel("RPI", color='r')
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        plt.title("OCDI and RPI: Extraction vs Maintenance Over Time")
        plt.savefig("ocdi_timeseries.png")
        plt.close()
        print("Plot saved to ocdi_timeseries.png")

if __name__ == "__main__":
    main()
