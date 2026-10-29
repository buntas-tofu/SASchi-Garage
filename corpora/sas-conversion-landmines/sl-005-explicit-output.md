# SL-005: An explicit OUTPUT changes row emission for the whole step

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: bounded Go repository/base-R witnesses, recorded at the pinned commit below; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: Program execution model; DS-006 adjacent; DS-040, DS-041, DS-042 composition.
Coverage assessment (2026-10-28): Snapshot values and multiplicity have original repository/base-R witnesses; skipped-OUTPUT suppression and later subsetting rejection have source tests. Multiple destinations remain deferred.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation. The [dated evidence map](../../research/GO_EVIDENCE_20261028.json)
pins Go `9b86f957941a2dca14a90e8504f7913759e7e269`. DS-006 remains adjacent
state context, not a dedicated OUTPUT rule.
[The event gate](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/examples/verify_events.py)
assigns 13, outputs, assigns 29, outputs, then assigns 47. Its two snapshots are
13 and 29, checked against independent R. The composed original program emits
five ordered snapshots from three selected input rows.
[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_events.py)
checks that a skipped conditional OUTPUT suppresses automatic output, that only
selected input rows emit, and that an earlier snapshot survives a later failed
subsetting IF.

The event profile supports one simple DATA destination, with bare OUTPUT or
OUTPUT to that destination. Multiple destinations remain deferred. DATA _NULL_
explicit OUTPUT is refused with PUT _ALL_ or counted/UNTIL/WHILE/OVER loops; scalar
DATA _NULL_ OUTPUT is outside these mapped named-dataset witnesses, not a general
source refusal. The original September 4/9 witness below remains a design, not
the executed 13/29/47 witness. Citation retrieval timed out again on 2026-10-28;
accessibility is unresolved, not proven broken. Its consultation date is retained.

DS-040 [DO OVER](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/DO_OVER.md) and DS-041
[nested counted loops](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/COUNTED_LOOPS.md) add source/R evidence for
snapshot scheduling, skipped-OUTPUT suppression and future schema discovery.
DS-042 [mixed PUT](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/MIXED_PUT.md) writes logical records without emitting
rows or changing OUTPUT suppression. Its original three-snapshot program checks
aliases and missing values independently in R. Logs have exact separate pins;
the public expected-data comparator continues to compare datasets only.

## Earlier snapshot

The [October 27 map](../../research/GO_EVIDENCE_20261027.json) remains unchanged
at Go `dc32d355b1ca27085970ff0e651df8d6b0726bcc`. It records the earlier evidence boundary.

## Failure mechanism

An explicit OUTPUT statement replaces automatic end-of-iteration output. Its position captures the current variable values, and multiple executions can emit multiple rows.

## Witness to build (not executed here)

A single iteration assigns x=4, outputs, assigns x=9, and outputs again. Expect two rows, 4 and 9, with no additional automatic row. A conditionally skipped OUTPUT may yield no row.

## Preservation contract and mitigation (recommendation)

Represent output as an event, not a final dataframe snapshot. Compare destination datasets, emission order, row multiplicity, and values at each output point.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S06: [OUTPUT statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
