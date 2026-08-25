---
name: voice-cloud-orchestrator
description: Voice-first cloud orchestrator — active build target; voice-to-sim-to-voice pipeline with per-community forks.
sources: [field]
aliases: [voice cloud orchestrator, voice-first orchestrator]
---

Active build target.

## Pipeline

voice -> energy_english constraint gate -> dispatcher -> cloud (Cloud Run or modal.com) ->
sim runner -> coating detector -> optics translator -> voice back

## Design

Multi-community, with a shared energy_english axiom and per-community forks. The shared axiom
is what makes the forks comparable; forking below the gate would produce systems that cannot
be read against each other.

See [[energy-english]].
