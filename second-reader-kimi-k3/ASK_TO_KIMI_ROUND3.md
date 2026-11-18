Short follow-up (round 3). Thank you for the last reply: the repository numbers you gave checked out, and your raw tables reproduced exactly once I used your start value of 0.0. What did not arrive was every table and code block; they came through as blank placeholders even in code fences.

Easiest way to answer: put everything below into ONE plain-text file (.txt), and send me the file, or paste its contents with no tables rendered (use simple lines of text with spaces or commas between columns, no pipes, no markdown tables). If you can, also send the files named in item 9.

Please label each part READ, RAN, RECALLED or INFERRED as before, and say "cannot recover" rather than regenerating anything. If you re-run something, label it RE-RUN.

1. Part B: the seven-row guard table. For each row: algebra.mm label, set.mm label, the algebra.mm guard (verbatim), the set.mm antecedent (verbatim), your verdict.
2. The n = 200 grid: every window, both limits (0.3 and 0.5), catches and false alarms out of 200.
3. The citations: for each of the five papers, the URL or DOI, and whether you saw only a search snippet or more.
4. Code, as text: (a) the series generators for planted, white, drift and step; (b) the surrogate calibration function signatures and whatever body you can recover; (c) the JavaScript port if it still exists.
5. The surrogate calibration raw counts: 4 signal classes x 4 windows, out of 100.
6. The six JavaScript cells: planted catches and white false alarms, with their Python counterparts.
7. Part A, the eight pairs: for each, were the quoted definitions copied from the source or paraphrased by you?
8. One question about your description of the flag: you wrote "window-streak of tau >= limit reaching streak 3". The module's rule, as I read it, is PRECURSOR when BOTH the variance trend and the autocorrelation trend are >= the limit; streak_limit is only used by its mode-shift part. Which did your fast path implement? (My implementation of the "both >= limit" rule reproduces all your counts.)
9. Files, if you can export them: precursor_calibration.png; precursor-window-calibration-note.md; precursor-fix-sweep-note.md.

Anything you cannot do, or chose not to do, is as useful to me as what you did.
