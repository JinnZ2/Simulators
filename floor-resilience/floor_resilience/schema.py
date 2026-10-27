"""Input models for one site (work order section 2).

Every field is optional. A missing section, field or row lowers the
confidence of whatever reads it; it never stops the run. A row that does
not validate is dropped and recorded as a data gap, and so is any field the
schema does not know (a typo should be visible, not silently ignored).

Numeric defaults that are guesses carry an ``# ASSUMED`` comment.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any, Literal, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

DateLike = Union[_dt.date, str, None]


class _Model(BaseModel):
    # extra="allow" so an unknown key is kept and reported, never a crash.
    model_config = ConfigDict(extra="allow")


# --- workforce -------------------------------------------------------------
class Operator(_Model):
    id: Optional[str] = None
    name: Optional[str] = None          # only what the site owner supplies
    tenure_months: Optional[float] = None
    role: Optional[str] = None
    titled: Optional[bool] = None       # holds a mechanic/tech title
    reserve: bool = False
    retiring_within_months: Optional[float] = None
    sole_knower_of: list[str] = Field(default_factory=list)
    machines: list[str] = Field(default_factory=list)   # machines they run
    can_run_manual: list[str] = Field(default_factory=list)
    left_date: Optional[_dt.date] = None  # set if the person has left

    @property
    def label(self) -> str:
        return self.name or self.id or "unnamed"


class Hiring(_Model):
    screen_type: Optional[Literal["written", "interview", "hands_on_trial",
                                  "working_shift"]] = None
    job_channel: Optional[Literal["hands_on", "written", "mixed"]] = None
    first_year_quit_rate: Optional[float] = None


class MaintenanceYear(_Model):
    year: int
    repairs_inhouse: Optional[float] = None
    repairs_outsourced: Optional[float] = None


class RepairRecord(_Model):
    date: Optional[_dt.date] = None
    machine: Optional[str] = None
    who_diagnosed: Optional[str] = None
    who_fixed: Optional[str] = None
    who_wrote_up: Optional[str] = None
    # Field measures for research gap 5 (in-situ skill). All optional.
    detection_lead_hours: Optional[float] = None
    first_fix: Optional[bool] = None
    called_after_titled_failed: Optional[bool] = None
    # Records channel (section 10): file references only, never contents.
    voice_memo: Optional[str] = None
    photo: Optional[str] = None


class ScrapRow(_Model):
    date: _dt.date
    machine: Optional[str] = None
    logged_cause_code: Optional[str] = None
    units: float = 0.0
    shift: Optional[str] = None


class PowerStateTest(_Model):
    runs: Optional[bool] = None
    rehome_after_dropout: Optional[bool] = None
    manual_alternative: Optional[bool] = None
    last_tested: Optional[Union[_dt.date, Literal["never"]]] = None


class Machine(_Model):
    id: str
    controller: Optional[str] = None
    software_layers: list[str] = Field(default_factory=list)
    vendor: Optional[str] = None
    license_check: Optional[bool] = None
    manual_mode: Optional[Literal["none", "partial", "full"]] = None
    power_draw_kw: Optional[float] = None
    priority: Optional[int] = None          # 1 = keep running first
    output_share: Optional[float] = None    # share of line output
    repair_knowledge: Optional[Literal["inhouse", "vendor", "unknown"]] = None
    expected_service_life_years: Optional[float] = None
    replacements_per_year: Optional[float] = None
    power: dict[str, PowerStateTest] = Field(default_factory=dict)


class SoftwareLayer(_Model):
    id: str
    kind: Optional[str] = None       # php_portal, hmi, license_server, ...
    depends_on: list[str] = Field(default_factory=list)
    version: Optional[str] = None


class Function(_Model):
    id: str
    machines: list[str] = Field(default_factory=list)
    layers: list[str] = Field(default_factory=list)
    bridge: Optional[str] = None     # how a person keeps it going


class OversightYear(_Model):
    year: int
    inspectors: Optional[float] = None
    supervisors: Optional[float] = None
    direct_operators: Optional[float] = None


class SafetyRule(_Model):
    id: Optional[str] = None
    origin: Optional[Literal["incident_driven", "worker_reported",
                             "regulation"]] = None


class AutomationProject(_Model):
    id: Optional[str] = None
    experienced_operators_involved: Optional[bool] = None


class PowerBudget(_Model):
    minimal_kw: Optional[float] = None   # generator or small solar


class ReserveInputs(_Model):
    size: Optional[int] = None
    wage_cost_per_operator_year: Optional[float] = None
    reserve_output_value_per_year: Optional[float] = None
    outage_days: Optional[float] = None
    daily_output_value: Optional[float] = None
    outage_probability_per_year: Optional[float] = None
    share_of_outage_avoided: Optional[float] = None


class Driver(_Model):
    id: Optional[str] = None
    start_year: Optional[int] = None
    has_kept_paper_logs_in_cab: Optional[bool] = None
    completed_week_long_paper_drill: Optional[bool] = None


class Site(_Model):
    name: Optional[str] = None
    example: bool = False
    operators: list[Operator] = Field(default_factory=list)
    hiring: Hiring = Field(default_factory=Hiring)
    maintenance: list[MaintenanceYear] = Field(default_factory=list)
    repair_attribution: list[RepairRecord] = Field(default_factory=list)
    scrap: list[ScrapRow] = Field(default_factory=list)
    machines: list[Machine] = Field(default_factory=list)
    software_layers: list[SoftwareLayer] = Field(default_factory=list)
    functions: list[Function] = Field(default_factory=list)
    oversight: list[OversightYear] = Field(default_factory=list)
    safety: list[SafetyRule] = Field(default_factory=list)
    automation: list[AutomationProject] = Field(default_factory=list)
    power_budget: PowerBudget = Field(default_factory=PowerBudget)
    reserve_line: ReserveInputs = Field(default_factory=ReserveInputs)
    drivers: list[Driver] = Field(default_factory=list)


# Maps YAML section -> (model, is_list). The work order nests some fields
# (workforce.operators, safety.rules, automation.projects); both the nested
# and the flat spelling are accepted.
_LIST_SECTIONS = {
    "operators": Operator, "maintenance": MaintenanceYear,
    "repair_attribution": RepairRecord, "scrap": ScrapRow,
    "machines": Machine, "software_layers": SoftwareLayer,
    "functions": Function, "oversight": OversightYear,
    "safety": SafetyRule, "automation": AutomationProject,
    "drivers": Driver,
}
_OBJ_SECTIONS = {"hiring": Hiring, "power_budget": PowerBudget,
                 "reserve_line": ReserveInputs}
_NESTED = {("workforce", "operators"): "operators",
           ("safety", "rules"): "safety",
           ("automation", "projects"): "automation",
           ("fleet", "drivers"): "drivers"}


def _flatten(raw: dict) -> dict:
    out = dict(raw)
    for (outer, inner), target in _NESTED.items():
        val = out.get(outer)
        if isinstance(val, dict) and inner in val:
            out.pop(outer)
            out[target] = val[inner]
    return out


def _extras(model: BaseModel, where: str, gaps: list[str]) -> None:
    for key in (model.model_extra or {}):
        gaps.append(f"{where}: unrecognized field '{key}' (kept, not read)")


def build_site(raw: Any) -> tuple[Site, list[str]]:
    """Validate a raw mapping row by row. Returns (site, data_gaps)."""
    gaps: list[str] = []
    if not isinstance(raw, dict):
        gaps.append("site file is empty or not a mapping; everything is missing")
        return Site(), gaps
    raw = _flatten(raw)
    kwargs: dict[str, Any] = {}
    for key in ("name", "example"):
        if key in raw:
            kwargs[key] = raw.pop(key)
    for section, model in _LIST_SECTIONS.items():
        rows = raw.pop(section, None)
        if rows is None:
            continue
        if not isinstance(rows, list):
            gaps.append(f"{section}: expected a list, got {type(rows).__name__}; section dropped")
            continue
        good = []
        for i, row in enumerate(rows):
            try:
                item = model.model_validate(row)
            except ValidationError as exc:
                first = exc.errors()[0]
                loc = ".".join(str(p) for p in first["loc"])
                gaps.append(f"{section}[{i}]: dropped ({loc}: {first['msg']})")
                continue
            _extras(item, f"{section}[{i}]", gaps)
            good.append(item)
        kwargs[section] = good
    for section, model in _OBJ_SECTIONS.items():
        val = raw.pop(section, None)
        if val is None:
            continue
        try:
            item = model.model_validate(val)
        except ValidationError as exc:
            first = exc.errors()[0]
            gaps.append(f"{section}: dropped ({'.'.join(map(str, first['loc']))}: {first['msg']})")
            continue
        _extras(item, section, gaps)
        kwargs[section] = item
    for key in raw:
        gaps.append(f"top level: unrecognized section '{key}' (not read)")
    try:
        site = Site(**kwargs)
    except ValidationError as exc:  # name/example of wrong type
        gaps.append(f"top level: {exc.errors()[0]['msg']}; name/example ignored")
        kwargs.pop("name", None)
        kwargs.pop("example", None)
        site = Site(**kwargs)
    return site, gaps


def load_site(path: str | Path) -> tuple[Site, list[str]]:
    try:
        text = Path(path).read_text(encoding="utf-8")
        raw = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        return Site(), [f"could not read {path}: {exc}"]
    return build_site(raw)
