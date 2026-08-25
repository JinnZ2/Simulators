# Findings -- four dataset uploads, 2026-08-25

Readings over `notes/datasets/uploads_2026_08_25.md`. The index records
what the files are; these are what follows from that, and two of them
run against what the files look like at a glance.

Nothing was run on the data. The instruction was to file, and these are
properties measured during filing, not results.

---

## U1 -- twenty-six workbooks, zero formulas, three false positives

`Practice-Datasets-for-Excel` is twenty-six `.xlsx` files, and a scan for
`<f>` elements returns three. All three are in `AB_NYC_2019.xlsx` and none
is a formula:

    B33569  = modern, a/c, easy check-in / book instantly ==
    B44059  = travelholic rooms (modern decor / clean) ==
    B45795  == happy travels / near columbia university ===

Airbnb listing titles that begin with `=`. Excel typed them as formulas
at import and stored them as such. The cells read, in full:

    <c r="B33569" s="0" t="e"><f aca="false">= modern, a/c, easy check-in
      / book instantly ==</f><v>#VALUE!</v></c>

`t="e"`, cached value `#VALUE!`. Stated in this order because the first
version of this finding said the cells "carry no `<v>` result", which is
wrong -- they carry one, and it is an error. The right discriminator is
better than the one asserted from plausibility: the cell declares its own
type as error and caches the error text. Checking rather than assuming is
what turned it up, half a minute after writing it.

Two consequences.

**For this corpus:** the true formula count is zero across all twenty-six.
None of these is a calculating workbook. `sheet-structure-scan`'s scan 3
(header collision), scan 4 (stated-relationship maintenance) and
`coupling.py` all need a formula layer and have none here; `WO7` criterion
(c) fails on every file. That is settled without running the screen,
because the property the screen would resolve is already measured.

**For the reader:** a formula count taken as a count of computation is
wrong on this corpus by three, in the direction that manufactures
structure. Same class as `sheet-structure-scan` SSS_048, where `often
times` matched as multiplication and was caught by the operand
requirement rather than by the operator match; same class again as
`UNI_009` and `T1-1`, a token matched by shape rather than by role.

`sheet-structure-scan/sheetmodel.py` does not read the `t` attribute at
all, so a cell of this kind reads as DERIVED there and enters the
precedent graph with an unparseable formula. Recorded as SSS_061 and
declared in that module's WHAT IS NOT READ section; behaviour is not
changed, because none of that folder's own target workbooks is checked
in and whether any of them carries the pattern cannot be re-checked here.
The size of the effect on its published numbers is therefore unknown, not
zero.

## U2 -- the EPA extract is a register, not a calculation

4969 rows, 15 columns, 4968 hyperlinks, one sheet, zero formulas, creator
field empty. Ships values with no provenance prose sheet and no stated
relationship between any two cells.

That is the LGO shape from SSS_043 exactly: a workbook that *collects*
rather than one that *states something about its own numbers*. SSS_043's
conclusion transfers -- a file of this kind is not addressable by scan 4
rather than unsupported by it, and reporting it as evidence about
stated-relationship maintenance would count a workbook that cannot answer
the question as an answer.

Where it differs from LGO, and it is the one thing that makes it worth
keeping: every row carries an external `product_url`. A `fold-matrix`
grid on any product in it has a downward arm that is reachable outside
the file, which the business-plan corpus (FM_024, FM_034) did not.

## U3 -- the only live use in the four: a repeat-measure pair

UCI `mechanical-analysis` gives each component eight attributes, of which
two are:

    5 - mis   - measure  (real)
    6 - misr  - earlier measure (real)

The same quantity, same component, same instrument, twice.

`triad-playground` TP_010 records that this repository's shadow-panel and
consensus statistics have the wrong reference: instrument resolution
bounds what the *instrument* can say, while shadow spread is bounded by
what an *observer* can repeat, so the correct denominator is same-observer
repeat variance -- and TP_003 records the same gap from the other side, as
the missing null. Nothing in this tree has ever had one.

This file carries 209 instances of one, on a real instrument, collected in
1990.

It is not free. Whether `mis` and `misr` are a repeat or a trend depends
on the interval between them, and the `.names` file does not state it --
a `reasoning-gate` G-RES pair with one side missing, which is what
`coupling_audit/provisioning.py` found in bone collagen and what
`nonidentity-census` T2-5 turned into a ratio. Unstated, so unusable until
someone bounds it. Recorded as a candidate, not as an instrument.

## U4 -- the World Bank catalogue is two things and neither is data

160 rows, 26 columns, one row per World Bank *collection*.

**(a) A target list.** `sheet-structure-scan` WO7 S1 asked whether the
population of testable workbooks is small, and could not find out: every
publisher host tried returns a refused CONNECT under this environment's
allowlist (SSS_053), so S1's hypothesis is untested *not because most
workbooks fail the screen but because none could be screened*. This file
does not change the egress fact. What it changes is that the selection
step is no longer the bottleneck -- 160 candidates with their URLs already
in a column, screenable by anyone with reach.

**(b) A clock corpus.** `Periodicity`, `Update Frequency`, `Update
Schedule` and `Last Revision Date` are four fields about one thing,
published side by side, 160 times. `fold-matrix` S5 wants clocks per
level and never collapsed; `claim-record` field 5 derives a shelf life
from a time constant and refuses a stored date. A published set of stated
update intervals against stated last-revision dates is a place where a
stated clock and an observed one can disagree, computable from this file
alone with no egress at all.

(b) is the cheaper of the two and is the one that needs nothing this
environment lacks.

## U5 -- the bytes are not in the repository, and that is a cost

16.6 MB across four files, 16.1 MB of it binary. This tree is text by
construction: `sheet-structure-scan/fixture.py` writes its own `.xlsx`
with `zipfile` at run time specifically so no workbook binary is checked
in. The practice zip would be the largest object in the repository by two
orders of magnitude and carries a third party's MIT terms into a CC0 tree.

The decision is recorded rather than taken silently, because the cost runs
the other way and is real: this container is ephemeral, and when it is
reclaimed the bytes are gone. What survives is the index.

That is why the index carries a sha256 per file and why
`notes/check_uploads.py` exists -- a re-obtained copy is checkable against
the recorded hash, size and shape, and one that differs is reported as
differing rather than assumed to be the same file. It is a weaker
guarantee than holding the bytes and it is not nothing.

The weakest link is the EPA extract: no creator, no source URL in its
metadata, origin inferable only from the `product_url` column. The other
three name their publisher in their own contents.

## U6 -- the checker caught the record before anything else did

`check_uploads.py --check` was run against the uploads while they were
still on disk. On the first run three of four returned PRESENT_MATCH and
the UCI archive returned a shape disagreement: six members recorded,
seven derived. The dropped member was
`older-version/mechanical-analysis.notused-instances` -- the file the index
spends a paragraph on, describing the twelve held-out instances by number.

Read by hand, the entry and the record look consistent, because the prose
discusses the file and the list simply does not contain it. Running the
derivation against the bytes is what separated them.

Worth stating plainly because the same operation one level up is what
`notes/check_d2.py` did on its first run (two of its own recorded paths
were wrong when written, and both were caught by running it, which is D2's
operation applied to the reading of D2). Two checkers, two first runs, two
errors in the checker's own record. Neither was found by reading.

The state that makes this possible is `NOT_PRESENT` being distinct from a
pass. A checker that returned clean on an empty directory would have
returned clean here too, after the container was reclaimed, forever.
