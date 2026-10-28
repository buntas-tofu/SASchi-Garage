# SL-005: An explicit OUTPUT changes row emission for the whole step

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: bounded Go repository/base-R witnesses, recorded at the pinned commit below; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: Program execution model; DS-006 adjacent.
Coverage assessment (2026-10-27): Snapshot values and multiplicity have original repository/base-R witnesses; skipped-OUTPUT suppression and later subsetting rejection have source tests. Multiple destinations remain deferred.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation. The [dated evidence map](../../research/GO_EVIDENCE_20261027.json)
pins Go `dc32d355b1ca27085970ff0e651df8d6b0726bcc`. DS-006 remains adjacent
state context, not a dedicated OUTPUT rule.
[The event gate](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/examples/verify_events.py)
assigns 13, outputs, assigns 29, outputs, then assigns 47. Its two snapshots are
13 and 29, checked against independent R. The composed original program emits
five ordered snapshots from three selected input rows.
[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/saschi/test_events.py)
checks that a skipped conditional OUTPUT suppresses automatic output, that only
selected input rows emit, and that an earlier snapshot survives a later failed
subsetting IF.

The event profile supports one simple DATA destination, with bare OUTPUT or
OUTPUT to that destination. Multiple destinations remain deferred. DATA _NULL_
explicit OUTPUT is refused with PUT _ALL_ or counted/UNTIL/WHILE loops; scalar
DATA _NULL_ OUTPUT is outside these mapped named-dataset witnesses, not a general
source refusal. The original September 4/9 witness below remains a design, not
the executed 13/29/47 witness. Citation retrieval timed out on 2026-10-27;
accessibility is unresolved, not proven broken. Its consultation date is retained.

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
