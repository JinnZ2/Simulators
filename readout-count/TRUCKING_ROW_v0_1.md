# readout_count — v0.1, trucking row

License: CC0. Data as of 2026-09-02. Companion to WORK_ORDER_readout_count.md.
Every claim below carries a source URL. Corrections welcome; open an issue.

## CORRECTION TO v0 DRAFT

    v0 draft said: trucking has NO driver channel at any layer, count 0.
    That was wrong. A federal driver channel exists and is codified.

    What exists:
      49 CFR 390.6      coercion rule — prohibits pressuring a driver to violate
                        the FMCSRs; covers carriers, shippers, receivers, brokers
      49 CFR 386.12(c)  driver files written complaint to NCCDB or the State
                        Division Administrator, within 90 days of the event
      49 CFR 386.12(b)  same route for harassment (390.36(b)(1))
      49 U.S.C. 31105   STAA whistleblower anti-retaliation; remedy is through
                        OSHA, not FMCSA; 180-day filing window
      OSHA–FMCSA MOU    each refers complainants to the other

    So the corrected finding is not absence. It is CHANNEL TYPE.

## THE DISTINCTION THE ROW ACTUALLY MEASURES

    complaint channel                     readout channel (ASRS / C3RS class)
    ------------------------------------  ------------------------------------
    alleges a VIOLATION by a named party  reports a CONDITION, no allegation
    identity disclosure required for      anonymous or de-identified by a
      prosecution (386.12(c)(3) says so)    third-party holder
    adversarial: a respondent is served   non-adversarial: no respondent
    filing deadline 90 days               no deadline; report while fresh
    protection is post-hoc retaliation    protection is pre-hoc: the report
      remedy via a separate agency          never carries the reporter's name
    output: enforcement action or none    output: de-identified trend data
                                            published back to the operators
    peer review: none                     peer review: labor + management +
                                            regulator on the same team

    → 390.6 is a real and useful channel. It is not a readout channel.
    → It fires only when a rule was broken and a party can be named.
    → The six things a driver knows (below) break no rule and name no party,
      so they are unfilable in this instrument.

## WHAT THE DRIVER READOUT CONTAINS  (stated by an operator, 2026-09-01)

    1  labor, movement, kinetic and mental load the job actually requires
    2  compensations needed to operate the specific machine as assigned
    3  maintenance beyond the mechanics' protocol that the company, machine,
       road, and weather dictate for that machine to run safely
    4  social requirements of the assigned route
    5  road requirements under variable conditions and how that truck behaves
    6  traffic / pedestrian / tourist patterns across those variations

    Each is person-plus-machine-plus-route bound. None is a rule violation.
    None has a field in ELD, CSA, DataQs, the roadside inspection record,
    or NCCDB. This is the quantity the row measures as uncarried.

## SIBLING CHANNELS UNDER THE SAME DEPARTMENT

    ASRS  (aviation)   FAA AC 00-46; immunity via 14 CFR 91.25; NASA-held
                       since 1976; non-adversarial; de-identified
    C3RS  (rail)       not a CFR part. Per-carrier IMOU: FRA + carrier + labor
                       organization. NASA holds reports; BTS confidentiality
                       under 49 U.S.C. 111; waivers from 49 CFR 240 certification
                       provisions to make immunity real. Peer review teams of
                       labor, management, FRA. Demonstration status since ~2007;
                       all Class I freight agreed 2023; carrier-by-carrier pilots
                       still being signed through 2024. Explicitly NOT a
                       whistleblower program.
    trucking           no analogue. No IMOU, no third-party holder, no peer
                       review team, no de-identified return to operators.

    → the trucking gap is an unsigned MOU, not an unwritten regulation
    → the missing party is a driver organization with standing to sign
      (most drivers non-union; OOIDA is owner-operator only and functions as
      a referral service, not a report holder)

## OTHER LAYERS, CODED

    layer            channel                 type        returns to operator?
    carrier HR       per-company, varies     complaint   advertised at hiring;
                                                         on use, routed to HR
                                                         and re-typed as driver
                                                         complaint (operator report,
                                                         2026-09-01)
    weigh station    unit inspection         inspection  no field for driver read
    officer          citation / none         enforcement no
    NHTSA VOQ /      equipment defect        readout     yes, partial — trend
      SaferTruck                             (equipment) analysis by make/model/
                                                         year, Privacy Act
                                                         protected; carries no
                                                         route, dispatch, load,
                                                         weather, or
                                                         person-plus-machine terms
    FMCSA NCCDB      coercion / harassment   complaint   enforcement only
    OSHA STAA        retaliation             remedy      individual remedy only

## COUNT, WITH THE CODING RULE STATED

    readout_count counts positions with a NON-ADVERSARIAL, HELD, RETURNING
    channel for condition reports.

    air        4-5
    rail       3-4  (per carrier; partial coverage)
    trucking   0.5  (NHTSA VOQ, equipment only, no immunity, no reply commitment)
    complaint_count for trucking is >= 3 and is a different quantity.

    → v0's error was folding two channel types into one count.
      Same defect this project is built to measure. Logged, not hidden.

## OPEN INSTANCE  (n=1, operator-reported, 2026-08-25 to 2026-09-01)

    A driver sent her carrier a written proposal for a technical submission path:
    a named receiver and a commitment to reply. Trigger: a stability system
    engaging on a downgrade, twice in one month, one unit.
    Channels tried: email (sent), the number provided in response (called),
    driver services (voicemail).
    Returns at day 7: 0 of 3.
    Estimated implementation cost, by the driver: ~5 minutes to designate a
    person, set up an address, and reply.

    This is one row. It is not evidence of an industry rate.
    The survey that would make it one is in the parent work order (N4):
    per-carrier reply rate to driver technical submissions, sampled from driver
    boards where the poster identity filter is self-enforcing.

## SOURCES

    49 CFR 386.12    https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-386/subpart-B/section-386.12
    FMCSA coercion FAQ  https://www.fmcsa.dot.gov/regulations/faqs-prohibited-coercion-cmv-drivers
    Coercion final rule 80 FR 78381  https://www.federalregister.gov/documents/2015/11/30/2015-30237/prohibiting-coercion-of-commercial-motor-vehicle-drivers
    NCCDB FAQs       https://www.fmcsa.dot.gov/consumer-protection/national-consumer-complaint-database-faqs
    NCCDB Privacy Act statement  https://nccdb.fmcsa.dot.gov/PrivacyAct.aspx
    NHTSA VOQ / SaferTruck — cite the current NHTSA complaint page before use
    ASRS, C3RS — cite FAA AC 00-46, 14 CFR 91.25, 49 U.S.C. 111, 49 CFR 240
      before use; C3RS IMOU text to be located

## STILL NEEDED FOR THIS ROW

    - fatal-crash rate series with a stable exposure denominator (per VMT),
      FMCSA/FARS, 1990–present, one source, one definition
    - NCCDB coercion complaint counts and disposition counts by year
      (filed vs investigated vs enforced) — tests return rate on the
      complaint channel directly
    - the C3RS IMOU template, to name exactly which parties must sign
    - whether any single carrier has ever run an internal non-adversarial
      readout channel with a published reply rate

## CHANGELOG

    v0    2026-09-01  draft, unsourced, claimed count 0
    v0.1  2026-09-02  sourced; count corrected to 0.5; complaint vs readout
                      channel distinction added as the actual measured quantity
