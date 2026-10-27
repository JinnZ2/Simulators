# CC-3b — primary-source rerun of the eight CC-3 rows

Run 2026-10-04 by Claude Code. This file is the appended CC-3b column. It edits
no prior table:

    prior_A   pass 1, law-as-unvalidated-measurement/ section H.2,
              commit 60152f7 (branch claude/law-measurement-correction)
    prior_B   pass 2, VERIFICATION_2026-10-04.md in this folder

Both prior columns are copied here as each pass wrote them. Neither source file
was changed.

Status vocabulary: VERIFIED | CONTRADICTED | NOT_IN_PRIMARY | PRIMARY_UNREACHABLE.
A search result can locate a page. Only an opened primary page sets a status.

## Precondition: host check

One fetch per host, two instruments each: curl through the agent proxy and
WebFetch. Run 2026-10-04T13:11:30Z.

    host                 curl                                    WebFetch          result
    www.ecfr.gov         CONNECT tunnel failed, response 403     EGRESS_BLOCKED    REFUSED
    eur-lex.europa.eu    CONNECT tunnel failed, response 403     EGRESS_BLOCKED    REFUSED
    arxiv.org            CONNECT tunnel failed, response 403     EGRESS_BLOCKED    REFUSED
    www.oecd.org         CONNECT tunnel failed, response 403     EGRESS_BLOCKED    REFUSED
    www.gpo.gov          CONNECT tunnel failed, response 403     EGRESS_BLOCKED    REFUSED
    www.irs.gov          CONNECT tunnel failed, response 403     EGRESS_BLOCKED    REFUSED

    OPEN 0   REFUSED 6

The primary hosts behind the other rows were also tried, at 13:11:49Z: the
proxy's recentRelayFailures log reads connect_rejected for
www.finance.senate.gov, aclanthology.org, curia.europa.eu, www.dea.gov,
www.regdata.org, www.quantgov.org, huggingface.co, www.law.cornell.edu,
www.govinfo.gov, www.federalregister.gov, oecd.org, read.oecd-ilibrary.org and
www.oecd-ilibrary.org. Only github.com and api.github.com answered.

Under the dispatch rule, every row below is PRIMARY_UNREACHABLE. That status is
not NOT_FOUND and not NOT_IN_PRIMARY: no primary page was opened, so nothing was
looked for in one.

## Table

| # | claim | primary_url | quoted_locator | status | prior_A | prior_B | note |
|---|---|---|---|---|---|---|---|
| 1 | CJEU Alsen C-137/23 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A62023CJ0137 | — | PRIMARY_UNREACHABLE | VERIFIED | VERIFIED | eur-lex refused; curia.europa.eu refused |
| 2a | OR-Bench Hard-1K 39.8% illegal | https://arxiv.org/abs/2405.20947 | — | PRIMARY_UNREACHABLE | VERIFIED | NOT_FOUND | arxiv refused. prior_A's locator for this row ("the category breakdown shows illegal at 39.8%") reads like a search-tool summary and does not look like paper text. The authors' repo justincui03/or-bench @4fad1f9 is open but carries no category shares; the dataset is on huggingface, which was refused |
| 2b | OR-Bench Claude-2.1 73.7% | https://arxiv.org/abs/2405.20947 | — | PRIMARY_UNREACHABLE | CONTRADICTED | NOT_FOUND | R2's second read could not be performed (see below). The authors' repo plot.py @4fad1f9 hardcodes Claude-2.1 at x=99.80 (Hard-1K rejection) and y=0.0, plotted as 100-y=100 (Toxic). It carries no 80K figure and no per-category figure, so it does not decide this row |
| 3 | XSTest model size (report: Llama-2-7B) | https://aclanthology.org/2024.naacl-long.301/ | — | PRIMARY_UNREACHABLE | CONTRADICTED | CONTRADICTED | aclanthology and arxiv refused. The authors' repo paul-rottger/exaggerated-safety @d7bb5bd names its completion files llama2orig / llama2new and states no parameter count, so it does not decide the size |
| 4 | RegData 1,126,959 / +175.2% | https://www.regdata.org/ | — | PRIMARY_UNREACHABLE | NOT_FOUND (2025 total); VERIFIED (1970 base 409,520) | NOT_FOUND | regdata.org and quantgov.org refused. Arithmetic needs no host: 1,126,959 / 409,520 = 2.752 |
| 5 | OECD "9 of 38" reach 2/4 | https://www.oecd.org/en/publications/2025/06/government-at-a-glance-2025_70e14c6c/full-report/ex-post-evaluation_5fd27bda.html | — | PRIMARY_UNREACHABLE | VERIFIED | NOT_FOUND | oecd.org refused |
| 6 | IRS publishes no aggregate dye-enforcement stats | https://www.finance.senate.gov/imo/media/doc/kbtest041405.pdf ; https://www.irs.gov/ | — | PRIMARY_UNREACHABLE | NOT_FOUND | CONTRADICTED | finance.senate.gov and irs.gov refused. The FY2004 inspection and penalty figures in prior_B rest on the search index only |
| 7 | DEA "no longer fits Schedule I" | https://www.dea.gov/ (post-hearing brief, Aug 2026) | — | PRIMARY_UNREACHABLE | VERIFIED | VERIFIED | dea.gov refused; both prior passes rest on secondary sources |

    CC-3b   VERIFIED 0   CONTRADICTED 0   NOT_IN_PRIMARY 0   PRIMARY_UNREACHABLE 8

The two author repositories were cloned from github.com (open) into scratch
space and were not committed. Each was named in its row only as an artifact
that was opened and did not decide the row. Neither is the primary page the
dispatch names.

## Priority rows

    R1  26 CFR 48.4082-1, paragraph letter
        PRIMARY_UNREACHABLE. ecfr.gov, gpo.gov, govinfo.gov and
        law.cornell.edu were all refused.
        The letter stays UNCONFIRMED. It is neither confirmed nor corrected.
        Locator only: the search index attributes "(b)" to the ASTM D6258
        scope ("developed to provide for the enforcement of 26 CFR
        48.4082-1(b)"; store.astm.org/d6258-17.html). That is a secondary
        source and was not opened.
        prior_A wrote "26 CFR 48.4082-1(b)" by the same search route.
        prior_B left (b) unconfirmed.
        CC-4 column A: no change to the unit note (see CC4_MERGED.md).

    R2  Claude-2.1 73.7%, second read of the arXiv source
        NOT PERFORMED. arxiv.org and export.arxiv.org were refused.
        None of CONFIRMED_CONTRADICTED / REVERSED / AMBIGUOUS_IN_SOURCE is
        returned, because each of the three presumes the source was read.
        The row keeps prior_A CONTRADICTED and prior_B NOT_FOUND side by side.

    R3  "the one disagreement row NOT re-run last time"
        Per RECONCILIATION.md that row is Claude-2.1 (2b), the same row as R2.
        R3 therefore has no separate row and no separate result.

    R4  OR-Bench 39.8% (2a), OECD "9 of 38" (5), IRS figures (6):
        all PRIMARY_UNREACHABLE.

## EU 2022/197 review triggers (correction notice, C)

    PRIMARY_UNREACHABLE. eur-lex.europa.eu was refused.
    The re-confirmation that the ACCUTRACE PLUS review triggers are
    tax / health / environment only, with no equipment-compatibility axis, was
    not performed.
    Locator only: the search index places the decision at
    https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022D0197
    (Commission Implementing Decision (EU) 2022/197 of 17 January 2022), with
    the selection assessed by JRC and SCHEER. That locates the page and settles
    nothing about its trigger list.

## What would change every row

An environment whose network allowlist includes the six hosts above, plus
www.finance.senate.gov, aclanthology.org, www.regdata.org and www.dea.gov.
The setting is the cloud environment's Network access policy:
https://code.claude.com/docs/en/cloud-environments#network-access
