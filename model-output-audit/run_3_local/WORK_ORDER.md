WORK ORDER (home server, local Gemma or other open model)
Input: JinnZ2/Simulators, branch model-output-audit, run_2/records.json
1. For each decided claim + the 8 pass claims: independent verdict, same class set.
2. Report agreement with run_2 per class; list every disagreement with quote.
3. Fidelity, real read: pick 5 of the 11 MATCH specs; compare step by step,
   spec vs code: omitted step / changed logic / added constraint / inverted condition.
4. Write run_3_local/ (auditor = model name + version); never edit run_1/run_2.
5. Stdlib only for any rerun. Agency void. No intent labels.
