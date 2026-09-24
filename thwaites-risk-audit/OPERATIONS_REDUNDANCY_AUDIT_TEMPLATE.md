# OPERATIONS REDUNDANCY AUDIT — Template
### Counts the nodes the diagram doesn't draw. For crews, fleets, shops, farms, small ops.
### Method adapted from `effective-redundancy-audit` (CC0), tuned for human channels.

---

## THE IDEA IN ONE LINE

> You don't have N backups. You have however many survive the same bad week.

Nominal redundancy counts channels. **Effective** redundancy counts channels after you
name the shared nodes — the things that kill several channels at once because they're a
*process, a budget, a season, a supplier, or one person* — none of which appear on any
equipment list.

---

## STEP 1 — LIST YOUR CHANNELS (the nominal count)

Everything that delivers a critical function: people, machines, suppliers, comms,
fuel sources, knowledge holders. Write what the org chart or equipment list would say.

Worksheet:
| # | Channel | Function it covers |
|---|---------|--------------------|
| 1 | | |
| 2 | | |
| ... | | |

**N_nominal = ____**

## STEP 2 — NAME THE SHARED NODES (the part nobody writes down)

Go through this checklist — these are the classic invisible shared nodes:

- [ ] **One person** who knows how X really works (the pairing, not the title)
- [ ] **One supplier / one parts chain** behind "redundant" machines
- [ ] **One fuel source / delivery route** (weather, road, river, or funding can cut all)
- [ ] **One season/weather window** several tasks silently depend on
- [ ] **One budget line or approval** several functions draw from
- [ ] **One comms path** (same cell carrier, same repeater, same person relaying)
- [ ] **One maintenance interval** — deferred maintenance couples "independent" machines
- [ ] **One information source** everyone reads (same gauge, same forecast, same app)

List what you found:
| Shared node | Channels that ALL die with it |
|-------------|-------------------------------|
| | |

## STEP 3 — SCORE EACH CHANNEL (two passes, two coders if possible)

For each channel: does it survive **every** shared node named in Step 2?
Coder's call, honestly made — considering ALL nodes, not the convenient ones.

- **Pass 1 (generous):** count only physical/logistical shared nodes.
- **Pass 2 (risk-weighted):** also count budget, approval, information, and
  knowledge-holder nodes.

If two people can code independently, do it blind and compare. Disagreement between
coders is a finding, not a problem — it means the answer depends on which shared nodes
you're willing to admit, and *that* is worth knowing before the bad week teaches it.

## STEP 4 — COMPUTE N_eff

```
N_eff = (channels surviving ALL shared nodes)
      + 1 if any channel collapsed
```

Interpretation:
- **N_eff = N_nominal** → your redundancy is real (rare; check Step 2 again honestly)
- **1 < N_eff < N_nominal** → partial; the collapsed group is one failure waiting
- **N_eff = 1** → you have one system wearing several name tags

## STEP 5 — THE OUTPUT IS A LIST, NOT A SCORE

The point isn't the number. The point is the Step 2 table: each shared node is a
specific, fixable exposure. Rank them by: (a) how many channels die with it ×
(b) how expensive/slow a second path is. Fix the cheap high-casualty ones first.

**Rules:**
- No manufactured answers. "Unknown whether X shares a node" is a valid cell —
  write UNKNOWN, not a guess. Unknowns are the to-do list.
- Re-run after any fix, and on a schedule (yearly, or after any near-miss).
  Redundancy decays silently: parts standardize, people leave, suppliers merge.
- A near-miss is free data. After any bad week, ask: which shared node just showed
  itself? Add it to the table while it's visible.

---

## WORKED MINI-EXAMPLE (constructed, labeled — not your operation)

Remote northern operation: two trucks, two welders, stockpiled fuel, satellite comms.

| Channel | Survives generous pass? | Survives risk-weighted pass? |
|---|---|---|
| Truck A | yes | NO — same sole fuel delivery route |
| Truck B | yes | NO — same route; same one mechanic's knowledge |
| Welder 1 | yes | NO — same parts supplier as Welder 2 |
| Welder 2 | yes | NO — same supplier |
| Satcomms | yes | NO — same single account/approval chain |

N_nominal = 5. N_eff (generous) = 5. N_eff (risk-weighted) = **1**.
The diagram said five channels. The shared nodes said: one road, one supplier, one
person's head. The fix list prices itself: second supplier account, documented
procedures out of the mechanic's head, fuel buffer sized to the road's closure history.
