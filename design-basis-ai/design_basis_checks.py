# design_basis_checks.py  —  CC0, stdlib only

def dissent_alarm(concurring_parties, independent_source_count):
    """P7. returns True if agreement is suspiciously wide for its base."""
    if independent_source_count <= 0:
        return True
    return concurring_parties / independent_source_count > 1  # tune threshold

def independence_ratio(distinct_upstreams, n_supporting):
    """P3/P7 for an evidence base. 1.0 = fully independent, ->0 = one upstream.
       distinct_upstreams: count of distinct {dataset,instrument,pipeline,
       funder,senior-author-network} across the supporting works."""
    return distinct_upstreams / n_supporting if n_supporting else float("nan")

def n_eff(channels_survive_shared_nodes):
    """core metric. list[bool]: does each channel survive ALL shared nodes."""
    independent = sum(1 for s in channels_survive_shared_nodes if s)
    collapsed   = 1 if any(not s for s in channels_survive_shared_nodes) else 0
    return independent + collapsed

# prediction to pre-register, testable on public metadata:
#   claims that later FAILED replication had high n_supporting, LOW independence_ratio.
#   kill condition: replication failure uncorrelated with independence_ratio.
