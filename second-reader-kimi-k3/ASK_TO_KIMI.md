Follow-up on your second-reader report and one-page precursor note (both dated 2026-11-19). Your texts are being filed unedited as working notes in a public CC0 repository, with a separate file recording what was checked. Your replies will be filed the same way, so please answer as plain text.

HOW TO ANSWER
- Plain text only. Put every table in a fenced code block. No rendered links, widgets or citation chips: in the paste I received, five of them arrived as blank placeholder characters, and that is how two tables and the citation links were lost.
- Answer by item number. Label each statement READ (you opened the source this session), RAN (you executed code this session), RECALLED (from memory, not opened), or INFERRED.
- If you cannot recover something, write "cannot recover". Please do not regenerate a missing table from memory. If you re-run something, give the new numbers separately and label them RE-RUN, so they are not mistaken for the original.

A. MISSING CONTENT (most needed)
1. Part B. In your report the seven-row table was lost. Give for each of the seven axioms: the algebra.mm label; the set.mm label compared; the algebra.mm guard, verbatim; the set.mm antecedent, verbatim; your verdict. Then: which repository, path and commit holds algebra.mm (I could not find it in the file listings of the Simulators or Geometric-to-Binary bridge repositories); the full hash of "metamath/set.mm develop @ blob e483895" and whether you fetched it or recalled it; and for the statements you quote (sqrtsq, sqrtth, df-div, resqrtth/sqsqrti), whether the text is READ or RECALLED.
2. The table after "Replay at series length 200" was lost. Give the full grid: every window, both limits (0.3 and 0.5), catches and false alarms, out of 200. Include the cells you quote: w40/0.5 (89 catches, 0 false alarms) and w60/0.5 (120 and 6).
3. The five citations (Dakos 2012; Boettiger & Hastings 2012; O'Brien 2023; Clements & Ozgul 2018; Scheffer 2009 if used): give the URL or DOI for each, and for each quoted phrase say whether you read it in the full text or in a search snippet.

B. REPRODUCIBILITY
4. Send the code you ran, as text: the Python replay, the JavaScript port, and the surrogate calibration. State the RNG and how seeds 0..199 and 10000..10199 became series; the starting value of the AR(1) series; the exact schedule of the coefficient (0.05 to 0.95); the drift and step constructions. (My own replication used Python's random module, with an assumed start value and linear schedule, and matched your raw table in 30 of 32 cells, so I need to know whether we share the same details.)
5. Your n=60 figures (79/8 and 120/20 at w30; "46 to 14" catches and "3 to 0; 12 to 1" false alarms at w20): did you run the n=60 side this session, or take it from a file in the repository? If from a file, which one?
6. Surrogates: how the phase randomization was done (what happens to the mean and the Nyquist term), the percentile used for each tau separately, one-sided or two-sided, and how "add-one p" was computed. Give the raw counts per cell for the 4 signal classes x 4 windows.
7. The "36/36 exact flag matches" check and the six JavaScript cells: which series, and the raw outputs.
8. Which of the two attached PNG files shows which table, and what the three panels and the curves are.

C. PROVENANCE
9. The date 2026-11-19: where did it come from (system clock, a tool, assumed), and in what time zone? I received the texts at about 19:00 UTC on 2026-11-18, which is already the 19th in UTC+8. I want to know whether that explains it.
10. Which files did you open live (give the URL and commit or hash) and which did you recall? In particular the version and sha256 of glyph/precursor.py you ran, and the TAF repository URL and full commit hash behind "16285cc".
11. Part A: for each of the eight pairs, were the quoted definition texts copied from the source or paraphrased by you? Mark each.
12. You disclosed that you saw the first reader's verdicts. Besides the section 9c lines, did you see anything else from the first reader's work before assigning?

Thank you. Anything you could not do, or chose not to do, is as useful to me as what you did.
