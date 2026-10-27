"""Tags shown beside every number in a report.

The first four come from the work order. SITE DATA is added here: a number
computed from the site's own YAML, with no outside assumption in it.
"""
OBSERVED = "OBSERVED"    # floor observation
FOUND = "FOUND"          # checked against a published source
PROPOSED = "PROPOSED"    # untested design choice
ASSUMED = "ASSUMED"      # placeholder number, overridable
SITE_DATA = "SITE DATA"  # computed from the site file
EXAMPLE = "EXAMPLE"      # invented, for illustration only

ALL = (OBSERVED, FOUND, PROPOSED, ASSUMED, SITE_DATA, EXAMPLE)
