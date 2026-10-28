# SL-022: A SAS array can alias variables rather than copy their values

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: DS-016 reference context plus DS-039/DS-040 arrays and DS-041/DS-042 composition witnesses; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-016 (reference context), DS-039/DS-040 (bounded numeric arrays), DS-041/DS-042 (loop/output composition).
Coverage assessment (2026-10-28): DS-039 executes numeric alias reads/writes, overlapping arrays, SUM OF, descriptors, scratch reset and OUTPUT composition. DS-016 helper evidence remains distinct; DO OVER and nested counted/mixed PUT compositions now have separately scoped full-program evidence.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation. The
[dated evidence map](../../research/GO_EVIDENCE_20261028.json) pins Go
`9b86f957941a2dca14a90e8504f7913759e7e269`.
[DS-016 reference fixtures](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/examples/verify_arrays.py)
retain helper-level aliases, custom bounds, DIM/LBOUND/HBOUND and temporary
retention context. They do not establish source execution of those broader forms.
[The DS-039 gate](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/examples/verify_numeric_arrays.py)
adds original source alias/snapshot pins, 19 helper pins, 1600 constructive R
cases and 26 shared refusals.
[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_numeric_arrays.py)
checks both alias directions, overlapping bindings, metadata, scratch row/run
reset, schema discovery, OUTPUT timing and atomic failures.

The [numeric profile](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/NUMERIC_ARRAYS.md)
admits one-dimensional numeric arrays with fixed/custom bounds or inferred
extents with names. Explicit, unpadded ascending numbered and generated names are
supported. At most 1024 declared element references per step include overlaps.
Bounds, stored values and new arithmetic/ordered SUM OF partial results stay
within signed 2147483647; values are finite binary64 or ordinary missing and new
plus/minus arithmetic must be exactly representable. SUM OF ignores ordinary
missing and returns missing when all elements are missing. Declarations are
unconditional and precede references; scratch members reset per input row.

Element references accept braces/brackets; declaration bounds also accept
parentheses. Parenthetical element references, character/multidimensional arrays,
temporary/initializer-retained storage, PDV-order lists, macro extents and
DIM/LBOUND/HBOUND source calls remain deferred. So do direct calls/division in
new array expressions, array WHERE/PUT_ALL/C++/MERGE execution and members used
as RETAIN/sum-statement/BY/loop-index state. Existing declaration/initial-lookup
ordering guards apply. The September design below remains unrun, and
independent review and live-SAS comparisons remain outstanding.

[DS-040](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/DO_OVER.md) adds single-level implicit numeric DO OVER.
Current-element reads/writes alias actual row cells in declaration order;
overlapping arrays share storage, and the internal position is not an output
column. The entire unchanged loops_foreach.sas has source/result/stdout pins and
independent base-R evidence. Explicit arrays as OVER controls, named/shared
implicit indices, nesting and mixed indexed/current references remain deferred.

[DS-041](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/COUNTED_LOOPS.md) adds captured computed controls and at most
eight counted levels, with a 10000 aggregate-iteration budget per DATA row.
[DS-042](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/docs/MIXED_PUT.md) adds quoted literals with ordinary numeric scalar
fields, preserving spaces within 64 logical columns. Direct array/current-element
PUT, fractions, formats and physical SAS log fidelity remain outside that scope.
Together they prove the entire unchanged 100_doors.sas, including all 100 final
R-simulated door states and an independent perfect-square hand check. The source
stays in Roku; neither whole program is copied into Garage.

## Earlier snapshot

The [October 27 map](../../research/GO_EVIDENCE_20261027.json) remains unchanged
at Go `dc32d355b1ca27085970ff0e651df8d6b0726bcc`. It records the earlier evidence boundary.

## Failure mechanism

A SAS ARRAY groups variables for indexed access; its name is not a separate ordinary dataset variable. Initialization and temporary arrays also affect retention.

## Witness to build (not executed here)

Declare an array over x and y, assign through the second element, and inspect y. Then assign y directly and inspect that array element; a copied Python list will not reproduce both directions automatically.

## Preservation contract and mitigation (recommendation)

Preserve aliasing, bounds, variable order, and initialization lifetime. Resolve special variable lists against the correct compile-time schema.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S22: [ARRAY statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p08do6szetrxe2n136ush727sbuo.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
