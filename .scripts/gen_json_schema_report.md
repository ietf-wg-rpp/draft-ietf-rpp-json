# JSON Schema Generator Report

Inputs:

- object model `.work/draft-ietf-rpp-data-objects.yaml` (export with `unique_identifier`, `owner`, `supported_processes`, `direct_access`, `visibility`, structured subsection `tables`, structured operation `input`/`output` items, `common_data_types`, element `restrictions` including the status `client_values`/`server_only_values` partition, object `conditions`, and the status object flags `at_least_one_status_by_server` and `status_not_required_for_client_request`)
- draft `src/draft-ietf-rpp-json.md` (branch `feature/generate-schemas`, commit `60a7526`)
- source text `.work/draft-ietf-rpp-data-objects.clean.txt`, checked where the YAML is silent

Generator: `.scripts/gen_json_schema.py`.

```
.scripts/.venv/bin/python .scripts/gen_json_schema.py .work/draft-ietf-rpp-data-objects.yaml \
    -o schema.json --split schemas/ --diagnostics diag.md \
    --compare src/draft-ietf-rpp-json.md --compare-out compare.md
```

`--replace src/draft-ietf-rpp-json.md [--replace-out FILE]` puts the generated schemas into the draft's schema blocks (see `.scripts/CLAUDE.md`). Against the current draft it replaces 83 of 91 blocks. It leaves 8 untouched: `identifier` and `Card` (placeholders), `restoreProcess.report`, `transferProcess.delete.domain` and `transferProcess.approve.domain` (no counterpart), and three `$ref` aliases or duplicates whose counterpart is already placed. 1 generated schema has no place in the draft: `restoreProcess.update`.

The generator produces 86 `$defs`. The bundle passes 2020-12 meta-schema validation, and every `$ref` in it resolves.

Generation precedence: **the draft's written rules, then the YAML content, then the shape of the draft's existing schemas**.
- `$defs` keys follow Rule 27 of PR #104 as updated by the M1 suggestion (review comment r4363681640), with YAML identifiers used as-is: `<id>` for components, and `<id>.create`, `<id>.read`, `<id>.update`, `<id>.reference` and `<id>.query` for resources.
- Process objects get `<id>.create`, `<id>.read` and `<id>.reference`, plus one view per other operation that has input data elements, keyed by the operation Identifier (`transferProcess.transferReject`, `restoreProcess.report`). Derived objects use their own identifier.
- `--compare` pairs draft keys with Rule 27 keys case-insensitively and flags each mismatch (`KEY MISMATCH`). Against PR #104, 32 of 69 draft keys differ (none by case only).
- Reference views use the exported `unique_identifier`; objects without one (Discovery) get no reference view. Aggregations of Data Objects and Process Objects reference the `<id>.reference` view (Rule 8); compositions embed the full view.
- The elements of each view come from the operations' exported Input/Output items: the `Elements` mutabilities of the create Input `Object` and the read Output `Object` that name the object itself. Update views hold the read-write elements (Rules 5–7); `Changes` items are not used. Operation views carry the `Input Data Elements` definitions.
- Create views carry `processes` only when the Create Input names a Process Object (`Object: Domain Create Process Object`). Only `domainName` qualifies.
- Elements with `visibility: onDemand` are not required in read views. `direct_access` does not change the representation.
- Status objects (M26): a status Component Object embedded in a Data Object gets a second definition `<id>.request` whose `label` enum holds only the client values (Set By `client` or `client, server`). Create and update views embed `<id>.request`, read views embed `<id>`. The status element is left out of create and update views when the status object has no client values, is optional there (no `required`, no `minItems`) when `status_not_required_for_client_request` is set, and is required in read views when `at_least_one_status_by_server` is set. `organisationRoleStatus` is embedded only in the single-schema `organisationRole` component, so it gets no `.request` definition.
- Prose constraints are **not** turned into keywords. Besides cardinality, mutability and data type, only the exported structured `restrictions` (→ `enum`, `minimum`/`maximum`, `pattern`, `minLength`/`maxLength`, `propertyNames`) and `conditions` (→ `if`/`then`) are used.
- Common Data Types are built from `common_data_types`: `base_type` plus `restrictions`, under the draft's keys (`identifier`, `clientIdentifier`, `phoneNumber`).
- A bare object name as a data type is treated as `Composition[Type]` (data-objects §8.2).
- Inheritance is flattened. Polymorphism is applied: a reference to a base object is a `oneOf` over the base object and all its descendants, each fixed by its `@type` (M8).
- Output is compact like the draft's schema blocks (flat objects and arrays on one line); `--expanded` gives one value per line.

---

## 1. Rules missing from the draft

Without these rules, the schemas can't be reproduced the way the draft writes them. Each item names the choice the generator made.

| # | Status | Gap | Where the draft schemas show it | Generator choice |
|---|--------|-----|-------------------------------|------------------|
| M1 | open | **No naming rule for `$defs`.** The draft names definitions after `<x>Object`, not after the `@type` identifier (`domainObject.*` for `domainName`, `contactObject.*` for `contact`). Components get bare names. Object-specific processes get an owner suffix (`transferProcess.create.domain`). PR #104 adds Rule 27 (keys from the Identifier plus the operation name); the M1 suggestion on PR #104 updates Rule 27 to cover Process Objects, `reference`/`query` views, operation Identifiers as-is and derived objects. Common Data Types have no Identifier, so Rule 27 doesn't name them. | all resource and process schemas | Rule 27: `<identifier>[.<view>]`; draft keys for Common Data Types |
| M2 | open | **No rule for which schema views exist and what each one contains.** Rules 5–7 suggest the views but never state that a create view holds create-only and read-write elements, an update view holds read-write elements, a read view holds everything, and a reference view holds `@type` and the identifier. There is also no rule for what operation-specific views (`transferProcess.transferReject`) contain, or for query responses (`messageObject.query` is an array of read views). | the `### Create/Read/Update/Reference` subsections | create and read: the `Elements` of the operations' Input/Output items; update: the read-write elements (Rules 5–7) |
| M3 | open | **No rule for which element is the "primary identifier".** The TODO comment under *Labelled associations* says so. The data-objects draft has an explicit `Unique Identifier` attribute, but this draft never refers to it. | `*.reference` | the exported `unique_identifier` (Y1 fixed) |
| M4 | open | **References contradict each other.** Rule 13 says a referenced object is represented as a JSON **string** (its identifier). Rules 8–10 and every schema in the draft use an **object** with `@type` and the identifier. | `registrant`, `contacts`, `nameservers` | object reference (`<id>.reference`) |
| M5 | open | **The bare `Type` notation is not mentioned.** In data-objects §8.2 a data type given as a bare object name means `Composition[Type]` (`Notation: Composition[Type] or Type`). The Association Rules here only show the bracketed form. The YAML now uses it only for Component Objects (for example `status: Domain Name Status Object`, `authInfo`, `provMetadata`); `registrant`, `parent` and `baseProfile` are now `Aggregation[...]`. | `status`, `authInfo`, `provMetadata` | composition: the component is embedded |
| M6 | open | **Aggregation with cardinality `1` or `0-1` is not covered.** Rule 8 only covers `0+` and `1+`. | message `process`, `registrant`, `parent`, `organisationId`, `baseProfile` | a single `$ref`, no array |
| M7 | open | **No rule for aggregating Process Objects.** The Processes Object embeds the full `*.read` view, while messages embed an inline limited object `{ "@type", "processId" }` whose `@type` has no `const`. | `processes`, all `*Message` | Rule 8: `Aggregation[...]` → `<id>.reference` (`processes.*`); the bare-type `process` of messages is a composition → `*.read` |
| M8 | open | **No rule for polymorphism.** Data-objects §2.5 allows any descendant to be used in place of a base object, but the JSON Representation Rules don't say whether a schema that references a base object also accepts its descendants, or how (`oneOf`/`anyOf` over the descendants, discriminated by the `@type` const). The draft currently uses `oneOf` over the base and its descendants in `processes.transferProcess`/`.createProcess`, every message's `process` and `message.data`. **Suggestion:** add a rule under *Inheritance* that states whether a base-object reference accepts descendants and, if so, how the schema expresses it. It should also say how that combines with the shared Processes Object (M24): a `domainTransferProcess` would otherwise be accepted in `contact.read.processes`. | `processes`, all `*Message.process`, `message.*.data` | `oneOf` over the base object and all its descendants |
| M9 | open | **The `@type` of derived objects is ambiguous in practice.** Rule 25 requires the object's own identifier, but the draft's domain transfer schemas inherit `"const": "transferProcess"` through `allOf`. | `transferProcess.*.domain` | own identifier (`domainTransferProcess`) |
| M10 | open | **No rule for `readOnly` on `@type`.** The draft sets it in read views, reference views and all-read-only components, and leaves it out of create and update views. | all | read views and all-read-only components only. It is left out of reference views, because those are sent in requests (Rule 5). |
| M11 | open | **No annotation rule for `create-only` elements outside request schemas.** Rule 6 covers requests only. The draft marks them `readOnly` in read views. Components have only one schema, so neither annotation fits there (status `label`/`reason`, `authInfo.method`/`authdata`, `reviewResponseMessage.message`). | `domainObject.read.name` | `readOnly` in read views; nothing in components |
| M12 | open | **The primitive mapping table is incomplete.** <br>• It lacks `Object`, `Fully Qualified Domain Name` and `Dictionary[Type]` (data-objects §2.1.9–2.1.11). <br>• It gives the JSON type, not the JSON Schema keywords. `Integer` maps to `number`, but every schema uses `"integer"`. The `format` values (`date-time`, `date`, `uri`) and the Binary encoding are never stated. <br>• FQDN is plain `string` in `domainObject` but `"format": "hostname"` in `hostObject`. | `dnsRecord.rdata`, `dnsControls`, `name`/`hostName` | `integer`; `format` from the notes column; FQDN → `hostname`; Object → `unevaluatedProperties: true` (composable; see C4); Dictionary → object with `additionalProperties` |
| M13 | open | **No rule mapping Common Data Types to `$ref`.** The draft mixes `{ "$ref": "#/$defs/identifier" }` (organisation, user, message) and `{ "type": "string" }` (contact `id`) for the same type. | contact vs organisation `id` | always `$ref` |
| M14 | open | **Dictionary associations have no cardinality rule.** Rules 10 and 12 don't say how `1+` is expressed. The draft uses `minProperties: 1` in `organisationObject.create` but not in `.update`. | `roles` | `minProperties: 1` |
| M15 | open | **Cardinalities other than `1`, `0-1`, `0+` and `1+` are not covered**, for example `contactInfo` with `1-2`. | `contactObject.*` | array with `minItems`/`maxItems` |
| M16 | open | **Labelled aggregation of a primitive is not covered**: `links: LabelledAggregation[String]`. Rule 9 assumes a referenced object. | `discoveryObject.read.links` | `{label, object: string}` |
| M17 | open | **External types have no schema-level rule.** Rule 15 says to embed the native JSON, but nothing says how the `External:<Profile>:<Type>` notation maps to a `$defs` name (the draft uses `Card`), or where the profile's constraints live. | `Card` | `$ref` `#/$defs/<Type>`, with a placeholder definition |
| M18 | open | **Required elements in update schemas.** Rule 23 says *every* definition lists its cardinality-`1`/`1+` elements as required. The draft's update schemas require only `@type` (contact also requires `contactInfo`). There is no rule that distinguishes full-update schemas from the partial-update (JSON Patch) path. | all `*.update` | Rule 23 applied |
| M19 | open | **Process data in create requests.** No rule says which create-process type to use when an object-specific one exists (`domainCreateProcess`), or that `processes` is left out when the Data Object supports no Create Process. There is also no basis for the draft's `"maxItems": 1`. | `domainObject.create.processes` | the Process Objects in the Create Input (`Object: <Process Object>`), each under the matching Processes Object element; no `processes` in create views otherwise; no `maxItems` |
| M20 | open | **Operation parameters** (`hostsFilter`, message query `type`): the draft doesn't say whether they have any JSON representation. They are presumably URL parameters. | — | left out (the `Parameters` items of the operation Input) |
| M21 | open | **Rule 22 needs enumerations that the model supplies only as prose.** No rule covers other constraint keywords either (`minimum`/`maximum`, `pattern`, `propertyNames`). | `period`, `dnsControls` | Rule 22 `enum` from `allowed_values`; the other restrictions mapped to the matching keyword (`range` → `minimum`/`maximum`, `key_pattern` → `propertyNames`, `value_range` → `additionalProperties` bounds) |
| M22 | open | **No rule for `Visibility: onDemand`** (data-objects §2.4). An element returned only on request cannot be required in a read schema. | `domainName.authInfo`, `contact.authInfo` | never required in read views (both are `0-1` today, so no visible effect) |
| M23 | open | **No rule for `Direct Access`** (sub-resource addressing). It is a protocol concern, but the draft doesn't say that the inline JSON representation is unaffected. | `processes.*`, `*.processes`, `organisation.users` | ignored |
| M24 | open | **The Processes Object is shared by all Data Objects.** No rule restricts it to the processes a Data Object supports (`supported_processes` plus owned processes). For example, `contact.read.processes` accepts `renewProcess`, `restoreProcess` and `createProcess`. | `processes` | one shared `processes` component; reported as a diagnostic |
| M25 | open | **No rule for cross-element conditions** (data-objects prose such as "`gainingClientId` is required for push transfers"). The draft expresses it as a `oneOf` over push/pull branches. | `transferProcess.create` | `if`/`then` per exported condition (`allOf` when more than one), in every view that holds all elements the condition names |
| M26 | resolved | **No rule for status objects in requests.** Rule 22 gives one `enum` per status object, and Rules 1, 4 and 23 make `status` (`1+`, read-write) required in create and update requests. Data-objects, however, lets a client set only the values whose *Set By* column contains `client`, lets the server always assign at least one value (`ok`, `active`), and lets a client omit the status when creating or updating the object. No rule says which values a request schema accepts, whether `status` is required in requests, or what happens when a status object has no client-settable value. | all `*.create`/`*.update` with `status`. Resolved: the draft now has Rules 28–31 (*Status Objects* under JSON Schema Definition Rules), which follow the generator choice. | `<id>.request` with the client values in requests; `status` optional in requests when the client may omit it; left out of requests when no value is client-settable; required in read views when the server always assigns one |

### Rule conflicts

| # | Status | Conflict | Generator choice |
|---|--------|----------|------------------|
| C1 | open | **Rule 18 vs Rule 5.** Process data must be sent in the `processes` element of create requests, but `processes` is read-only, and read-only properties must not appear in requests. | Rule 18: a dedicated `processes` object in create views (only `domainName.create`, see M19) |
| C2 | open | **Rule 8 vs Rule 24.** Rule 8 says aggregation schemas MUST allow extra elements of the referenced object. Rule 24 injects `unevaluatedProperties: false` before validation, so a reference schema with only `@type` and the identifier then rejects those extra elements. | not resolved; reported |
| C3 | open | **Rule 26 vs the create/update schemas.** Rule 26 forbids `authInfo` in JSON request bodies "when an operation requires authorization information", yet `domainObject.create`, `domainObject.update` and `contactObject.create` carry `authInfo` to *set* it. The scope of Rule 26 needs to be stated. | `authInfo` kept (it is read-write in the YAML) |
| C4 | open | **Rule 24's open-object keyword vs its own enrichment.** Rule 24 names `"additionalProperties": true` for the Object type, but the enrichment it requires works with `unevaluatedProperties`. `additionalProperties` sees only `properties`/`patternProperties` in the same schema object, so it doesn't compose through `$ref`/`allOf`. Rule 24 also doesn't say that the injected `"unevaluatedProperties": false` must not replace an existing `"unevaluatedProperties": true`. | `"unevaluatedProperties": true` for Object; the consistency checker already skips nodes that carry `unevaluatedProperties` or `additionalProperties` |

---

## 2. Draft schemas that don't match the draft's own rules

| # | Status | Rule | Violation |
|---|--------|------|-----------|
| D1 | open | Inheritance (flat schemas, no `allOf`) | `transferProcess.create.domain` and `transferProcess.read.domain` use `allOf` over the base. `organisationObject.read` uses `allOf` over `organisationObject.create`. The `$ref`-alias definitions (`renewProcess.create.domain`, `transferProcess.create.contact`, `transferProcess.delete/approve/reject.domain`) are the same pattern. |
| D2 | open | Rule 25 (`@type` const = own identifier) | Domain transfer schemas validate `"@type": "transferProcess"`, not `domainTransferProcess`. Every message schema's inline `process` object has `@type` without a `const`. |
| D3 | open | Rule 24 (no `additionalProperties`/`unevaluatedProperties: false`) | `contactObject.create`, `.read` and `.update` set `"unevaluatedProperties": false`. Separately, `dnsRecord.rdata` uses `"unevaluatedProperties": true`, where the rule names `"additionalProperties": true` for the Object type. |
| D4 | open | Rule 5 (`read-only` ⇒ `readOnly`) | `provMetadata` in `domainObject.read`, `contactObject.read` and `hostObject.read` has no `readOnly`. Neither does `profileObject.read.baseProfile`, nor `userObject.read.organisationId` (read-only in the YAML). |
| D5 | open | Rule 5 (no read-only properties in requests) | `contactObject.update` includes `processes`. `userObject.create` includes `organisationId`, which is read-only in the YAML. `organisationObject.update` includes `status` marked `readOnly`. |
| D6 | open | Rule 6 (`create-only` ⇒ `writeOnly` in requests) | Missing in `renewProcess.create` (`expiryDate`, `renewalPeriod`), `transferProcess.create` (`transferDir`, `gainingClientId`), `createProcess.create.period`, `contactObject.create.id` and `organisationObject.create.id`. `domainObject.create` does apply it, so the draft is inconsistent with itself. |
| D7 | open | Rule 23 (required = cardinality `1`/`1+`) | <br>• `transferProcess.read` requires `transferDir`, which is `0-1`. <br>• `restoreReport` requires `statements`, which is `0+`. <br>• No update schema lists its cardinality-1 read-write elements. <br>• (resolved) `domainName.read` and `host.read` now require `status`. <br>• `userObject.read` requires `userId`, a property the YAML doesn't define (it uses `id`). |
| D8 | open | Rule 4 (`1+` ⇒ `minItems: 1`) | (resolved for `status`: read views carry `minItems: 1`; request views drop it per M26.) `roles` has `minProperties: 1` only in create. |
| D9 | open | Rule 20 (one schema per component) | (resolved for the per-type status objects, which the draft now has.) The status request definitions `<id>.request` (M26) are now present too. Still missing: `disclose`, `baseProcess`, `domainCreateProcess`, `restoreProcess.report` (the YAML's Report operation) and `host.update` (still `TODO`). |
| D10 | open | `$defs` uniqueness | `transferProcess.reject.domain` is defined twice, once for the reject request and once for the reject response (Domain Name → Transfer). The combined schema keeps only the second definition. |
| D11 | open | Prose vs schema | The `messageObject.create` caption says the body also carries `id`, `creationDate` and `status`, but the schema doesn't. `userObject.*.description` has `"const": "user"`, which looks like a copy-paste error (`description` is free text). |

---

## 3. Where the YAML is not enough to build schemas like the draft's

The "In source?" column says whether the information is in `draft-ietf-rpp-data-objects.clean.txt` but missing from the export.

| # | Status | Missing information | In source? | Effect |
|---|--------|---------------------|-----------|--------|
| Y1 | fixed | **`Unique Identifier`** object attribute | Yes | Now exported as `unique_identifier`; the reference views use it and the heuristic was removed. |
| Y2 | fixed | **Owner Data Object** of object-specific processes | Yes | Now exported as `owner`; the identifier-prefix heuristic was removed. Together with `supported_processes` it decides the create `processes` type (M19). |
| Y3 | fixed | **`Direct Access`** and **`Visibility`** element attributes | Yes | Now exported as `direct_access` and `visibility`; see M22 and M23. The generator also checks that a Direct Access element with cardinality above 1 targets an object with a Unique Identifier. |
| Y4 | fixed | **Status value tables** | Yes | Now exported as structured `subsections[].tables` (columns `Status Value`, `Set By`, `Description`). The status labels' `allowed_values` are resolved from them, so every status `label` gets a Rule 22 `enum`. |
| Y5 | fixed (partly) | **Enumerations, ranges and patterns** (`period` 1–99, `y`/`m`; `trStatus`, `transferDir`, `restoreStatus`, message `status`, organisation-role and user status values; `dnsControls` key syntax) | Yes, but only as prose constraints | Now exported as `restrictions` and generated. Still prose only: the `restoreReport.statements` count (1–2), `discoveryVersion.version` (Semantic Versioning). |
| Y6 | fixed (partly) | **Conditional requirements**: `gainingClientId` is required for `push` transfers | Prose only | Now exported as `conditions` and generated as `if`/`then` (M25). Still prose only: the `restoreProcess` presence rules (`reportDueDate` only when `restoreStatus` is `pendingRestore`), which need a "value is not" condition the export cannot express. |
| Y7 | fixed (partly) | **Common Data Types** (Identifier, Client Identifier, Phone Number syntax) | Yes (§7), as prose | Now exported as `common_data_types`; Client Identifier and Phone Number carry `base_type` and `restrictions`. Identifier has neither (its syntax is a reference to RFC 5730 §2.8), so only `{"type": "string"}` (Rule 21) is generated. |
| Y8 | open | **External type** `RPP-JSContact-Profile:Card` | No (external profile) | Placeholder object. The draft's `Card` schema has to come from the profile. |
| Y9 | open | **`Object` type structure** (`dnsRecord.rdata`, RDATA structures subsection) | Prose only | Open object. |
| Y10 | open | **Disclose Object** has no data elements | No (source says `Description: TBD`) | Only an empty `disclose` schema can be generated. |
| Y11 | fixed | **Operation input and output** | Yes | Now exported as structured `input`/`output` items (Uniform interface defaults filled in). The generator takes the view elements, the create `processes` Process Objects, the query cardinality, the Input Data Elements and the Parameters from them. |
| Y12 | open | **Maintenance Message Object** | **No** (missing from the YAML and from the source) | The draft defines `maintenanceMessage`, so `message.data` in the draft has an extra `oneOf` branch. |
| Y13 | fixed | **`userStatus.label` allowed values** | Yes (User Status Values table, `{#tbl-user-status-values}`) | The table is exported, but `allowed_values` is not resolved from it: `restrictions` is `{}` and the constraint stays prose ("Only status values defined in [Status Values](#user-status-values)…"). The generated `userStatus.label` is a plain string with no Rule 22 `enum` (`active`, `pending`, `suspended`, `deactivated`), unlike the other status objects (see Y4). Now resolved: `allowed_values` is exported and the generated `enum` holds the four values. |
| Y14 | fixed | **Who sets each status value, and whether the status is required in requests** | Yes (*Set By* column of the status values tables; status values prose) | Now exported as the `client_values`/`server_only_values` restrictions of each status `label` and the object flags `at_least_one_status_by_server` and `status_not_required_for_client_request`. The generator builds the `<id>.request` definitions and the request/read requirements from them (M26). |

### YAML data-quality issues found while generating

- (fixed) Trailing periods in data types (`contact.id`, `contact.disclose`).
- `domainName.authInfo` and `contact.authInfo` use `Authorisation Information Object`, but the object is named `Authorisation Information`.
- `contact.disclose` uses `Disclose Object`, but the object is named `Disclose`.
- (fixed) `user.organisationId` used the `<Object> Reference` notation; it is now `Aggregation[Organisation Data Object]`.
- (fixed) `domainName.registrant`, `organisation.parent` and `profile.baseProfile` used the bare type (Composition); they are now `Aggregation[...]`, so the generator emits `*.reference` like the draft.
- `domainTransferProcess` redefines the inherited `processId`, which data-objects §2.5 forbids.
- (fixed) The Output of every operation (and the Uniform interface default) listed `Elements: read-write, read-only`, so create-only elements (`domainName.name`, `contact.id`, `transferProcess.transferDir`, …) were never returned. The Output now lists `create-only, read-write, read-only`, and the generator's override was removed.
- `organisationRoleStatus` has no `at_least_one_status_by_server`/`status_not_required_for_client_request` flags, although the other five status objects have both. It is embedded only in `organisationRole` (`0+`), so the generated schemas don't change.
- `contact.contactInfo` has cardinality `1-2`, which is not in the data-objects cardinality notation (§2.4).
- The `user` element constraints are again given as `'-'` rather than `[]` (`details`, `description`, `status`, `organisationId`); this was fixed in an earlier export and has regressed.

---

## 4. Where the YAML and the draft disagree on content (for information)

The generator follows the YAML on all of these, so they show up as differences in `--compare`:

- (resolved) **`status`**: the draft's create, update and read schemas now match the generated ones (M26).
- **`user`**: the YAML gives `details` as a JSContact `Card`, `status` as a single `String` (`1`), and the identifier as `id`. The draft has a contact reference, an array of enums, and `userId`. `organisationId` is read-only in the YAML, so it is missing from `user.create` but required in `user.read`.
- **`organisationRole.status`**: the YAML uses `Organisation Role Status Object`; the draft uses an array of enum strings.
- **`contactInfo`**: the YAML gives `1-2` (an array); the draft has a single `Card`.
- **Process elements**: `restoreReport` is an input data element of the `restoreProcess` Create and Report operations in the YAML; the generated `restoreProcess.create` matches the draft, and the Report operation gives an extra `restoreProcess.report` view. `createProcess` has no `period` in the YAML; it is in `domainCreateProcess`.
- **Create `processes`**: only `domainName` supports a Create Process Object in the YAML, so the generated `contact.create`, `host.create`, `organisation.create` and `user.create` have no `processes` property.
- **Common Data Type syntax**: the YAML's Client Identifier pattern is `^\S+( \S+)*$`; the draft's is `^[a-zA-Z0-9]([-a-zA-Z0-9]*[a-zA-Z0-9])?$`. The YAML's Phone Number pattern limits the number to 14 digits and has no space before the `x` extension separator; the draft's has `( x[0-9]+)?` and no digit limit. The draft's `identifier` pattern and `maxLength` 89 have no YAML counterpart.
- **`dnsControls` keys**: the YAML's `key_pattern` is `^[a-z][a-z0-9-]*$`; the draft's `propertyNames` pattern is `^[a-z]+$`.
- **Enumerations the draft lacks**: `transferRequestMessage.status` (`pending`) and `transferDir` in the domain transfer and message schemas.
- **`processId`**, inherited from `baseProcess`, is in every process read view in the YAML and absent from all of the draft's process schemas.

A quick check of the draft's `# Examples` against the generated schemas confirms the main breaks. The examples fail on:
- the `status` shape and requirement,
- the `@type` of derived processes (`domainCreateProcess`),
- `contactInfo` being an array,
- (resolved) the user `status`: the user examples now carry a `userStatus` object,
- the limited `process` objects inside messages.
