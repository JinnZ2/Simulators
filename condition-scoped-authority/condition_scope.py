#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
condition_scope.py - a single ranking cannot represent scope. Exhaustively.

    python3 condition_scope.py [--selftest]

Marker under exploration. Delivered spec: SPEC_CONDITION_SCOPE.md.
Companion to stop-authority/.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE CLAIM IS CHECKABLE RATHER THAN ARGUABLE. "Authority is held by a position
FOR A CLASS OF CONDITION. Rank and scope are different objects and a single
ranking cannot represent scope." A total order over positions either does or
does not reproduce a condition-scoped authority table, so `rank_search()`
enumerates EVERY total order and scores each. That is a complete search at
these sizes, not a sample: with n positions there are n! orders and all of
them are checked.

RANK DOES NOT INVERT, AND MODELLING IT AS INVERSION IS ALREADY THE ERROR.
The spec is explicit: the domain is partitioned, and inside the partition the
principal was never the decider. So the table here is not "guard outranks
principal during a threat" -- it is "the threat condition is not the
principal's domain at all". `holds()` returns NOT_IN_DOMAIN, not a lower
number, because a smaller quantity of the same thing is the representation
the spec says does not fit.

THE PARTITION MUST BE SYMMETRIC OR IT IS NOT A PARTITION. "Neither party reads
the other's domain. The specialist does not claim the executive's domain
either. This constrains both equally, which is why it survives argument -- it
is not a transfer of power." A claimed scope where one party holds a domain
and also holds the other's is a power transfer wearing the vocabulary, and
`Partition` refuses to build one.

BOUND AND ADVISORY ARE BOTH CALLED AUTHORITY, AND A MEASUREMENT THAT DOES NOT
SAY WHICH IS UNSIGNED. That is the spec's word and it is the same word the
stop-count carries in stop-authority/: a number whose sign is not determined
by the measurement. `AuthorityClaim` refuses to compare or score an UNSTATED
claim rather than defaulting it either way.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import itertools
import sys

HOLDS = ("DECIDES", "NOT_IN_DOMAIN")
KINDS = ("BOUND", "ADVISORY", "UNSTATED")


class ScopeError(Exception):
    pass


class Partition(object):
    """Positions, condition classes, and who decides in each.

    Not a ranking. The table is a mapping from condition class to the single
    position whose reading capacity sits there.
    """

    def __init__(self, name, positions, table, declared_by):
        if not declared_by:
            raise ScopeError(
                "a partition records who declared it. Which domain a "
                "position reads is a claim about competence, and an "
                "unattributed one is this module's assertion")
        missing = [c for c, p in table.items() if p not in positions]
        if missing:
            raise ScopeError("condition classes assign to unknown "
                             "positions: %s" % ", ".join(sorted(missing)))
        holders = set(table.values())
        idle = [p for p in positions if p not in holders]
        if idle:
            raise ScopeError(
                "every position must hold at least one condition class, or "
                "it is not a party to the partition: %s. A position with no "
                "domain is not constrained by the arrangement and gains "
                "from it for free" % ", ".join(sorted(idle)))
        self.name = name
        self.positions = list(positions)
        self.table = dict(table)
        self.declared_by = declared_by

    def holds(self, position, condition):
        """DECIDES or NOT_IN_DOMAIN. Never a smaller quantity of authority."""
        if condition not in self.table:
            raise ScopeError("unknown condition class %r" % condition)
        return "DECIDES" if self.table[condition] == position \
            else "NOT_IN_DOMAIN"

    def domains(self, position):
        return sorted(c for c, p in self.table.items() if p == position)

    def is_symmetric(self):
        """Does any position hold every domain, or hold another's as well.

        The spec's justification is symmetric by construction: neither party
        reads the other's domain. A partition where one position holds all
        classes is a rank in partition clothing.
        """
        counts = dict((p, len(self.domains(p))) for p in self.positions)
        total = len(self.table)
        monopolist = [p for p, n in counts.items() if n == total]
        return {"symmetric": not monopolist,
                "counts": counts,
                "monopolist": monopolist[0] if monopolist else None,
                "why": "each position is excluded from the others' classes, "
                       "which constrains both equally" if not monopolist
                       else "%s holds every condition class, which is a "
                            "ranking written as a table" % monopolist[0]}


def rank_predicts(order, partition):
    """What a total order predicts: the highest-ranked position decides.

    This is the only thing a rank CAN say. It has no condition column, so it
    says the same thing in every condition class.
    """
    top = order[0]
    return dict((c, top) for c in partition.table)


def score_order(order, partition):
    pred = rank_predicts(order, partition)
    wrong = sorted(c for c in partition.table
                   if pred[c] != partition.table[c])
    return {"order": list(order),
            "wrong": wrong,
            "n_wrong": len(wrong),
            "n_conditions": len(partition.table),
            "exact": not wrong}


def rank_search(partition):
    """Every total order, scored. Complete, not sampled."""
    results = [score_order(o, partition)
               for o in itertools.permutations(partition.positions)]
    exact = [r for r in results if r["exact"]]
    best = min(r["n_wrong"] for r in results)
    return {
        "partition": partition.name,
        "n_positions": len(partition.positions),
        "n_orders_checked": len(results),
        "n_orders_possible": _fact(len(partition.positions)),
        "complete": len(results) == _fact(len(partition.positions)),
        "n_exact": len(exact),
        "best_n_wrong": best,
        "best_orders": [r for r in results if r["n_wrong"] == best],
        "all": results,
        "verdict": "NO_RANK_REPRESENTS_IT" if not exact
                   else "A_RANK_REPRESENTS_IT",
        "why": "a total order has no condition column, so it names one "
               "decider and names them in every class. The table names "
               "different deciders in different classes, and no reordering "
               "changes that",
    }


def _fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


# --- the delivered case ----------------------------------------------------

DETAIL = Partition(
    name="protective detail (as delivered)",
    positions=["principal", "bodyguard"],
    table={
        "schedule": "principal",
        "finances": "principal",
        "politics": "principal",
        "clientele": "principal",
        "threat_live": "bodyguard",
    },
    declared_by="operator, SPEC_CONDITION_SCOPE.md worked case")

# EXTENSION, not delivered: a third scoped position, to see whether adding
# domains makes a rank fit better or worse.
DETAIL_3 = Partition(
    name="protective detail + medical (EXTENSION, not delivered)",
    positions=["principal", "bodyguard", "physician"],
    table={
        "schedule": "principal",
        "finances": "principal",
        "politics": "principal",
        "clientele": "principal",
        "threat_live": "bodyguard",
        "medical_emergency": "physician",
    },
    declared_by="this module, marked as an extension")


def worked_case():
    return rank_search(DETAIL)


def extension_case():
    return rank_search(DETAIL_3)


def where_the_best_rank_fails():
    """Which class the least-wrong ranking gets wrong. Not a random one."""
    r = worked_case()
    best = r["best_orders"][0]
    return {"best_order": best["order"],
            "n_wrong": best["n_wrong"],
            "wrong_classes": best["wrong"],
            "why_it_matters": "the best available ranking is the one that "
                              "puts the principal on top, and the single "
                              "class it gets wrong is the live threat -- the "
                              "class in which the spec says the specialist "
                              "holds total authority including physical "
                              "force against the principal's stated "
                              "preference. The approximation fails exactly "
                              "where the stakes are",
            "accuracy": 1.0 - best["n_wrong"] / best["n_conditions"],
            "why_accuracy_misleads": "80% of condition classes correct reads "
                                     "as a good approximation. The classes "
                                     "are not interchangeable and averaging "
                                     "over them is the same move as scoring "
                                     "a facility on the variables still "
                                     "being read"}


# --- BOUND vs ADVISORY -----------------------------------------------------

class AuthorityClaim(object):
    """A claim that some position holds authority. Unsigned unless stated."""

    def __init__(self, position, condition, kind, evidence=None):
        if kind not in KINDS:
            raise ScopeError("kind must be one of %s" % (KINDS,))
        self.position = position
        self.condition = condition
        self.kind = kind
        self.evidence = list(evidence or [])

    def measurable(self):
        if self.kind == "UNSTATED":
            return {"measurable": False, "state": "UNSIGNED",
                    "why": "BOUND and ADVISORY are both called authority. A "
                           "measurement using the word without saying which "
                           "is unsigned, and defaulting it either way "
                           "invents the sign"}
        return {"measurable": True, "state": self.kind,
                "why": "the kind is stated, so the claim has a sign"}


# The EHS evidence list, as delivered. The criterion applied: an item
# discriminates BOUND from ADVISORY only if it would be FALSE under an
# advisory arrangement.
EHS_EVIDENCE = [
    {"item": "visibility",
     "true_under_advisory": True,
     "why": "an advisor is visible. Visibility is satisfied by being seen, "
            "which does not require the finding to stand"},
    {"item": "seat at executive meetings",
     "true_under_advisory": True,
     "why": "an advisor has a seat. Attendance is satisfied by presence, "
            "which does not require reversal to be unavailable"},
    {"item": "influence on strategy",
     "true_under_advisory": True,
     "why": "influence is what advisory means. The word names the "
            "advisory case"},
]

# What would discriminate. Named so the zero above is a measured zero.
WOULD_DISCRIMINATE = [
    {"item": "a finding that stood against a party who sought its reversal",
     "true_under_advisory": False,
     "why": "reversal being unavailable is exactly what BOUND asserts and "
            "advisory denies"},
    {"item": "a documented reversal, and by whom",
     "true_under_advisory": False,
     "why": "a reversal record distinguishes the two directly. Its absence "
            "does not -- see stop-authority/binding.py, where an empty "
            "reversal record beside zero findings is NOT_LOOKED"},
]


def evidence_audit():
    """How many offered items separate BOUND from ADVISORY."""
    disc = [e for e in EHS_EVIDENCE if not e["true_under_advisory"]]
    return {
        "n_offered": len(EHS_EVIDENCE),
        "n_discriminating": len(disc),
        "offered": EHS_EVIDENCE,
        "would_discriminate": WOULD_DISCRIMINATE,
        "criterion": "an item discriminates only if it would be FALSE under "
                     "an advisory arrangement",
        "verdict": "EVERY_OFFERED_ITEM_IS_SATISFIABLE_BY_ADVISORY"
                   if not disc else "SOME_ITEMS_DISCRIMINATE",
        "why": "the strong configuration is evidenced entirely by indicators "
               "an advisory arrangement also produces. That is not weak "
               "evidence for BOUND, it is no evidence either way -- the "
               "indicators do not vary between the two cases",
    }


def collapsed_claim(partition):
    """Write down what a rank-only structure states silently.

    "The structure then asserts that the top of the hierarchy holds every
    domain's reading capacity simultaneously. Nobody would defend that claim
    if it were written down. The structure states it silently."
    """
    top = partition.positions[0]
    classes = sorted(partition.table)
    return {
        "position": top,
        "asserted": "%s holds the reading capacity for all %d condition "
                    "classes simultaneously: %s"
                    % (top, len(classes), ", ".join(classes)),
        "classes_claimed": classes,
        "classes_actually_held": partition.domains(top),
        "n_claimed": len(classes),
        "n_actually_held": len(partition.domains(top)),
        "overclaim": [c for c in classes
                      if c not in partition.domains(top)],
        "why": "rank has no condition column, so a rank-only structure says "
               "the same thing in every class. Written out, the claim is "
               "about reading capacity in domains the position does not "
               "read",
    }


def confidence():
    return {"the_search": "complete, not sampled. Every one of n! total "
                          "orders is enumerated and scored, so 'no rank "
                          "represents it' is established for THIS table "
                          "rather than argued",
            "the_table": "the delivered worked case, carried as stated. "
                         "Whether protective details actually partition this "
                         "way is the operator's claim and is not checked "
                         "here",
            "the_extension": "the third position is this module's, marked as "
                             "such. It tests whether more scoped domains "
                             "help a rank fit, and they do not",
            "the_evidence_audit": "applies a stated criterion -- would the "
                                  "item be FALSE under advisory -- to the "
                                  "three items the spec lists. It is a "
                                  "reading of three phrases, not a survey "
                                  "of the EHS literature",
            "resolved": False}


def breaks():
    return [
        "NO TOTAL ORDER REPRODUCES THE DELIVERED TABLE, AND THE BEST ONE "
        "FAILS EXACTLY WHERE THE STAKES ARE. Both of the two possible "
        "rankings are wrong: principal-on-top misses one class of five, "
        "bodyguard-on-top misses four. The one class the better ranking "
        "misses is the live threat -- the class in which the spec says the "
        "specialist holds total authority including physical force against "
        "the principal's stated preference. 80% of classes correct is not a "
        "good approximation when the classes are not interchangeable",
        "ADDING SCOPED DOMAINS MAKES A RANK FIT WORSE, NOT BETTER. With a "
        "third scoped position the search checks all six orders and the best "
        "is wrong on two classes of six. Every domain with its own reading "
        "capacity is another class the single ranking must get wrong, so the "
        "representation degrades with exactly the thing that makes the "
        "structure work",
        "EVERY ITEM IN THE OFFERED EVIDENCE LIST IS SATISFIABLE BY AN "
        "ADVISORY ARRANGEMENT, WHICH MAKES IT NO EVIDENCE EITHER WAY. "
        "Visibility, a seat at executive meetings, influence on strategy: an "
        "advisor has all three. These are not weak indicators of BOUND, they "
        "are indicators that do not vary between BOUND and ADVISORY, so a "
        "configuration scoring high on all three is unmeasured rather than "
        "strong. What would discriminate is named beside them, and the "
        "absence of a reversal record is not it -- see "
        "stop-authority/binding.py, where an empty reversal record beside "
        "zero findings reads NOT_LOOKED",
        "THE PARTITION IS TAKEN ON THE SPEC'S WORD AND THE MODULE COMPUTES "
        "OVER IT. Whether a bodyguard really holds total authority in a live "
        "threat, and really holds none over clientele, is a claim about how "
        "protective details work. If the partition is wrong then the search "
        "is a complete proof about a table nobody should have written",
        "SYMMETRY IS CHECKED STRUCTURALLY AND CANNOT BE CHECKED IN "
        "SUBSTANCE. Partition refuses a table where one position holds every "
        "class, and refuses a position with no class at all. It cannot tell "
        "whether the domains assigned actually match where reading capacity "
        "sits -- which is the spec's whole justification and is a claim "
        "about competence that no arrangement of the table verifies",
    ]


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def report():
    L = ["CONDITION-SCOPED AUTHORITY -- rank has no condition column",
         "=" * 72, ""]
    L.append("  Authority is held by a position FOR A CLASS OF CONDITION.")
    L.append("  Rank and scope are different objects.")
    L.append("")
    L.append("  THE PARTITION, AS DELIVERED")
    L.append("")
    L.append("    %-20s %s" % ("condition class", "decides"))
    for c in sorted(DETAIL.table):
        L.append("    %-20s %s" % (c, DETAIL.table[c]))
    L.append("")
    L.append("    the bodyguard in 'schedule': %s"
             % DETAIL.holds("bodyguard", "schedule"))
    L.append("    the principal in 'threat_live': %s"
             % DETAIL.holds("principal", "threat_live"))
    L.append("")
    L.append("    NOT_IN_DOMAIN, not a smaller number. Rank does not")
    L.append("    invert -- inside the partition the principal was never")
    L.append("    the decider.")
    L.append("")
    sym = DETAIL.is_symmetric()
    L.append("    symmetric: %s" % sym["symmetric"])
    for line in _wrap(sym["why"], "      "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  EVERY TOTAL ORDER, CHECKED")
    L.append("")
    w = worked_case()
    L.append("    orders checked %d of %d possible -- complete: %s"
             % (w["n_orders_checked"], w["n_orders_possible"],
                w["complete"]))
    L.append("")
    L.append("    %-26s %s" % ("order", "wrong"))
    for r in w["all"]:
        L.append("    %-26s %d" % (" > ".join(r["order"]), r["n_wrong"]))
        for line in _wrap("misses: " + ", ".join(r["wrong"]), "      "):
            L.append(line)
    L.append("")
    L.append("    exact matches: %d      VERDICT: %s"
             % (w["n_exact"], w["verdict"]))
    L.append("")
    for line in _wrap(w["why"], "    "):
        L.append(line)
    L.append("")
    fw = where_the_best_rank_fails()
    L.append("    best available ranking: %s" % " > ".join(fw["best_order"]))
    L.append("    accuracy over classes:  %.2f" % fw["accuracy"])
    L.append("    class it misses:        %s" % ", ".join(fw["wrong_classes"]))
    L.append("")
    for line in _wrap(fw["why_it_matters"], "    "):
        L.append(line)
    L.append("")
    for line in _wrap(fw["why_accuracy_misleads"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  DOES ADDING SCOPED DOMAINS HELP A RANK FIT")
    L.append("")
    e = extension_case()
    L.append("    %-46s %-8s %s" % ("partition", "orders", "best wrong"))
    L.append("    %-46s %-8d %d of %d"
             % ("2 positions (delivered)", w["n_orders_checked"],
                w["best_n_wrong"], len(DETAIL.table)))
    L.append("    %-46s %-8d %d of %d"
             % ("3 positions (extension)", e["n_orders_checked"],
                e["best_n_wrong"], len(DETAIL_3.table)))
    L.append("")
    L.append("    exact matches in the extension: %d" % e["n_exact"])
    L.append("    Every domain with its own reading capacity is another")
    L.append("    class the single ranking must get wrong.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  WHAT THE COLLAPSED STRUCTURE STATES SILENTLY")
    L.append("")
    cc = collapsed_claim(DETAIL)
    for line in _wrap(cc["asserted"], "    "):
        L.append(line)
    L.append("")
    L.append("    classes actually held by that position: %d of %d"
             % (cc["n_actually_held"], cc["n_claimed"]))
    L.append("    overclaimed: %s" % ", ".join(cc["overclaim"]))
    L.append("")
    for line in _wrap(cc["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  BOUND vs ADVISORY -- THE OFFERED EVIDENCE")
    L.append("")
    a = evidence_audit()
    for line in _wrap("criterion: " + a["criterion"], "    "):
        L.append(line)
    L.append("")
    L.append("    %-34s %s" % ("offered item", "true under advisory"))
    for it in a["offered"]:
        L.append("    %-34s %s" % (it["item"], it["true_under_advisory"]))
    L.append("")
    L.append("    offered: %d   discriminating: %d"
             % (a["n_offered"], a["n_discriminating"]))
    L.append("    VERDICT: %s" % a["verdict"])
    L.append("")
    for line in _wrap(a["why"], "    "):
        L.append(line)
    L.append("")
    L.append("    what would discriminate:")
    for it in a["would_discriminate"]:
        for line in _wrap("- " + it["item"], "      "):
            L.append(line)
    L.append("")
    u = AuthorityClaim("EHS function", "any", "UNSTATED").measurable()
    L.append("    an UNSTATED claim: measurable=%s, state=%s"
             % (u["measurable"], u["state"]))
    for line in _wrap(u["why"], "      "):
        L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("a position outside its domain is NOT_IN_DOMAIN, not a lower number",
       DETAIL.holds("bodyguard", "schedule") == "NOT_IN_DOMAIN"
       and DETAIL.holds("principal", "threat_live") == "NOT_IN_DOMAIN")
    ck("and inside it, DECIDES",
       DETAIL.holds("bodyguard", "threat_live") == "DECIDES")
    ck("NOT_IN_DOMAIN is one of only two values -- no partial authority",
       set(HOLDS) == {"DECIDES", "NOT_IN_DOMAIN"})

    try:
        Partition("x", ["a", "b"], {"c1": "a"}, declared_by="op")
        ok = False
    except ScopeError:
        ok = True
    ck("a position with no condition class is refused: it is not a party "
       "to the arrangement", ok)
    try:
        Partition("x", ["a", "b"], {"c1": "a", "c2": "b"}, declared_by=None)
        ok = False
    except ScopeError:
        ok = True
    ck("a partition records who declared it", ok)
    mono = Partition("m", ["a", "b"], {"c1": "a", "c2": "a", "c3": "b"},
                     declared_by="op")
    ck("symmetry holds when each position is excluded from the others'",
       DETAIL.is_symmetric()["symmetric"] is True
       and mono.is_symmetric()["symmetric"] is True)

    w = worked_case()
    ck("the search is complete, not sampled",
       w["complete"] is True
       and w["n_orders_checked"] == w["n_orders_possible"] == 2)
    ck("no total order reproduces the table",
       w["n_exact"] == 0 and w["verdict"] == "NO_RANK_REPRESENTS_IT")
    ck("the principal-on-top ranking misses exactly one class",
       any(r["order"] == ["principal", "bodyguard"] and r["n_wrong"] == 1
           for r in w["all"]))
    ck("and the bodyguard-on-top ranking misses four",
       any(r["order"] == ["bodyguard", "principal"] and r["n_wrong"] == 4
           for r in w["all"]))
    ck("so rank does not invert -- neither direction fits",
       all(not r["exact"] for r in w["all"]))

    fw = where_the_best_rank_fails()
    ck("the class the best ranking misses is the live threat",
       fw["wrong_classes"] == ["threat_live"])
    ck("its accuracy over classes reads high", fw["accuracy"] > 0.75)
    ck("and the module says why that number misleads",
       "not interchangeable" in fw["why_accuracy_misleads"])

    e = extension_case()
    ck("the extension checks all six orders",
       e["n_orders_checked"] == 6 and e["complete"] is True)
    ck("still no exact match", e["n_exact"] == 0)
    ck("and the best ranking is wrong on MORE classes, not fewer",
       e["best_n_wrong"] > w["best_n_wrong"])

    cc = collapsed_claim(DETAIL)
    ck("the silent claim is written out in full",
       "all 5 condition classes simultaneously" in cc["asserted"])
    ck("and the overclaim is named",
       cc["overclaim"] == ["threat_live"]
       and cc["n_actually_held"] < cc["n_claimed"])

    a = evidence_audit()
    ck("every offered evidence item is satisfiable by advisory",
       a["n_discriminating"] == 0
       and a["verdict"] == "EVERY_OFFERED_ITEM_IS_SATISFIABLE_BY_ADVISORY")
    ck("the criterion is stated, so the zero is measured not asserted",
       "FALSE under an advisory" in a["criterion"])
    ck("and what would discriminate is named beside it",
       len(a["would_discriminate"]) >= 2
       and all(not x["true_under_advisory"]
               for x in a["would_discriminate"]))

    ck("an UNSTATED authority claim is unsigned and refuses to measure",
       AuthorityClaim("p", "c", "UNSTATED").measurable()["measurable"]
       is False)
    ck("a stated one measures",
       AuthorityClaim("p", "c", "BOUND").measurable()["state"] == "BOUND")

    ck("the no-rank-fits result leads the breaks list",
       "NO TOTAL ORDER REPRODUCES" in breaks()[0])
    ck("more domains making the fit worse is disclosed",
       any("WORSE, NOT BETTER" in b for b in breaks()))
    ck("the partition being taken on the spec's word is disclosed",
       any("TAKEN ON THE SPEC'S WORD" in b for b in breaks()))
    ck("that substance-symmetry cannot be checked is disclosed",
       any("cannot be checked in" in b.lower() for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "EVERY TOTAL ORDER, CHECKED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="condition-scoped authority")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
