# SL-007: Conditional LAG tracks invocation history, not previous rows

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: bounded Go repository/base-R witnesses, recorded at the pinned commit below; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-007.
Coverage assessment (2026-10-27): DS-007 now has bounded direct-assignment source execution, independent per-occurrence queues, conditional and counted DO schedules, numeric depths 1 through 100 and step/run reset evidence. Broader consumers remain deferred.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation. The [dated evidence map](../../research/GO_EVIDENCE_20261027.json)
pins Go `dc32d355b1ca27085970ff0e651df8d6b0726bcc` and DS-007.
[The execution gate](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/examples/verify_lag_execution.py)
compares four pins and 300 constructed runtime cases against an independent R
prior-invocation model, across depths 1 through 100. Existing raw reference queue
fixtures remain separate evidence. Conditional calls on rows two and four return
missing then 20; unconditional calls whose results are used conditionally follow
a different schedule. Ordinary missing arguments still enter the queue.

[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/saschi/test_lag_execution.py)
checks structural occurrence identity, including identical calls, IF/ELSE leaves
and counted-loop trips. Queues persist across input rows/trips, reset per DATA
step and run, survive BY boundaries, and do not advance merely on OUTPUT.
WHERE and subsetting IF retain their timing around invocations.

The profile admits numeric LAG/DIF or LAG1 through LAG100/DIF1 through DIF100 as
direct assignment RHS calls, including bounded IF/ELSE and counted-DO leaves.
Arguments are finite numeric or ordinary missing literals, numeric variables or
_N_. Character/tagged/nonfinite arguments, expressions, nested or arithmetic
consumers, queue calls in predicates/WHERE, arrays, PUT_ALL, C++ and UNTIL/WHILE
queue scheduling remain deferred. Depth limits and atomic refusals are tool
policies, not SAS limits or diagnostic emulation. The September queue remains
DESIGN_ONLY_NOT_RUN; independent review and live-SAS traces remain outstanding.

## Failure mechanism

Each LAG occurrence has a queue. It advances only when that occurrence executes, and a BY boundary does not by itself flush the queue.

## Witness to build (not executed here)

On values 10,20,30,40, invoke one LAG occurrence only on rows two and four. Expected returns at those invocations are missing and 20, rather than 10 and 30 from an unconditional shift.

## Preservation contract and mitigation (recommendation)

Distinguish conditional invocation from conditional use of an unconditional result. Preserve the existing independent-occurrence, missing-argument, LAG2 and group-boundary witnesses. Assigning a missing result at FIRST.key masks that result; it does not flush the queue.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S02: [LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm). Scope: SAS 9.3 function reference. Consulted 2026-09-15.
