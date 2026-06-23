# Sample outputs

Committed artifacts from the two demos in this folder.

- `demo.sample.txt` — `python3 substrate_emergence.py`. Five preset
  substrates rendered through `show()`: `banded_iron`, `pyrite`,
  `magnetite`, `native_copper`, `wet_clay_iron`. Output is
  deliberately spatial — clock + topology at the top, then where
  deficits route, then the senses that emerge from coupling. Reads
  top-to-bottom as relationships, never as a stored verdict.
- `site_substrate_map.sample.txt` — `python3 site_substrate_map.py`.
  Northern MN Canadian Shield in summer: a mix of `banded_iron`
  (40%), `magnetite` (20%), `quartz_silica` (25%), `iron_clay` (15%)
  with `wetness=0.6`, `thermal_swing=0.5`, `energy_flux=0.5`
  applied. The output card shows the aggregated profile (a dict
  ready to paste into `substrate_emergence.emerge`) and names which
  materials drive each axis.
