# MongoDB export transformation example

A small, streaming Python utility for a **specific NDJSON migration mapping**. It processes
one JSON document per line using Python's standard `json` module. It is not an AI agent or a
general-purpose MongoDB migration engine.

## What the current mapping does

- Keeps only records whose `ecm:primaryType` is `Policy`, `Billing` or `Payments`; other records
  are omitted. Do not use it unchanged for a repository with other document types.
- Recursively renames key substrings `af:` to `true:` and `af_` to `true_` (values are not renamed).
- Optionally replaces `ecm:parentId` and `ecm:ancestorIds` for each supported type, including
  nested matching keys.
- Adds the `Migration` facet when absent and a `migration:migrationDate` extended-JSON date.
- Writes one transformed record per line. Memory use depends on the largest individual record;
  it does not load the whole export, use ijson/ujson or batch output writes.

## Requirements

Python 3.10 or later. No third-party packages are required. Run commands from this repository.

## Example with synthetic fixtures

```bash
python3 src/json_processor.py tests/data/test_input.ndjson /tmp/transformed-example.ndjson \
  --policy-parent example-policy-parent --policy-ancestors example-root \
  --billing-parent example-billing-parent --billing-ancestors example-root \
  --payments-parent example-payments-parent --payments-ancestors example-root
```

Each parent/ancestor argument is optional. If omitted, the corresponding identifiers are
preserved. Ancestors are supplied as a comma-separated string. The command adds the current UTC
migration timestamp. For a deterministic test, the Python function accepts an explicit date.

The output must be a new path, distinct from the input. The tool refuses an existing output
rather than overwriting it. Choose a directory that already exists.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests use synthetic records and cover mapping behavior, type filtering, omitted replacements
and protection against input/output collision. They do not benchmark large exports.

## Adaptation and limits

Review `VALID_TYPES`, `replace_prefix` and `build_replacements` before adopting this mapping.
There is no configurable mapping file, database connection, checkpoint/resume facility,
transactional rollback or automatic validation of the destination. Malformed JSON stops the
run and may leave a partial output; review or remove that output before rerunning with a new
path. Compare retained/skipped counts and sample metadata with your expected mapping before
importing anything. A prefix collision can overwrite a key; confirm the input schema first.

No throughput or time-saving guarantee is implied. See
[security](SECURITY.md) and the [MIT license](LICENSE).
