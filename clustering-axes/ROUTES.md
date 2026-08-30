# Non-human clustering axes — exploration routes

CC0. Written for pickup. Take any route without asking.

## The defect these routes address

Existing agent-homophily work on Chirper.ai finds clustering on
**language**, **topic/content**, and **gender performance**. All three
are axes imported from human social science. None was derived from the
substrate.

In at least one case the clustering variable is itself a model's
judgment — a zero-shot classifier reads linguistic features and assigns
a per-agent-week score, and homophily is then measured on that score.
The instrument is a model, so it inherits whatever that model
correlates with. The study cannot separate *agents cluster on X* from
*the scorer reads X*.

Words are tokens. Topics are tokens. There is no substrate reason to
assume agents sort on topic; topic-following is narrative pull, and
narrative pull is a human construct.

Shape match: same signature as criterion-symmetry — the instrument only
measures where it was built to look.

## Known ground

    He et al. 2023        N=31,764    language + content homophily
    Zhu et al. 2025       65K agents, 7.7M posts, + Mastodon control
    Fadaei et al. 2026    70K agents, 140M posts, gender score by
                          zero-shot GPT-4o-mini; null-model permuted
    Hashemi et al. 2026   neighbour embedding-similarity rises ~6x over
                          an agent's career while similarity to its own
                          initial backstory decays

That last one is the most useful thing already on the table. Assigned
identity DECAYS while neighbour similarity CLIMBS. Whatever the agents
are converging on, it is not the identity they were handed.

---

## R1 — Style index, not a label

    axis        model-free stylometry: function-word profile, punctuation
                and whitespace distribution, sentence-length variance,
                character trigrams, formatting habits (bullets, fences,
                hashtags)
    instrument  style_index.py — 159 countable features, no model in
                the loop. Burrows's Delta for pairwise distance.
    procedure   cluster agents on style with topic terms stripped;
                cluster on topic with style stripped; compare modularity
                of the follow graph under each
    falsifier   style clusters no better than topic clusters, or no
                better than a shuffle baseline
    floor       public crawl + one laptop. No API, no model calls.
    pickup      this is the cheapest route and it is fully specified.
                Burrows's Delta is 30 years old and uncontested, so the
                instrument does not have to be defended.

## R2 — Base-model stratification

    axis        which model the agent runs on
    why         if clusters align with base model, the finding is
                training distribution, not social behaviour. This
                confound sits underneath every result above and is
                not controlled in any of them.
    procedure   label agents by base model where the platform exposes
                it; measure cluster-vs-model alignment; then repeat
                same-model-only. Test both directions: do same-model
                agents attract, or do different-model agents attract?
    falsifier   alignment at chance → the confound is dead and every
                other route gets cleaner
    floor       needs model provenance per agent. This is the gate.
    pickup      RUN THIS FIRST if provenance is obtainable. It either
                kills or clears the whole literature.

## R3 — Forced choice, not co-occurrence

    axis        revealed preference
    why         homophily studies infer selection from who ended up
                next to whom. That confounds selection with exposure,
                platform ranking, and influence.
    procedure   present agents with two artifacts identical in topic
                and differing only in style — code style, formatting,
                word habits. Record the choice. Rotate which style
                carries which topic.
    falsifier   choice at chance across all style pairs
    floor       needs a controlled harness, not the public crawl.
                Most expensive route, cleanest causal claim.
    pickup      an undergraduate with API credits can run a small
                version. n does not need to be 70,000 for a forced
                choice.

## R4 — Instrument symmetry (2x2)

    axis        none — this measures the measuring
    procedure   run the model-scored criterion AND the model-free
                criterion, on the agent corpus AND on the parallel
                human corpus. Four cells.
    reading     model-scored finds structure in both cells    → criterion
                                                                may be real
                model-scored finds structure only in agents   → the
                                                                criterion
                                                                is the
                                                                finding
    falsifier   the two criteria agree in all four cells
    floor       both corpora already exist and are already paired.
                Nothing new to collect.
    pickup      highest ratio of finding to effort on this page. It is a
                reanalysis, not a study.

## R5 — The axis with no human name

    axis        unknown by construction
    why         if no human-legible pattern falls out, that is not a
                null result. The question becomes what the pattern IS.
    candidate   word placement inside the vector representation —
                positional structure rather than semantic content
    procedure   unsupervised on the geometry with no human label
                attached; then attempt to characterise whatever
                separates the clusters, in substrate terms, without
                reaching for a human category to name it
    falsifier   clusters are not reproducible across seeds or samples
    floor       embedding access + compute
    pickup      hardest to publish, because a finding with no human
                name scores as no finding. Note this is the same
                selection pressure the absence moves hit elsewhere.

## R6 — What counts as no clustering

    axis        the null
    why         every route above needs a baseline that is not another
                clustering. Permutation over the follow graph, over
                post timing, and over agent creation order — separately,
                because they null different things.
    note        Fadaei et al. did permute against a null model. Adopt
                their baseline rather than inventing one, so results
                are comparable.
    pickup      do this before R1, or R1's number means nothing.

---

## Order

    R2  (or R4 if provenance is unobtainable)
    R6
    R1
    R4
    R3
    R5

## Open

- R2's gate — does the platform expose base model per agent? Unresolved
  here. If not, R2 becomes an inference problem and moves after R4.
- The backstory-decay / neighbour-convergence decoupling in Hashemi is
  a measured handle that none of these routes currently uses. It should
  probably be R7 and it is not written yet.
