# alignment-under-coupling

STATUS: marker under exploration. Uncoalesced. Confidence ~0.4, below comfort
threshold. Separate trajectory from `../MARKER.md` (custody-verification-band)
— do NOT merge them.

Correct response: test fit, extend, or report where it breaks.

LICENSE: CC0. stdlib only. No deps. No numpy.

---

## SHAPE BEING TESTED

    Three observed phenomena may sit in the same formal family
    (local coupling + weak global field -> ordering, with a critical point):

    1. model consensus following popularity
    2. ferrimagnetic / domain alignment under external field
    3. loop-formation threshold in optimal transport networks (Kaiser 2020)

    If they are the same family, the discontinuous-transition result
    appears a third time and the shape is worth a confidence bump.
    If SIM-D fails, the easy version of the analogy is dead.

## WHAT THE LITERATURE ALREADY SUPPLIES

    majority force coefficient   De Marzo et al. Measured tendency of model
                                 agents to follow the majority.
                                 => this is J, the coupling constant.

    consensus insensitive to     Networked-LLM-agent work. Final beliefs
    initial positions            largely independent of starting positions —
                                 a DEPARTURE from DeGroot, which predicts
                                 consensus = centrality-weighted average of
                                 initial opinions. Attractor set by
                                 pretraining/alignment bias.
                                 => this is h, external field, dominating J.

    HK threshold nonlinearity    Modified Hegselmann-Krause. Marginal impact
                                 of threshold on consensus is nonlinear,
                                 sharp change near 0.5.
                                 => candidate third discontinuous transition.

    instruction tuning lowers    Lower next-token entropy and fewer embedding
    diversity                    clusters vs base models. ATTRACTOR STATES
                                 found by perturbing generation trajectories
                                 and observing return.
                                 => a basin, not a bias.

    recursive training entropy   4.2 -> 2.5 nats under synthetic retraining.
                                 3.5 -> 3.3 with domain anchoring.
                                 => same shape as buffer-counted-as-supply:
                                    fluency survives, long tail goes,
                                    aggregate metric holds until it doesn't.

    TEMPERATURE HAS NO EFFECT    Guo, Shang, Clavel. Counterintuitive.
                                 => ordering lives in the LEARNED
                                    DISTRIBUTION, not in sampling.
                                 => FALSIFIES the naive field model.
                                    This is the load-bearing constraint.

## SIMS

    SIM-A  field vs coupling      does h-dominance reproduce
                                  initial-condition insensitivity?
    SIM-B  entropy depletion      reproduce 4.2->2.5 vs 3.5->3.3;
                                  find the anchoring fraction that holds
    SIM-C  loop threshold         is the transition discontinuous, and
                                  where is the critical point
    SIM-D  temperature null       ORDERING TEST. If temperature moves
                                  homogenization in the model but not in
                                  the literature, the model is wrong.

## OPEN

    - no critical exponent has been fitted to any of the three. Until one
      is, "same family" is a shape read, not an established claim.
    - is the majority force coefficient measured on the same scale across
      studies, or study-local? If study-local it is not yet a J.
    - SIM-D is the discriminator. Run it first.
