# JSON Schema Generator Report

Inputs:

- object model `.work/draft-ietf-rpp-data-objects.yaml`
- draft `src/draft-ietf-rpp-json.md` (branch `feature/generate-schemas`, commit `64022e4`)
- source text `.work/draft-ietf-rpp-data-objects.clean.txt`, checked where the YAML is silent

Generator: `.scripts/gen_json_schema.py`.

```
.scripts/.venv/bin/python .scripts/gen_json_schema.py .work/draft-ietf-rpp-data-objects.yaml \
    -o schema.json --split schemas/ --diagnostics diag.md \
    --compare src/draft-ietf-rpp-json.md --compare-out compare.md
```

The generator produces 73 `$defs`. The bundle passes 2020-12 meta-schema validation, and every `$ref` in it resolves.

Generation precedence: **the draft's written rules, then the YAML content, then the shape of the draft's existing schemas**.
- `$defs` names are built from the YAML identifier: `<id>` for components, and `<id>.create`, `<id>.read`, `<id>.update`, `<id>.reference` and `<id>.query` for resources.
- Process objects get `<id>.create` and `<id>.read`, plus one view per operation that has input data elements (for example `transferProcess.reject`).
- Prose constraints are **not** turned into keywords. Only cardinality, mutability and data type are used.

---

## 1. Rules missing from the draft

Without these rules, the schemas can't be reproduced the way the draft writes them. Each item names the choice the generator made.

| # | Gap | Where the draft schemas show it | Generator choice |
|---|-----|-------------------------------|------------------|
| M1 | **No naming rule for `$defs`.** The draft names definitions after `<x>Object`, not after the `@type` identifier (`domainObject.*` for `domainName`, `contactObject.*` for `contact`). Components get bare names. Object-specific processes get an owner suffix (`transferProcess.create.domain`). | all resource and process schemas | `<identifier>[.<view>]` |
| M2 | **No rule for which schema views exist and what each one contains.** Rules 5–7 suggest the views but never state that a create view holds create-only and read-write elements, an update view holds read-write elements, a read view holds everything, and a reference view holds `@type` and the identifier. There is also no rule for operation-specific views (Reject), or for query responses (`messageObject.query` is an array of read views). | the `### Create/Read/Update/Reference` subsections | derived from mutability and operations, as stated |
| M3 | **No rule for which element is the "primary identifier".** The TODO comment under *Labelled associations* says so. The data-objects draft has an explicit `Unique Identifier` attribute, but this draft never refers to it. | `*.reference` | heuristic (see Y1) |
| M4 | **References contradict each other.** Rule 13 says a referenced object is represented as a JSON **string** (its identifier). Rules 8–10 and every schema in the draft use an **object** with `@type` and the identifier. | `registrant`, `contacts`, `nameservers` | object reference (`<id>.reference`) |
| M5 | **The bare `Type` notation is not mentioned.** In data-objects §8.2 a data type given as a bare object name means `Composition[Type]` (`Notation: Composition[Type] or Type`). The Association Rules here only show the bracketed form. Examples: `registrant: Contact Data Object`, `parent: Organisation Data Object`, `baseProfile: Profile Data Object`. For these three, the draft's references (`*.reference`) are correct: the elements should be `Aggregation[...]` in the data-objects draft (see §3, YAML data-quality issues). | `registrant`, `parent`, `baseProfile` | composition: the full view of the target (`contact.create`/`.read`/`.update`, `organisation.*`, `profile.read`) is embedded |
| M6 | **Aggregation with cardinality `1` or `0-1` is not covered.** Rule 8 only covers `0+` and `1+`. | message `process` | a single `$ref`, no array |
| M7 | **No rule for aggregating Process Objects.** The Processes Object embeds the full `*.read` view, while messages embed an inline limited object `{ "@type", "processId" }` whose `@type` has no `const`. | `processes`, all `*Message` | `*.read` |
| M8 | **No rule for polymorphism.** Data-objects §2.5 allows any descendant to be used in place of a base object. The draft uses `oneOf` only for `message.data`; `processes.transferProcess` accepts only `transferProcess.read`, although `domainTransferProcess` extends it. | `messageObject.*`, `processes` | `oneOf` over the base object and all its descendants |
| M9 | **The `@type` of derived objects is ambiguous in practice.** Rule 25 requires the object's own identifier, but the draft's domain transfer schemas inherit `"const": "transferProcess"` through `allOf`. | `transferProcess.*.domain` | own identifier (`domainTransferProcess`) |
| M10 | **No rule for `readOnly` on `@type`.** The draft sets it in read views, reference views and all-read-only components, and leaves it out of create and update views. | all | read views and all-read-only components only. It is left out of reference views, because those are sent in requests (Rule 5). |
| M11 | **No annotation rule for `create-only` elements outside request schemas.** Rule 6 covers requests only. The draft marks them `readOnly` in read views. Components have only one schema, so neither annotation fits there (status `label`/`reason`, `authInfo.method`/`authdata`, `reviewResponseMessage.message`). | `domainObject.read.name` | `readOnly` in read views; nothing in components |
| M12 | **The primitive mapping table is incomplete.** <br>• It lacks `Object`, `Fully Qualified Domain Name` and `Dictionary[Type]` (data-objects §2.1.9–2.1.11). <br>• It gives the JSON type, not the JSON Schema keywords. `Integer` maps to `number`, but every schema uses `"integer"`. The `format` values (`date-time`, `date`, `uri`) and the Binary encoding are never stated. <br>• FQDN is plain `string` in `domainObject` but `"format": "hostname"` in `hostObject`. | `dnsRecord.rdata`, `dnsControls`, `name`/`hostName` | `integer`; `format` from the notes column; FQDN → `hostname`; Object → `additionalProperties: true`; Dictionary → object with `additionalProperties` |
| M13 | **No rule mapping Common Data Types to `$ref`.** The draft mixes `{ "$ref": "#/$defs/identifier" }` (organisation, user, message) and `{ "type": "string" }` (contact `id`) for the same type. | contact vs organisation `id` | always `$ref` |
| M14 | **Dictionary associations have no cardinality rule.** Rules 10 and 12 don't say how `1+` is expressed. The draft uses `minProperties: 1` in `organisationObject.create` but not in `.update`. | `roles` | `minProperties: 1` |
| M15 | **Cardinalities other than `1`, `0-1`, `0+` and `1+` are not covered**, for example `contactInfo` with `1-2`. | `contactObject.*` | array with `minItems`/`maxItems` |
| M16 | **Labelled aggregation of a primitive is not covered**: `links: LabelledAggregation[String]`. Rule 9 assumes a referenced object. | `discoveryObject.read.links` | `{label, object: string}` |
| M17 | **External types have no schema-level rule.** Rule 15 says to embed the native JSON, but nothing says how the `External:<Profile>:<Type>` notation maps to a `$defs` name (the draft uses `Card`), or where the profile's constraints live. | `Card` | `$ref` `#/$defs/<Type>`, with a placeholder definition |
| M18 | **Required elements in update schemas.** Rule 23 says *every* definition lists its cardinality-`1`/`1+` elements as required. The draft's update schemas require only `@type` (contact also requires `contactInfo`). There is no rule that distinguishes full-update schemas from the partial-update (JSON Patch) path. | all `*.update` | Rule 23 applied |
| M19 | **Process data in create requests.** No rule says which create-process type to use when an object-specific one exists (`domainCreateProcess`). There is also no basis for the draft's `"maxItems": 1`. | `domainObject.create.processes` | owner-specific type when it exists; no `maxItems` |
| M20 | **Operation parameters** (`hostsFilter`, message query `type`): the draft doesn't say whether they have any JSON representation. They are presumably URL parameters. | — | left out |
| M21 | **Rule 22 needs enumerations that the model supplies only as prose.** No rule covers other constraint keywords either (`minimum`/`maximum`, `pattern`, `propertyNames`). | `period`, `dnsControls` | not generated (structure-only mode) |

### Rule conflicts

| # | Conflict | Generator choice |
|---|----------|------------------|
| C1 | **Rule 18 vs Rule 5.** Process data must be sent in the `processes` element of create requests, but `processes` is read-only, and read-only properties must not appear in requests. | Rule 18: a dedicated `processes` object in create views |
| C2 | **Rule 8 vs Rule 24.** Rule 8 says aggregation schemas MUST allow extra elements of the referenced object. Rule 24 injects `unevaluatedProperties: false` before validation, so a reference schema with only `@type` and the identifier then rejects those extra elements. | not resolved; reported |
| C3 | **Rule 26 vs the create/update schemas.** Rule 26 forbids `authInfo` in JSON request bodies "when an operation requires authorization information", yet `domainObject.create`, `domainObject.update` and `contactObject.create` carry `authInfo` to *set* it. The scope of Rule 26 needs to be stated. | `authInfo` kept (it is read-write in the YAML) |

---

## 2. Draft schemas that don't match the draft's own rules

| # | Rule | Violation |
|---|------|-----------|
| D1 | Inheritance (flat schemas, no `allOf`) | `transferProcess.create.domain` and `transferProcess.read.domain` use `allOf` over the base. `organisationObject.read` uses `allOf` over `organisationObject.create`. The `$ref`-alias definitions (`renewProcess.create.domain`, `transferProcess.create.contact`, `transferProcess.delete/approve/reject.domain`) are the same pattern. |
| D2 | Rule 25 (`@type` const = own identifier) | Domain transfer schemas validate `"@type": "transferProcess"`, not `domainTransferProcess`. Every message schema's inline `process` object has `@type` without a `const`. |
| D3 | Rule 24 (no `additionalProperties`/`unevaluatedProperties: false`) | `contactObject.create`, `.read` and `.update` set `"unevaluatedProperties": false`. Separately, `dnsRecord.rdata` uses `"unevaluatedProperties": true`, where the rule names `"additionalProperties": true` for the Object type. |
| D4 | Rule 5 (`read-only` ⇒ `readOnly`) | `provMetadata` in `domainObject.read`, `contactObject.read` and `hostObject.read` has no `readOnly`. Neither does `profileObject.read.baseProfile`, nor `userObject.read.organisationId` (read-only in the YAML). |
| D5 | Rule 5 (no read-only properties in requests) | `contactObject.update` includes `processes`. `userObject.create` includes `organisationId`, which is read-only in the YAML. `organisationObject.update` includes `status` marked `readOnly`. |
| D6 | Rule 6 (`create-only` ⇒ `writeOnly` in requests) | Missing in `renewProcess.create` (`expiryDate`, `renewalPeriod`), `transferProcess.create` (`transferDir`, `gainingClientId`), `createProcess.create.period`, `contactObject.create.id` and `organisationObject.create.id`. `domainObject.create` does apply it, so the draft is inconsistent with itself. |
| D7 | Rule 23 (required = cardinality `1`/`1+`) | <br>• `transferProcess.read` requires `transferDir`, which is `0-1`. <br>• `restoreReport` requires `statements`, which is `0+`. <br>• No update schema lists its cardinality-1 read-write elements. <br>• `domainObject.read` and `hostObject.read` don't require `status` (`1+` in the YAML). <br>• `userObject.read` requires `userId`, a property the YAML doesn't define (it uses `id`). |
| D8 | Rule 4 (`1+` ⇒ `minItems: 1`) | `status` arrays (`1+` in the YAML) have no `minItems`. `roles` has `minProperties: 1` only in create. |
| D9 | Rule 20 (one schema per component) | No schema for `domainStatus`, `hostStatus`, `contactStatus`, `organisationStatus` or `organisationRoleStatus` (the draft has one generic `status`). Also missing: `disclose`, `baseProcess`, `domainCreateProcess`, `restoreProcess.update` and `host.update` (still `TODO`). |
| D10 | `$defs` uniqueness | `transferProcess.reject.domain` is defined twice, once for the reject request and once for the reject response (Domain Name → Transfer). The combined schema keeps only the second definition. |
| D11 | Prose vs schema | The `messageObject.create` caption says the body also carries `id`, `creationDate` and `status`, but the schema doesn't. `userObject.*.description` has `"const": "user"`, which looks like a copy-paste error (`description` is free text). |

---

## 3. Where the YAML is not enough to build schemas like the draft's

The "In source?" column says whether the information is in `draft-ietf-rpp-data-objects.clean.txt` but missing from the export.

| # | Missing information | In source? | Effect |
|---|---------------------|-----------|--------|
| Y1 | **`Unique Identifier`** object attribute (`name`, `id`, `hostName`, `processId`, `(None)` for discovery) | **Yes**, in each object's preamble | The reference views use a heuristic (first cardinality-1 element of type Identifier or FQDN, else `id`/`name`). It happens to give the right result for all 7 objects. |
| Y2 | **Owner Data Object** of object-specific processes (`domainCreateProcess` and `domainTransferProcess` are nested under *Domain Name → Processes*) | **Yes**, through section nesting (§11.4) | The owner is guessed from the identifier prefix. The draft's owner-suffixed names (`*.domain`) and the domain create `processes` type depend on it. |
| Y3 | **`Direct Access`** and **`Visibility`** element attributes (for example, `Direct Access: true` on the process aggregations and `Visibility: onDemand` on `restoreReport`) | **Yes** | Not used. `onDemand` could affect required/optional status in read views. |
| Y4 | **Status value tables** (`Table: Domain Name Status Values`, etc.) | **Yes**, as tables; the YAML keeps only the table caption in `subsections.notes` | Rule 22 enums for `label` can't be generated. |
| Y5 | **Enumerations, ranges and patterns** (`period` 1–99, `y`/`m`; `trStatus`, `transferDir`, `restoreStatus`, message `status`, organisation-role and user status values; `dnsControls` key syntax) | Yes, but only as prose constraints | Not generated. A structured `allowed_values`/`range` field would make Rule 22 mechanical. |
| Y6 | **Conditional requirements**: `gainingClientId` is required for `push` transfers | Prose only | The draft's `oneOf` for push/pull in `transferProcess.create` can't be derived. |
| Y7 | **Common Data Types** (Identifier, Client Identifier, Phone Number syntax) | Yes (§7), as prose | Placeholder `{"type": "string"}` definitions are generated. |
| Y8 | **External type** `RPP-JSContact-Profile:Card` | No (external profile) | Placeholder object. The draft's `Card` schema has to come from the profile. |
| Y9 | **`Object` type structure** (`dnsRecord.rdata`, RDATA structures subsection) | Prose only | Open object. |
| Y10 | **Disclose Object** has no data elements | No (source says `Description: TBD`) | Only an empty `disclose` schema can be generated. |
| Y11 | **Operation input and output for resources** (`input`/`output` are empty for every resource operation). That Create carries Create Process data (Rule 18) and what a Query returns are described only in prose. | Prose only | The create `processes` property and the `query` view are generated by rule, not from the data. |
| Y12 | **Maintenance Message Object** | **No** (missing from the YAML and from the source) | The draft defines `maintenanceMessage`, so `message.data` in the draft has an extra `oneOf` branch. |

### YAML data-quality issues found while generating

- `contact.id` has data type `Identifier.` and `contact.disclose` has `Disclose Object.` (trailing period).
- `domainName.authInfo` uses `Authorisation Information Object`, but the object is named `Authorisation Information` (`contact.authInfo` uses the short form).
- `user.organisationId` uses `Organisation Data Object Reference`, which is not one of the defined association types.
- `domainName.registrant` (`Contact Data Object`), `organisation.parent` (`Organisation Data Object`) and `profile.baseProfile` (`Profile Data Object`) use the bare type, which means Composition (data-objects §8.2). They relate to independent objects and should be `Aggregation[...]`. Until that is fixed, the generator embeds the full target object where the JSON draft correctly uses `*.reference`.
- `domainTransferProcess` redefines the inherited `processId`, which data-objects §2.5 forbids.
- `contact.contactInfo` has cardinality `1-2`, which is not in the data-objects cardinality notation (§2.4).
- The `user` element constraints are given as `'-'` rather than `[]`.

---

## 4. Where the YAML and the draft disagree on content (for information)

The generator follows the YAML on all of these, so they show up as differences in `--compare`:

- **`status`**: the YAML has a per-type status object, `1+`, read-write. The draft has a generic `status`, optional and `readOnly`. Because the YAML marks it `1+`, the generated create and update views require `status`.
- **`user`**: the YAML gives `details` as a JSContact `Card`, `status` as a single `String` (`1`), and the identifier as `id`. The draft has a contact reference, an array of enums, and `userId`.
- **`organisationRole.status`**: the YAML uses `Organisation Role Status Object`; the draft uses an array of enum strings.
- **`contactInfo`**: the YAML gives `1-2` (an array); the draft has a single `Card`.- **Process elements**: `restoreReport` is in `restoreProcess` (read-write) in the YAML, but only in the draft's create view. `createProcess` has no `period` in the YAML; it is in `domainCreateProcess`.
- **`processId`**, inherited from `baseProcess`, is in every process read view in the YAML and absent from all of the draft's process schemas.

A quick check of the draft's `# Examples` against the generated schemas confirms the main breaks. The examples fail on:
- the `status` shape and requirement,
- the `@type` of derived processes (`domainCreateProcess`),
- `contactInfo` being an array,
- the user `status` and `id`,
- the limited `process` objects inside messages.
