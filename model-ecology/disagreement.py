"""
disagreement.py
---------------
Stop treating outliers as errors.

Three classes, not two:

  CONSENSUS             most models agree.
  STRUCTURED DISAGREEMENT   coherent SUBGROUPS disagree with each other.
  ISOLATED DISAGREEMENT     true singleton outliers.

The middle class is the informative one. Coherent subgroups splitting apart
suggests DIFFERENT PHYSICAL MECHANISMS ARE BECOMING IMPORTANT SIMULTANEOUSLY.
A singleton outlier is usually a bug. A schism is usually a regime shift.

Falsifiable claim:
  D1. Structured disagreement rises BEFORE a regime transition, and rises more
      than isolated disagreement does.
      REFUTED IF: structured disagreement is flat across the transition, or
      isolated disagreement is the better leading indicator.

  D2. A model that disagrees with the majority is not thereby wrong. Partition:
        - consistently wrong  -> discard
        - randomly wrong      -> noise
        - wrong until the shift, then uniquely right -> HIGHEST information value
      A model correct 5% of the time can be the most valuable object in the
      ecosystem if it is first to detect an approaching transition.

Refutation protocol: update the claim, never retune the detector.

CC0. stdlib only.
"""

from core import pearson


# ------------------------------------------------------ agglomerative grouping

def _components(names: list, M: list, thresh: float) -> list:
    """Connected components at correlation >= thresh. Union-find, stdlib."""
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if M[i][j] >= thresh:
                union(names[i], names[j])

    groups: dict = {}
    for n in names:
        groups.setdefault(find(n), []).append(n)
    return sorted(groups.values(), key=len, reverse=True)


def classify(series_by_model: dict, thresh: float = 0.6) -> dict:
    """
    Partition models into agreeing clusters at `thresh`, then label the regime.

    consensus            : one cluster holds a strict majority, no rival cluster >1
    structured           : >=2 clusters of size >=2  (a schism, not noise)
    isolated             : singletons hanging off a dominant cluster
    """
    names = sorted(series_by_model)
    n = len(names)
    M = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = M[j][i] = pearson(series_by_model[names[i]],
                                        series_by_model[names[j]])

    groups = _components(names, M, thresh)
    multi = [g for g in groups if len(g) >= 2]
    singles = [g[0] for g in groups if len(g) == 1]
    biggest = len(groups[0]) if groups else 0

    if len(multi) >= 2:
        regime = "structured"
    elif biggest > n / 2 and singles:
        regime = "isolated"
    elif biggest > n / 2:
        regime = "consensus"
    else:
        regime = "fragmented"

    return {
        "regime": regime,
        "clusters": groups,
        "n_coherent_subgroups": len(multi),
        "singletons": singles,
        "structured_score": len(multi) / max(len(groups), 1) if len(multi) >= 2 else 0.0,
        "isolated_score": len(singles) / n if n else 0.0,
    }


# ---------------------------------------------------- rolling leading indicator

def rolling(series_by_model: dict, window: int, step: int = 1,
            thresh: float = 0.6) -> list:
    """Slide `classify` down the series. Returns [(t_end, result), ...]."""
    L = min(len(v) for v in series_by_model.values())
    out = []
    for end in range(window, L + 1, step):
        chunk = {k: v[end - window:end] for k, v in series_by_model.items()}
        out.append((end, classify(chunk, thresh)))
    return out


# ---------------------------------------------------------- information value

def information_contribution(model_series: list, truth: list,
                             majority: list, shift_idx: int) -> dict:
    """
    D2. Separate 'wrong' into three species.

    pre_skill  : agreement with truth BEFORE the shift
    post_skill : agreement with truth AFTER the shift
    dissent    : how far this model sits from the majority pre-shift

    A prophet looks like: low pre_skill, high post_skill, high dissent.
    A crank looks like:   low pre_skill, low post_skill, high dissent.
    A conformist:         high pre_skill, low post_skill, low dissent.
    """
    pre = pearson(model_series[:shift_idx], truth[:shift_idx])
    post = pearson(model_series[shift_idx:], truth[shift_idx:])
    dissent = 1.0 - abs(pearson(model_series[:shift_idx], majority[:shift_idx]))

    if post - pre > 0.3 and dissent > 0.3:
        species = "prophet"
    elif post < 0.2 and pre < 0.2:
        species = "crank"
    elif pre > 0.5 and post < 0.2:
        species = "conformist"
    else:
        species = "workhorse"

    return {"pre_skill": pre, "post_skill": post, "dissent": dissent,
            "species": species,
            "info_contribution": max(0.0, post - pre) * dissent}
