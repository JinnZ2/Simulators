"""Batch runner — grade every cataloged proxy through the protocol and rank.

Produces comparative coverage scores: which proxies in the catalog are grounded
and which are mostly assumed, so investigation effort goes where it matters.
"""
from .grounding import ChainLink, GroundingChain
from .coverage import coverage_report
from .instruments import GRADE_WEIGHT

def grade_catalog_entry(entry: dict) -> dict:
    chain = GroundingChain([ChainLink(name=n, mechanism="", fidelity=f, grade=g)
                            for n, f, g in entry["chain"]])
    chain_rep = chain.report()
    aspects = [{"aspect": n, "grade": g, "grounding_level":
                {"measured": "G2", "estimated": "G3", "assumed": "G4"}[g],
                "upgrade_path": "run lab investigation"} for n, f, g in entry["chain"]]
    cov = coverage_report(aspects)
    return {"id": entry["id"], "mode": entry["mode"],
            "target": entry["target"], "observable": entry["observable"],
            "chain_fidelity": chain_rep["chain_fidelity"],
            "weakest_link": chain_rep["weakest_link"]["name"],
            "grounded_fraction": cov["grounded_fraction"],
            "verdict": cov["verdict"]}

def run_batch(catalog: list) -> list:
    results = [grade_catalog_entry(e) for e in catalog]
    return sorted(results, key=lambda r: r["grounded_fraction"], reverse=True)
