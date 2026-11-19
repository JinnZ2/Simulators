# Excerpt of P2/numcheck/check.py, original line numbers kept (lines 1-53, 110-119, 188-240, 296-305, 415-440, 443-557 of 592). Lines not shown are omitted, not empty.

    1| """check -- data points and intersections. Co-authored.
    2| 
    3| Units first: every formula goes through branch 1 (unitaudit). Unless that
    4| verdict is PASS, the numeric check is VOID with branch 1's reason.
    5| 
    6| A data point: "lhs = rhs", a value per symbol (a number, or an interval
    7| [lo, hi]; with its unit and its own status tag) and a tolerance t >= 0.
    8| With D an enclosure of lhs - rhs:
    9|   HOLDS      D lies inside [-t, t]
   10|   FAILS      D lies wholly outside [-t, t]
   11|   UNDECIDED  D straddles the edge at the last tier
   12|   VOID       units not PASS, a missing or unreadable value, no value on
   13|              these inputs (division by an interval containing 0, ...),
   14|              unsupported syntax, internal error
   15| The verdict comes from the interval tier: Fraction intervals, with sqrt exp
   16| ln sin cos as outward enclosures (precision doubling up to max_precision
   17| when one was used). It is the only rigorous tier. float and Decimal run
   18| first as TRIAGE: each gives a predicted_verdict or says "too close to
   19| call". Every HOLDS / FAILS is confirmed at the interval tier, and the record
   20| sets predicted beside confirmed; a mismatch is listed on the record and
   21| counted in the report. The margin rule behind a prediction is a heuristic
   22| with no bound over a long chain of steps, so a prediction is never the
   23| verdict, unless the check asks for fast (entry "fast": true, or --fast):
   24| then confirmation is skipped, the prediction is the verdict, and the record
   25| carries rigorous: false.
   26| 
   27| A straddle on interval inputs is bisected (the inputs are split, widest
   28| first, to the depth limit) and every piece is read:
   29|   every piece HOLDS                          -> HOLDS
   30|   pieces that HOLD and pieces that FAIL      -> MIXED: both kinds are listed
   31|   pieces that FAIL, none that hold           -> FAILS, located
   32|   otherwise                                  -> UNDECIDED
   33| An UNDECIDED at tolerance 0 with no piece against it, whose two sides agree
   34| at every sampled exact point, is put on the record as an identity candidate
   35| ("proposal"). If lhs - rhs is a polynomial in the interval inputs and is 0
   36| on a full grid of (degree + 1) exact points per variable, that is a proof:
   37| the proposal's status is DERIVED and it carries the proof. Otherwise it
   38| stays PROPOSED, with the reason. The check's own verdict is not changed.
   39| 
   40| An intersection: two formulas and a region (a box: an interval per region
   41| variable). On a subbox, both formulas HOLD (enclosure inside tolerance:
   42| true at every point of the subbox), or one FAILS (enclosure outside: false
   43| at every point of it), or the subbox is bisected along its widest side, to
   44| a depth limit.
   45|   BOTH_HOLD   every subbox reached: both hold
   46|   MIXED       subboxes where both hold, and subboxes where one fails
   47|               everywhere (both kinds listed)
   48|   ONE_FAILS   subboxes where one formula fails everywhere (located), and
   49|               none where both hold
   50|   UNDECIDED   neither, at the depth limit
   51|   VOID        as above; or a subbox with no value at the depth limit and no
   52|               failure found
   53| """
  ...

  110| def _blank(kind, entry, index, input_path):
  111|     get = entry.get if isinstance(entry, dict) else (lambda *_: None)
  112|     return {"kind": kind, "verdict": "VOID", "void_reason": None, "status": None,
  113|             "deciding_tier": None, "precision": None, "rigorous": None, "fast": None,
  114|             "tiers": [], "triage": None, "located": None, "proposal": None,
  115|             "intervals": None, "inputs": None, "units": None,
  116|             "provenance": {"source_path": get("source_path"), "input": input_path,
  117|                            "index": index, "tool": VERSION},
  118|             "slots": slot_record(get("slots")),
  119|             "human_interest": None, "ai_interest": None}
  ...

  188| def _bisect_point(sides, tol, env, prec, depth_limit):
  189|     """A straddle on interval inputs: split the inputs (widest first) and look
  190|     again, on every piece, to the depth limit. Returns (verdict or None, detail).
  191|       every piece HOLDS                               -> HOLDS
  192|       pieces that HOLD and pieces that FAIL           -> MIXED (both kinds listed)
  193|       pieces that FAIL, none that hold                -> FAILS, located
  194|       otherwise (pieces straddle at the depth limit)  -> None (UNDECIDED)
  195|     A piece HOLDS / FAILS when the formula does so at every point of it."""
  196|     if depth_limit < 0 or 2 ** depth_limit > MAX_SUBBOXES:
  197|         raise Bad(f"depth must be between 0 and {MAX_SUBBOXES.bit_length() - 1}")
  198|     names = sorted(n for n, v in env.items() if not v.is_point)
  199|     stack = [({n: env[n] for n in names}, 0)]
  200|     counts = {"examined": 0, "hold": 0, "fail": 0, "straddle_at_depth_limit": 0}
  201|     deepest, first_open, holds, fails = 0, None, [], []
  202|     while stack:
  203|         box, depth = stack.pop()
  204|         counts["examined"] += 1
  205|         deepest = max(deepest, depth)
  206|         _, _, d = _difference(sides, dict(env, **box), IntSys(prec))
  207|         v, _ = IntSys(prec).judge(d, tol)
  208|         piece = {"subbox": {n: box[n].as_record() for n in names}, "depth": depth,
  209|                  "difference": d.as_record()}
  210|         if v == "HOLDS":
  211|             counts["hold"] += 1
  212|             if len(holds) < LIST_CAP:
  213|                 holds.append(piece)
  214|         elif v == "FAILS":
  215|             counts["fail"] += 1
  216|             if len(fails) < LIST_CAP:
  217|                 fails.append(piece)
  218|         elif depth >= depth_limit:
  219|             counts["straddle_at_depth_limit"] += 1
  220|             first_open = first_open or piece
  221|         else:
  222|             widest = max(names, key=lambda n: box[n].width)
  223|             a, b = box[widest].split()
  224|             stack.append((dict(box, **{widest: b}), depth + 1))
  225|             stack.append((dict(box, **{widest: a}), depth + 1))
  226|     h, f, o = counts["hold"], counts["fail"], counts["straddle_at_depth_limit"]
  227|     verdict = ("MIXED" if h and f else "FAILS" if f else "HOLDS" if not o else None)
  228|     return verdict, {**counts, "depth_limit": depth_limit, "deepest": deepest,
  229|                      "variables_split": names, "tolerance": str(tol),
  230|                      "list_cap": LIST_CAP,
  231|                      "reading": {"MIXED": "holds on some pieces of the given values and "
  232|                                           "fails on others",
  233|                                  "FAILS": "fails at every point of the located pieces; "
  234|                                           "no piece holds",
  235|                                  "HOLDS": "holds on every piece",
  236|                                  None: "pieces still straddle at the depth limit"}[verdict],
  237|                      "pieces_that_hold": holds, "pieces_that_fail": fails,
  238|                      "pieces_that_hold_listed": len(holds), "pieces_that_fail_listed": len(fails),
  239|                      "located": fails[0] if fails else None,
  240|                      "first_straddling_piece": first_open}
  ...

  296| def _identity_candidate(entry, sides, tol, env, rec, prec, index, input_path):
  297|     """tolerance 0, interval inputs, UNDECIDED, and nothing against it: the two
  298|     sides may be the same function. Sample exact points; if the difference
  299|     is 0 at every one, hand the pair on as a PROPOSED identity. Nothing is
  300|     proved here by sampling. If lhs - rhs is a polynomial in the interval
  301|     inputs, the full-grid check of _polynomial_proof IS a proof: the
  302|     proposal then carries it and its status is DERIVED."""
  303|     b = rec["bisection"]
  304|     if tol != 0 or b is None or b["hold"] or b["fail"]:
  305|         return None
  ...

  415|             rec["bisection"] = None
  416|             if not verdict and not points:
  417|                 verdict, rec["bisection"] = _bisect_point(sides, tol, env, prec,
  418|                                                           int(opt["depth"]))
  419|                 rec["located"] = rec["bisection"]["located"]
  420|                 rec["verdict"] = verdict or "UNDECIDED"
  421|                 rec["proposal"] = _identity_candidate(entry, sides, tol, env, rec, prec,
  422|                                                       index, input_path)
  423|             rec.update(verdict=verdict or "UNDECIDED", deciding_tier="interval",
  424|                        precision="exact" if exact else prec, rigorous=True, status="DERIVED")
  425|         confirmed = rec["verdict"] if rec["rigorous"] else None
  426|         per_tier = [{"tier": t["tier"], "predicted_verdict": t["predicted_verdict"],
  427|                      "confirmed_verdict": confirmed,
  428|                      "match": None if confirmed is None else t["predicted_verdict"] == confirmed}
  429|                     for t in tiers if t.get("predicted_verdict")]
  430|         rec["triage"] = {"predictions": per_tier,
  431|                          "confirmed_verdict": confirmed,
  432|                          "confirmed_at": "interval" if confirmed else None,
  433|                          "mismatches": [x["tier"] for x in per_tier if x["match"] is False],
  434|                          "note": None if confirmed else
  435|                          "fast: the prediction was taken as the verdict, not confirmed"}
  436|     except (Bad, NumVoid) as e:
  437|         rec.update(verdict="VOID", void_reason=str(e), status=None)
  438|     except Exception as e:                       # fail closed
  439|         rec.update(verdict="VOID", void_reason=f"internal: {type(e).__name__}: {e}", status=None)
  440|     return rec
  ...

  443| def check_intersection(entry, index=None, input_path=None):
  444|     rec = _blank("intersection", entry, index, input_path)
  445|     try:
  446|         forms = entry.get("formulas") if isinstance(entry, dict) else None
  447|         if not isinstance(forms, list) or len(forms) != 2:
  448|             raise Bad("an intersection needs exactly two formulas")
  449|         region = entry.get("region")
  450|         if not isinstance(region, dict) or not region:
  451|             raise Bad("an intersection needs a region: {variable: [lo, hi]}")
  452|         values = entry.get("values")
  453|         parsed, rec["units"], rec["formulas"] = [], [], []
  454|         needed = set()
  455|         for i, f in enumerate(forms):
  456|             if not isinstance(f, dict) or not isinstance(f.get("formula"), str):
  457|                 raise Bad(f"formula {i + 1}: no formula string")
  458|             u, reason = _units(f["formula"], values)
  459|             rec["units"].append(u)
  460|             rec["formulas"].append(f["formula"])
  461|             if reason:
  462|                 raise Bad(f"formula {i + 1}: {reason}")
  463|             sides = _parse(f["formula"])
  464|             tol = to_fraction(f.get("tolerance", 0), f"tolerance {i + 1}")
  465|             if tol < 0:
  466|                 raise Bad(f"tolerance {i + 1} is negative")
  467|             parsed.append((sides, tol))
  468|             needed |= _names(sides[0][1]) | _names(sides[1][1])
  469|         for name in region:
  470|             if name not in needed:
  471|                 raise Bad(f"region variable {name!r} is in neither formula")
  472|         env, rec["inputs"] = _inputs(values, needed, region)
  473|         prec = int(entry.get("precision", DEFAULTS["precision"]))
  474|         depth_limit = int(entry.get("depth", DEFAULTS["depth"]))
  475|         if depth_limit < 0 or 2 ** depth_limit > MAX_SUBBOXES:
  476|             raise Bad(f"depth must be between 0 and {MAX_SUBBOXES.bit_length() - 1}")
  477|         names = sorted(region)
  478|         stack = [({n: env[n] for n in names}, 0)]
  479|         counts = {"examined": 0, "both_hold": 0, "undecided_at_depth_limit": 0,
  480|                   "no_value_at_depth_limit": 0}
  481|         first_open, first_void, deepest = None, None, 0
  482|         holds, fails = [], []
  483|         counts["one_fails"] = 0
  484|         while stack:
  485|             box, depth = stack.pop()
  486|             counts["examined"] += 1
  487|             deepest = max(deepest, depth)
  488|             cur = dict(env, **box)
  489|             state, void_reason, diffs = [], None, []
  490|             for sides, tol in parsed:
  491|                 S = IntSys(prec)
  492|                 try:
  493|                     _, _, d = _difference(sides, cur, S)
  494|                     state.append(S.judge(d, tol)[0])
  495|                     diffs.append(d.as_record())
  496|                 except NumVoid as e:
  497|                     state.append("VOID")
  498|                     diffs.append(None)
  499|                     void_reason = str(e)
  500|             sub = {n: box[n].as_record() for n in names}
  501|             if "FAILS" in state:
  502|                 i = state.index("FAILS")
  503|                 counts["one_fails"] += 1
  504|                 if len(fails) < LIST_CAP:
  505|                     fails.append({"subbox": sub, "depth": depth, "formula_number": i + 1,
  506|                                   "formula": rec["formulas"][i], "difference": diffs[i],
  507|                                   "tolerance": str(parsed[i][1]),
  508|                                   "other_formula_on_this_subbox": state[1 - i]})
  509|             elif state == ["HOLDS", "HOLDS"]:
  510|                 counts["both_hold"] += 1
  511|                 if len(holds) < LIST_CAP:
  512|                     holds.append({"subbox": sub, "depth": depth})
  513|             elif depth >= depth_limit:
  514|                 if void_reason:
  515|                     counts["no_value_at_depth_limit"] += 1
  516|                     first_void = first_void or {"subbox": sub, "depth": depth,
  517|                                                 "reason": void_reason}
  518|                 else:
  519|                     counts["undecided_at_depth_limit"] += 1
  520|                     first_open = first_open or {"subbox": sub, "depth": depth,
  521|                                                 "states": state, "differences": diffs}
  522|             else:
  523|                 widest = max(names, key=lambda n: box[n].width)
  524|                 if box[widest].width == 0:
  525|                     counts["undecided_at_depth_limit"] += 1
  526|                     first_open = first_open or {"subbox": sub, "depth": depth, "states": state,
  527|                                                 "differences": diffs}
  528|                     continue
  529|                 a, b = box[widest].split()
  530|                 stack.append((dict(box, **{widest: b}), depth + 1))
  531|                 stack.append((dict(box, **{widest: a}), depth + 1))
  532|         located = fails[0] if fails else None
  533|         rec["subboxes"] = {**counts, "depth_limit": depth_limit, "deepest": deepest,
  534|                            "list_cap": LIST_CAP}
  535|         rec["located"] = located
  536|         rec["subboxes_where_both_hold"] = holds
  537|         rec["subboxes_where_one_fails"] = fails
  538|         rec["first_undecided_subbox"] = first_open
  539|         rec["first_subbox_with_no_value"] = first_void
  540|         rec.update(deciding_tier="interval", precision=prec, rigorous=True)
  541|         if located and counts["both_hold"]:
  542|             rec.update(verdict="MIXED", status="DERIVED")
  543|         elif located:
  544|             rec.update(verdict="ONE_FAILS", status="DERIVED")
  545|         elif counts["no_value_at_depth_limit"]:
  546|             rec.update(verdict="VOID", status=None,
  547|                        void_reason="no value on a subbox at the depth limit: "
  548|                                    + first_void["reason"])
  549|         elif counts["undecided_at_depth_limit"]:
  550|             rec.update(verdict="UNDECIDED", status="DERIVED")
  551|         else:
  552|             rec.update(verdict="BOTH_HOLD", status="DERIVED")
  553|     except (Bad, NumVoid) as e:
  554|         rec.update(verdict="VOID", void_reason=str(e), status=None)
  555|     except Exception as e:                       # fail closed
  556|         rec.update(verdict="VOID", void_reason=f"internal: {type(e).__name__}: {e}", status=None)
  557|     return rec
