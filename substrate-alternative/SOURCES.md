# SOURCES

Every structural element in `pilot_loop.py` carries a provenance state and, where
that state is `CITED`, a source id from this file.

## Provenance states

```
CITED          taken from a source below
ASSUMED        doctrine silent on something the model needs; the model supplies it
CARRIED        from memory; no citation confirmed. Not a citation.
NOT_ACTIVATED  doctrine present, and doctrine itself provides for non-activation
EXCLUDED       doctrine present, and a spec requirement excludes it
```

`EXCLUDED` must name the requirement that excluded it and what was omitted, and a
run that uses it reports that at the top of its output rather than in a footnote.

## Citation depth

Every source below is **VERIFIED LOCATOR / UNVERIFIED SECTION**.

The URLs are real and resolve. Page and section numbers were **not read from the
PDFs**. They were retrieved externally and relayed to a session whose network
cannot reach the host, so nothing here has been opened by the party that wrote
the model. Depth is unconfirmed and is marked per row.

```
S-NIMS3     NIMS Third Edition, October 2017
            https://www.fema.gov/sites/default/files/2020-07/fema_nims_doctrine-2017.pdf
            locator VERIFIED   section UNVERIFIED

S-ICS-ORG   ICS Organizational Structure and Elements
            https://training.fema.gov/emiweb/is/icsresource/assets/ics organizational structure and elements.pdf
            locator VERIFIED   section UNVERIFIED

S-ICS-REV   ICS Review Document
            https://training.fema.gov/emiweb/is/icsresource/assets/ics review document.pdf
            locator VERIFIED   section UNVERIFIED

S-ICS-FORMS ICS Forms Descriptions
            https://training.fema.gov/emiweb/is/icsresource/assets/ics forms descriptions.pdf
            locator VERIFIED   section UNVERIFIED
```

## OPEN VERIFICATION ITEMS

These are not resolved. Each names what would settle it.

```
V-1  Is there a NIMS edition later than the Third (October 2017)?
     If yes, that edition governs and every citation here is superseded.
     STATUS: NOT ANSWERABLE FROM THE BUILDING SESSION. All three FEMA hosts
     return no response (measured: 000, against a reachable control). The
     building session's own training data is not a source and is not offered
     as one.
     SETTLES IT: open the NIMS landing page from a host that can reach it.

V-2  Section and page numbers for every CITED element in pilot_loop.py.
     STATUS: UNVERIFIED for all of them, by the citation-depth rule above.
     SETTLES IT: open each PDF and record section numbers against the
     element ids printed by `python3 pilot_loop.py --provenance`.

V-3  The span-of-control range and optimum.
     The model takes span limits from params and does not hardcode a
     doctrinal figure. A commonly stated range is recorded in pilot_loop.py
     as CARRIED, not CITED, and nothing in the model reads it.
     SETTLES IT: locate the range in S-ICS-ORG or S-ICS-REV and move the
     element from CARRIED to CITED with its section.

V-4  The NIMS Resource Typing Library is not held here. Resource kinds and
     types are supplied per scenario in params/. A kind absent from the
     supplied catalog returns UNTYPED rather than being typed by guesswork.
     SETTLES IT: obtain the published typing definitions for any kind the
     pilot needs to type.
```

## CONDITIONAL ACTIVATION, the resolving line

`Finance/Administration` is represented in the structure with activation state
`NOT_ACTIVATED`. It is not deleted and it is not `EXCLUDED`, because doctrine
itself provides for its non-activation:

> not all incidents require a Finance/Administration Section; it is activated
> only when involved agencies have a specific need for finance services

Relayed from S-ICS-ORG. Locator verified, section unverified.

`Intelligence/Investigations` is represented the same way: a sixth function used
only when the incident requires it. Same source, same depth.

Modelling a documented non-activation state is neither inventing structure nor
excluding documented structure.
