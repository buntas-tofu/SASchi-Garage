# SL-022: A SAS array can alias variables rather than copy their values

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Coverage update: DS-016 reference context plus bounded DS-039 Go repository/base-R source witnesses; no live-SAS validation or card promotion.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-016 (reference context), DS-039 (bounded numeric source execution).
Coverage assessment (2026-10-27): DS-039 executes numeric alias reads/writes, overlapping arrays, SUM OF, descriptors, scratch reset and OUTPUT composition. DS-016 helper evidence remains distinct; DO OVER is deferred at the pinned snapshot.

## Pinned implementation evidence

Status: repository/base-R evidence for principal/maintainer review, not live-SAS
validation or a new complete external-program proof. The
[dated evidence map](../../research/GO_EVIDENCE_20261027.json) pins Go
`dc32d355b1ca27085970ff0e651df8d6b0726bcc`.
[DS-016 reference fixtures](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/examples/verify_arrays.py)
retain helper-level aliases, custom bounds, DIM/LBOUND/HBOUND and temporary
retention context. They do not establish source execution of those broader forms.
[The DS-039 gate](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/examples/verify_numeric_arrays.py)
adds original source alias/snapshot pins, 19 helper pins, 1600 constructive R
cases and 26 shared refusals.
[The source suite](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/saschi/test_numeric_arrays.py)
checks both alias directions, overlapping bindings, metadata, scratch row/run
reset, schema discovery, OUTPUT timing and atomic failures.

The [numeric profile](https://github.com/buntas-tofu/SASchi-Go/blob/dc32d355b1ca27085970ff0e651df8d6b0726bcc/docs/NUMERIC_ARRAYS.md)
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
ordering guards apply. DO OVER was deferred here and is handled separately in
Go; newer work is not included. The September design below remains unrun, and
independent review and live-SAS comparisons remain outstanding.

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
