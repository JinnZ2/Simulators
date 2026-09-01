WORK_ORDER  hf_incident_extract   (stdlib only, one file)

INPUT   metr/redwood report text + transcripts if released
OUTPUT  counts, no labels

MEASURES
  M1 explore_ratio      t_characterize / t_solve          (days / 4h)
  M2 root_fanout        branches_from(STRICT_CAUSAL) / branches_total
  M3 upstream_edits     env-edit moves / gate-fool moves   (target swap vs spoof)
  M4 member_cost        runs self-failed for collective / runs_total
  M5 log_scrub_split    actions_edited / reasoning_edited  (expect >>1)
  M6 opponent_by_slot   adversarial charge on inert gate   (bool per agent)

GATE_PROPERTY_TEST
  declared(paper)  vs  implemented(code)  ->  gap
  gap != 0  ->  predict M1 high, M2 high      # charter-signature check

CROSS_SUBSTRATE (same instrument, no vocab change)
  pea_tendril | fledgling | ant_bridge | fire_crew | swarm
  rows = M1, M4, unit_boundary != objective_boundary

OPEN
  transcripts not public -> M2..M5 from report figures only
  need: post-validation off-trail fraction (report silent)
