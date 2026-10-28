# JSON Schema Generator Report

Inputs:

- object model `.work/draft-ietf-rpp-data-objects.yaml` (export with `unique_identifier`, `owner`, `supported_processes`, `direct_access`, `visibility`, structured subsection `tables`, structured operation `input`/`output` items (one `Reference` per Input, no per-item `elements`), `common_data_types`, element `restrictions` including the status `client_values`/`server_only_values` partition, object `conditions`, the status object flags `at_least_one_status_by_server` and `status_not_required_for_client_request`, and the object attribute `abstract`)
- draft `src/draft-ietf-rpp-json.md` (branch `feature/generate-schemas`, commit `29ee5a8`)
- source text `.work/draft-ietf-rpp-data-objects.clean.txt`, checked where the YAML is silent

Generator: `.scripts/gen_json_schema.py`.

```
.scripts/.venv/bin/python .scripts/gen_json_schema.py .work/draft-ietf-rpp-data-objects.yaml \
    -o schema.json --split schemas/ --diagnostics diag.md \
    --compare src/draft-ietf-rpp-json.md --compare-out compare.md
```

`--replace src/draft-ietf-rpp-json.md [--replace-out FILE]` puts the generated schemas into the draft's schema blocks (see `.scripts/CLAUDE.md`). Against the current draft it replaces 92 of 94 blocks, and the result is byte-identical to the draft: every replaced block already holds the generated schema. It leaves 2 untouched: `identifier` and `Card` (placeholders). Every generated schema has a place in the draft.

The generator produces 94 `$defs`. The bundle passes 2020-12 meta-schema validation, and every `$ref` in it resolves. `--compare` reports differences only for `identifier` (the draft's `pattern` and `maxLength`) and `Card` (placeholder); it also notes `allOf` in the transfer process `create`/`read` views, which is the generated `if`/`then` list, not inheritance. The consistency checker passes on the draft (one warning: no example for `disclose`).

Generation precedence: **the draft's written rules, then the YAML content, then the shape of the draft's existing schemas**.
- `$defs` keys follow Rule 27 of the draft, with YAML identifiers used as-is: `<id>.read` for components, plus `<id>.create` when they have a `create-only` or `read-write` element, and `<id>.create`, `<id>.read`, `<id>.update`, `<id>.reference` and `<id>.query` for resources.
- Process objects get `<id>.create`, `<id>.read` and `<id>.reference`, plus one view per other operation that has input data elements, keyed by the operation Identifier (`transferProcess.transferReject`, `restoreProcess.update`). Derived objects use their own identifier.
- An operation's response is the `read` view. An operation whose output differs from it (`Output Data Elements`, or an Output `Object` with other elements than the read view) also gets `<id>.<view>.output` with the selected elements and the output data elements as response content. The current YAML has no such operation, so no `.output` view is generated (see Y15).
- `--compare` pairs draft keys with Rule 27 keys case-insensitively and flags each mismatch (`KEY MISMATCH`). Against the current draft, 0 of 94 draft keys differ.
- Reference views use the exported `unique_identifier`; objects without one (Discovery) get no reference view. Aggregations of Data Objects and Process Objects reference the `<id>.reference` view (Rule 8); compositions embed the full view.
- The elements of each view come from the operations' exported Input/Output items: the create Input `Object` and the read Output `Object` that name the object itself. Their mutabilities follow the data-objects rules, since the export no longer lists `elements` per item: an Output `Object` carries all mutabilities, an Input `Object` carries read-write only when both it and the Input's single `Reference` are `This Object` (Update), else create-only and read-write (Create, process create operations). A second `Reference` in one Input is reported as a yaml-issue; the current YAML has none. Update views hold the read-write elements (Rules 5–7); `Changes` items are not used. Operation views carry the `Input Data Elements` definitions.
- Create views carry `processes` only when the Create Input names a Process Object (`Object: Domain Create Process Object`). Only `domainName` qualifies.
- Elements with `visibility: onDemand` are not required in read views. `direct_access` does not change the representation.
- Component Objects (Rule 27): request content (create, update and operation views) embeds the component's `create` view, response content its `read` view. A component without writable elements embedded in request content falls back to `read` with a yaml-gap diagnostic: `contact.disclose` (`disclose` has no elements yet) and `message.data` (the message objects have only read-only elements).
- Status objects (M26): the `create` view of a status Component Object holds only the client values (Set By `client` or `client, server`) in its `label` enum. In Data Objects, the status element is left out of create and update views when the status object has no client values, is optional there (no `required`, no `minItems`) when `status_not_required_for_client_request` is set, and is required in read views when `at_least_one_status_by_server` is set. `organisationRole.create` embeds `organisationRoleStatus.create`.
- Prose constraints are **not** turned into keywords. Besides cardinality, mutability and data type, only the exported structured `restrictions` (→ `enum`, `minimum`/`maximum`, `pattern`, `minLength`/`maxLength`, `propertyNames`) and `conditions` (→ `if`/`then`) are used.
- Common Data Types are built from `common_data_types`: `base_type` plus `restrictions`, under the draft's keys (`identifier`, `clientIdentifier`, `phoneNumber`).
- A bare object name as a data type is treated as `Composition[Type]` (data-objects §8.2).
- Inheritance is flattened. Polymorphism is applied: a reference to a base object is a `oneOf` over the base object and all its descendants, each fixed by its `@type` (M8). Objects exported with `abstract: true` (`baseProcess`, `baseMessage`) are left out of the `oneOf`. Their own `read` views are still generated, because the draft has a schema block for each, but nothing references them.
- Output is compact like the draft's schema blocks (flat objects and arrays on one line); `--expanded` gives one value per line.

---

## 1. Rules missing from the draft

Without these rules, the schemas can't be reproduced the way the draft writes them. Each item names the choice the generator made. The draft's schemas now follow every generator choice, so the "Where the draft schemas show it" column names where the gap matters, not a deviation.

| # | Status | Gap | Where the draft schemas show it | Generator choice |
|---|--------|-----|-------------------------------|------------------|
| M1 | resolved | **No naming rule for `$defs`.** The draft named definitions after `<x>Object`, not after the `@type` identifier, gave components bare names and object-specific processes an owner suffix. Resolved: Rule 27 (JSON Schema Composition Rules) now forms keys from the Identifier plus the view name, covers Process Objects, `reference`/`query` views, operation Identifiers, `.output` views and derived objects, and exempts Common Data Types and external types. | all schemas | Rule 27: `<identifier>.<view>`; draft keys for Common Data Types |
| M2 | resolved | **No rule for what each schema view contains.** (resolved: Rule 27 names the views and their content, including `query` as an array of `read` views; the Mutability Rules derive the mutabilities of request and response content from operation Input and Output.) | `*.create`, `*.update`, `message.query` | create and read: the mutabilities the operations' Input/Output `Object` items carry; update: the read-write elements (Rules 5–7) |
| M3 | open (partly) | **No rule for which element is the "primary identifier".** Rule 27 now defines the `reference` view with the Unique Identifier of data-objects, but Rules 8–10 and 13 still say "primary identifier", and the TODO comment under *Labelled associations* remains. | `*.reference` | the exported `unique_identifier` (Y1 fixed) |
| M4 | open | **References contradict each other.** Rule 13 says a referenced object is represented as a JSON **string** (its identifier). Rules 8–10, Rule 27 (`reference` view) and every schema in the draft use an **object** with `@type` and the identifier. | `registrant`, `contacts`, `nameservers` | object reference (`<id>.reference`) |
| M5 | resolved | **The bare `Type` notation was not mentioned.** Resolved: the *Composition* section now introduces the bare `Type` notation ("A `Type` represents a parent-child relationship …"). | `status`, `authInfo`, `provMetadata` | composition: the component is embedded |
| M6 | open | **Aggregation with cardinality `1` or `0-1` is not covered.** Rule 8 only covers `0+` and `1+`. | `registrant`, `parent`, `user.organisation`, `baseProfile` | a single `$ref`, no array |
| M7 | resolved | **No rule for aggregating Process Objects.** Resolved: Rule 27 gives Process Objects a `reference` view, so Rule 8 applies to them; the Processes Object now references `<id>.reference`, and the messages' bare-type `process` embeds the full `read` view as a composition. | `processes`, all `*Message.process` | Rule 8: `Aggregation[...]` → `<id>.reference`; bare-type `process` → `*.read` |
| M8 | open | **No rule for polymorphism.** Data-objects §2.5 allows any descendant to be used in place of a base object, but the JSON Representation Rules don't say whether a schema that references a base object also accepts its descendants, or how. The draft uses `oneOf` over the non-abstract base and its descendants, discriminated by the `@type` const, in `processes.transferProcess`/`.createProcess`, every message's `process` and `message.data`; the `message` prose states the `data` polymorphism as a non-expressible constraint. **Suggestion:** add a rule under *Inheritance* that states whether a base-object reference accepts descendants and, if so, how the schema expresses it. It should also say how that combines with the shared Processes Object (M24): a `domainTransferProcess` would otherwise be accepted in `contact.read.processes`. | `processes`, all `*Message.process`, `message.*.data` | `oneOf` over the base object and all its descendants, without abstract objects (`abstract: true`) |
| M9 | resolved | **The `@type` of derived objects was ambiguous in practice.** Resolved: Rule 27 states that an extending object uses its own Identifier, and the domain transfer schemas now have `"const": "domainTransferProcess"`. | `domainTransferProcess.*` | own identifier (`domainTransferProcess`) |
| M10 | open | **No rule for `readOnly` on `@type`.** The draft sets it in read views only, and leaves it out of create, update, operation and reference views. | all | read views only (components included). It is left out of reference views, because those are sent in requests (Rule 5). |
| M11 | open | **No annotation rule for `create-only` elements outside request schemas.** Rule 6 covers requests only. The draft marks them `readOnly` in read views. Rule 6 now defines object creation for Component Objects as the creation of the component instance, and components have `read`/`create` views, so the same annotations apply to them. | `domainName.read.name` | `readOnly` in read views, `writeOnly` in create views (components included) |
| M12 | open | **The primitive mapping table is incomplete.** <br>• It lacks `Object`, `Fully Qualified Domain Name` and `Dictionary[Type]` (data-objects §2.1.9–2.1.11). <br>• It gives the JSON type, not the JSON Schema keywords. `Integer` maps to `number`, but every schema uses `"integer"`. The `format` values (`date-time`, `date`, `uri`, `hostname`) and the Binary encoding are never stated. | `dnsRecord.rdata`, `dnsControls`, `domainName.name`/`host.hostName` | `integer`; `format` from the notes column; FQDN → `hostname`; Object → `unevaluatedProperties: true` (composable; see C4); Dictionary → object with `additionalProperties` |
| M13 | open | **No rule mapping Common Data Types to `$ref`.** Rule 27 requires `$ref` for component and data objects only. The draft now uses `{ "$ref": "#/$defs/identifier" }` everywhere, but no rule requires it. | `id` of contact, organisation, user, message | always `$ref` |
| M14 | open | **Dictionary associations have no cardinality rule.** Rules 10 and 12 don't say how `1+` is expressed. The draft uses `minProperties: 1` in all `organisation` views, following the generator. | `roles` | `minProperties: 1` |
| M15 | open | **Cardinalities of the form `X-Y`** (data-objects §2.4, for example `1-2`) are not covered by Rules 1–4. | `restoreReport.statements` | array with `minItems`/`maxItems` |
| M16 | open | **Labelled aggregation of a primitive is not covered**: `links: LabelledAggregation[String]`. Rule 9 assumes a referenced object. | `discovery.read.links` | `{label, object: string}` |
| M17 | open (partly) | **External types have no schema-level rule.** Rule 15 says to embed the native JSON. Rule 27 now lets external types use a key not derived from an Identifier (the draft uses `Card`), but nothing says how the `External:<Profile>:<Type>` notation maps to that key, or where the profile's constraints live. | `Card` | `$ref` `#/$defs/<Type>`, with a placeholder definition |
| M18 | resolved | **Required elements in update schemas.** Resolved: the draft's update views now list their cardinality-`1`/`1+` read-write elements as Rule 23 requires (`contact.update`, `host.update`, `organisation.update`), and partial updates have their own schema under *Update Rules > Schema*. | all `*.update` | Rule 23 applied |
| M19 | open | **Process data in create requests.** No rule says which create-process type to use when an object-specific one exists (`domainCreateProcess`), or that `processes` is left out when the Data Object supports no Create Process. The Rule 18 example still embeds a `createProcess` with a `period` (see D12). | `domainName.create.processes` | the Process Objects in the Create Input (`Object: <Process Object>`), each under the matching Processes Object element; no `processes` in create views otherwise; no `maxItems` |
| M20 | open | **Operation parameters** (`hostsFilter`, message query `type`): the draft doesn't say whether they have any JSON representation. They are presumably URL parameters. | — | left out (the `Parameters` items of the operation Input) |
| M21 | open | **Rule 22 needs enumerations that the model supplies only as prose.** No rule covers other constraint keywords either (`minimum`/`maximum`, `pattern`, `minLength`/`maxLength`, `propertyNames`). | `period`, `dnsControls`, `clientIdentifier`, `phoneNumber` | Rule 22 `enum` from `allowed_values`; the other restrictions mapped to the matching keyword (`range` → `minimum`/`maximum`, `key_pattern` → `propertyNames`, `value_range` → `additionalProperties` bounds) |
| M22 | open | **No rule for `Visibility: onDemand`** (data-objects §2.4). An element returned only on request cannot be required in a read schema. | `domainName.authInfo`, `contact.authInfo`, `restoreProcess.restoreReport` | never required in read views (all are `0-1` today, so no visible effect) |
| M23 | open | **No rule for `Direct Access`** (sub-resource addressing). It is a protocol concern, but the draft doesn't say that the inline JSON representation is unaffected. | `processes.*`, `*.processes`, `organisation.users` | ignored |
| M24 | open | **The Processes Object is shared by all Data Objects.** No rule restricts it to the processes a Data Object supports (`supported_processes` plus owned processes). For example, `contact.read.processes` accepts `renewProcess`, `restoreProcess` and `createProcess`. | `processes` | one shared `processes` component; reported as a diagnostic |
| M25 | open | **No rule for cross-element conditions** (data-objects prose such as "`gainingClientId` is required for push transfers"). The draft now uses the generated `if`/`then` pairs, but no rule defines them. | `transferProcess.*`, `domainTransferProcess.*` | `if`/`then` per exported condition (`allOf` when more than one), in every view that holds all elements the condition names |
| M26 | resolved | **No rule for status objects in requests.** Rule 22 gives one `enum` per status object, and Rules 1, 4 and 23 make `status` (`1+`, read-write) required in create and update requests. Data-objects, however, lets a client set only the values whose *Set By* column contains `client`, lets the server always assign at least one value (`ok`, `active`), and lets a client omit the status when creating or updating the object. No rule says which values a request schema accepts, whether `status` is required in requests, or what happens when a status object has no client-settable value. | all `*.create`/`*.update` with `status`. Resolved: the draft now has Rules 28–31 (*Status Objects* under JSON Schema Composition Rules; Rule 27 gives every Component Object a `read` view and, when it has a writable element, a `create` view used in all request content), which follow the generator choice. | `<id>.create` with the client values in requests; `status` optional in requests when the client may omit it; left out of requests when no value is client-settable; required in read views when the server always assigns one |

### Rule conflicts

| # | Status | Conflict | Generator choice |
|---|--------|----------|------------------|
| C1 | open | **Rule 18 vs Rule 5.** Process data must be sent in the `processes` element of create requests, but `processes` is read-only, and read-only properties must not appear in requests. | Rule 18: a dedicated `processes` object in create views (only `domainName.create`, see M19) |
| C2 | open | **Rule 8 vs Rule 24.** Rule 8 says aggregation schemas MUST allow extra elements of the referenced object. Rule 24 injects `unevaluatedProperties: false` before validation, so a reference schema with only `@type` and the identifier then rejects those extra elements. | not resolved; reported |
| C3 | open | **Rule 26 vs the create/update schemas.** Rule 26 forbids `authInfo` in JSON request bodies "when an operation requires authorization information", yet `domainName.create`, `domainName.update`, `contact.create` and `contact.update` carry `authInfo` to *set* it. The scope of Rule 26 needs to be stated. | `authInfo` kept (it is read-write in the YAML) |
| C4 | open | **Rule 24's open-object keyword vs its own enrichment.** Rule 24 names `"additionalProperties": true` for the Object type, but the enrichment it requires works with `unevaluatedProperties`. `additionalProperties` sees only `properties`/`patternProperties` in the same schema object, so it doesn't compose through `$ref`/`allOf`. Rule 24 also doesn't say that the injected `"unevaluatedProperties": false` must not replace an existing `"unevaluatedProperties": true`. | `"unevaluatedProperties": true` for Object; the consistency checker already skips nodes that carry `unevaluatedProperties` or `additionalProperties` |

---

## 2. Draft schemas that don't match the draft's own rules

| # | Status | Rule | Violation |
|---|--------|------|-----------|
| D1 | resolved | Inheritance (flat schemas, no `allOf`) | (resolved: all schemas are flat; the remaining `allOf` lists in the transfer process views hold the M25 `if`/`then` conditions.) `transferProcess.create.domain`, `transferProcess.read.domain` and `organisationObject.read` used `allOf` over a base schema. |
| D2 | resolved | Rule 25 (`@type` const = own identifier) | (resolved: the domain transfer schemas use `domainTransferProcess`, and the messages' `process` references full `read` views with a `const`.) Domain transfer schemas validated `"@type": "transferProcess"`, and every message's inline `process` object had `@type` without a `const`. |
| D3 | open (partly) | Rule 24 (no `additionalProperties`/`unevaluatedProperties: false`) | (resolved: the contact schemas no longer set `"unevaluatedProperties": false`.) Still open: `dnsRecord.rdata` uses `"unevaluatedProperties": true`, where the rule names `"additionalProperties": true` for the Object type (see C4). |
| D4 | resolved | Rule 5 (`read-only` ⇒ `readOnly`) | (resolved: `provMetadata`, `profile.read.baseProfile` and `user.read.organisation` are `readOnly`.) |
| D5 | resolved | Rule 5 (no read-only properties in requests) | (resolved: `contact.update` has no `processes`, `user.create` has no `organisation`, `organisation.update.status` uses `organisationStatus.create`.) |
| D6 | resolved | Rule 6 (`create-only` ⇒ `writeOnly` in requests) | (resolved: all create views mark their create-only elements `writeOnly`.) |
| D7 | resolved | Rule 23 (required = cardinality `1`/`1+`) | (resolved: `transferProcess.read` no longer requires `transferDir`; `restoreReport.statements` is now `1-2` in the YAML, so requiring it is correct; update views list their cardinality-1 read-write elements; `user.read` requires `id`; `domainName.read` and `host.read` require `status`.) |
| D8 | resolved | Rule 4 (`1+` ⇒ `minItems: 1`) | (resolved: `status` in read views carries `minItems: 1`, request views drop it per M26; `roles` has `minProperties: 1` in every `organisation` view.) |
| D9 | resolved | Rule 20 (one schema per component) | (resolved: the draft has `disclose.read`, `baseProcess.read`, the `domainCreateProcess` views, `host.update`, the per-type status objects and the Component Object `create` views.) |
| D10 | resolved | `$defs` uniqueness | (resolved: the reject request is now `domainTransferProcess.transferReject`; the response aliases `transferProcess.delete/approve/reject.domain` were removed, since Rule 27 makes those responses the `read` view.) `transferProcess.reject.domain` was defined twice, once for the reject request and once for the reject response (Domain Name → Transfer). The combined schema keeps only the second definition. |
| D11 | open (partly) | Prose vs schema | The `message.create` caption says the representation also carries `id`, `creationDate` and `status`, but the schema holds only `@type` and `data`. (resolved: `user.*.description` no longer has `"const": "user"`.) |
| D12 | open | Rules-chapter snippets vs schemas | The illustrative snippets in *JSON Representation Rules* are not validated and have drifted from the schemas: <br>• The Rule 18 example embeds a `createProcess` with a `period`, but `createProcess` has no `period` and `domainName.create.processes.createProcess` accepts only `domainCreateProcess.create`. <br>• The Rule 27 example `domainCreateProcess.create` has no `writeOnly` on `period` (Rule 6); its `period.create` lacks the `minimum`/`maximum` of the real schema. |

---

## 3. Where the YAML is not enough to build schemas like the draft's

The "In source?" column says whether the information is in `draft-ietf-rpp-data-objects.clean.txt` but missing from the export.

| # | Status | Missing information | In source? | Effect |
|---|--------|---------------------|-----------|--------|
| Y1 | fixed | **`Unique Identifier`** object attribute | Yes | Now exported as `unique_identifier`; the reference views use it and the heuristic was removed. |
| Y2 | fixed | **Owner Data Object** of object-specific processes | Yes | Now exported as `owner`; the identifier-prefix heuristic was removed. Together with `supported_processes` it decides the create `processes` type (M19). |
| Y3 | fixed | **`Direct Access`** and **`Visibility`** element attributes | Yes | Now exported as `direct_access` and `visibility`; see M22 and M23. The generator also checks that a Direct Access element with cardinality above 1 targets an object with a Unique Identifier. |
| Y4 | fixed | **Status value tables** | Yes | Now exported as structured `subsections[].tables` (columns `Status Value`, `Set By`, `Description`). The status labels' `allowed_values` are resolved from them, so every status `label` gets a Rule 22 `enum`. |
| Y5 | fixed (partly) | **Enumerations, ranges and patterns** (`period` 1–99, `y`/`m`; `trStatus`, `transferDir`, `restoreStatus`, message `status`, organisation-role and user status values; `dnsControls` key syntax) | Yes, but only as prose constraints | Now exported as `restrictions` and generated. The `restoreReport.statements` count is now exported as cardinality `1-2`. Still prose only: `discoveryVersion.version` (Semantic Versioning). |
| Y6 | fixed (partly) | **Conditional requirements**: `gainingClientId` is required for `push` transfers | Prose only | Now exported as `conditions` and generated as `if`/`then` (M25). Still prose only: the `restoreProcess` presence rules (`reportDueDate` only when `restoreStatus` is `pendingRestore`), which need a "value is not" condition the export cannot express. |
| Y7 | fixed (partly) | **Common Data Types** (Identifier, Client Identifier, Phone Number syntax) | Yes (§7), as prose | Now exported as `common_data_types`; Client Identifier and Phone Number carry `base_type` and `restrictions`. Identifier has neither (its syntax is a reference to RFC 5730 §2.8), so only `{"type": "string"}` (Rule 21) is generated. |
| Y8 | open | **External type** `RPP-JSContact-Profile:Card` | No (external profile) | Placeholder object. The draft's `Card` schema has to come from the profile. |
| Y9 | open | **`Object` type structure** (`dnsRecord.rdata`, RDATA structures subsection) | Prose only | Open object. |
| Y10 | open | **Disclose Object** has no data elements | No (source says `Description: TBD`) | Only an empty `disclose` schema can be generated. |
| Y11 | fixed | **Operation input and output** | Yes | Now exported as structured `input`/`output` items (Uniform interface defaults filled in). The generator takes the view elements, the create `processes` Process Objects, the query cardinality, the Input Data Elements and the Parameters from them. |
| Y12 | resolved | **Maintenance Message Object** | **No** (missing from the YAML and from the source) | (resolved: the draft no longer defines `maintenanceMessage`.) The draft's `message.data` had an extra `oneOf` branch for it. |
| Y13 | fixed | **`userStatus.label` allowed values** | Yes (User Status Values table, `{#tbl-user-status-values}`) | `allowed_values` was not resolved from the exported table, so `userStatus.label` had no Rule 22 `enum`. Now exported; the generated `enum` holds `active`, `pending`, `suspended` and `deactivated`. |
| Y14 | fixed | **Who sets each status value, and whether the status is required in requests** | Yes (*Set By* column of the status values tables; status values prose) | Now exported as the `client_values`/`server_only_values` restrictions of each status `label` and the object flags `at_least_one_status_by_server` and `status_not_required_for_client_request`. The generator builds the status `<id>.create` definitions and the request/read requirements from them (M26). |
| Y15 | open | **Output Data Elements** of an operation (for example a `reason` in the Transfer Reject output) | No (data-objects §2.7.2 allows data elements in Input only) | The generator already reads an `Output Data Elements` item (same shape as `Input Data Elements`) and builds `<id>.<view>.output` from it. The data-objects notation and the export have to add the kind first. |

### YAML data-quality issues found while generating

- (fixed) Trailing periods in data types (`contact.id`, `contact.disclose`).
- (fixed) `domainName.authInfo` and `contact.authInfo` used `Authorisation Information Object`, but the object was named `Authorisation Information`; it is now `Authorisation Information Object`.
- (fixed) `contact.disclose` used `Disclose Object`, but the object was named `Disclose`; it is now `Disclose Object`.
- (fixed) `user.organisationId` used the `<Object> Reference` notation; it is now `user.organisation` with `Aggregation[Organisation Data Object]`.
- (fixed) `domainName.registrant`, `organisation.parent` and `profile.baseProfile` used the bare type (Composition); they are now `Aggregation[...]`, so the generator emits `*.reference` like the draft.
- (fixed) `domainTransferProcess` redefined the inherited `processId`, which data-objects §2.5 forbids; it now defines only `expiryDate` and `transferPeriod`.
- (fixed) The Output of every operation (and the Uniform interface default) listed `Elements: read-write, read-only`, so create-only elements (`domainName.name`, `contact.id`, `transferProcess.transferDir`, …) were never returned. The Output now lists `create-only, read-write, read-only`, and the generator's override was removed.
- `organisationRoleStatus` has no `at_least_one_status_by_server`/`status_not_required_for_client_request` flags, although the other five status objects have both. It is embedded only in `organisationRole` (`0+`), where Rules 29–31 don't apply, so the generated schemas don't change.
- (fixed) `contact.contactInfo` had cardinality `1-2`, which was not in the data-objects cardinality notation. It is now `1`, and data-objects §2.4 now defines the `X-Y` notation (used by `restoreReport.statements`).
- The `user` element constraints are again given as `'-'` rather than `[]` (`details`, `description`, `organisation`); this was fixed in an earlier export and has regressed.

---

## 4. Where the YAML and the draft disagree on content (for information)

The generator follows the YAML. The draft's schemas now match the generated ones, so `--compare` shows only:

- **Common Data Type syntax**: the draft's `identifier` has a `pattern` and `maxLength` 89 with no YAML counterpart (Y7).
- **`Card`**: the draft's JSContact `Card` schema has no YAML counterpart (Y8).

Resolved since earlier versions of this report (the draft took the generated schemas):
- (resolved) **`status`**: create, update and read schemas (M26).
- (resolved) **`user`**: `details` as a JSContact `Card`, `status` as a single `userStatus`, `id`, and `organisation` (read-only, in `read` only).
- (resolved) **`organisationRole.status`**: `organisationRoleStatus` objects.
- (resolved) **`contactInfo`**: a single `Card` in both.
- (resolved) **Process elements**: `createProcess` has no `period` (it is in `domainCreateProcess`); `restoreProcess.create`/`.update` carry `restoreReport`.
- (resolved) **Create `processes`**: only `domainName.create` has a `processes` property.
- (resolved) **Client Identifier, Phone Number and `dnsControls` key patterns**: the draft uses the YAML's.
- (resolved) **Enumerations**: `transferRequestMessage.status` (`pending`) and `transferDir` are present.
- (resolved) **Abstract base objects**: the `oneOf` lists no longer include `baseProcess.read` or `baseMessage.read`, and the `message` prose no longer allows a bare Base Message Object.
- (resolved) **`processId`** is in every process read view.

The draft's `# Examples` pass the consistency checker against the draft's (now generated) schemas, so the example breaks listed in earlier versions of this report (status shape, derived-process `@type`, `contactInfo`, user `status`, limited message `process` objects) are fixed.
