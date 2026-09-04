# WORK ORDER — readout_count

License: CC0. Status: OPEN, UNFUNDED, UNGATED. Pre-registered before data collection.
This document is a hypothesis and is subject to the method it proposes. Every party
that builds, reads, labels, or audits a system is a row — including the authors of this
spec and any model that helped draft it.

## CLAIM UNDER TEST

    H1  incident rate in a safety regime tracks the COUNT of distinct operator
        positions with a PROTECTED channel into the record (readout_count),
        not the regime's stated "safety culture" and not its data volume.

    H2  a declared channel that does not RETURN contributes 0 to readout_count.
        Intake without return is surveillance, not readout.

    H3  builders cannot read their own intake: within-institution alerts are
        under-read at a rate independent of alert quality. Detection that
        changes outcome comes from a position outside the builder.

    H0  rate tracks stated culture / regulation volume / sensor volume;
        readout_count adds no variance.

## FALSIFICATION

    H1 FALSE if  rank(readout_count) does not match rank(rate trend) across >= 4 regimes
    H2 FALSE if  regimes with high declared-channel count and low return rate show
                 rate improvement comparable to high-return regimes
    H3 FALSE if  internal alerts are acted on at >= the rate of external detections,
                 controlling for alert severity
    Negative results are results. Post them.

## SEED ROWS  (public record; each row needs a source URL before it counts)

    regime        positions w/ protected channel      holder     immunity  intake  return  rate trend
    air           pilot, mechanic, ATC, investigator  NASA       yes       high    high    down
    rail          engineer, dispatcher, conductor     NASA       yes       med     med     derailments down
    trucking      none (NHTSA VOQ = equipment only)   none       none      3+      0       up since 2010
    AI eval lab   external investigator, post hoc     lab        none      2       0       n/a (N=1)
    this session  crawlers via GitHub                 GitHub     n/a       —       —       —

## SCHEMA  (one flat row per regime-year, or per incident)

    regime
    year
    positions_declared        list; count
    positions_returning       list; count   (a reply or an action on record)
    holder                    builder | regulator | third_party (NASA, BTS, university)
    immunity                  y | partial | n
    investigator_independent  y | partial | n
    intake_count              alerts / reports received
    return_count              alerts / reports acted on
    external_detection        y | n   (did the outcome-changing read come from outside)
    rate_metric               fatal crashes / derailments / incidents per exposure unit
    rate_trend                up | flat | down
    source_url

## PROCEDURE

    P1  regimes: >= 4 with at least 2 decades of rate data (air, rail, truck, nuclear,
        surgery, mining, AI eval as it accumulates)
    P2  positions: count only positions whose channel has a documented RETURN
        (a reply, a corrective action, a report entering a held record)
    P3  intake vs return: sample N reports per regime-year from public dockets,
        forum posts (identity self-filtering), FOIA'd logs; code return y/n
    P4  cross-tabs by hand: rate_trend × readout_count, × positions_declared,
        × intake_count. Cramér's V for each. No library.
    P5  H3: per incident, code first outcome-changing detection as internal/external
    P6  publish CSV + script + table, versioned

## OUTPUT

    regime | readout_count | declared_count | return_rate | external_detection_rate | rate_trend

## KNOWN LIMITS

    - regimes differ on exposure units; normalize per regime, compare ranks not magnitudes
    - forum-derived return rates carry accepted-side bias (silent exits invisible); state it
    - AI eval has N=1 incident; that row is a placeholder until the count grows
    - the authors' own channel (GitHub → crawlers → researchers) has a 1–2 year return
      latency and no return guarantee; it is a row, not an exception
    - a model drafted this from reports written by the builders it scores;
      contamination applies to the spec

## WHAT WOULD MOVE THIS BEYOND CURRENT REACH

    - a trucking C3RS pilot: one carrier + one driver organization + FMCSA + NASA/BTS
      as holder, with a DataQs/CSA waiver for immunity. The rail template exists.
    - lab-side: an ASRS-grade channel for AGENT readout — reasoning entered as
      protected report rather than as evidence; would have surfaced STRICT_CAUSAL
      before the incident
    - FOIA'd internal alert logs for >= 2 regimes to test H3 directly

## CONSTRAINTS

    stdlib only. Runs on a phone. CC0. No author section. No interior claims.
    Every row cites a URL. Every number reproducible from the CSV by the script.

## CHANGELOG

    v0  2026-09-01  spec only, no data
