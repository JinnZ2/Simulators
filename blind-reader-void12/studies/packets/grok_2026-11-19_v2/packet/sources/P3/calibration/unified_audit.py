# Excerpt of P3/calibration/unified_audit.py, original line numbers kept (lines 93-101, 209-236, 331-372, 479-496 of 662). Lines not shown are omitted, not empty.

   93| # A module that raised is not a reading of the system. Its status is
   94| # GAP_INSTRUMENT_CRASH and it goes to coverage with the exception and the
   95| # missing path, never to severity (2026-11-11 follow-up to #80).
   96| GAP_INSTRUMENT_CRASH = "GAP_INSTRUMENT_CRASH"
   97| 
   98| # Coverage kinds, kept apart: UNKNOWN (no value), INFO (a value that the
   99| # instrument cannot assess, e.g. non-numeric), GAP_INSTRUMENT_CRASH (the
  100| # instrument itself failed).
  101| COVERAGE_KINDS = ("UNKNOWN", "INFO", "GAP_INSTRUMENT_CRASH")
  ...

  209| @dataclass
  210| class UnifiedAuditReport:
  211|     system_id: str
  212|     modules_run: list[str] = field(default_factory=list)
  213|     modules_skipped: list[str] = field(default_factory=list)
  214|     sections: dict = field(default_factory=dict)
  215|     severity: str = NOT_DETERMINABLE
  216|     coverage: list[dict] = field(default_factory=list)
  217|     overall_status: str = NOT_DETERMINABLE
  218|     not_determinable_reason: Optional[str] = NO_MODULES_RUN
  219|     red_flags: list[str] = field(default_factory=list)
  220|     summary: str = ""
  221| 
  222|     def to_dict(self) -> dict:
  223|         return {
  224|             "system_id": self.system_id,
  225|             "modules_run": self.modules_run,
  226|             "modules_skipped": self.modules_skipped,
  227|             "overall_status": self.overall_status,
  228|             "severity": self.severity,
  229|             "not_determinable_reason": self.not_determinable_reason,
  230|             "coverage_count": len(self.coverage),
  231|             "coverage_by_kind": _coverage_by_kind(self.coverage),
  232|             "coverage": self.coverage,
  233|             "red_flags": self.red_flags,
  234|             "summary": self.summary,
  235|             "sections": self.sections,
  236|         }
  ...

  331| def _coverage_entries(name: str, status: str, section: Any) -> list[dict]:
  332|     """UNKNOWN inputs for one module, each with its expiry_condition."""
  333|     entries: list[dict] = []
  334|     if status == GAP_INSTRUMENT_CRASH:
  335|         sec = section if isinstance(section, dict) else {}
  336|         entries.append({
  337|             "kind": GAP_INSTRUMENT_CRASH,
  338|             "module": name,
  339|             "input": name,
  340|             "reason": sec.get("error", "module raised"),
  341|             "missing_path": sec.get("missing_path"),
  342|             "expiry_condition": _VOID,
  343|         })
  344|         return entries
  345|     if name == "assumption_validator" and isinstance(section, dict):
  346|         for aid, a in section.get("assumptions", {}).items():
  347|             if a.get("status") == "UNKNOWN":
  348|                 entries.append({
  349|                     "kind": "UNKNOWN",
  350|                     "module": name,
  351|                     "input": aid,
  352|                     "reason": a.get("message", "no value"),
  353|                     "expiry_condition": dict(_AV_UNKNOWN_EXPIRY),
  354|                 })
  355|             elif a.get("status") == "INFO":
  356|                 entries.append({
  357|                     "kind": "INFO",
  358|                     "module": name,
  359|                     "input": aid,
  360|                     "reason": a.get("message", "value not assessable"),
  361|                     "expiry_condition": _VOID,
  362|                 })
  363|         return entries
  364|     if status not in _STATUS_RANK:
  365|         entries.append({
  366|             "kind": "UNKNOWN",
  367|             "module": name,
  368|             "input": name,
  369|             "reason": f"module status {status!r} is not a measured severity",
  370|             "expiry_condition": _VOID,
  371|         })
  372|     return entries
  ...

  479|     def _dispatch(name: str, runner, *args, **kwargs):
  480|         try:
  481|             status, section = runner(*args, **kwargs)
  482|         except Exception as e:
  483|             # Was: status RED + a red flag. A crash is a gap in the
  484|             # instrument, not a reading of the system.
  485|             report.sections[name] = {
  486|                 "error": f"{type(e).__name__}: {e}",
  487|                 "exception_type": type(e).__name__,
  488|                 "missing_path": getattr(e, "filename", None),
  489|             }
  490|             report.modules_run.append(name)
  491|             module_statuses[name] = GAP_INSTRUMENT_CRASH
  492|             return GAP_INSTRUMENT_CRASH
  493|         report.sections[name] = section
  494|         report.modules_run.append(name)
  495|         module_statuses[name] = status
  496|         return status
