# Agents.md — `.scripts/` tooling

Python tooling for the draft `src/draft-ietf-rpp-json.md`. Edit files in this
folder only when the user explicitly asks (see the root `Agents.md`).

## Environment

- `.scripts/.venv` is a git-ignored Python venv with the packages in
  `.scripts/requirements.txt`. `generate_schemas.sh` creates it when missing.
- Run every script with `.scripts/.venv/bin/python` from the repository root.

## JSON consistency checker — `check_json_consistency.py`

Checks the JSON Schema definitions and worked examples in the draft against each
other. It is the authoritative check that the schemas are valid and the examples
conform to them.

- Run: `.scripts/.venv/bin/python .scripts/check_json_consistency.py [-q] [--model YAML] [--no-deep-type-check] src/draft-ietf-rpp-json.md`
- Always pass the draft path. The built-in default still points to the old file
  name `src/draft-wullink-rpp-json.md`, which no longer exists.
- `-q` suppresses OK and info lines but always shows the `>>` location markers.
- `--model YAML` (default `.work/draft-ietf-rpp-data-objects.yaml`) names the
  data-objects export. Objects marked `abstract: true` in it need no example.
- Spec: `.scripts/check_json_consistency_spec.md`.
- Exits with 1 on errors and 0 when clean. Run it after any edit that touches a
  JSON Schema definition or an example.

The checker treats the three chapters that contain JSON differently:
1. `# JSON Representation Rules`: partial snippets, **not** validated (skipped).
2. `# JSON Schema Definitions`: each block is validated as a JSON Schema and must
   have exactly one `$defs` entry. The `@type` rule is enforced per subchapter:
   forbidden under *Common Data Types Schemas*, required with a `const` everywhere
   else. Polymorphic definitions (`core.<base>`, `any.<base>`; draft Rules
   27.1–27.2) are exempt only if they have exactly the required shape, and every
   `$dynamicRef` must resolve to an `any.<base>` anchor (Rule 27.3). See the spec.
3. `# Examples`: each full example is validated against its matching schema(s).

It also checks two sections outside these chapters. Blocks in `Update Rules > Schema`
and `Extension Framework > Effective Schema` are standalone JSON Schema documents:
validated as JSON Schema, with every `$ref` and `rpp:extends` entry resolving locally
or into `https://rpp.example/rpp/schema.json` (the combined `$defs`). Blocks in
`Update Rules > Schema > Examples` are examples; untyped ones (partial update
requests) are validated against the `Update Rules > Schema` schema. JSON blocks
inside HTML comments and in `Update Rules > Partial > Matching` are ignored.

## JSON Schema generator — `gen_json_schema.py`

Builds JSON Schema 2020-12 definitions from the object model export of
draft-ietf-rpp-data-objects (`.work/draft-ietf-rpp-data-objects.yaml`). It applies
the JSON Representation Rules of the draft. Its main use is to find gaps and
inconsistencies between the rules, the draft's schemas and the data model.

```
.scripts/.venv/bin/python .scripts/gen_json_schema.py MODEL.yaml [-o OUT.json] [--split DIR] \
    [--compare src/draft-ietf-rpp-json.md] [--compare-out FILE] \
    [--replace src/draft-ietf-rpp-json.md] [--replace-out FILE] [--diagnostics FILE] [--partial] [--expanded] [-q]
```

- **`-o OUT.json`** writes the bundled schema, with every definition under one
  `$defs`. Default: stdout.
- **`--split DIR`** writes one file per definition, shaped like the schema blocks in
  the draft. Components and common types get `{"$defs": …}`; processes and
  resources also get `$schema` and `$ref`.
- **`--compare DRAFT`** matches each definition under `# JSON Schema Definitions` in
  the draft to a generated one and lists the differences. Matching is
  case-insensitive and tolerates the draft's naming styles (`<x>Object`, owner
  suffixes, operation names without the process stem); every draft key that differs
  from the Rule 27 key is flagged `KEY MISMATCH`, with a count at the top. Further
  differences: properties, `required`, and per-property type, `$ref`, `readOnly`,
  `writeOnly`, `format` and the restriction keywords; value types such as Common
  Data Types are compared on their own keywords. Differences that come from prose constraints are tagged
  `[prose constraint]`. It also reports duplicate `$defs` names in the draft.
- **`--replace DRAFT`** rewrites, in place, every schema block under
  `# JSON Schema Definitions` that has a generated counterpart (same matching as
  `--compare`). The block gets the `--split` shape under the Rule 27 key, so keys
  such as `domainObject.create` become `domainName.create`. It leaves a block
  untouched when it has no counterpart, has more than one `$defs` entry, maps to a
  counterpart already placed by an earlier block, or maps to a placeholder (an
  external type, a Common Data Type without exported syntax). It prints a report
  to stdout: the replaced blocks, the untouched ones with the reason, and every
  generated schema that has no place in the draft, in full. With `--replace-out
  FILE` the draft is left unchanged and the result goes to FILE. A second run on
  the result changes nothing. Running it on the live draft is a draft edit: follow
  the root `Agents.md` Edit Workflow (approval first), and run the consistency
  checker afterwards. Replaced schemas can reference definitions that the draft
  does not have (for example `baseProcess`), and the examples still follow the
  draft's old schemas.
- **`--diagnostics FILE`** writes generator diagnostics grouped by category:
  `rule-gap`, `rule-conflict`, `yaml-gap`, `yaml-issue` and `heuristic`. They are
  also printed to stderr unless `-q` is given.
- **`--partial`** also generates `<id>.update.partial` after every `<id>.update`:
  the *Update Rules > Schema* shape narrowed to the object, with one `oneOf`
  alternative per top-level path and operation (path as `const`, `value` tied to
  the property, element or dictionary-entry schema; see the report, M27). With
  `--compare`, the comparison ends with a validation of the partial update
  examples in *Update Rules > Schema > Examples* against `<@type>.update.partial`,
  where `@type` comes from the example document that precedes them. Without
  `--partial` the output is unchanged.
- **Output style:** compact by default, like the draft. An object or array that
  contains no object, and fits within 100 characters, is written on one line.
  `--expanded` writes one value per line instead.
- **Self-check:** the generated bundle is validated against the 2020-12 meta-schema,
  every `$ref` must resolve, and every `$dynamicRef` must have a matching
  `$dynamicAnchor`. The exit code is 1 if either check fails.

### Generation decisions (agreed with the user)

- **Precedence:** the draft's written rules, then the YAML content, then the shape
  of the draft's existing schemas.
- **Scope:** every component, process and resource in the YAML.
- **Naming:** `$defs` keys follow Rule 27 of PR #104, as updated by the M1 suggestion.
  Identifiers from the YAML are used as-is, with no case conversion.
  - Components: `<id>.read`, plus `<id>.create` when they have a `create-only` or
    `read-write` element. Request content embeds `create`, response content `read`.
  - Resources: `<id>.create`, `.read`, `.update`, `.reference`, and `.query` when
    the object has a query operation.
  - Processes: `<id>.create`, `<id>.read` and `<id>.reference`, plus `<id>.update` and one view per
    other operation that has input data elements, keyed by the operation
    Identifier (for example `transferProcess.transferReject`).
  - Operation outputs: the response of an operation is the `read` view, unless
    the operation's output has `Output Data Elements` or its Output `Object`
    selects other mutabilities than the read view. Then it gets
    `<id>.<view>.output` (for example `transferProcess.transferReject.output`),
    holding the selected elements plus the output data elements as response
    content. This applies to processes and resources, but not to Read and Query.
  - Derived objects use their own identifier (`domainTransferProcess.create`).
  - Common Data Types have no Identifier; the draft's keys are kept.
- **Inheritance** is flattened, with no `allOf`.
- **Polymorphism** follows the draft's *Polymorphism* section (Rules 27.1–27.3). A
  data element whose data type is an extensible base object (one that another
  object extends) gets `"$dynamicRef": "#any.<base>"`, where `<base>` is the
  key the base object resolves to in that view. A single-schema base whose
  descendants have per-operation views takes their suffix (`baseProcess.read`).
  For each `<base>` the bundle gets `core.<base>` (`anyOf` over the base and all
  its descendants, in the same view) and `any.<base>`. Objects exported with
  `abstract: true` are never candidates. `--compare` compares the
  `core.<base>` member lists, which is the completeness check the consistency
  checker cannot do.
- **View contents** come from the operations' `input`/`output` items. The export
  no longer lists the mutabilities of an `Object` item; they follow from the
  data-objects rules: an Output `Object` carries all mutabilities; an Input
  `Object` carries read-write only when both it and the Input's (single)
  `Reference` are `This Object` (an existing object being modified, i.e. Update),
  else create-only and read-write (an object being created). Update views hold the read-write
  elements (Rules 5–7); `Changes` items are ignored. `Input Data Elements`
  go into operation views, `Output Data Elements` (read-only) into `.output` views; `Parameters` are left out. A Process Object in the
  create Input becomes the create `processes` property.
- **Bare-type data elements** (`Type` with no association) are compositions, as in
  data-objects §8.2: "Composition[Type] or Type".
- **Status objects:** in the `create` view of a status Component Object (its `label`
  restrictions carry `client_values`/`server_only_values`) the `label` enum holds
  only `client_values`. In the create and update views of a Data Object
  the status element is left out when there are no client values, and is optional
  (no `required`, no `minItems`) when `status_not_required_for_client_request` is
  set. In read views it is required when `at_least_one_status_by_server` is set.
- **Prose constraints** are not turned into keywords. Only the structured
  attributes are used: cardinality, mutability, data type, `restrictions`
  (`allowed_values` → `enum` per Rule 22; `range`, `pattern`, `min_length`,
  `max_length`, `key_pattern`, `value_range` → the matching keyword) and object
  `conditions` (→ `if`/`then`, in views holding every element they name).
- **Common Data Types** are built from `common_data_types` (`base_type` plus
  `restrictions`); without a `base_type` they are plain strings (Rule 21 for
  Identifier).
- **Placeholders** are generated for external types, because the YAML doesn't
  define them.

The YAML export format is documented in the header comment of the YAML file
itself. Read it before changing how the generator parses the model.

## Standing rule — keep the generator report current

`.scripts/gen_json_schema_report.md` records:
- rules missing from the draft (M*) and rule conflicts (C*),
- draft schemas that break the draft's own rules (D*),
- gaps in the YAML export (Y*) and YAML data-quality issues,
- content differences between the YAML and the draft.

Keep it in sync. It must always describe the current tool, the current YAML export
and the current draft.

1. **After every change to `gen_json_schema.py`**, update the report wherever the
   change affects it: the generator choices in the M*/C* tables, the summary at the
   top (number of `$defs`, the naming scheme), and the run command.
2. **When the YAML export changes** (a new `.work/draft-ietf-rpp-data-objects.yaml`,
   or a change to its format, such as newly exported attributes like
   `Unique Identifier`, owner, `Direct Access` or `Visibility`):
   - rerun the generator with `--compare` and `--diagnostics`;
   - mark every Y* entry and data-quality issue that has been fixed as resolved
     (see 4);
   - add any new gaps or issues;
   - when a fix makes a heuristic unnecessary, also update the generator to use the
     exported data instead.
3. **When the draft changes in a way that affects the rules or the schemas**, rerun
   `--compare` and update the M*, C* and D* entries and the §4 content differences
   to match.
4. Keep the existing item IDs stable, so references to them still work. Mark a
   resolved item `(resolved)` with a short note rather than renumbering the table.
   Update the commit and branch named in the report's *Inputs* list.
5. Put generated artifacts (bundle, split files, comparison output) in the session
   scratchpad, not in the repository, unless the user asks otherwise.
