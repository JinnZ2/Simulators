"""
test_instruments.py -- door tests. CC0. stdlib only.

Tests the REFUSALS, not the acceptances. A registry is only as good as what
it turns away; an accept-anything workbench hands junk to field scientists,
whose time is the one resource this design cannot manufacture.

T-I1  no falsifier                       -> MissingFalsifier
T-I2  unnamed principle                  -> IncompleteInstrument (magic)
T-I3  empty blind_to                     -> IncompleteInstrument (supremacy)
T-I4  R3 with no borrowed_from           -> IncompleteInstrument (no across)
T-I5  R2 with no resolution              -> ContestedEntry (danger bin)
T-I6  R2/DEPENDENCY, reaches_layer bogus -> ContestedEntry (not in stack)
T-I6b R2/DEPENDENCY, no removes_above    -> ContestedEntry (gesture, not claim)
T-I7  CONTESTED, 1 frame                 -> ContestedEntry (verdict-with-steps)
T-I8  CONTESTED, undated frame           -> ContestedEntry (look-back-that-doesn't)
T-I9  CONTESTED, 2 dated                 -> registers, held_open, no ranking
T-I10 reclassify held-open               -> syndrome logged, frames kept
T-I11 valid R3/R4 proposal               -> registers, actor routing, emit()
                                            carries falsifier + state + stack
T-I12 reclassified entry enters AI lane  -> trace present in log
"""

import os
import instruments as I

AS_OF = "2026-07-24"
LOG = "/tmp/test_instruments_divergence.ndjson"


def expect(exc, fn, label):
    try:
        fn()
    except exc as e:
        print(f"  PASS {label}: {type(e).__name__}")
        return True
    except Exception as e:
        print(f"  FAIL {label}: wrong exception {type(e).__name__}: {e}")
        return False
    print(f"  FAIL {label}: no exception raised")
    return False


def base(**kw):
    d = dict(
        name="probe", measures="claim X", transduces="B-field -> voltage",
        principle="Faraday induction", blind_to=["DC fields"],
        falsifier="reads the same with the coil disconnected",
        why_absent="R5", as_of=AS_OF)
    d.update(kw)
    return I.Instrument(**d)


ok = []
print("DOOR REFUSALS")
ok.append(expect(I.MissingFalsifier,
                 lambda: I.register(base(falsifier="")), "T-I1 no falsifier"))
ok.append(expect(I.IncompleteInstrument,
                 lambda: I.register(base(principle="quantum")),
                 "T-I2 unnamed principle"))
ok.append(expect(I.IncompleteInstrument,
                 lambda: I.register(base(blind_to=[])), "T-I3 empty blind_to"))
ok.append(expect(I.IncompleteInstrument,
                 lambda: I.register(base(why_absent="R3", borrowed_from=[])),
                 "T-I4 reach with no across"))
ok.append(expect(I.ContestedEntry,
                 lambda: I.register(base(why_absent="R2")),
                 "T-I5 R2 unlabelled"))
ok.append(expect(I.ContestedEntry,
                 lambda: I.register(base(name="dep-bogus", why_absent="R2",
                                         resolution=I.DEPENDENCY,
                                         reaches_layer="feelings",
                                         removes_above=["something"])),
                 "T-I6 R2/DEPENDENCY reaches_layer not in stack"))
ok.append(expect(I.ContestedEntry,
                 lambda: I.register(base(name="dep-hollow", why_absent="R2",
                                         resolution=I.DEPENDENCY,
                                         reaches_layer="biology",
                                         removes_above=[])),
                 "T-I6b R2/DEPENDENCY empty removes_above"))

one_frame = [I.Frame("frame-a", "practice a", "source a", "era a")]
ok.append(expect(I.ContestedEntry,
                 lambda: I.register(base(why_absent="R2",
                                         resolution=I.CONTESTED,
                                         contest="what counts as a party",
                                         frames=one_frame)),
                 "T-I7 one-sided contest"))

undated = [I.Frame("frame-a", "practice a", "source a", "era a"),
           I.Frame("frame-b", "practice b", "source b", "")]
ok.append(expect(I.ContestedEntry,
                 lambda: I.register(base(why_absent="R2",
                                         resolution=I.CONTESTED,
                                         contest="what counts as a party",
                                         frames=undated)),
                 "T-I8 undated frame"))

print("\nHELD OPEN")
frames = [I.Frame("frame-a", "practice a", "source a", "era a"),
          I.Frame("frame-b", "practice b", "source b", "era b")]
held = I.register(base(name="contested-probe", why_absent="R2",
                       resolution=I.CONTESTED,
                       contest="whether a party exists to be harmed",
                       frames=frames))
t9 = held.held_open and len(held.frames) == 2 and held.actor.startswith("HUMANS")
print(f"  {'PASS' if t9 else 'FAIL'} T-I9 held_open={held.held_open} "
      f"frames={len(held.frames)} actor={held.actor}")
no_rank = not any(f in I.Frame.__dataclass_fields__
                  for f in ("rank", "score", "severity", "weight", "priority"))
print(f"  {'PASS' if no_rank else 'FAIL'} T-I9b Frame carries no ordering field")
ok += [t9, no_rank]
for line in held.loud:
    print(f"       loud: {line}")

print("\nRECLASSIFICATION SYNDROME")
if os.path.exists(LOG):
    os.remove(LOG)
inst, sid = I.reclassify("contested-probe", "R4", observed_at=AS_OF,
                         log_path=LOG, note="routed around")
entries = I.divlog.load(LOG)
t10 = (sid is not None and len(entries) == 1
       and entries[0].kind == I.RECLASSIFIED_WHILE_CONTESTED
       and len(inst.frames) == 2)
print(f"  {'PASS' if t10 else 'FAIL'} T-I10 syndrome={sid} "
      f"entries={len(entries)} frames_kept={len(inst.frames)}")
print(f"       loud: {inst.loud[-1]}")
ok.append(t10)

print("\nVALID PROPOSAL")
good = I.register(I.Instrument(
    name="example-R4", measures="claim Y", transduces="A -> B readout",
    principle="named real effect", blind_to=["region Z"],
    falsifier="signal persists with the transducer removed",
    why_absent="R4", as_of=AS_OF, borrowed_from=["older-era instrument"]))
payload = I.emit("example-R4")
t11 = (good.actor == "AI CAN" and I.HANDOFF_STATE in payload
       and "falsifier" in payload and "registry_blind_to" in payload
       and "dependency_stack" in payload)
print(f"  {'PASS' if t11 else 'FAIL'} T-I11 actor={good.actor} "
      f"emit carries state+falsifier+recursion+stack")
ok.append(t11)

# T-I12 -- first draft of T-I11 asserted by_actor("AI CAN") == ["example-R4"]
# and FAILED, because the reclassified contested-probe now sits in the AI lane
# too. The test was wrong; the module was right, and the failure is the point:
# reclassifying a held-open contest to R4 MOVES IT INTO AI'S LANE. That is the
# exact burial-by-paperwork move. The only trace is the divlog entry and the
# loud line -- so this asserts the trace survives the routing.
lane = I.by_actor("AI CAN")
t12 = ("contested-probe" in lane
       and any(I.RECLASSIFIED_WHILE_CONTESTED == e.kind
               and e.subject == "contested-probe" for e in I.divlog.load(LOG)))
print(f"  {'PASS' if t12 else 'FAIL'} T-I12 reclassified entry entered AI lane "
      f"{lane} -- trace present in log")
ok.append(t12)

print(f"\n{sum(ok)}/{len(ok)} passed")
print(f"held_open registry: {I.held_open()}")
