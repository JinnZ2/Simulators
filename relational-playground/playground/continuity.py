"""Layer E. Continuity matrix. Five readings, kept apart.

Reorganization is not an ending: a configuration change with the system
criterion still met reads REORGANIZED, never CEASED.
"""
READINGS = ("system_continuity", "configuration_continuity", "transition_dynamics",
            "recovery_and_reorganization", "persistence_under_change")


class ContinuityMatrix:
    """system_criterion(state) -> bool and configuration_of(state) -> hashable are DECLARED
    by the experimenter. Without them the reading is UNDECLARED, not a default."""

    def __init__(self, system_criterion=None, configuration_of=None, basis="UNDECLARED"):
        self.system_criterion, self.configuration_of, self.basis = system_criterion, configuration_of, basis

    def read(self, times, states):
        if self.system_criterion is None or self.configuration_of is None:
            return {r: "UNDECLARED" for r in READINGS}
        alive = [bool(self.system_criterion(s)) for s in states]
        conf = [self.configuration_of(s) for s in states]
        changes = [(times[i], conf[i - 1], conf[i]) for i in range(1, len(conf)) if conf[i] != conf[i - 1]]
        lapses = [times[i] for i in range(1, len(alive)) if alive[i - 1] and not alive[i]]
        recov = [times[i] for i in range(1, len(alive)) if not alive[i - 1] and alive[i]]
        if all(alive):
            sysc = "CONTINUOUS"
        elif alive[-1]:
            sysc = "INTERRUPTED_THEN_RECOVERED"
        else:
            sysc = "CRITERION_NOT_MET_AT_END"
        return dict(
            system_continuity=sysc,
            configuration_continuity="UNCHANGED" if not changes else "CHANGED %d time(s)" % len(changes),
            transition_dynamics=changes,
            recovery_and_reorganization=("REORGANIZED" if changes and alive[-1] else "NONE" if not changes else "CHANGED_AND_CRITERION_LOST"),
            persistence_under_change=dict(fraction_of_samples_meeting_criterion=sum(alive) / len(alive), lapses=lapses, recoveries=recov),
        )
