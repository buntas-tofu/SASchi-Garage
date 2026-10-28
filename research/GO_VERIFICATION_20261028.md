# Go verification inventory, October 28, 2026

Status: recorded hosted repository/base-R evidence for principal/maintainer inspection.
This is not a new Go run, live-SAS validation or a SAS-wide capability count.

Pinned Go commit: `9b86f957941a2dca14a90e8504f7913759e7e269`.
[Successful main run](https://github.com/buntas-tofu/SASchi-Go/actions/runs/40718206801).
[Machine-readable inventory](GO_VERIFICATION_20261028.json).

There are 50 fixture runners and 40 suites containing 755 tests, with zero skips.
Class labels below are editorial groupings, labeled inference. IDs and registration
order come from the pinned verify_all.py; suite counts come from the public hosted
receipt. Fixtures include semantic, catalogue and packaging gates. These are
different units, and passing a fixture does not imply whole-language support.

## Fixture gate classes

| Class | Gates |
| --- | --- |
| Numeric and format semantics (9) | `rounding_n`, `rounding_n_R`, `numfmt`, `missarith`, `sigfig`, `mod`, `division`, `int`, `formats` |
| Calendar and intervals (3) | `intck`, `intnx`, `calendar` |
| Data, state and metadata (10) | `bygroup`, `sort`, `merge`, `transpose`, `csvimport`, `data-events`, `typed-metadata`, `lag-dif`, `lag-execution`, `sum-statement` |
| Statistics and matrices (6) | `numstat`, `weights`, `fisher`, `freq`, `laplace`, `matrix` |
| Arrays and control flow (8) | `arrays`, `numeric-arrays`, `do-counted`, `do-if`, `do-until`, `do-while`, `do-over`, `counted-nested` |
| Character and string semantics (6) | `funcs`, `count`, `length-reverse`, `concat-catx`, `substr`, `substr-compositions` |
| PUT output (5) | `put-literal`, `put-character-list`, `put-all`, `put-numeric-list`, `put-mixed-numeric` |
| Bitwise semantics (1) | `bitwise` |
| Catalog and packaging (2) | `capability-manifest`, `wheel-install` |

## Suites

All 40 IDs are listed with their observed test counts.

| Suite | Class | Tests | Source |
| --- | --- | ---: | --- |
| `suite-parser` | Parser, rules and execution infrastructure | 20 | [saschi.test_parser](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_parser.py) |
| `suite-rules` | Parser, rules and execution infrastructure | 28 | [saschi.test_rules](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_rules.py) |
| `suite-emitter` | Parser, rules and execution infrastructure | 19 | [saschi.test_emit_py](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_emit_py.py) |
| `suite-rulebook` | Parser, rules and execution infrastructure | 8 | [saschi.test_rulebook](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_rulebook.py) |
| `suite-plan` | Parser, rules and execution infrastructure | 26 | [saschi.test_plan](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_plan.py) |
| `suite-cpp` | Parser, rules and execution infrastructure | 2 | [saschi.test_cpp](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_cpp.py) |
| `suite-operations` | Parser, rules and execution infrastructure | 12 | [saschi.test_operations](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_operations.py) |
| `suite-comparison` | Parser, rules and execution infrastructure | 5 | [saschi.test_compare](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_compare.py) |
| `suite-events` | Data, state and metadata | 14 | [saschi.test_events](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_events.py) |
| `suite-metadata` | Data, state and metadata | 14 | [saschi.test_metadata](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_metadata.py) |
| `suite-functions` | Functions and application surfaces | 38 | [saschi.test_functions](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_functions.py) |
| `suite-job` | Functions and application surfaces | 11 | [saschi.test_job](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_job.py) |
| `suite-catalog` | Functions and application surfaces | 10 | [saschi.test_catalog](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_catalog.py) |
| `suite-showcase` | Functions and application surfaces | 4 | [saschi.test_showcase](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_showcase.py) |
| `suite-assistant` | Functions and application surfaces | 5 | [saschi.test_assistant](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_assistant.py) |
| `suite-web` | Functions and application surfaces | 10 | [saschi.test_web](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_web.py) |
| `suite-put` | PUT output | 13 | [saschi.test_put](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_put.py) |
| `suite-put-list` | PUT output | 28 | [saschi.test_put_list](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_put_list.py) |
| `suite-put-all` | PUT output | 16 | [saschi.test_put_all](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_put_all.py) |
| `suite-do-counted` | Loops and scheduling | 27 | [saschi.test_do_counted](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_do_counted.py) |
| `suite-put-numeric` | PUT output | 23 | [saschi.test_put_numeric](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_put_numeric.py) |
| `suite-do-put` | Loops and scheduling | 6 | [saschi.test_do_put](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_do_put.py) |
| `suite-length-reverse` | Strings and composition | 23 | [saschi.test_length_reverse](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_length_reverse.py) |
| `suite-concat-catx` | Strings and composition | 21 | [saschi.test_concat_catx](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_concat_catx.py) |
| `suite-string-composition` | Strings and composition | 9 | [saschi.test_string_composition](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_string_composition.py) |
| `suite-substr` | Strings and composition | 16 | [saschi.test_substr](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_substr.py) |
| `suite-substr-compositions` | Strings and composition | 20 | [saschi.test_substr_compositions](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_substr_compositions.py) |
| `suite-do-if` | Loops and scheduling | 23 | [saschi.test_do_if](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_do_if.py) |
| `suite-bitwise` | Numeric, bitwise and calendar | 24 | [saschi.test_bitwise](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_bitwise.py) |
| `suite-lag-execution` | Data, state and metadata | 26 | [saschi.test_lag_execution](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_lag_execution.py) |
| `suite-calendar` | Numeric, bitwise and calendar | 20 | [saschi.test_calendar](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_calendar.py) |
| `suite-sum-statement` | Loops and scheduling | 20 | [saschi.test_sum_statement](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_sum_statement.py) |
| `suite-do-until` | Loops and scheduling | 20 | [saschi.test_do_until](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_do_until.py) |
| `suite-division` | Numeric, bitwise and calendar | 16 | [saschi.test_division](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_division.py) |
| `suite-int` | Numeric, bitwise and calendar | 14 | [saschi.test_int](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_int.py) |
| `suite-do-while` | Loops and scheduling | 20 | [saschi.test_do_while](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_do_while.py) |
| `suite-numeric-arrays` | Numeric arrays | 42 | [saschi.test_numeric_arrays](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_numeric_arrays.py) |
| `suite-do-over` | Loops and scheduling | 33 | [saschi.test_do_over](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_do_over.py) |
| `suite-counted-nested` | Loops and scheduling | 39 | [saschi.test_counted_nested](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_counted_nested.py) |
| `suite-put-mixed-numeric` | PUT output | 30 | [saschi.test_put_mixed_numeric](https://github.com/buntas-tofu/SASchi-Go/blob/9b86f957941a2dca14a90e8504f7913759e7e269/saschi/test_put_mixed_numeric.py) |

## Separate checks

The same full run also passes 60 faithful synthesis cases and catches 60 naive
variants. Both 1k workloads add 39 checks. Eleven complete external-program proofs
are reported by the source suites; they are not 11 additional suites. Governance
lint and manifest CI checks are separate from the 50 fixture runners.

The JSON pins every runner/module file and the registry with SHA-256, and records
the public artifact and receipt digests. The Garage snapshot resolver checks those
paths and registration order without executing Go or SAS.
