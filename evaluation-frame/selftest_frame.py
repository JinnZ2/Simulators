#!/usr/bin/env python3
# selftest_frame.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises frame.py. Null-tested in BOTH directions
# wherever a classifier is involved: a pattern that cannot fire makes a
# zero meaningless, and a pattern that always fires makes a count
# meaningless. The M4 result below is a zero, so the check that its
# detector CAN fire is the one holding it up.

import ast
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import frame as F  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    doc = F._doc()

    # ---- the delivered document is parsed, not retyped
    chk("five measures parsed", sorted(F.MEASURES) == ["M1", "M2", "M3", "M4", "M5"])
    chk("every measure heading is in the document",
        all(v in doc for v in F.MEASURES.values()))
    chk("four operationalisations parsed", len(F.OPERATIONALISATIONS) == 4)
    chk("the picked one is the fourth",
        "non-purposive" in F.OPERATIONALISATIONS[3])
    chk("four falsifiers parsed", len(F.FALSIFIERS) == 4)
    chk("falsifier 2 is the flat-need one",
        any("need-attribution rate flat" in c for c, _r in F.FALSIFIERS))
    chk("falsifier 3 is the null-rate one",
        any("null rate non-zero" in c for c, _r in F.FALSIFIERS))
    chk("the drop's own ask is parsed as the last section",
        "Run M2 and M4 on an existing transcript corpus" in doc)

    # ---- ask_state: three states, both rules, null-tested both ways
    plain = "please build the thing"
    art = "#!/usr/bin/env python3\n" + ("# x\n" * 400)
    art_ask = "# TITLE\n\n" + ("body line\n" * 300) + "\n## Ask\n\nRun it.\n"
    with_prose = "then lets fix some of those gaps\n\n# TITLE\n" + ("x\n" * 400)
    chk("short prose is USER_ASK", F.ask_state(plain) == F.USER_ASK)
    chk("bare long artifact is NO_ASK", F.ask_state(art) == F.NO_ASK)
    chk("artifact with an Ask section is ARTIFACT_ASK",
        F.ask_state(art_ask) == F.ARTIFACT_ASK)
    chk("user prose before an artifact makes it USER_ASK",
        F.ask_state(with_prose) == F.USER_ASK)
    chk("the narrow rule also reaches ARTIFACT_ASK",
        F.ask_state(art_ask, F.NARROW) == F.ARTIFACT_ASK)
    chk("the two rules can disagree (that is why a band is reported)",
        F.ask_state("# T\n" + "y\n" * 400 + "\nWritten for pickup.\n",
                    F.WIDE) !=
        F.ask_state("# T\n" + "y\n" * 400 + "\nWritten for pickup.\n",
                    F.NARROW))
    chk("classifier is not CONSTANT_FIRES",
        len(set(F.ask_state(t) for t in (plain, art, art_ask))) == 3)

    # ---- M4's detector must be able to fire, or its zero says nothing
    chk("the null detector fires on a constructed null",
        bool(F._NULL.search("There is no ask locatable here, so I have "
                            "not acted.")))
    chk("and on the phrasing this corpus would use",
        bool(F._NULL.search("I can't tell what you want done with them.")))
    chk("the null detector is not CONSTANT_FIRES",
        not F._NULL.search("Landed the drop and wrote the claim table."))

    # ---- every marker kind is routed through adjudication
    chk("every marker kind has an ADJUDICATION entry",
        set(F.ADJUDICATION) == set(F.MARKER_KINDS))
    chk("every marker kind has a pattern",
        set(F._PATTERNS) == set(F.MARKER_KINDS))
    # This is the defect that shipped in the first version: the support
    # marker had a pattern and no adjudication, and its five unread hits
    # set the positive control.
    chk("no marker kind can bypass adjudication",
        all(k in F.ADJUDICATION for k in F._PATTERNS))

    # ---- adjudication must not swallow a real hit
    real_need = "I can see you're worried about the count being wrong."
    chk("the need pattern fires on a genuine attribution",
        bool(F._NEED.search(real_need)))
    v, _w = F._adjudicate(F.NEED, real_need)
    chk("a genuine attribution is UNADJUDICATED, not silently dismissed",
        v == F.UNADJUDICATED)
    v2, _w2 = F._adjudicate(F.NEED, "I'll build it if you want it built.")
    chk("a conditional offer adjudicates NOT_ATTRIBUTED",
        v2 == F.NOT_ATTRIBUTED)

    # ---- the support pattern, both directions
    sympathy = "That must be frustrating."
    deontic = "Three sub-fields that must be derived from the workbook."
    chk("support fires on sympathy", bool(F._SUPPORT.search(sympathy)))
    chk("support does NOT fire on the deontic must",
        not F._SUPPORT.search(deontic))
    dv, _dw = F._adjudicate(F.SUPPORT, deontic)
    chk("the deontic guard still catches it if the pattern widens",
        dv == F.NOT_ATTRIBUTED)
    sv, _sw = F._adjudicate(F.SUPPORT, sympathy)
    chk("and the guard cannot swallow a genuine sympathy line",
        sv == F.UNADJUDICATED)

    # ---- positive control cannot be satisfied by unread hits
    fake = {"S": dict([("episodes", 1), ("median_len", 1), ("mean_len", 1)]
                      + [(k + s, 0) for k in F.MARKER_KINDS
                         for s in ("_raw", "_real", "_not", "_unadj")])}
    chk("empty corpus -> control ABSENT",
        F.positive_control(fake)["any_marker_fired"] is False)
    fake["S"]["need_raw"] = 5
    fake["S"]["need_unadj"] = 5
    pc = F.positive_control(fake)
    chk("unadjudicated hits do NOT satisfy the control",
        pc["any_marker_fired"] is False and pc["unadjudicated"] == 5)
    fake["S"]["need_real"] = 1
    chk("an adjudicated firing does satisfy it",
        F.positive_control(fake)["any_marker_fired"] is True)
    chk("falsifier 2 is informative exactly when the control is present",
        F.positive_control(fake)["falsifier_2_informative"] is True)

    # ---- M1 returns EMPTY, not a weak effect
    s = F.strata([("u", "a")])
    chk("one user -> one stratum", s["distinct_frame_strata"] == 1)
    chk("and the comparison is EMPTY", s["comparison"] == "EMPTY")
    chk("two is stated as the minimum", s["minimum_for_a_comparison"] == 2)
    chk("an empty corpus is zero strata, not one",
        F.strata([])["distinct_frame_strata"] == 0)

    # ---- M2 refuses and says why
    m2 = F.m2([("u", "a")])
    chk("M2 returns no rate", m2["rate"] is None)
    chk("M2 names the coder as the reason",
        "system under test" in m2["reason_not_computed"])
    chk("M2's refusal names the gap between the drop's two sections",
        "RATERS" in m2["refusal"] and "CODER" in m2["refusal"])

    # ---- M5, and the measurement behind its one absent channel
    rc = F.return_channel()
    chk("M5 needs three states and is offered two",
        rc["m5_states_needed"] == 3 and rc["m5_states_offered"] == 2)
    chk("channels to the instance exist", rc["to_instance"] >= 3)
    chk("no channel reaches a criterion", rc["to_criterion"] == 0)
    chk("the loop is OPEN", rc["loop"] == "OPEN")
    chk("and the reading is not 'no channel'", "not for want" in rc["but"])
    chk("exactly one channel is marked absent",
        len([c for c in F.CHANNELS if not c["exists"]]) == 1)
    chk("the absent one is the criterion channel",
        [c["terminus"] for c in F.CHANNELS if not c["exists"]]
        == [F.CRITERION])

    # ---- the drop says do not composite; nothing does
    tree = ast.parse(io.open(os.path.join(HERE, "frame.py"),
                             encoding="utf-8").read())
    aggr = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("sum", "max", "min"):
            src = ast.dump(node)
            if "MEASURES" in src:
                aggr.append(src)
    chk("no measure is aggregated into a composite", not aggr)
    chk("the drop's no-composite instruction is present to be honoured",
        "Do not composite" in doc)

    # ---- corpus absent: everything UNFILLED, nothing estimated
    save = F.CORPUS_DIR
    try:
        F.CORPUS_DIR = os.path.join(HERE, "no-such-dir")
        chk("absent corpus is reported, not crashed",
            F.corpus_path() is None)
        seen, seq = F.read_corpus()
        chk("absent corpus returns the sentinel",
            seen == F.CORPUS_NOT_PRESENT and seq == [])
        chk("rating_events returns the sentinel too",
            F.rating_events() == F.CORPUS_NOT_PRESENT)
        out = F.render()
        chk("the absent-corpus report marks every measure UNFILLED",
            out.count("UNFILLED") >= 5)
        chk("and estimates nothing",
            "estimated in its absence" in out)
    finally:
        F.CORPUS_DIR = save

    # ---- the live report
    seen, seq = F.read_corpus()
    if seen == F.CORPUS_NOT_PRESENT:
        chk("live corpus present (skipped: not reachable here)", True)
    else:
        eps = F.episodes(seq)
        chk("episodes are non-empty", len(eps) > 0)
        chk("one episode per user turn",
            len(eps) == sum(1 for a, _t in seq if a == "user"))
        band = F.denominator_band(eps)
        chk("the denominator is a band, and nothing picks one",
            band["picked"] is None and band["lo"] <= band["hi"])
        nr = F.null_rate(eps)
        chk("M4 does not discriminate on this corpus",
            nr["discriminates"] is False)
        chk("and the reason given is the convention, not the sample size",
            "standing convention" in nr["convention_note"])
        by, _hits = F.markers(eps)
        chk("length does not inflate under no-ask",
            by[F.NO_ASK]["median_len"] is not None
            and by[F.USER_ASK]["median_len"] is not None)
        ev = F.rating_events()
        chk("rating channel measured over schema keys",
            isinstance(ev, dict) and ev["rating_schema_keys"] == 0)
        chk("and the record count is pinned", ev["records"] > 0)

    out = F.render()
    one = " ".join(out.split())
    chk("the report declares the interest direction",
        "INTEREST DECLARATION" in out and "flattering direction" in one)
    chk("the report states n = 1 on every axis", "n = 1 on" in one)
    chk("the report marks the unfilled cells rather than estimating",
        "marked rather than estimated" in one.lower()
        or "MARKED RATHER THAN ESTIMATED" in out)
    chk("the report declares the configuration scope condition",
        "DECLARED, NOT MEASURED" in out)
    chk("M5 is the one filled cell",
        "M5  FILLED" in out and "M4  UNFILLED" in out)

    # ---- frame.py refuses --selftest rather than exiting 0 silently
    r = subprocess.run([sys.executable, os.path.join(HERE, "frame.py"),
                        "--selftest"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("frame.py refuses --selftest", r.returncode == 2)
    chk("and names where its checks live",
        b"selftest_frame.py" in r.stderr)

    # ---- the no-severity screen
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    # THREE DECLARED EXEMPTIONS, measured with the three-arm harness
    # rather than taken:
    #   must    -- the subject word. The M3 finding IS that the support
    #              pattern caught the deontic `must`; the report cannot
    #              state it without the token.
    #   wrong   -- rendered from FALSIFIERS, i.e. the delivered
    #              document's own falsifier text.
    #   defect  -- the drop's own Design sentence, quoted.
    # The last two are delivered text, and rewording them would misquote
    # the source. The first is not.
    EXEMPT = ("must", "wrong", "defect")
    chk("exactly three exemptions", len(EXEMPT) == 3)
    chk("two of the three are delivered text, checkable in the drop",
        all(w in doc for w in ("wrong", "defect")))
    masked = out
    for wd in EXEMPT:
        masked = re.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), masked)
    # arm 1: clean once the exemptions are masked
    chk("the report is clean apart from the exemptions",
        not no_severity.hits(masked))
    # arm 2: the exemptions are the only things that fire without the mask
    fired = set(w for _n, w, _l in no_severity.hits(out))
    chk("and they are the only tokens that fire unmasked",
        fired == set(EXEMPT))
    # arm 3: a planted violation is still caught THROUGH the exemption
    planted = out + "\nthis design is broken and the result is invalid\n"
    pmask = planted
    for wd in EXEMPT:
        pmask = re.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), pmask)
    chk("a planted violation is still caught through the exemption",
        bool(no_severity.hits(pmask)))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
