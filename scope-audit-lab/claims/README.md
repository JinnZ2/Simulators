# claims: live registry (SAL-WO4)

Four claims from late October 2026, recorded from 2026-10-27 under the
continuation report's own tracking protocol. `claims.jsonl` is append-only:
each event names the event it supersedes, and nothing is edited in place.

## Adding the next event

```python
import claim_tracker as ct
ct.append({
    "event_id": "E005", "claim_id": "openai-eth-disproof",
    "state": "CERTIFIED_FORMAL_ONLY",            # one of ct.STATES
    "event_date": "YYYY-MM-DD",                  # as the source reports it, or None
    "observed_at": "YYYY-MM-DD",                 # when this registry saw it
    "depth": "search_result",                    # or "primary"
    "summary": "...", "sources": ["url"], "supersedes": "E001",
})
```

`append` refuses a repeated id, an unknown state, a located state with no
source, an event dated after it was observed, and a supersedes link that
points forward or to another claim.

Updates need network access; this environment reaches search results but
not arxiv.org. The registry is written by a Claude model, so the
Anthropic-attributed item is recorded at the depth reached and is not
adjudicated.

    python3 claim_tracker.py               current state and days in state (two clocks)
    python3 claim_tracker.py --validate
    python3 test_claim_tracker.py
