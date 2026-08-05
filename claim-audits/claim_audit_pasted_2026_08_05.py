#!/usr/bin/env python3
"""
claim_audit_pasted_2026_08_05.py -- audit of a five-piece paste from
other models.  Same verdict shape as claim_audit_visibility.py.

WHAT WAS PASTED
    1. local_scalar_drift.py     scalar-field drift of α, G from kink params
    2. tension_geometry.py       portable obstruction-geometry engine
                                 + muon g-2 demo
    3. metrology_engine.py       Pyodide-friendly cosmological gate engine
       (metrology_challenge.html) public-facing browser UI
    4. ai_api.py                 JSON-in/out gate evaluator
       autonomous_search.py      Bayesian scan wrapper
    5. CROSS_DOMAIN_ARCHETYPES   35-form shape library + 5-step validation

ALL FIVE PIECES ARE MODEL-AUTHORED.  The K/M attribution below is
adapted: K = the *operational* content (formula / code / algorithm as
written); M = the *framing* prose around it (marketing, "beautifully",
overclaims of what the piece demonstrates).  Load-bearing bugs live
in K.  Overclaims live in M.

VERDICT CODES (same as claim_audit_visibility.py)
    VERIFIED          source checked, mechanism holds
    SIGN_BACKWARDS    the quantity is real, the direction is inverted
    UNGROUNDED_NUMBER threshold with no derivation, units, or calibration
    DIMENSIONALLY_VOID the expression is not a quantity
    GAMEABLE          metric is maximized by doing the opposite of the intent
    IDENTITY          true but empty -- a bookkeeping relation
    UNVERIFIED        cited source not locatable
    SOUND             holds as stated
"""

from dataclasses import dataclass
from typing import List
from collections import Counter


@dataclass
class Claim:
    cid: str
    who: str          # K = operational (formula/code); M = framing/prose
    text: str
    verdict: str
    why: str
    fix: str = ""


CLAIMS: List[Claim] = [

    # ═════════════════════════════════════════════════════════════════
    # PIECE 1  --  local_scalar_drift.py
    # ═════════════════════════════════════════════════════════════════

    Claim("D1", "K",
        "H0_GeV = H0_km_s_Mpc * 2.133e-44   # H0 in GeV (ℏ=1)",
        "VERIFIED",
        "Independently checked: H0 = 67.4 km/s/Mpc = 67.4 / 3.086e19 [1/s] "
        "× ℏ [6.582e-25 GeV·s] = 1.438e-42 GeV.  Code's multiplier 2.133e-44 "
        "reproduces this to four digits.  This is the ONE unit conversion "
        "the code got right.",
        "Keep."),

    Claim("D2", "K",
        "yr_to_GeVinv = 1.956e8      # 1 year in GeV^-1",
        "UNGROUNDED_NUMBER",
        "1 year = 3.156e7 s.  1 s = 1/ℏ = 1/6.582e-25 GeV^-1 = 1.519e24 "
        "GeV^-1.  So 1 yr = 4.795e31 GeV^-1.  The stated 1.956e8 is "
        "**off by 2.45e23 (23 orders of magnitude)**.  Not a typo -- the "
        "number does not match any recognizable physical constant I can "
        "identify.  Load-bearing: it multiplies the drift prefactor "
        "linearly.",
        "yr_to_GeVinv = 4.795e31   # 1 yr / ℏ"),

    Claim("D3", "K",
        "rho_crit = 3 * H0_GeV**2 * M_P**2 / (8 * np.pi)   # GeV^4  "
        "(uses M_P = 2.435e18 GeV, the REDUCED Planck mass)",
        "UNGROUNDED_NUMBER",
        "For the reduced Planck mass, G = 1/(8π M_P²) so ρ_c = 3H²/(8πG) "
        "= 3 H² M_P²  (no additional /(8π) factor).  Independently "
        "verified against textbook: 1.878e-29·h²·(g/cm³) with h=0.674 "
        "gives 3.68e-47 GeV⁴; 3 H0² M_P² gives 3.68e-47 GeV⁴  --  match.  "
        "The /(8π) in the code makes ρ_c come out at 1.46e-48 GeV⁴, "
        "**off by 25×**.  The formula would be correct for M_Pl = "
        "1.22e19 GeV (the FULL Planck mass), but the code uses M_P = "
        "2.435e18 GeV (the reduced Planck mass), so the (8π) division "
        "is wrong.",
        "rho_crit = 3 * H0_GeV**2 * M_P**2    # remove /(8π)"),

    Claim("D4", "K",
        "drift_prefactor = phi_dot_over_M * yr_to_GeVinv   # 1/yr",
        "SIGN_BACKWARDS",
        "The FORMULA is correct (drift = β · φ̇/M_P is the standard "
        "quintessence-drift relation and yr_to_GeVinv is meant to convert "
        "GeV to per-year).  But because D2 and D3 compound, the numerical "
        "value is **off by 1.23e24**.  Concretely:\n"
        "  correct prefactor at 1+w0=0.096 = 3.06e-11 /yr\n"
        "  code returns                     = 2.49e-35 /yr\n"
        "The plot's β-axis exclusion regions are meaningless as a result: "
        "code says β must exceed 4e17 to reach the α limit; correct value "
        "is β > 3e-7.  A 24-order overestimate of the required coupling "
        "makes every kink parameterization look untestable.",
        "Fix D2 and D3, then rerun.  With both fixed, Damour-Polyakov-"
        "class couplings (β ~ 1e-6 to 1e-2) become the natural test range."),

    Claim("D5", "M",
        "plot title: 'Local scalar drift from the late-time kink'  --  "
        "framed as an instrument-design forecast",
        "GAMEABLE",
        "Because the prefactor is 10²⁴× too small (D4), every candidate "
        "coupling in the plot's range (β ∈ [1e-10, 1]) reads as 'not "
        "detectable, ΛCDM safe.'  The plot's headline conclusion "
        "('no coupling is detectable') is a numerical artifact of the "
        "unit bug, not a physical result.  If used as an argument that "
        "the kink cannot be constrained by α/G drift, it is exactly the "
        "wrong direction.",
        "After fixing D2/D3, α clocks can already exclude β > 3e-7 for "
        "the champion kink -- a much sharper story than 'no coupling "
        "detectable.'  Land the corrected plot; retract the pre-fix one."),

    # ═════════════════════════════════════════════════════════════════
    # PIECE 2  --  tension_geometry.py + muon g-2 example
    # ═════════════════════════════════════════════════════════════════

    Claim("T1", "K",
        "cosine matrix C_ij = J_i · J_j / (|J_i| |J_j|), Jacobian "
        "J_ij = ∂g_i/∂p_j numerically via approx_fprime",
        "SOUND",
        "This is the correct construction of the DP-9 gate-gradient "
        "cosine matrix.  Same shape as what already lives inside "
        "energy/'s obstruction-geometry work.  Well-formed for the "
        "load-bearing observable (identifies antagonistic gate pairs "
        "with cos → −1, co-moving gates with cos → +1).",
        "Keep this core."),

    Claim("T2", "K",
        "obstruction_rank via SVD, count singular values > tol · S_max",
        "SOUND",
        "Standard SVD-rank estimate.  The relative-tolerance trick "
        "(tol × S_max) is the honest way to handle floating-point-"
        "degenerate matrices -- ties in to F1 in energy/FINDINGS.md: "
        "avoid claiming '14 orders of magnitude' when the null-space "
        "dimension is what actually matters.",
        "Keep."),

    Claim("T3", "K",
        "farkas_cone(point) returns 'the negative of the mean gradient "
        "direction if it has negative dot products with all gradients' "
        "-- labeled as a Farkas-lemma feasibility check",
        "DIMENSIONALLY_VOID",
        "A Farkas cone is a SET of directions δ satisfying J·δ < 0.  "
        "The code returns a single heuristic direction (−mean(J)/|·|) "
        "and tests whether it happens to be feasible.  Two problems: "
        "(a) the name 'cone' implies a set; the function returns a "
        "single ray.  (b) The heuristic (negative mean gradient) is "
        "not Farkas; it does not even test the cone's existence -- if "
        "the heuristic direction fails, the function returns None even "
        "though a feasible direction may exist elsewhere.  The label "
        "'improvement cone' is doing rhetorical work that the algorithm "
        "does not.",
        "Either (a) implement real Farkas via scipy.optimize.linprog on "
        "min t  s.t.  J·δ ≤ t·1,  ‖δ‖∞ ≤ 1, feasible iff t* < 0; or "
        "(b) rename to `try_negative_mean_gradient_direction` and drop "
        "the Farkas language."),

    Claim("T4", "M",
        "muon g-2 example demonstrates the geometry: 'a classic single-"
        "parameter antagonism that lets the geometry shine in its "
        "simplest, most transparent form'",
        "IDENTITY",
        "In 1D parameter space, the cosine matrix has ONE nontrivial "
        "off-diagonal, which is ±1 by construction (both gradients "
        "point along the sole dimension).  The 'geometry' collapses to "
        "'two constraints with opposite signs.'  There is no SVD rank "
        "insight (rank = min(2 gates, 1 param) = 1 by construction), "
        "no cosine structure to discover, no cone to compute.  True but "
        "empty -- 'demonstrates' the concept the way a two-cell "
        "spreadsheet demonstrates linear algebra.",
        "Replace with a 2D or 3D example where the cosine matrix has "
        "genuine off-diagonal structure -- e.g., the (H0, S8, θ*) "
        "problem from PROVENANCE DP-9, which is where the geometry "
        "actually earns its keep."),

    Claim("T5", "M",
        "'Expected output: at the compromise minimum around a_μ ≈ "
        "a_SM + 125×10⁻¹¹, Exp ≈ 1.7, SM ≈ 2.9, D ≈ 0.28'",
        "UNVERIFIED",
        "Numbers not independently checked in this audit; the weighted-"
        "mean estimate (a_exp/σ_exp² + a_SM/σ_SM²)/(1/σ_exp² + 1/σ_SM²) "
        "gives ~182×10⁻¹¹, not 125.  The pasted 'expected output' may "
        "correspond to a different objective (minimum D-metric rather "
        "than minimum weighted-χ²) -- possible, but should be labeled "
        "as such and verified.  Not a fatal error; just an unverified "
        "advertising claim.",
        "Compute and print the actual optimum before shipping the "
        "example.  Distinguish 'minimum D' from 'minimum weighted-χ² "
        "residual' -- they are different points, and DP-15 says D is "
        "a ranking heuristic, not a distance."),

    # ═════════════════════════════════════════════════════════════════
    # PIECE 3  --  metrology_engine.py + metrology_challenge.html
    # ═════════════════════════════════════════════════════════════════

    Claim("E1", "K",
        "sound_horizon:  H = 100 * H0_km_s_Mpc / c_kms * np.sqrt(Esq) / "
        "a_vals   # in 1/Mpc",
        "UNGROUNDED_NUMBER",
        "H0/c already gives 1/Mpc: 67.4/299792 = 2.25e-4 /Mpc.  The "
        "extra factor of 100 makes H come out at 100× the true value, "
        "so cs/(a·H) is 100× too small, and the resulting r_s is 100× "
        "too small (≈ 1.47 Mpc vs the ≈ 147 Mpc Planck value).  Every "
        "θ* pull derived from this sound_horizon is meaningless.  "
        "Speculation: the author may have confused H0_km_s_Mpc with "
        "h = H0/100, and multiplied by 100 to 'undo' the conversion -- "
        "but H0_km_s_Mpc is already 67.4 in the code, so the 100× is "
        "an extraneous factor.",
        "H = (H0_km_s_Mpc / c_kms) * np.sqrt(Esq) / a_vals    # drop the 100"),

    Claim("E2", "K",
        "growth_factor's ODE RHS uses idx = np.searchsorted(a_vals, a) "
        "then Esq[idx] and finite-diff dEsq_da from adjacent grid points",
        "UNGROUNDED_NUMBER",
        "solve_ivp calls the RHS at arbitrary a values that solve_ivp "
        "chooses adaptively.  The code snaps each a to the nearest "
        "index of a fixed a_vals grid and reads Esq[idx] there -- so "
        "the RHS is piecewise-constant on that grid, with uncontrolled "
        "quantization error where the adaptive stepper wants finer "
        "resolution.  Worse: dEsq/da is a symmetric-difference on the "
        "grid, so it is *independent of the current a* over each grid "
        "cell.  In the matter era where growth is stiff, this produces "
        "systematic error at the 1-10% level that no rtol/atol will "
        "control.",
        "Precompute a scipy.interpolate.interp1d of Esq(a) once, then "
        "evaluate the interpolant *and* its analytic derivative inside "
        "the RHS.  Or better: fold the Friedmann background into the "
        "ODE state so both are integrated adaptively together."),

    Claim("E3", "K",
        "def gate_H0(w_func): return 0.0    # placeholder; could be "
        "extended",
        "DIMENSIONALLY_VOID",
        "The H0 gate returns identically zero regardless of input.  "
        "Any w(a) fed to evaluate_model reports 'H0 gate passes at 0σ' "
        "-- but this says nothing about H0 tension because the gate "
        "doesn't measure it.  A constant-silent gate under a "
        "gate-vector API is exactly the shape null-harness would flag "
        "as CONSTANT_SILENT (see PROVENANCE F-9 on M2's Gate 1 for the "
        "same failure mode).  Ship a gate that measures nothing at "
        "your peril: downstream verdicts will look artificially clean.",
        "Either compute H0 from the model's r_s vs an anchored angular "
        "scale, or remove the gate from the API and note H0 is a "
        "parameter of the background, not a downstream verdict."),

    Claim("E4", "K",
        "DESI covariance: sigma_w0=0.12, sigma_wa=0.45, correlation "
        "coefficient -0.8",
        "UNVERIFIED",
        "The energy/ codebase carries different DESI mock numbers "
        "(DESI_MU = (-0.86, -0.53), σ_w0=0.04, σ_wa=0.16, corr=0.4 -- "
        "see PROVENANCE §7.1).  These pasted values differ substantially "
        "and are not sourced to a DESI publication.  Not a bug per se "
        "-- someone else's mock -- but downstream 'σ' numbers from this "
        "engine are NOT comparable to numbers from the energy/ stack.",
        "Adopt the energy/ covariance for consistency, or explicitly "
        "declare and cite the source of the alternative one.  Cross-"
        "engine σ comparisons without a shared covariance are noise."),

    # ═════════════════════════════════════════════════════════════════
    # PIECE 4  --  ai_api.py + autonomous_search.py
    # ═════════════════════════════════════════════════════════════════

    Claim("A1", "K",
        "verify_anchors() calls ltl.self_test() and reads "
        "'theta_star_offset_sigma' from it",
        "UNVERIFIED",
        "self_test() is not currently defined in late_trigger_lens.py.  "
        "The same paste proposes ADDING it -- so the API cannot run "
        "against the shipped module.  Also, the additions block "
        "references H(z) and luminosity_distance() as if they already "
        "exist, but late_trigger_lens.py exports sound_horizon, "
        "chi_ls, run_background, growth_today -- different names, "
        "different signatures.  The two files describe compatible "
        "shapes on paper; on the actual codebase, ai_api.py will "
        "ImportError at line 1 of verify_anchors().",
        "Either land the additions to late_trigger_lens first (per the "
        "'Additions' section of the paste), or rewrite ai_api against "
        "the actual exported functions.  Don't ship both halves and "
        "leave the reader to reconcile."),

    Claim("A2", "K",
        "evaluate_model uses exec(code, {'np': np}, local_vars) on "
        "user-supplied Python strings",
        "SOUND",
        "For a local scripting tool this is fine -- the operator is "
        "running their own code.  The security posture is only "
        "relevant if this API is exposed over a network (metrology_"
        "challenge.html) -- there, arbitrary code execution in the "
        "Pyodide sandbox is technically confined but should still be "
        "flagged in any deployment guide.",
        "Add a note in the challenge-page README that user code runs "
        "in the visitor's own browser sandbox and does not touch a "
        "server."),

    Claim("A3", "K",
        "gate_H0 = 0.0 inside evaluate_model, mirroring metrology_"
        "engine's placeholder",
        "GAMEABLE",
        "Bayesian optimization (autonomous_search.py) minimizes the "
        "aggregate D-distance.  Because D uses log10(1+g), a gate that "
        "returns 0 contributes log10(1)=0 to the sum -- so H0 is "
        "silently DROPPED from every optimization run.  The optimizer "
        "will find models that maximize DESI/σ8/CMB pass while H0 is "
        "'trivially satisfied' by construction.  The 'closing models' "
        "the search reports are three-gate closures, not four.",
        "Either drop H0 from the API entirely (be honest about a "
        "3-gate scheme) or wire it to a real H0 measurement.  In "
        "either case, do not run the autonomous search over a 4-gate "
        "objective where one gate is identically zero."),

    Claim("A4", "M",
        "'The module is now live. You can immediately hand a task to "
        "an AI successor.'",
        "IDENTITY",
        "Framing prose asserting readiness.  The three K-level "
        "problems above (A1 depends on unwritten code; A3 gate is "
        "identically zero) make the API not live in the operational "
        "sense.  This is what claim-audits calls SOUND-vs-VERIFIED "
        "separation applied to a code artifact: the plumbing exists as "
        "written, but has not been executed against the actual shipped "
        "engines.",
        "Verify before advertising.  Run `python ai_api.py model.json` "
        "against the current late_trigger_lens.py once, land the "
        "output as a sample file, then update the framing prose."),

    # ═════════════════════════════════════════════════════════════════
    # PIECE 5  --  CROSS_DOMAIN_ARCHETYPES v0
    # ═════════════════════════════════════════════════════════════════

    Claim("C1", "K",
        "35-form shape library covering monotone, saturating, resonance, "
        "combined-mechanism, critical-scaling, transport, thermodynamic, "
        "and network families; fitted to typically 20-50 points, ranked "
        "by R²",
        "SOUND",
        "The library itself is well-scoped and each entry names a "
        "domain-neutral shape with clear parameters.  The R²-ranking "
        "over 2-4 parameters against 20-50 points is standard practice "
        "for shape identification.  The failure mode isn't the library; "
        "it's what happens when a match is reported without the gate "
        "at the bottom.",
        "Keep -- worth shipping."),

    Claim("C2", "K",
        "'on white noise it WILL return a confident match'",
        "VERIFIED",
        "This is the exact failure mode null-harness/null_harness.py "
        "was built to catch (see PROVENANCE F-9 for M2 Gate 1 as the "
        "same-family bug).  The pasted spec correctly names the "
        "problem: fit-with-many-forms against noise always produces a "
        "high-R² winner.  Verified by direct construction -- try any "
        "sinusoid + white noise fit against a Voigt library, R² will "
        "clear 0.8 for spurious matches at N ≤ 50.",
        "The spec's own gate (item #2, the null-run) is the fix.  "
        "Land the library with that gate MANDATORY, not optional."),

    Claim("C3", "K",
        "5-step gate: (1) AIC/BIC not correlation; (2) null-run on "
        "white noise, hit must beat the null distribution; "
        "(3) trials-factor report; (4) out-of-sample; "
        "(5) parameter plausibility",
        "SOUND",
        "This is the correct methodology and it maps 1-to-1 to what "
        "already lives in the repo:\n"
        "  (1) AIC/BIC vs correlation → matches DP-15 (D as ranking "
        "      heuristic, not metric)\n"
        "  (2) null run                → null-harness/null_harness.py "
        "      + divergence-playground/null_ensemble.py\n"
        "  (3) trials factor           → coincidence.C2 in "
        "      divergence-playground\n"
        "  (4) out-of-sample           → coincidence.C4 (real common "
        "      cause via prediction)\n"
        "  (5) parameter plausibility  → analogous to F-8's 'combined "
        "      strength ≤ 0.05' physical prior.\n"
        "The paste's contribution is packaging these into a mandatory "
        "gate on any shape-match claim, which is the useful bit.",
        "Land as null-harness/archetype_library.py with the null-run "
        "gate ENFORCED (raise an exception if a match is requested "
        "without the null distribution having been computed)."),

    Claim("C4", "M",
        "'#2 is the one everyone skips and the only one that makes "
        "the answer real'",
        "SOUND",
        "Correct diagnosis.  Same lesson as PROVENANCE F-9 and the "
        "null-harness pyramid.  This piece is the ONLY one of the "
        "five pastes that arrives with its own honesty gate built in "
        "and clearly labeled 'do not skip.'",
        "Keep the framing verbatim when landing."),

    Claim("C5", "K",
        "Warning: 'over a one-sided interval these [power/exp/stretched/"
        "log/hyperbolic] are mutually correlated >0.95.  Discriminating "
        "between them requires 2+ decades of x, or a fit-residual "
        "comparison, never a correlation score.  (This is exactly what "
        "broke the cartographer.)'",
        "VERIFIED",
        "The parenthetical is a direct reference to energy/'s "
        "singularity_cartographer, which classifies wall types via "
        "Pearson-correlation scores between the approach profile and "
        "candidate functional forms (see F4 in energy/FINDINGS.md).  "
        "A correlation-based classifier on a one-sided interval is "
        "exactly the shape that will confidently mis-classify.  This "
        "audit's own R-D lens (exploration_layers/rg_flow_lens.py) "
        "reached the same conclusion by a different route.",
        "Cross-reference to F4/FK-5 in energy/FINDINGS.md; the "
        "archetype library and the cartographer share a failure mode."),
]


def report():
    print(__doc__)
    tally = Counter(c.verdict for c in CLAIMS)
    by_who = Counter(c.who for c in CLAIMS)

    print(f"{'id':<5}{'who':<5}{'verdict':<20}claim")
    for c in CLAIMS:
        print(f"{c.cid:<5}{c.who:<5}{c.verdict:<20}{c.text[:60]}")

    print(f"\n  {dict(tally)}")
    print(f"  attribution: {dict(by_who)}  "
          "(K = operational content; M = framing prose)")

    print("\n  BY PIECE  ---------------------------------------")
    for prefix, name in [("D", "local_scalar_drift.py"),
                         ("T", "tension_geometry.py + muon g-2 demo"),
                         ("E", "metrology_engine.py"),
                         ("A", "ai_api.py + autonomous_search.py"),
                         ("C", "CROSS_DOMAIN_ARCHETYPES v0")]:
        rows = [c for c in CLAIMS if c.cid.startswith(prefix)]
        broken = [c for c in rows if c.verdict not in ("SOUND", "VERIFIED")]
        status = "SHIP" if not broken else "REJECT" if len(broken) >= len(rows) // 2 else "PARTIAL"
        print(f"  {prefix}  {name:<45} {len(rows)} claims  "
              f"{len(broken)} broken   -> {status}")

    print("\n  HEADLINES")
    print("    D. local_scalar_drift.py IS BROKEN: two compounding unit")
    print("       bugs make the drift prefactor 1.23e24× too small.  β")
    print("       required for α detection reads 4e17 (absurd) when the")
    print("       correct answer is 3e-7.  DO NOT LAND without fixing D2, D3.")
    print()
    print("    E. metrology_engine.py sound_horizon has a factor-100 H0")
    print("       error, producing r_s ≈ 1.5 Mpc where Planck is 147 Mpc.")
    print("       Its ODE growth_factor also uses grid-snapped RHS values")
    print("       under solve_ivp, giving uncontrolled numerical error.")
    print("       DO NOT LAND.")
    print()
    print("    A. ai_api.py depends on functions the paste proposes to add")
    print("       to late_trigger_lens but hasn't landed yet, and its H0")
    print("       gate is identically zero -- Bayesian optimization over")
    print("       this API silently drops one of four gates.  DO NOT LAND")
    print("       until A1 and A3 are fixed.")
    print()
    print("    T. tension_geometry.py has a sound core (cosine matrix +")
    print("       SVD rank) but misnames a heuristic as 'Farkas cone' and")
    print("       demonstrates itself in 1D where the geometry is trivial.")
    print("       PARTIAL LAND: extract the core, rename the misnomer,")
    print("       replace the demo with the 3D DESI/σ8/CMB case from")
    print("       energy/'s DP-9.")
    print()
    print("    C. CROSS_DOMAIN_ARCHETYPES v0 SHIPS.  It's the only piece")
    print("       that arrives with its own honesty gate built in and")
    print("       clearly labeled 'do not skip.'  Landed as")
    print("       null-harness/archetype_library.py with the null-run")
    print("       gate ENFORCED (raises if a match is claimed without a")
    print("       null distribution to beat).")


if __name__ == "__main__":
    report()
