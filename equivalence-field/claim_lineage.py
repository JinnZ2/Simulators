# claim_lineage.py
# CC0. stdlib-only. phone-buildable.
#
# Falsification as a POINTER, not a tombstone.
#
# A refuted claim is evidence the variable set was incomplete. The break
# points at a missing dimension. The protocol does not retire the claim to a
# graveyard -- it spawns a CHILD:  parent + the exposed variable + a NEW
# independent falsifiable prediction that the new variable makes on its own.
#
# GUARDRAIL (against epicycles): a child is admitted only if the new variable
#   (a) is independently measurable, and
#   (b) predicts something BEYOND rescuing the parent.
# A variable whose only job is to save the old claim, predicting nothing new,
# is an epicycle -> rejected. This is the line between science and rescue.
#
# The record grows a GENEALOGY of understanding, not a list of dead claims.
#
# energy_english: statements/break-notes recorded as given; no moral labels,
# no intent, no interior-state overlay. Status is a measured position, not a
# verdict on the claimant.

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Status(Enum):
    OPEN = "open"          # stated, not yet tested against its condition
    STANDING = "standing"  # tested, its prediction has held so far
    REFUTED = "refuted"    # tested, prediction broke -> pointer to missing var
    RETIRED = "retired"    # superseded by an admitted child


class EpicycleRejected(Exception):
    """Raised when a proposed extension only rescues the parent."""


@dataclass
class Claim:
    cid: str
    statement: str
    variables: tuple[str, ...]         # dimensions the claim is defined over
    prediction: str                    # its OWN independent falsifiable prediction
    refuted_if: str                    # break condition (human-checkable)
    parent: Optional[str] = None
    added_variable: Optional[str] = None   # dimension a refutation exposed
    status: Status = Status.OPEN
    break_note: str = ""               # what broke it (recorded as given)


@dataclass
class Lineage:
    claims: dict[str, Claim] = field(default_factory=dict)

    # -- lifecycle ---------------------------------------------------------
    def add_root(self, claim: Claim) -> Claim:
        self.claims[claim.cid] = claim
        return claim

    def stand(self, cid: str) -> Claim:
        """Mark a claim as having survived a test of its prediction."""
        c = self.claims[cid]
        c.status = Status.STANDING
        return c

    def refute(self, cid: str, break_note: str, exposed_variable: str) -> Claim:
        """
        A break is not death. Record what broke it and the dimension the
        break points at. The claim is now a POINTER awaiting extension.
        """
        c = self.claims[cid]
        c.status = Status.REFUTED
        c.break_note = break_note
        c.added_variable = exposed_variable
        return c

    def extend(
        self,
        refuted_cid: str,
        child_cid: str,
        statement: str,
        new_variable: str,
        new_prediction: str,
        refuted_if: str,
        *,
        independently_measurable: bool,
        predicts_beyond_parent: bool,
    ) -> Claim:
        """
        Spawn a child from a REFUTED claim, enforcing the epicycle guardrail.
        Only admitted if the new variable is independently measurable AND
        makes a prediction beyond rescuing the parent.
        """
        parent = self.claims[refuted_cid]
        if parent.status is not Status.REFUTED:
            raise ValueError("extend only from a REFUTED claim")
        if not (independently_measurable and predicts_beyond_parent):
            raise EpicycleRejected(
                f"'{new_variable}': measurable={independently_measurable}, "
                f"predicts_beyond_parent={predicts_beyond_parent} "
                f"-> epicycle, not admitted"
            )
        child = Claim(
            cid=child_cid,
            statement=statement,
            variables=parent.variables + (new_variable,),
            prediction=new_prediction,
            refuted_if=refuted_if,
            parent=refuted_cid,
            added_variable=new_variable,
            status=Status.OPEN,
        )
        self.claims[child_cid] = child
        parent.status = Status.RETIRED      # superseded, not deleted
        return child

    # -- reading -----------------------------------------------------------
    def genealogy(self, cid: str) -> list[str]:
        """Ordered root -> ... -> cid lineage."""
        chain, cur = [], self.claims.get(cid)
        while cur:
            chain.append(cur.cid)
            cur = self.claims.get(cur.parent) if cur.parent else None
        return list(reversed(chain))

    def frontier(self) -> list[Claim]:
        """Claims currently carrying the understanding (not retired/refuted)."""
        return [c for c in self.claims.values()
                if c.status in (Status.OPEN, Status.STANDING)]

    def pending_pointers(self) -> list[Claim]:
        """Refuted claims awaiting an extension -- the live search directions."""
        return [c for c in self.claims.values() if c.status is Status.REFUTED]


# ---------------------------------------------------------------------------
# self-check: refute -> extend, plus an epicycle rejection
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    L = Lineage()
    L.add_root(Claim(
        cid="K0",
        statement="a border installation reads as pressure by density gradient alone",
        variables=("density",),
        prediction="pressure magnitude tracks the density gradient across the border",
        refuted_if="two cases with equal density gradient show unequal pressure",
    ))

    # it breaks: equal density gradient, different pressure -> missing variable
    L.refute("K0",
             break_note="equal density gradient, pressure differed",
             exposed_variable="capital_ownership_concentration")

    # admitted extension: new var is measurable AND predicts on its own
    child = L.extend(
        "K0", "K1",
        statement="pressure tracks density gradient CONDITIONED on ownership concentration",
        new_variable="capital_ownership_concentration",
        new_prediction="at fixed density gradient, higher ownership concentration "
                        "raises pressure independently",
        refuted_if="ownership concentration varies with no effect at fixed density",
        independently_measurable=True,
        predicts_beyond_parent=True,
    )
    print("genealogy K1:", L.genealogy("K1"))
    print("frontier:", [c.cid for c in L.frontier()])

    # attempted epicycle: a var that only rescues K1, predicts nothing new
    L.refute("K1", break_note="another mismatch", exposed_variable="mood_of_the_week")
    try:
        L.extend("K1", "K2",
                 statement="...but only when we say so",
                 new_variable="mood_of_the_week",
                 new_prediction="(none beyond rescuing K1)",
                 refuted_if="n/a",
                 independently_measurable=False,
                 predicts_beyond_parent=False)
    except EpicycleRejected as e:
        print("rejected:", e)
