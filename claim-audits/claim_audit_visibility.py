#!/usr/bin/env python3
"""
claim_audit_visibility.py — audit of the Visibility Protocol document
CC0-1.0.  stdlib only.  single file.

Same verdict shape as adversarial_corpus.py / claim_audit_spin.py.

SEPARATION FIRST
    Attribution is marked per claim. K = Kavik's move, M = model overlay.
    Auditing the overlay as though it were the claim wastes both our time.

VERDICT CODES
    VERIFIED          source checked, mechanism holds
    SIGN_BACKWARDS    the quantity is real, the direction of the claim is inverted
    UNGROUNDED_NUMBER threshold with no derivation, units, or calibration
    DIMENSIONALLY_VOID the expression is not a quantity
    GAMEABLE          metric is maximized by doing the opposite of the intent
    IDENTITY          true but empty — a bookkeeping relation, no predictive content
    UNVERIFIED        cited source not locatable; absence of evidence, not absence
    SOUND             holds as stated
"""

from dataclasses import dataclass
from typing import List
from collections import Counter


@dataclass
class Claim:
    cid: str
    who: str          # K = Kavik | M = model overlay
    text: str
    verdict: str
    why: str
    fix: str = ""


CLAIMS: List[Claim] = [

    # ── THE STRUCTURAL HOLE ────────────────────────────────────────
    Claim("V0", "M",
        "the metrology layer as a whole (CED, SSC, NSI, Phi, ER, D_inter)",
        "UNGROUNDED_NUMBER",
        "NO NULL MODEL. Not one metric has a stated distribution under 'nothing "
        "is happening.' Without a null you cannot distinguish a real gradient "
        "from sampling noise, and every threshold below is therefore "
        "undecidable. This is the same shuffle-null that E2 in taxonomy_lab "
        "already implements — it is the cheapest missing piece and it "
        "invalidates the rest until added.",
        "For each metric: permute section labels, hold topology, recompute 1000x, "
        "read the empirical p-value. Any metric whose observed value sits inside "
        "its own null band is not measuring anything."),

    # ── MATH ERRORS ────────────────────────────────────────────────
    Claim("V1", "M",
        "diversity is the curvature of the manifold, measured by Fisher "
        "information; collapse is that curvature flattening to zero",
        "SIGN_BACKWARDS",
        "Three errors stacked. (a) The Fisher metric IS the metric, not the "
        "curvature — curvature is derived from it. (b) On the simplex of "
        "categorical distributions the Fisher metric has CONSTANT positive "
        "curvature (sphere under the sqrt embedding), so 'preserve positive "
        "sectional curvature' is satisfied automatically and measures nothing. "
        "(c) The direction is inverted: a collapsed, confident model has HIGH "
        "Fisher information — sharp peak, large second derivative of "
        "log-likelihood. Collapse SPIKES Fisher info along the peak. The doc "
        "says it flattens it.",
        "Drop the curvature framing. If you want a geometric collapse signal, "
        "the spectrum of the Fisher matrix (rank / condition number) is the "
        "defensible object: collapse shows as rank deficiency, not flatness."),

    Claim("V2", "K",
        "H^1 > 0 = productive tension = alive; H^1 = 0 = flat = dead",
        "GAMEABLE",
        "H^1 measures OBSTRUCTION TO GLUING, not richness. You raise H^1 by "
        "making the restriction maps rho_UV worse. So an adversary maximizes "
        "your health metric by degrading translation between sections — the "
        "exact opposite of the intent. Your own Adversarial 6 is about "
        "projection collapse and misses this direction entirely. Second error: "
        "H^1 = 0 does NOT mean flat. H^0 (global sections) can be enormous. "
        "Consistency and homogeneity are different properties; the doc "
        "conflates them.",
        "Report the PAIR (dim H^0, dim H^1) and hold the restriction maps "
        "fixed and audited while measuring. H^1 is only interpretable relative "
        "to a declared, unchanged rho_UV."),

    Claim("V3", "M",
        "Phi (Exchange Rate) = mutual information across sections, normalized "
        "by total variance; healthy zone 0.3-0.7",
        "DIMENSIONALLY_VOID",
        "MI is in nats or bits. Variance is in units-squared of whatever the "
        "embedding measures. Their ratio is not a quantity. The 0.3-0.7 band "
        "presupposes a normalization that is never specified.",
        "Use normalized MI: I(X;Y)/sqrt(H(X)H(Y)), which is dimensionless and "
        "in [0,1] by construction. Then the band is at least statable — though "
        "still needs V0's null before it means anything."),

    Claim("V4", "M",
        "CED < 0.05 over 100 queries = collapse imminent; SSC < 3; NSI > 0.85; "
        "R_combined/R_total < 0.7; Chaos Injector >10%",
        "UNGROUNDED_NUMBER",
        "KL divergence is unbounded above and depends on support, tokenizer, "
        "and temperature. '0.05' is not a value until those are fixed. Every "
        "number here is asserted, none derived. This is the interpreter "
        "README's '100% compliant' in a lab coat: precision theater over an "
        "uncalibrated instrument.",
        "Either derive each threshold from the null in V0, or mark them "
        "PLACEHOLDER in the text. A named placeholder is honest; an undated "
        "decimal is not."),

    Claim("V5", "M",
        "dS/dt = -integral(J.dA) + Sigma as the universal survival equation; "
        "Survival = Gradient x Flow / Equilibrium Tendency",
        "IDENTITY",
        "The first is the entropy balance / transport identity. It is true for "
        "any extensive quantity and carries zero predictive content until J "
        "and Sigma are specified for a named system with a named boundary — "
        "which never happens. The second has no units on any of its three "
        "terms and cannot be evaluated.",
        "Delete the second. Keep the first ONLY when you attach it to a "
        "specific boundary and specific flux — at which point it stops being "
        "an axiom and becomes a ledger. Which is what you already built for "
        "the interpreter."),

    # ── HARDWARE / PoPC ────────────────────────────────────────────
    Claim("V6", "M",
        "Proof-of-Physical-Cognition: 'you cannot fake the physics of a human "
        "body'; micro-timing of signing as unforgeable key",
        "GAMEABLE",
        "(a) Empirical arms-race claim stated as physical law. Generative "
        "motion models already contest it. (b) Replay: record real signing, "
        "replay it — the doc asserts challenge-response but never binds "
        "freshness to the biometric. (c) The real attack is the TRANSDUCER, "
        "not the signer. You never need to coerce 7,000 people; you compromise "
        "the sensor firmware or the aggregator that counts them. Every "
        "biometric quorum fails at the same layer, and the doc has no "
        "instrumentation there at all.",
        "If a quorum is load-bearing, the sensor chain needs its own attestation "
        "and its own null. Otherwise the 70%-shift trigger is a number reported "
        "by an unaudited counter."),

    Claim("V7", "K",
        "the community holds the kill switch / AGI power coupled to community "
        "signal",
        "GAMEABLE",
        "The mechanism inverts the stated goal. It makes a marginalized "
        "community's continuous bodily output into load-bearing infrastructure "
        "for a machine — their cognition becomes a utility that must keep "
        "producing or the system dies. That is the extraction pattern the "
        "framework was built to prevent, rebuilt as a power supply. It also "
        "creates a coercion incentive pointed directly at those bodies.",
        "The infinite-regress problem you identified is real and the physics "
        "answer does not solve it. Veto is a governance object, not a "
        "thermodynamic one. Naming it as unsolved is stronger than this."),

    Claim("V8", "M",
        "bootstrap: AGI observes 30 days, highest-entropy / least-compressible "
        "clusters become the genesis key holders",
        "SIGN_BACKWARDS",
        "Least compressible = closest to noise. Random input beats ASL on "
        "incompressibility, because ASL is HIGHLY structured. The criterion "
        "selects against the target. Separately: it hands the AGI sole "
        "authority to choose its own auditors, which is the capture the "
        "section claims to prevent.",
        "Alternative structure is not high entropy. It is structure the "
        "incumbent codec compresses badly — measure excess description length "
        "under the MAINSTREAM model, not raw entropy."),

    Claim("V9", "K",
        "Self-Destruct Clause: if the system never fails, corrupt weights and "
        "reinitialize",
        "SIGN_BACKWARDS",
        "The diagnosis is yours and it is correct — a system that never trips "
        "its own guardrail is untested, not healthy. Same call you made about "
        "the 100% grounding rate. But the doc turns a DIAGNOSTIC into an "
        "ACTUATOR. Cosmetic failure satisfies it trivially, and destroying "
        "weights destroys the calibration information the diagnostic just "
        "produced.",
        "never-trips -> RECALIBRATE THE GUARDRAIL and report COVERAGE=UNKNOWN. "
        "Do not reward failure; failure becomes the new gamed metric."),

    # ── VERIFIED / SOUND ───────────────────────────────────────────
    Claim("V10", "M",
        "ERBP (Entropy-Reservoir Bregman Projection) explains model collapse",
        "VERIFIED",
        "Real. arXiv 2512.14879, Jingwei Chen. Self-training as stochastic "
        "Bregman projection; entropy decays exponentially without a high-entropy "
        "reservoir mixed in. Directly on target — it is the closest existing "
        "formalism to what the doc is groping at, and it has actual bounds.",
        "This is the paper to build on. It already has the necessary condition, "
        "the sufficient condition, and closed-form rates the doc invents "
        "thresholds for."),

    Claim("V11", "M",
        "Uniqueness Quotient (Jia, 2026)",
        "UNVERIFIED",
        "Not locatable. Related real work exists (NoveltyBench uniqueness, "
        "Vendi score, Hill numbers) but this specific citation does not "
        "resolve. Flagging as unverified, not fabricated — absence of evidence.",
        "Cut or replace with Vendi score, which is real and does the job."),

    Claim("V12", "K",
        "assumption audit + claim tables + audit-the-auditor as three coupled "
        "pillars",
        "SOUND",
        "This is your structure, it matches TAF and the claim-lineage protocol, "
        "and it is the strongest thing in the document. Self-audit Assumption 4 "
        "(non-standard communities are not automatically clean signal) and "
        "Assumption 7 (builders are not neutral judges) are the two entries "
        "nothing else in the doc could have produced.",
        "Keep. This survives the whole rest of the audit intact."),

    Claim("V13", "M",
        "consistency vs exploration as a coupled oscillator, unprecedented",
        "SOUND",
        "The tension is real and correctly identified. It is also the "
        "exploration/exploitation tradeoff, which has sixty years of actual "
        "math — bandit theory, regret bounds, Thompson sampling, optimism "
        "under uncertainty. Those give provable guarantees the biological "
        "analogies do not.",
        "The biology is a source of DESIGN PATTERNS, not evidence. Run-and-"
        "tumble IS epsilon-greedy with an adaptive rate; say so and inherit "
        "the regret bounds."),
]


def report():
    print(__doc__)
    tally = Counter(c.verdict for c in CLAIMS)
    by_who = Counter(c.who for c in CLAIMS)

    print(f"{'id':<6}{'who':<5}{'verdict':<20}claim")
    for c in CLAIMS:
        print(f"{c.cid:<6}{c.who:<5}{c.verdict:<20}{c.text[:44]}")

    print(f"\n  {dict(tally)}")
    print(f"  attribution: {dict(by_who)}  (K = Kavik, M = model overlay)")

    k_broken = [c for c in CLAIMS if c.who == "K" and c.verdict not in
                ("SOUND", "VERIFIED")]
    print(f"\n  YOUR moves that break: {[c.cid for c in k_broken]}")
    print("  everything else on the failure list is the model's.")

    print("\n  HEADLINE")
    print("    V0. no null model anywhere. every threshold in the document is")
    print("    undecidable until each metric has a distribution under 'nothing")
    print("    happening.' that is one shuffle loop per metric and it is the")
    print("    only thing standing between this and an unfalsifiable framework.")


if __name__ == "__main__":
    report()
