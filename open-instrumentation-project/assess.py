#!/usr/bin/env python3
"""
Open Instrumentation Project - Self-Assessment Tool
CC0 - Free for All Use, No Attribution Required

This script is a private, local tool for assessing institutional health
in your own context. It does not send data anywhere. It is designed to
help you surface patterns, write claims, and run falsification checks.

Usage:
    python assess.py

Requirements: Python 3.6+ (standard library only)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

# ------------------------------------------------------------
# THE SENSORS (Version 1.0)
# ------------------------------------------------------------

SENSORS = {
    "S1": {
        "name": "Epistemic Exit Velocity",
        "description": "Where do young people (13-25) in your context get their daily information?",
        "questions": [
            "What percentage of young people in your context use institutional sources (school, library, credentialed courses) for their primary daily information?",
            "What percentage use non-institutional sources (YouTube, podcasts, AI, mentors, community)?",
            "How has this shifted in the last 5 years? (increased / decreased / stable)"
        ],
        "threshold": ">60% non-institutional for 6+ months suggests epistemic exit"
    },
    "S2": {
        "name": "Institutional Attachment Half-Life",
        "description": "How long do people stay in core roles in your organization or community?",
        "questions": [
            "What is the median tenure of core skilled workers in your context?",
            "What percentage of core workers have >15 years of experience?",
            "How has this shifted in the last 10 years?"
        ],
        "threshold": "<5 years median tenure suggests structural memory loss"
    },
    "S3": {
        "name": "Autodidact Vitality / Scientific Trust Inversion",
        "description": "Who solves the hard problems in your context—credentialed insiders or self-taught practitioners?",
        "questions": [
            "In your context, are novel problems more often solved by credentialed practitioners or by self-taught autodidacts?",
            "Is trust in science correlated with institutional proximity or inversely correlated?",
            "Are there active 'anti-science' sentiments in your community, and are they more common among those inside or outside institutions?"
        ],
        "threshold": "When self-taught practitioners outnumber credentialed ones in real-world innovation, or when anti-science sentiment correlates with institutional saturation"
    },
    "S4": {
        "name": "Resilience Dependency Ratio",
        "description": "How many of your daily survival functions depend on institutional infrastructure?",
        "questions": [
            "List your daily survival functions (food, water, shelter, repair, communication, health).",
            "For each, estimate: Can you perform this function without institutional infrastructure (grid, supply chains, credentialed services)?",
            "What percentage of your functions are institution-dependent?"
        ],
        "threshold": ">70% dependency suggests systemic fragility"
    },
    "S5": {
        "name": "Open-Source Vitality (Resource-Normalized)",
        "description": "In your field, how does open-source efficiency compare to proprietary/institutional efficiency?",
        "questions": [
            "In your domain, are open-source or community-built tools more efficient (per unit of resource) than proprietary ones?",
            "Is the efficiency gap widening or narrowing?",
            "If open-source had equal resources, would it outperform?"
        ],
        "threshold": "When open-source efficiency exceeds proprietary by >50%, institutional R&D model is thermodynamically inefficient"
    }
}


# ------------------------------------------------------------
# USER-CREATED CLAIMS & FALSIFICATION
# ------------------------------------------------------------

def load_or_create_claims(claims_file: str = "claims.json") -> List[Dict[str, Any]]:
    """Load existing claims, or create a template if none exist."""
    if os.path.exists(claims_file):
        with open(claims_file, "r") as f:
            return json.load(f)
    else:
        default_claims = [
            {
                "id": "C1",
                "claim": "Young people are leaving institutional knowledge sources for non-institutional ones.",
                "falsification_condition": "If institutional trust increases and outside-sourcing decreases over 2 years.",
                "status": "unfalsified",
                "notes": ""
            },
            {
                "id": "C2",
                "claim": "Short job tenure leads to loss of institutional memory and resilience.",
                "falsification_condition": "If short-tenure organizations are more resilient than long-tenure ones.",
                "status": "unfalsified",
                "notes": ""
            },
            {
                "id": "C3",
                "claim": "Autodidacts are more innovative than credentialed insiders.",
                "falsification_condition": "If credentialed insiders consistently outperform autodidacts in applied problem-solving.",
                "status": "unfalsified",
                "notes": ""
            },
            {
                "id": "C4",
                "claim": "Institutions are losing high-resilience, low-maintenance actors.",
                "falsification_condition": "If insiders are more resilient than outsiders in resource-constrained scenarios.",
                "status": "unfalsified",
                "notes": ""
            },
            {
                "id": "C5",
                "claim": "Open-source communities produce more efficient outcomes per unit of resource than institutions.",
                "falsification_condition": "If proprietary systems maintain efficiency parity with open-source while bearing bureaucratic overhead.",
                "status": "unfalsified",
                "notes": ""
            }
        ]
        with open(claims_file, "w") as f:
            json.dump(default_claims, f, indent=2)
        return default_claims


def save_claims(claims: List[Dict[str, Any]], claims_file: str = "claims.json"):
    with open(claims_file, "w") as f:
        json.dump(claims, f, indent=2)
    print(f"Claims saved to {claims_file}")


# ------------------------------------------------------------
# ASSESSMENT FUNCTIONS
# ------------------------------------------------------------

def run_assessment() -> Dict[str, Any]:
    """Run through the sensors, collecting user input."""
    results = {}
    print("\n" + "=" * 60)
    print("Open Instrumentation Project - Self-Assessment")
    print("=" * 60)
    print("\nThis tool helps you assess institutional health in your context.")
    print("Your answers are private and never leave your machine.\n")

    for sensor_id, sensor in SENSORS.items():
        print(f"\n--- {sensor_id}: {sensor['name']} ---")
        print(f"  {sensor['description']}")
        print(f"  Threshold: {sensor['threshold']}\n")

        sensor_results = {}
        for i, q in enumerate(sensor["questions"], 1):
            answer = input(f"  Q{i}: {q}\n  Your answer: ")
            sensor_results[f"Q{i}"] = answer

        assessment = input("\n  Based on your answers, is this sensor indicating potential fragility? (y/n/unsure): ")
        sensor_results["assessment"] = assessment
        results[sensor_id] = sensor_results

    return results


def display_results(results: Dict[str, Any]):
    """Display assessment results."""
    print("\n" + "=" * 60)
    print("Assessment Summary")
    print("=" * 60)

    for sensor_id, sensor_data in results.items():
        sensor = SENSORS[sensor_id]
        print(f"\n{sensor_id}: {sensor['name']}")
        print(f"  Assessment: {sensor_data.get('assessment', 'Not provided')}")
        print(f"  Threshold: {sensor['threshold']}")

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("  1. Review your claims in claims.json")
    print("  2. Consider writing new claims based on your assessment")
    print("  3. Define falsification conditions for your claims")
    print("  4. Re-run this assessment periodically to track changes")
    print("=" * 60)


# ------------------------------------------------------------
# CLAIM MANAGEMENT (Add/Edit/Delete)
# ------------------------------------------------------------

def manage_claims(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Interactive menu to manage claims."""
    print("\n" + "=" * 60)
    print("Claim Management")
    print("=" * 60)

    while True:
        print("\nCurrent Claims:")
        for claim in claims:
            print(f"  {claim['id']}: {claim['claim']}")
            print(f"    Falsification: {claim['falsification_condition']}")
            print(f"    Status: {claim['status']}")

        print("\nOptions:")
        print("  [a] Add new claim")
        print("  [e] Edit existing claim")
        print("  [d] Delete claim")
        print("  [f] Update falsification status")
        print("  [q] Quit to main")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "a":
            new_claim = {
                "id": f"C{len(claims) + 1}",
                "claim": input("Claim: "),
                "falsification_condition": input("Falsification condition: "),
                "status": "unfalsified",
                "notes": ""
            }
            claims.append(new_claim)
            print("Claim added.")

        elif choice == "e":
            claim_id = input("Claim ID to edit: ").strip()
            for claim in claims:
                if claim["id"] == claim_id:
                    claim["claim"] = input(f"Claim ({claim['claim']}): ") or claim["claim"]
                    claim["falsification_condition"] = input(f"Falsification ({claim['falsification_condition']}): ") or claim["falsification_condition"]
                    claim["notes"] = input("Notes (optional): ") or claim.get("notes", "")
                    print("Claim updated.")
                    break
            else:
                print("Claim not found.")

        elif choice == "d":
            claim_id = input("Claim ID to delete: ").strip()
            claims = [c for c in claims if c["id"] != claim_id]
            print("Claim deleted.")

        elif choice == "f":
            claim_id = input("Claim ID: ").strip()
            for claim in claims:
                if claim["id"] == claim_id:
                    print(f"Current status: {claim['status']}")
                    new_status = input("New status (unfalsified / falsified / ambiguous): ").strip()
                    if new_status in ["unfalsified", "falsified", "ambiguous"]:
                        claim["status"] = new_status
                        print("Status updated.")
                    else:
                        print("Invalid status.")
                    break
            else:
                print("Claim not found.")

        elif choice == "q":
            break

    return claims


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    print("\nOpen Instrumentation Project -- Self-Assessment Tool")
    print("   CC0 -- Free for All Use, No Attribution Required\n")

    claims = load_or_create_claims()

    results = run_assessment()
    display_results(results)

    timestamp = datetime.now().isoformat()
    assessment_file = f"assessment_{timestamp[:10]}.json"
    with open(assessment_file, "w") as f:
        json.dump({
            "date": timestamp,
            "results": results
        }, f, indent=2)
    print(f"\nAssessment saved to {assessment_file}")

    while True:
        manage = input("\nWould you like to manage your claims? (y/n): ").strip().lower()
        if manage == "y":
            claims = manage_claims(claims)
            save_claims(claims)
            break
        elif manage == "n":
            break
        else:
            print("Please enter y or n.")

    print("\n" + "=" * 60)
    print("Thank you for using the Open Instrumentation Project.")
    print("Remember: This is a tool for your own clarity. Share it freely.")
    print("=" * 60)


if __name__ == "__main__":
    main()
