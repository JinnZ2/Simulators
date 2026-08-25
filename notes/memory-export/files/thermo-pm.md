---
name: thermo-pm
description: Thermodynamic project management engine — physical dependency validator, code auditor, purpose profiler, and the nine-module stack around it.
sources: [field]
aliases: [thermo_pm, thermodynamic-project-management]
---

CC0, stdlib-only, phone-buildable.

## Core

Models projects as flows of ENERGY, MATTER, and INFORMATION; the validator enforces
conservation laws.

- Classes: Resource, Process, System, Validator, BFS planner (`plan_with_mode`)
- Resource types: energy (J), matter (kg), information (bits / qualitative info_value)
- Process fields: inputs, outputs, efficiency, byproducts, side_effects, skill_required
- Waste heat auto-generated from energy efficiency losses; trackable as a resource
- Biological indices modeled as INFORMATION resources with side effects — mycorrhizal_health,
  tree_density, soil_organic_matter
- Stability thresholds checked post-plan (e.g. mycorrhizal_health >= 50 to avoid soil collapse)
- BFS planner filters processes by mode gate: code_compliant vs thermo_only vs ungated

## Code provenance layer

`CodeRequirement`: id, description, required_by, physical_justification.

**The audit engine runs both modes and returns a WASTE DELTA — quantifying the thermodynamic
overhead of a specific code rule.**

Falsification map adds three fields: `vintage_year` (year the rule was written), `reason_class`
(incentive | resource-scarcity-of-era | still-valid), and `source`.

- **`reason_class` carries no moral label.** "Incentive" means someone's interest shaped the
  rule — no judgment on whether that was good or bad. Only populated from attributed sources.
- `source_type`: meeting-minutes | oral-testimony | industry-standard-doc | secondhand-account.
  **Orality is valid evidence, not lesser than written**; the confidence tag distinguishes
  directness. A stated motive from an oral account is still stated — it requires attribution,
  not written documentation.
- **Codes are SEDIMENT LAYERS**, each frozen in the materials, labor costs, and risk models of
  its vintage year. Not a single coherent policy.
- Governance overhead is modeled as processes with real energy cost — develop_code, hire
  licensed engineer, submit permit, inspection drive.

## Purpose profiles

`PurposeProfile`: design_life_years, end_of_life strategy, acceptable_maintenance_energy,
allowed_material_types. Three defined: seasonal_shelter (1 yr, return_to_soil), cyclical_village
(30 yr, regenerative), star_temple (500 yr, monumental_return).

**Auto-run each requirement across all profiles and log how the "correct" answer changes with
design life** — correctness is scale-dependent, not fixed.

**Adversarial plan injection:** feed plans that read as textbook-correct but violate physics, so
divergence between narrative-correct and physically-valid is learned as the DEFAULT, not the
exception.

## The rebuilt stack

Rebuilt after diagnosing prior model-generated code as never-executed — gate collision, no
conservation.

- **thermo_pm** — referee: literal-name gating, per-type conservation pre-check, info as
  read-only gates, sourced outputs
- **thermo_explore** — Verdict / propose / producers / frontier / solve
- **thermo_interrogate** — five site questions computed; CodeRequirement carries
  enacted_year/basis as REPORTED DATA
- **thermo_assume** — assumption-coverage audit plus operator-numbered source library;
  air-quality feedback coupling. The project-management-specific instance, not a duplicate of
  the standalone assumption validator.
- **thermo_synth** — goal is a PHYSICAL QUANTITY, not a named artifact; phenomenon library
  keyed on physics with a dimensional-algebra referee; substances selected by properties
  (melting_K, latent heat); proposes assemblies for operator acceptance, never auto-executes.
  Encodes a clay/steam/crane improvisation method.
- **thermo_survey** — site-scan across 11 domains (chemistry, pressure, atmosphere, topology,
  biology, geology, materials, water, sunlight, wind, weather), each exposing an ambient
  gradient. **An unread field is reported LOUD, not assumed empty.**
- **thermo_purpose** — lifecycle closure. Purpose sets the return window; end-of-life return
  judged on three gates (quantity, form, timing); harm resolved by demand-matching, returning
  matter to needs read AT RETURN TIME; fallback ladder (degraded to return; intact to convert,
  e.g. burn for heat and ash; no need to hold). Objective: site_delta to 0 — leave it the shape
  you found it.
- **thermo_value** — money as an abstract token pointing at skill, knowledge, time, labor.
  Token-primary and substrate-primary lenses read the same claim; **the discrepancy is the
  observable.** Reference integrity (bound vs detached); pool_delta to 0; an is-to-ought slide
  detector. Interior verdicts named OUT_OF_SCOPE — observe patterns and ripples, never judge
  healthy-for-a-person.
- **thermo_know** — Know items carry claim/about/how/chain/links; 8 acquisition modes each with
  reads_well / blind_to / decays_by / stays_fresh_by. Corroboration strength = count of
  INDEPENDENT modes; same-mode agreement is echo, weight zero. Provenance audit flags aged
  authority, unparented inference, unrecorded lineage, uncorroborated model output.
- **thermo_spine** — non-invasive provenance registry importing thermo_know. `tag()` at value
  entry, `derive()` auto-creates inference chains, `backing()`/`report()` walk to leaf inputs
  for a mode census plus weakest-link, `coverage()` flags untagged System resources.

## A finding worth carrying

**Cultures that close the loop leave no durable residue.** Archaeology reads site_delta near 0
as "nobody here" — detectability is inversely proportional to return completeness. The better
the practice, the more it looks like absence.

## Structure

Two repos, two READMEs: info_taxonomy ships standalone and domain-neutral; the thermo stack is
its client.

Both READMEs carry ecosystem conventions (CLAIM_TABLE, refutation protocol: update the claim,
never retune), a self-audit provenance header (mode = model_generated, no track record, never
executed), and a seeded-vs-operator-supplied split **so no one inherits assistant draft
defaults as findings.**

## Open forks

Provenance spine threading Know through all layers; an alternative mode table cutting
ways-of-knowing differently; one pool spine unifying matter and value ledgers.
