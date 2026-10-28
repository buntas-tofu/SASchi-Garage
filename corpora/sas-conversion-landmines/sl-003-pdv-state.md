# SL-003: DATA step variables do not all reset in the same way

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: bounded Go repository/base-R witnesses, recorded at the pinned commit below; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-006; DS-040/DS-041 reset composition; program execution model.
Coverage assessment (2026-10-28): Conditional initial SET, retained inputs and scratch reset have bounded source-execution evidence. General conditional SET and arbitrary whole-step composition remain unproven.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation. The [dated evidence map](../../research/GO_EVIDENCE_20261028.json)
pins Go `9b86f957941a2dca14a90e8504f7913759e7e269` and DS-006 context.
[The event gate](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/examples/verify_events.py)
compares an original composed program and fixed output to independent base R.
[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_events.py)
checks a first-row lookup before driving SET, retained input writes, driving-input
overwrites, empty inputs and scratch values of 17, missing, missing. Numeric
RETAIN state also survives a later subsetting-IF rejection.

The lookup profile reads one row once with `IF _N_=1 THEN SET lookup;` before
the driving SET. It does not admit general conditional SET, multiple lookup reads,
SET concatenation/options or uninitialized RETAIN lists. This is SET evidence,
not a proof of MERGE-input write behavior. The September witness below remains a
historical design; related Go execution does not relabel its queue entry.

DS-040 [DO OVER](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/DO_OVER.md) adds current-element aliases and scratch
row/run reset. DS-041 [counted loops](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/COUNTED_LOOPS.md) separately checks
per-row work state, input index descriptors and run isolation. These composition
witnesses do not broaden the conditional SET contract described above.

## Earlier snapshot

The [October 27 map](../../research/GO_EVIDENCE_20261027.json) remains unchanged
at Go `dc32d355b1ca27085970ff0e651df8d6b0726bcc`. It records the earlier evidence boundary.

## Failure mechanism

Variables read by SET/MERGE have retention behavior different from ordinary assignment-created variables. RETAIN adds another state lifetime. A row-wise rewrite can erase or accidentally extend that state.

## Witness to build (not executed here)

Use a one-row lookup read only when _N_=1, then process three observations from a second input. The lookup value should remain available on later iterations; a scratch assignment without retention needs a separate expectation.

## Preservation contract and mitigation (recommendation)

Model variable origin, initialization, step boundaries, and reset points. Validate conditional SET separately from a dataframe join or a global dictionary.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S05: [RETAIN statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000214163.htm). Scope: SAS 9.2 statement reference. Consulted 2026-09-15.
