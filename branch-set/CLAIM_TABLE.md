# branch-set -- claim table

| id | claim | status | number | falsifier |
|---|---|---|---|---|
| BS_001 | Priority is derived from the count of open branches sharing a result, never declared; on the fixture three branches fit R1 and the queue puts all three ahead of the lone R2 branch, cheapest first. | SUPPORTED | queue: m_matcher, h_catalog, g_model, lone | a queue ordering that does not follow (priority desc, cost asc) |
| BS_002 | An eliminated branch without a named discriminator is refused; a prediction in the origin domain is refused. | SUPPORTED | 2 refusals in selftest | either accepted |
| BS_003 | Triage is a function of two declared fields (record state, suppression cause and kind) and the rule is printed; it infers nothing from free text. | SUPPORTED | 3 gaps, 3 distinct triages | a triage that reads generator or discriminator prose |
| BS_004 | A lag of 30 years on a branch stating `prior` is flagged as an access marker and the row is left as delivered. | SUPPORTED | 1 flag | a rewritten suppression_cause |
| BS_005 | No real branch set has been serialized; the fixture is constructed. | UNVERIFIED | -- | a held set transported and re-read |
