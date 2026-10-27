# WORKED CASE 2: ALWAYS-ON AI WEARABLES AT WORK

Instrument: `spec.md`. This case applies the spec to camera-bearing and
always-listening AI wearables (glasses, pendants) carried into
workplaces. It is not a finding about any product, maker or user.

Status tags: OBSERVED / DERIVED / PROPOSED / UNMEASURED.
Citation states: VERIFIED / CORRECTED / NOT FOUND (checked 2026-10-16,
through search-result text; primary pages were not opened).

---

## 0. REPORTED FACTS AND CITATION CHECK

Devices announced at Meta Connect 2026 (2026-09-23; some reports date
the keynote 2026-09-24).

| # | Reported line | State | What the sources say |
|---|---|---|---|
| W1 | VR Glasses, $1,299 | VERIFIED | Price reported; release timing reported inconsistently (spring / spring 2027) [1][2] |
| W2 | VR Glasses, full-view display | NOT FOUND | Not stated explicitly in the sources read |
| W3 | Muse Charm, always-on AI pendant | VERIFIED | Pendant/keychain with a small screen showing a character and a fingerprint scanner [3] |
| W4 | Muse Charm ships December | VERIFIED as reported target | Reported (Axios via secondary sources); not confirmed by the maker; no price [3] |
| W5 | Muse Charm, no camera | NOT FOUND | No source states this explicitly |
| W6 | Ray-Ban Meta Audio, camera-free | VERIFIED | Camera-free, $349, available Oct 13, 12 h battery [3] |
| W7 | Ray-Ban Meta Audio, conversation boost | NOT FOUND (for this model) | An FDA-cleared hearing-enhancement / OTC hearing-aid feature was announced for supported glasses; whether the Audio model has it is not stated [4] |

Sources:
1. https://www.cnbc.com/2026/09/23/mark-zuckerberg-1299-meta-vr-glasses-ai-agent.html
2. https://www.tomsguide.com/news/live/meta-connect-2026-live
3. https://www.androidauthority.com/ray-ban-meta-audio-muse-charm-launched-3714882/
4. https://thenextweb.com/news/meta-vr-glasses-hearing-aid-connect-2026

[UNMEASURED] If an audio wearable boosts or filters ambient sound, its
effect on hearing backup beepers, alarms, horns and radio calls on a
worksite has no measurement on record.

---

## 1. JURISDICTION (INTERFACE 8, 9, 14)

- [OBSERVED, carried] OSHA's General Duty Clause applies to recognized
  hazards in the workplace; employer liability follows.
- Gaps (all DERIVED):
  - Commercial motor vehicle drivers: the FMCSA handheld mobile phone
    rule was written for phones; whether an always-on wearable is a
    "mobile telephone" in use is AMBIGUOUS.
  - State handheld laws: same question, fifty times.
  - All-party-consent wiretap states: a wearable that records audio in
    a cab, a dock or a break room records parties who did not consent.
  - Contractors and gig workers: no employer of record carries the
    OSHA duty.

---

## 2. THE GIG BIND (INTERFACE 9, 11, 13)

- [DERIVED] If a platform bans wearables for its gig workers, the ban
  is evidence of control, and control is evidence of misclassification.
- [DERIVED] If the platform stays silent, it keeps device liability
  without control.
- [PROPOSED] Resolution: the layered subcontractor model already used
  in trucking and courier work. Device rules become contract terms
  that flow down each layer, not employer policy.
- [DERIVED] Gig workers have no regulatory layer that sees them as a
  workforce. [PROPOSED] A registration layer is needed before any rule
  can attach.

---

## 3. CHAIN OF CUSTODY (INTERFACE 6)

- [DERIVED] Wearables break custody: a load, a document, a patient
  record or a site seen by a wearable leaves through a channel no
  custody log covers.
- [DERIVED] Client and shipper contracts were written before
  always-listening devices; their confidentiality and custody clauses
  do not name them.
- [UNMEASURED] How often custody-sensitive material is captured.

---

## 4. LIABILITY CHAIN (INTERFACE 6, 11, 13)

    wearer -> device -> cloud -> AI processor

- [DERIVED] No law apportions a loss across this chain.
- [DERIVED] The cloud holder bears the security duty for stored data.
- [DERIVED] A third party captured by the device (the owner of a
  document, a bystander, a client) has no contract with the vendor.
- [DERIVED] Ingestion into training is irreversible: data used to train
  cannot be recalled from the model.
- [OBSERVED, carried] HIPAA business-associate agreements flow duties
  down a chain of processors. That is the precedent. [DERIVED] No
  equivalent flow-down exists for wearables.

Law table (spec 1.13), first pass:

| Body of law | State |
|---|---|
| tort / product | AMBIGUOUS |
| criminal | AMBIGUOUS (wiretap in all-party states) |
| privacy / wiretap | AMBIGUOUS |
| contract | ABSENT (custody clauses predate the device) |
| insurance | AMBIGUOUS (cyber vs general liability) |
| property | FITS |
| 4th Amendment | AMBIGUOUS (third-party doctrine for cloud copies) |

[DERIVED] n_ambiguous = 5 of 7 on this first pass (a reading, not a
measurement).

---

## 5. OPEN GAPS

- [UNMEASURED] Ambient-sound masking of worksite alarms (section 0).
- [UNMEASURED] Capture rate of custody-sensitive material.
- [DERIVED] Device status under handheld rules.
- [DERIVED] Consent across all-party states for workers who cross state
  lines in one shift.
- [PROPOSED] Contract flow-down language for the liability chain.
