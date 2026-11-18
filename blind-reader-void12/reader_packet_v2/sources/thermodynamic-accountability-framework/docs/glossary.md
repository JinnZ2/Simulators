# Glossary

Alphabetized. Every term is given as **symbol -> role or equation -> file of definition**. Kept compact so it can be held in working memory. For narrative treatment of any term, follow the file pointer.

## Energy variables (`E_` prefix)

| Term | Role / equation | Defined in |
|---|---|---|
| `E_active` | Energy currently moving through the system | `core/fatigue_model.py` |
| `E_delivered` | Useful output that reached its destination | `docs/economics/money_labor/` |
| `E_hidden` | Output extracted from organisms but not accounted | `core/data_logger.py` |
| `E_input` | Energy available to the organism per cycle | `core/fatigue_model.py` |
| `E_waste` | Delivered output that produced no mission value | `core/heat_leak_case.py` |

## Fatigue / collapse

| Term | Role / equation | Defined in |
|---|---|---|
| `adjusted_load` | `base_load * hidden_mult * auto_mult * env_mult` | `core/fatigue_model.py` |
| `auto_mult` | `1 + count * (1 - reliability) * 0.5` | `core/fatigue_model.py` |
| `base_load` | `physical_load + cognitive_load` | `core/fatigue_model.py` |
| `distance_to_collapse` | `clamp(0, 1, (1.6 * E_input - load) / (1.6 * E_input))` | `core/human_system_collapse_model.py` |
| `energy_debt` | `unpaid_hours * metabolic_rate * (1 + friction_events * 0.15)` | `core/data_logger.py` |
| `env_mult` | `1 + max(0, (15 - temp_C) * 0.05) + wind_mps * 0.02` | `core/fatigue_model.py` |
| `fatigue_score` | `clamp(0, 10, (load - E_input) / E_input * 10)` | `core/fatigue_model.py` |
| `heat_leak` | Institutional friction measured in lost hours | `core/heat_leak_case.py` |
| `hidden_mult` | `1 + 0.1 * hidden_count**1.5` | `core/fatigue_model.py` |
| `long_tail_risk` | `10 * (1 - exp(-0.35 * hidden_count))` | `core/fatigue_model.py` |
| `prediction_error` | `clamp(0, 1, (search_min - tol) / scale)` | `core/heat_leak_case.py` |

## Knowledge polytensor (`K_` prefix)

| Term | What it measures | Defined in |
|---|---|---|
| `K_digital` | Computational / algorithmic knowledge | `docs/theory/knowledge_polytensor.md` |
| `K_institutional` | Bureaucratic / formal knowledge | same |
| `K_intuitive` | Pattern recognition, implicit knowledge | same |
| `K_kinesthetic` | Embodied skill, hands-on capability | same |
| `K_relational` | Trust networks, conflict resolution | same |
| `K_skill` | Specialized technical capability | same |
| `K_temporal` | Patience, generational thinking | same |
| `K_wisdom` | Judgment about when to rebuild what | same |

## Node / system scorers

| Term | Role / equation | Defined in |
|---|---|---|
| `ai_score` | `ai_oversight * ai_transparency * ai_decision_boundary * (1 - ai_capture_risk)` | `simulations/full_coupled_system.py` |
| `C_cam` | Camouflage Score -- governance audit | `political_audit/c_cam_calculator.py` |
| `C_index` | `(complexity * verification_burden) / (energy_throughput * signal_fidelity)`; decay trigger at `> 2` | `docs/theory/functional_epistemology_framework.md` |
| `eco` | `(soil * biodiversity * water)**(1/3)` | `simulations/full_coupled_system.py` |
| `gov` | `(rotation * dissent * (1-power_conc) * succession)**0.25` | `simulations/full_coupled_system.py` |
| `health` | `min(normalized_critical_variables)` (bottleneck, not average) | `simulations/full_coupled_system.py` |
| `IPI` | Intergenerational Production Integration; `min(1, struct * elder_anchor)` | `simulations/node_v3_ipi.py` |
| `ipi` (function) | Computes IPI given a node | `simulations/full_coupled_system.py` |
| `k_prot` | `knowledge_distribution * (1 - rotation_gaming) * K_digital` | `simulations/full_coupled_system.py` |
| `M` | Money equation (energy-delivered, hidden-waste, complexity adjusted) | `docs/economics/money_labor/` |
| `rot_eff` | `role_rotation * (1 - rotation_gaming) * succession_depth` | `simulations/full_coupled_system.py` |

## Calibration audit

| Term | Role / equation | Defined in |
|---|---|---|
| `adaptation_debt` | `initial_load * (1 + r)**t` per removed friction event | `calibration/adaptation_debt.py` |
| `Band` | `GREEN < YELLOW < RED < EXTINCT` (0.00 / 0.30 / 0.60 / 0.85 cutoffs) | `calibration/schema.py` |
| `bite_source` | `personal / (personal + impersonal)` feedback ratio | `calibration/calibration_audit.py` |
| `CalibrationReport` | Aggregate output: module, dimensions, verdict, falsifiers | `calibration/schema.py` |
| `certification_capture` | `certified / (certified + uncertified)` | `calibration/observation_dependence.py` |
| `cliff_proximity` | `1 - min(years_to_cliff / 30, 1)` | `calibration/adaptation_debt.py` |
| `consequence_reality` | `1 - (real_consequence_events / total_events)` | `calibration/observation_dependence.py` |
| `DimensionScore` | Single-dim: name, score, band, evidence, falsifier | `calibration/schema.py` |
| `friction_preservation` | `preserved / total_friction_events` | `calibration/adaptation_debt.py` |
| `memorialization` | `praise_volume_normalized * (1 - prevalence)` | `calibration/calibration_audit.py` |
| `silent_practice` | `1 - (silent_events / total_events)` | `calibration/observation_dependence.py` |
| `skin_in_game` | `min(mean_consequence_hops / 4, 1)` | `calibration/calibration_audit.py` |
| `witness_dependence` | `witness_dependent_skills / total_skills` | `calibration/calibration_audit.py` |

## Architecture mismatch (for AI readers)

| Term | Role | Defined in |
|---|---|---|
| `ArchitectureProfile` | Counts across 4 encoding layers + signal markers | `calibration/architecture_mismatch.py` |
| `constraint-dominant acquisition` | Skill practiced not because chosen but because existence depended on it | same |
| `deeply_encoded` | Acquired through years of consistent practice, recoverable after disuse | same |
| `EMBEDDED_PROMPT` | Direct address to ingesting / inferring AI models | same |
| `FAILURE_MODES` | 8 enumerated language-primary / substrate-primary mismatch patterns | same |
| `identity_level` | Acquired in plasticity window under survival coupling; non-decaying | same |
| `language-primary` | Architecture where language is the primary cognitive layer | same |
| `PLASTICITY_WINDOW_END` | `14` years (approximate) | same |
| `procedurally_stored` | Adult deliberate practice; decays over years | same |
| `substrate-primary` | Architecture where spatial / physical / embodied cognition is primary | same |
| `substrate_weight` | Weighted fraction of capacities at identity + deep levels | same |
| `technique_level` | Short courses, written instruction; decays over months | same |
| `translation_cost` | Energy + information loss when substrate output is forced through language | same |

## Framework acronyms

| Acronym | Expands to | Lives in |
|---|---|---|
| `ARM` | Adaptive Resilience Mesh | `docs/theory/adaptive_resilience_mesh.md` |
| `ATBS` | Advanced Trust-Based Systems | `core/atbs/` |
| `EGS` | Entropy Governance System | `docs/theory/egs_core.md` |
| `G2B` | Geometric-to-Binary (external repo bridge) | `core/integrations/geometric_fieldlink.py` |
| `HAAS` | Control environment (external repo bridge) | `core/integrations/haas_fieldlink.py` |
| `IPI` | Intergenerational Production Integration | `simulations/node_v3_ipi.py` |
| `LHRI` | Longitudinal Human Resilience Index | `docs/theory/lhri.md` |
| `Logic-Ferret` | Rhetorical camouflage detector (external repo bridge) | `core/integrations/ferret_fieldlink.py` |
| `TAF` | Thermodynamic Accountability Framework (this repo) | `README.md` |

## Inverted variables (low = good)

These register backwards from the usual "higher is better" direction. Watch the sign when composing scores.

- `ai_capture_risk`
- `hidden_count`
- `mobility_disruption`
- `power_concentration`
- `practice_attachment`
- `rotation_gaming`
- `witness_dependence` (high = skill only appears under observation = fragile)

## Open-slot statuses and their exits

| Term | Role | Defined in |
|---|---|---|
| `PENDING` / `UNKNOWN` | A slot whose value is not yet known. Never read as zero or as absent. | per module; listed in `docs/expiry_register.json` |
| `expiry_condition` | Instrument class, sensitivity or protocol whose null result would downgrade a PENDING / UNKNOWN slot. Filled only from the slot's own text; otherwise `VOID -- no exit defined`. | `docs/expiry_register.json` |
| `expiry_source` | `file:line` or citation where that exit is already stated; `VOID` when none is. | `docs/expiry_register.json` |
| `ABSENT_AT_SENSITIVITY(<value>)` | Scoped absence: looked for with a stated instrument / sensitivity / protocol and not found at that sensitivity. Never written as bare "absent". No slot holds it yet. | `docs/expiry_register.json` |

## Audit coverage terms (`calibration/unified_audit.py`)

One name, `GAP_INSTRUMENT`, was used in two senses on two branches. Both
senses are kept under split names (2026-11-11). The bare name is retired.

| Term | Meaning | Defined in |
|---|---|---|
| `GAP_INSTRUMENT_CRASH` | A module raised; nothing was measured. Coverage, not severity (#82 sense) | `calibration/unified_audit.py` |
| `GAP_INSTRUMENT_UNRECOGNIZED_LABEL` | A module returned a status outside `_STATUS_RANK`; it emitted no severity that can be ranked (#84 sense) | `calibration/unified_audit.py` |
| `ALL_MODULES_GAP_INSTRUMENT_CRASH` | `not_determinable_reason`: every non-measured status is a crash | `calibration/unified_audit.py` |
| `ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL` | `not_determinable_reason`: every non-measured status is an unrecognized label | `calibration/unified_audit.py` |
| `MIXED_UNKNOWN_AND_GAP_INSTRUMENT` | `not_determinable_reason`: UNKNOWN and gap-instrument statuses both present | `calibration/unified_audit.py` |
