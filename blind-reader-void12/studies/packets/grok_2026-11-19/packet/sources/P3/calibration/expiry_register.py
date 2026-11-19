# Excerpt of P3/calibration/expiry_register.py, original line numbers kept (lines 51-60, 216-235 of 342). Lines not shown are omitted, not empty.

   51| CLASSES = ("SLOT", "EMITTER", "DEFAULT", "VOCAB", "RULE", "MENTION", "ARCHIVE", "OTHER_SENSE")
   52| CARRY_EXPIRY = ("SLOT", "EMITTER", "DEFAULT")
   53| EXPIRY_KEYS = ("instrument_class", "sensitivity", "protocol", "provenance")
   54| SCOPED = re.compile(r"^ABSENT_AT_SENSITIVITY\((.+)\)$")
   55| SELF = "calibration/expiry_register.py"
   56| 
   57| 
   58| def E(instrument, protocol, provenance, sensitivity="void"):
   59|     return dict(instrument_class=instrument, sensitivity=sensitivity, protocol=protocol, provenance=provenance)
   60| 
  ...

  216| def exit_state(e):
  217|     if e is None:
  218|         return None
  219|     if e == "void":
  220|         return "none"
  221|     if not isinstance(e, dict) or sorted(e) != sorted(EXPIRY_KEYS):
  222|         raise ValueError(f"expiry_condition must be void or carry {EXPIRY_KEYS}")
  223|     if any(e[k] in ("", "void") for k in ("instrument_class", "protocol", "provenance")):
  224|         raise ValueError("partial expiry_condition: instrument_class, protocol and provenance are required")
  225|     return "incomplete" if e["sensitivity"] == "void" else "complete"
  226| 
  227| 
  228| def slot_state(s):
  229|     """For a slot's state value: ABSENT_AT_SENSITIVITY needs its sensitivity; a bare absent is refused."""
  230|     if s in ("absent", "ABSENT", "ABSENT_AT_SENSITIVITY"):
  231|         raise ValueError("an absence needs its sensitivity: ABSENT_AT_SENSITIVITY(<value>)")
  232|     m = SCOPED.match(s)
  233|     if s.upper().startswith("ABSENT") and (not m or m.group(1).strip() in ("", "void")):
  234|         raise ValueError("ABSENT_AT_SENSITIVITY with no sensitivity")
  235|     return "scoped_absence" if m else s
