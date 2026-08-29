# household-scope-audit

Family-functioning, parenting-capacity and child-welfare risk
instruments are scoped to the household, which is the level dysfunction
is *observed* at. Conditions imposed from outside it — shift
scheduling, housing instability, benefit cliffs, transport access — are
in most of them absent, or present only as an attribute of the
caregiver. Where the variable is absent, an externally caused state has
nowhere to land except on the persons measured.

`SOURCE_DROP.md` is delivered verbatim. The ask is Arm 1, and for *"a
reading room and a coding scheme, nothing else."*

**The coding scheme is built. The reading room is not available and is
not substituted for.**

    python3 household-scope-audit/coding.py        # the scheme
    python3 household-scope-audit/audit.py         # the design audit
    python3 household-scope-audit/selftest_hsa.py  # the checks

## No instrument is coded here

Every publisher, statutory and archive host tested returns no response
through this environment's proxy; only `github.com` answers, and egress
is an allowlist so substituting a publisher does not help. The
measurement is in the report rather than asserted.

**Nothing is invented in its place.** An E-fraction table produced from
imagined items would read as a result about family-functioning scales
and child-welfare risk tools — instruments that carry weight in
decisions about real families. The fixtures used below are authored in
`coding.py`, labelled there, and no fraction over them is a statement
about any instrument.

## The finding: `X` is not a property of the item

LOCUS as delivered has `P` = *property of a person* and `X` = *external
condition coded AS a personal property*. Given the item text those are
not distinguished by anything in it — both have a person as their
subject. What separates them is whether the underlying variable is
externally caused, which is a claim about housing markets and shift
rotas.

So **two coders who disagree about what causes housing instability
produce different X-fractions on identical items**, and X-fraction is
one of the three published outcomes. The audit's subject is
misattribution and its headline number is produced by an attribution.

**One judgment moves two of the three outcomes.** Declaring one
fixture's cause, changing no text:

    X-fraction               0.2308  ->  0.3077
    attenuation denominator  7       ->  6
    attenuation coverage     0.1429  ->  0.1667
    E-fraction               0.1538  ->  0.1538   unchanged

Attenuation coverage is taken over *P and H items*, so moving an item to
X removes it from that denominator. And **the direction flatters**: the
item that moved carried no attenuation rule, so its departure raised
coverage — a coder attributing more to external cause makes the
instrument score higher on discounting for external cause, on an
unchanged manual.

E-fraction does not move. It is a property of the text, which is the
control.

## The split, and it is built

`LOCUS` is **derived**, never hand-set — asserted over the AST:

    subject_class      mechanical, from the item's grammatical subject,
                       via nonidentity-census's extractor, imported not
                       reimplemented. Recomputable by anyone with the text.
    externally_caused  declared per item WITH a stated basis. Refused
                       without one, in both directions.

    X = subject is a person AND externally_caused declared True

An item whose subject is a person and whose causal field is
`NOT_DECLARED` codes **P, not X** — a conclusion nobody declared is not
one. Two fixtures exercise that near-miss, one undeclared and one
declared False.

## Three more against the design

**Reverse causation reaches Arm 1.** The confound section says the audit
arm is unaffected because it measures representational capacity rather
than causal share. True of the E-fraction; false of the X-fraction,
since reverse causation is exactly the case where a person-subject
item's variable is *not* externally caused. Same items, two defensible
readings: X 0.3077 against 0.2308, E unchanged either way.

**One coded field has no outcome, and it is the one that separates
recording from explaining.** DIRECTIONALITY asks whether an external
cause may *explain* a household observation or only co-occur with it. It
is collected and not reported, as is ACTIONABILITY TARGET. Two item
sets, identical on all three published outcomes, differ 0.5 against 0.0
on whether external causes may explain — so an instrument that records
external conditions and never lets them do any work is
indistinguishable in the published numbers from one that does. The fix
is one line in the outcome list; `outcomes()` returns it as
`explain_fraction_ADDED`.

**Three denominators, one named.** The ask says to mark unclassified
items rather than forcing them, and does not say which denominator they
sit in. On the fixtures: E-fraction 0.1538 with them in, 0.1667 with
them out — and keeping them in biases it *toward* the drop's own
prediction. Both reported, neither picked.

## What the drop gets right

`UNCLASSIFIED` is required by the ask itself, before any code existed —
the repair this repository has recorded a dozen times, designed in. The
classifier is null-tested both ways (6 of 6 classified, 0 of 3 forced),
because either half alone passes for a coder that is not doing its job.

And this is the third drop in the family to invoke the null-rate
instrument, and **the first to ship the partner**: E-fraction pairs with
attenuation coverage, where `evaluation-frame` M4 and
`move-set-derivation` Arm 1 each shipped one side of a pair.

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `coding.py` | the scheme; derived LOCUS, refused undeclared claims, authored fixtures |
| `audit.py` | egress measurement and the design findings, each demonstrated |
| `selftest_hsa.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `HSA_001..HSA_011` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs of both modules |

Both modules refuse `--selftest` rather than exiting 0 on an invocation
that runs nothing.

## Scope

No E-fraction, X-fraction or attenuation coverage is produced for any
instrument, and nothing here bears on the drop's own retraction
condition in either direction. Arm 2 is UNMEASURED — human scorers, and
a simulated practitioner panel would be a fabricated claim about
practitioners. Arm 3 is UNMEASURED — administrative records, unreachable
and not public.

A second constraint binds whoever *does* have the reading room: much
instrument wording is licensed rather than free, so the scheme codes by
reference with the text optional — and the field most in need of
checking is then the hardest to publish beside its item.

No `no_severity` exemptions: every screen hit was reworded rather than
exempted.

CC0. Stdlib only, parses under 3.9, phone-buildable.
