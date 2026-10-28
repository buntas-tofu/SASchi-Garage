# SASchi-Garage

The SAS migration field guide: semantics, landmines, and evidence.

Status: candidate engineering reference, not an agency finding or proof of
cross-language equivalence. The examples and proposed tests have not been newly
executed against SAS as part of this collection.

Go and Roku are the cars. Garage holds the workshop notes.

## Start here

| Collection | Cards | What it covers |
|---|---:|---|
| [Macro landmines](corpora/macro-landmines/README.md) | 12 | Timing, scope, quoting, rescanning, and generated code |
| [LLM migration quirks](corpora/llm-migration-quirks/README.md) | 12 | Invented APIs, incomplete conversions, evidence mistakes, and evaluation design |
| [SAS conversion landmines](corpora/sas-conversion-landmines/README.md) | 25 | Row counts, DATA step state, metadata, statistics, and engine contracts |

Read the [SAS research synthesis](research/SAS_REBUILD_RESEARCH_20260915.md),
[LLM evidence review](research/LLM_MIGRATION_QUIRKS_20260915.md), or
[25 proposed validation cases](research/SAS_FIXTURE_QUEUE_20260915.csv).
The [research source register](research/SOURCES_20260915.json) records 43 sources;
the macro collection has its own [source register](corpora/macro-landmines/SOURCES.md).

The [October 27 Go evidence map](research/GO_EVIDENCE_20261027.json) connects
SL-003, SL-004, SL-005, SL-007 and SL-022 to exact public gate/source links at
Go commit `dc32d355b1ca27085970ff0e651df8d6b0726bcc`, with content hashes,
rule IDs, covered behavior and remaining gaps. Status: bounded repository/base-R
evidence for principal/maintainer review, not live-SAS validation or collection
promotion. Recorded acceptance is not a new full verification run. DO OVER was
deferred at that snapshot; newer Go work is outside this map.

This focused coverage refresh is not a full source re-review or a finding that
the underlying September research is obsolete. The dated research queue remains
`DESIGN_ONLY_NOT_RUN`, and the import manifest remains a historical record.

## The family

- [SASchi-Go](https://github.com/buntas-tofu/SASchi-Go) owns the translator,
  executable semantic rules, fixtures, and verification receipts.
- [SASchi-Roku](https://github.com/buntas-tofu/SASchi-Roku) preserves the community
  SAS program corpus and its upstream provenance.
- **SASchi-Garage** owns the authored teaching cards, research, citations, and
  proposed tests. AWS packaging and deployment remain in a separate consumer.

A research card can describe a known behavior before Go supports it. A citation
is not an execution receipt. Stable IDs (ML-001, LQ-001, SL-001) connect research
to implementation without duplicating either repository's source of truth.

## Consume and check

`collections.json` lists all 49 cards, their source references, and evidence
metadata without coupling them to a retrieval provider. Use the explicit lists;
do not recursively ingest the repository. Research and proposed test answers
are not held-out evaluation material.

```sh
python3 tools/check_catalog.py
```

The validator uses Python 3.11+ and the standard library. It checks inventory,
IDs, evidence metadata, local links, and import records. It does not execute SAS
or certify the factual accuracy of a cited claim.

It also validates evidence-map references, pinned URLs, dates, evidence levels
and catalog/card consistency without a network or sibling checkout. To resolve
every mapped Go path, content hash, rule ID and named source test against the
immutable Git snapshot, use a read-only local Go repository:

```sh
python3 tools/check_catalog.py --go-repository ../saschi-go
python3 -m unittest discover -s tools -p 'test_check_catalog.py'
```

These checks validate the evidence map, not Go execution. Negative controls
exercise invalid references and prevent historical designs or collection status
from being promoted through the map.

[Garage CI](.github/workflows/catalog.yml) runs the catalog checker, all validator
tests and artifact-style checks on pushes and pull requests, using Python 3.11
and the standard library. Its actions are pinned to commits. CI checks Garage
without fetching a sibling repository or running Go or SAS. A passing result
does not promote the collections or establish semantic equivalence.

Run the same checks locally:

```sh
python3 tools/check_catalog.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_artifact_style.py
```

The style checker covers tracked Markdown, JSON, CSV/TSV, Python, YAML, text,
TOML, shell and Git/editor configuration files. Stage new artifacts before
checking; ignored and untracked working records are outside its scope. It rejects
em dashes, Unicode ellipses and three-dot ellipses with file and line diagnostics.

Pin a full Git commit when building a retrieval corpus. Keep each card whole and
preserve its status and references. All current cards are asserted/unreviewed.
Promotion requires independent review and appropriately scoped runtime evidence.

## Contributing and provenance

Add a named mechanism, a scoped source, an observable failure, and a proposed
witness. Distinguish documented contracts, local observations, and inference.
Keep raw internal records, credentials, deployment configuration, and held-out
answers outside this repository.

[PROVENANCE.md](PROVENANCE.md) explains the initial extraction and
[IMPORT_MANIFEST.json](IMPORT_MANIFEST.json) records the original file hashes.
[NOTICE.md](NOTICE.md) states the current rights boundary.
