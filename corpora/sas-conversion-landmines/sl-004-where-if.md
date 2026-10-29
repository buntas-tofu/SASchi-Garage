# SL-004: Moving a filter can change FIRST./LAST. and group results

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: bounded Go repository/base-R witnesses, recorded at the pinned commit below; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-005, DS-006.
Coverage assessment (2026-10-28): WHERE/IF timing has an executed repository/base-R FIRST discriminator; source tests also pin LAST and multi-key flag propagation. Broader engine and predicate behavior remains outside this evidence.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation. The [dated evidence map](../../research/GO_EVIDENCE_20261028.json)
pins Go `9b86f957941a2dca14a90e8504f7913759e7e269` and DS-005/DS-006 context.
[The event gate](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/examples/verify_events.py)
uses groups 7,7,9 and keep values 0,1,1. FIRST.g is 1,1 after WHERE, versus 0,1
after subsetting IF. The independent R discriminator checks that difference.
[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_events.py)
also checks _N_ timing, LAST.g on selected groups, and FIRST./LAST. propagation
when an earlier key changes in a multi-key BY list.

WHERE reads driving-input columns before flags form; assignments do not change
its input selection. Subsetting IF runs in source order after the read and flags.
The profile requires ascending input sorted after WHERE and bounded predicates;
WHERE on automatic or newly created variables refuses. These witnesses do not
cover every BY option or SAS engine. The September queue design remains unrun.

## Earlier snapshot

The [October 27 map](../../research/GO_EVIDENCE_20261027.json) remains unchanged
at Go `dc32d355b1ca27085970ff0e651df8d6b0726bcc`. It records the earlier evidence boundary.

## Failure mechanism

WHERE filters input before BY groups are established; a subsetting IF acts later. Equivalent-looking predicates therefore need not preserve group-boundary logic.

## Witness to build (not executed here)

For one group with rows keep=0 then keep=1, compare WHERE keep=1 followed by FIRST.key with subsetting IF keep=1 followed by FIRST.key. Only the WHERE version makes the surviving row the first row of its filtered group.

## Preservation contract and mitigation (recommendation)

Preserve the sequence of input selection, group formation, state changes, and output. Do not push a filter upstream merely as an optimization.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S03: [WHERE statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1xbr9r0s9veq0n137iftzxq4g7e.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
