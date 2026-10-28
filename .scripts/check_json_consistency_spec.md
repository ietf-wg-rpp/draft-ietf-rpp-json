# check_json_consistency.py — Specification Notes

## Purpose
Checks `src/draft-wullink-rpp-json.md` for consistency between JSON examples and JSON schemas.

## Source file
`src/draft-wullink-rpp-json.md` — a Mmark/IETF Internet-Draft in Markdown.

## Three named top-level chapters (by `# Heading` level)

| Chapter title                  | Content type                                              |
|-------------------------------|-----------------------------------------------------------|
| `JSON Representation Rules`   | JSON snippets (invalid/partial JSON) — listed, not validated |
| `JSON Schema Definitions`     | JSON Schema definitions — validated                       |
| `Examples`                    | Full JSON object examples — validated                     |

Two further sections are checked outside these chapters:

| Section (chapter path)                          | Content type                                  |
|------------------------------------------------|-----------------------------------------------|
| `Update Rules > Schema`                         | Standalone JSON Schema documents — validated (Section 3) |
| `Update Rules > Schema > Examples`              | Examples — validated (Section 4)              |
| `Extension Framework > Effective Schema`        | Standalone JSON Schema documents — validated (Section 3) |

Section paths are matched without trailing mmark anchors (`Schema {#partial-schema}` matches `Schema`).
The lists are `STANDALONE_SCHEMA_SECTIONS` and `EXTRA_EXAMPLE_SECTIONS` in the script.

Any ` ```json ` block outside these chapters and sections is flagged as "other" (warning).
` ```json ` blocks inside HTML comments (`<!-- ... -->`) are ignored, and so are blocks in
`Update Rules > Partial > Matching` and its subsections (`IGNORED_SECTIONS`); the summary counts the latter.

---

## Section 2 — JSON Schema Definitions

### Sub-chapter classification

Each schema block belongs to a level-2 sub-chapter of `JSON Schema Definitions`.
The sub-chapter determines what `@type` rules apply:

| Sub-chapter                   | `@type` rule | Example coverage required      |
|------------------------------|--------------|-------------------------------|
| `Common Data Types Schemas`  | **forbidden** — error if present | none (no `@type`, no example check) |
| `Component Objects Schemas`  | **required** — error if missing  | nested (at any depth in any example) |
| `Process Object Schemas`     | **required** — error if missing  | top-level example required     |
| `Domain Name Data Object`    | **required** — error if missing  | top-level example required     |
| `Contact Data Object`        | **required** — error if missing  | top-level example required     |
| `Host Data Object`           | **required** — error if missing  | top-level example required     |
| `Organisation Data Object`   | **required** — error if missing  | top-level example required     |
| `Discovery Data Object`      | **required** — error if missing  | top-level example required     |
| `Profile Data Object`        | **required** — error if missing  | top-level example required     |

### Rules checked per schema block
- Must be valid JSON
- Must contain `$defs` with **exactly one** named definition
- `@type` rule per sub-chapter (see table above):
  - `forbidden`: `@type` property MUST NOT appear in the definition — **error** if present
  - `required`: `@type` property MUST appear with `"type": "string"` and a `"const"` value — **error** if missing or malformed
    - Deep check (default, disable with `--no-deep-type-check`): if `@type` is not in top-level `properties`, the script traverses `allOf`/`anyOf`/`oneOf` and follows `$ref` pointers to locate it:
      - `allOf`: at least one branch must define/constrain `@type`
      - `anyOf`/`oneOf`: **all** branches must define/constrain `@type`
      - `$ref`: followed into the combined `$defs` (cycle-safe)
      - `items`: for an array schema, the `@type` of the item schema
- All `$ref: #/$defs/<name>` pointers are checked against the combined `$defs` map — **error** if unresolved
- Schema must be a valid JSON Schema (draft 2020-12) — `check_schema()` is called
- Cross-references are resolved by merging all schemas into one combined `$defs` map

---

## Section 3 — Standalone JSON Schemas

Blocks in the standalone schema sections are complete JSON Schema documents (they may have several `$defs` entries, a root `$ref`, an `$id` and the `rpp:extends` metadata property). They are **not** merged into the combined `$defs`, and the one-`$defs` and `@type` rules of Section 2 do not apply.

### Rules checked per standalone schema block
- Must be valid JSON — **error** if not
- Must be a valid JSON Schema (draft 2020-12) — **error** if not
- Every `$ref`, and every key and value of `rpp:extends`, must resolve — **error** if not:
  - a local reference (`#/...`, or the block's own `$id`) resolves as a JSON Pointer within the block
  - a reference into `https://rpp.example/rpp/schema.json` (`BASE_SCHEMA_ID`) resolves within the combined `$defs` of Section 2
  - any other URI is unresolved

---

## Section 4 — Examples

Examples come from the `Examples` chapter and from `Update Rules > Schema > Examples`.

### Rules checked per example block
- Must be valid JSON
- An example in `Update Rules > Schema > Examples` without a top-level `"@type"` (e.g. a partial update request, which is a JSON array) is validated against the standalone schemas of `Update Rules > Schema`, as written (no `unevaluatedProperties` injection) — **error** if it validates against none, or if no usable standalone schema exists. Its nested `"@type"` values count towards Section 5 coverage.
- Must have a top-level `"@type"` property — **error** if missing
- Must have at least one matching schema (matched by `@type` value == schema's `@type` const) — **error** if none found
- Schemas with unresolved `$ref`s are skipped for validation (already flagged in section 2); if all matching schemas are skipped, validation is marked as not possible
- Must validate against at least one matching schema — **error** if all fail; **warning** if some fail but at least one passes

---

## Section 5 — Typed schemas without examples

For each schema with a `@type` const, example coverage is checked according to the sub-chapter rule (see table above):

- **Top-level required** (Process Objects, Data Objects): the `@type` value must appear as the top-level `"@type"` of at least one example — **error** if missing
- **Nested sufficient** (Component Objects): the `@type` value must appear at any depth in any example — **warning** if missing
- **Abstract types**: objects marked `abstract: true` in the data-objects YAML export (`--model`, default `.work/draft-ietf-rpp-data-objects.yaml`) only occur through their descendants and are exempt from example coverage. Without the file, no type is exempt.

---

## Running the script
```bash
# From project root, using the bundled venv:
.scripts/.venv/bin/python .scripts/check_json_consistency.py

# Quiet mode — suppress OK/info lines; >> location markers always shown:
.scripts/.venv/bin/python .scripts/check_json_consistency.py -q

# Disable deep @type traversal via allOf/anyOf/oneOf/$ref:
.scripts/.venv/bin/python .scripts/check_json_consistency.py --no-deep-type-check

# Custom file path:
.scripts/.venv/bin/python .scripts/check_json_consistency.py path/to/file.md
```

## Dependencies
- Python 3.10+
- `jsonschema` 4.x (installed in `.scripts/.venv`)

## Exit codes
- `0` — no errors (warnings may still be present)
- `1` — one or more errors found
