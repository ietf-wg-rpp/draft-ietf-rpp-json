#!/usr/bin/env python3
"""
gen_json_schema.py

Builds JSON Schema (draft 2020-12) definitions for the RPP data objects from
the structured object model export of draft-ietf-rpp-data-objects (YAML),
following the JSON Representation Rules of draft-ietf-rpp-json.

Usage:
    python3 gen_json_schema.py MODEL.yaml [-o OUT.json] [--split DIR]
                               [--compare DRAFT.md] [--compare-out FILE]
                               [--replace DRAFT.md] [--replace-out FILE]
                               [--diagnostics FILE] [--expanded] [-q]

  MODEL.yaml        object model export (e.g. .work/draft-ietf-rpp-data-objects.yaml)
  -o OUT.json       write the bundled schema (all $defs) to OUT.json (default: stdout)
  --split DIR       additionally write one file per definition, shaped like the
                    schema blocks in draft-ietf-rpp-json
  --compare DRAFT   compare generated definitions with the schemas in the
                    "JSON Schema Definitions" chapter of DRAFT
  --compare-out F   write the comparison to F instead of stdout
  --replace DRAFT   replace the schema blocks of DRAFT in place with their generated
                    counterparts (Rule 27 keys) and print the generated schemas left unused
  --replace-out F   write the updated draft to F instead of DRAFT
  --diagnostics F   write generator diagnostics (rule gaps, YAML gaps, heuristics) to F
  -q                do not print diagnostics to stderr

Generation decisions (precedence: draft rules > YAML content > draft schema shape):

  * $defs keys follow Rule 27 (as updated by the M1 suggestion on PR #104), with
    identifiers used as-is: components "<id>", resources
    "<id>.create|read|update|query|reference",
    processes "<id>.create|read[|update]" plus one view per other operation that
    carries input data elements, keyed by the operation Identifier
    (e.g. "transferProcess.transferReject"). Derived objects use their own id.
  * Inheritance ("extends") is flattened (draft section "Inheritance").
  * Polymorphism: a reference to a base object accepts every object extending
    it, expressed as "oneOf" over the candidates (each fixed by its "@type").
  * Reference views (resources and processes) use the exported
    "unique_identifier"; objects without one get no reference view.
    Aggregations of resources and processes reference the reference view (Rule 8).
  * View elements follow the "Elements" of the operations' Input/Output items
    (create Input Object, read Output Object); update views hold the read-write
    elements (Rules 5-7). Operation views carry the operation's
    Input Data Elements; Parameters are left out.
  * Create views carry "processes" only when the Create Input names a
    Process Object.
  * Elements with Visibility "onDemand" are not required in read views.
    Direct Access does not change the representation.
  * Status Component Objects (those whose label restrictions export
    "client_values"/"server_only_values") get a second definition
    "<id>.request" whose label enum holds only the client values. Create and
    update views embed it; read views embed the full "<id>". A status element
    is left out of create and update views when the status object has no
    client values, is optional there when "status_not_required_for_client_request"
    is set, and is required in read views when "at_least_one_status_by_server"
    is set.
  * Prose constraints are NOT converted to keywords; only the structured
    attributes are used: cardinality, mutability, data type, "restrictions"
    (enum, minimum/maximum, pattern, minLength/maxLength, propertyNames) and
    "conditions" (if/then). Common Data Types come from "common_data_types".
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"

# Primitive Type Mappings (draft-ietf-rpp-json) plus the data-objects primitives
# that the mapping table does not cover (Object, Fully Qualified Domain Name).
PRIMITIVES = {
    "String":    {"type": "string"},
    "Integer":   {"type": "integer"},
    "Boolean":   {"type": "boolean"},
    "Decimal":   {"type": "string", "pattern": "^-?(0|[1-9][0-9]*)(\\.[0-9]+)?$"},
    "Date":      {"type": "string", "format": "date"},
    "Timestamp": {"type": "string", "format": "date-time"},
    "URL":       {"type": "string", "format": "uri"},
    "Binary":    {"type": "string", "contentEncoding": "base64"},
}
PRIMITIVES_NOT_IN_RULES = {
    "Object":                      {"type": "object", "unevaluatedProperties": True},
    "Fully Qualified Domain Name": {"type": "string", "format": "hostname"},
}

# Common Data Types: name -> $defs name (the draft's keys; they have no Identifier).
COMMON_TYPES = {
    "Identifier":        "identifier",
    "Client Identifier": "clientIdentifier",
    "Phone Number":      "phoneNumber",
}

ASSOC_RE = re.compile(r"^(Aggregation|Composition|LabelledAggregation|DictionaryAggregation|"
                      r"LabelledComposition|DictionaryComposition)\[(.+)\]$")
DICT_RE = re.compile(r"^Dictionary\[(.+)\]$")
EXTERNAL_RE = re.compile(r"^External:([^:]+):(.+)$")

STANDARD_VIEWS = ("create", "read", "update", "query")
REQUEST_VIEWS = ("create", "update")
STATUS_RESTRICTIONS = ("client_values", "server_only_values")

COMPOSITIONS = {"Composition", "LabelledComposition", "DictionaryComposition"}
LABELLED = {"LabelledAggregation", "LabelledComposition"}
DICTIONARY = {"DictionaryAggregation", "DictionaryComposition"}


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

CATEGORIES = {
    "rule-gap":      "No rule in draft-ietf-rpp-json covers this; generator choice applied",
    "rule-conflict": "Rules of draft-ietf-rpp-json conflict; generator choice applied",
    "yaml-gap":      "Information not present in the YAML export",
    "yaml-issue":    "YAML content inconsistent with the data-objects conventions",
    "heuristic":     "Value derived heuristically (not stated in the YAML)",
}


class Diagnostics:
    def __init__(self):
        self.items = {}  # (category, message) -> list of contexts

    def add(self, category, message, context=""):
        ctxs = self.items.setdefault((category, message), [])
        if context and context not in ctxs:
            ctxs.append(context)

    def render(self):
        out = []
        for cat, title in CATEGORIES.items():
            entries = [(m, c) for (k, m), c in self.items.items() if k == cat]
            if not entries:
                continue
            out.append(f"## {cat}: {title}\n")
            for msg, ctxs in entries:
                out.append(f"- {msg}")
                if ctxs:
                    out.append(f"  ({', '.join(ctxs)})")
            out.append("")
        return "\n".join(out)


# ---------------------------------------------------------------------------
# Object model
# ---------------------------------------------------------------------------

def norm_name(name):
    """Normalise an object name for lookup; returns (key, is_reference)."""
    n = name.strip().rstrip(".").strip().lower()
    is_ref = n.endswith(" reference")
    if is_ref:
        n = n[: -len(" reference")]
    if n.endswith(" object"):
        n = n[: -len(" object")]
    return n, is_ref


def common_key(name):
    """$defs key of a Common Data Type: the draft's key, else the camelCase name."""
    return COMMON_TYPES.get(name) or lc_first("".join(w[:1].upper() + w[1:] for w in name.split()))


def lc_first(s):
    return s[:1].lower() + s[1:]


def uc_first(s):
    return s[:1].upper() + s[1:]


class Obj:
    def __init__(self, raw):
        self.raw = raw
        self.id = raw["identifier"]
        self.name = raw["name"]
        self.kind = raw["object_type"]
        self.parent = None
        self.children = []
        self.elements = []    # flattened, inherited first
        self.operations = []  # flattened: list of (op, defining Obj)

    def ancestors(self):
        p, out = self.parent, []
        while p is not None:
            out.append(p)
            p = p.parent
        return out

    def descendants(self):
        out = []
        for c in self.children:
            out.append(c)
            out.extend(c.descendants())
        return out

    def is_a(self, other):
        return self is other or other in self.ancestors()

    def stem(self):
        """Operation prefix of a process object: "transferProcess" -> "transfer"."""
        return self.id[: -len("Process")] if self.id.endswith("Process") else self.id


class Model:
    def __init__(self, data, diag):
        self.diag = diag
        self.objs = {}
        self.by_name = {}
        self.common = {c["name"]: c for c in data.get("common_data_types") or []}
        for section in ("components", "processes", "resources"):
            for raw in data.get(section) or []:
                o = Obj(raw)
                self.objs[o.id] = o
                self.by_name[norm_name(o.name)[0]] = o
        for o in self.objs.values():
            ext = o.raw.get("extends") or ""
            if ext:
                base = self.lookup(ext, f"{o.id} extends")
                if base is None:
                    diag.add("yaml-issue", f"Base object '{ext}' not found", o.id)
                else:
                    o.parent = base
                    base.children.append(o)
        for o in self.objs.values():
            self._flatten(o)

    def lookup(self, name, context=""):
        key, is_ref = norm_name(name)
        o = self.by_name.get(key)
        if o is not None and name.strip() != o.name:
            short = name.strip() + " Object" == o.name
            if name.strip().endswith("."):
                self.diag.add("yaml-issue", "Data type value has a trailing period", context)
            elif is_ref:
                self.diag.add("yaml-issue", "Data type uses the '<Object Name> Reference' notation, "
                                            "which is not one of the defined association types", context)
            elif not short:
                self.diag.add("yaml-issue",
                              f"Object referenced as '{name.strip()}' but defined as '{o.name}'",
                              context)
        return o

    def _flatten(self, o):
        chain = list(reversed(o.ancestors())) + [o]
        seen = {}
        for obj in chain:
            for e in obj.raw.get("elements") or []:
                if e["identifier"] in seen and obj is o and o.parent is not None:
                    self.diag.add("yaml-issue",
                                  f"Derived object redefines inherited data element "
                                  f"'{e['identifier']}' (data-objects Inheritance: MUST NOT)",
                                  o.id)
                seen[e["identifier"]] = e
        o.elements = list(seen.values())
        ops = {}
        for obj in chain:
            for op in obj.raw.get("operations") or []:
                ops[self.op_suffix(op, obj)] = (op, obj)
        o.operations = list(ops.values())

    @staticmethod
    def op_suffix(op, owner):
        """Operation kind: "transferCreate" on transferProcess -> "create".

        Only used to recognise standard views and overrides; never part of a $defs key."""
        oid = op["identifier"]
        stem = owner.stem() if owner.kind == "Process" else ""
        if stem and oid.startswith(stem) and len(oid) > len(stem):
            return lc_first(oid[len(stem):])
        return oid

    # -- operation Input / Output (data-objects "Operation Input and Output") --

    def io(self, op, owner, side):
        """Items of an operation's "input" or "output" ([] for "(None)")."""
        items = op.get(side)
        if items is None:
            self.diag.add("yaml-gap", f"Operation has no {side} and no Uniform interface default "
                                      f"applies ([OP IO MISSING])", f"{owner.id}.{op['identifier']}")
            return []
        return items

    @staticmethod
    def definitions(op, kind):
        """Definitions of the "Input Data Elements" or "Parameters" item of an operation."""
        return [d for item in op.get("input") or [] if item["kind"] == kind
                for d in item.get("definitions") or []]

    def io_target(self, item, owner):
        """Object named by a Reference/Object item, resolved against the defining object."""
        t = item["target"]
        if t == "This Object":
            return owner
        if t == "Owner Data Object":
            return self.owner_of(owner)
        o = self.lookup(t, f"{owner.id} operation {item['kind']}")
        if o is None:
            self.diag.add("yaml-issue", f"Operation {item['kind']} target '{t}' is not a defined object",
                          owner.id)
        return o

    @staticmethod
    def conditions(o):
        """Cross-element conditions of an object, inherited first."""
        return [c for obj in list(reversed(o.ancestors())) + [o] for c in obj.raw.get("conditions") or []]

    def owner_of(self, proc):
        """Owner Data Object of an object-specific process ("owner" in the export)."""
        oid = proc.raw.get("owner") or ""
        if not oid:
            return None
        owner = self.objs.get(oid)
        if owner is None or owner.kind != "Resource":
            self.diag.add("yaml-issue", f"Owner '{oid}' is not a Data Object", proc.id)
            return None
        return owner

    def unique_id(self, o):
        """Unique Identifier element ("unique_identifier" in the export), or None."""
        uid = o.raw.get("unique_identifier") or ""
        if not uid:
            return None
        pick = next((e for e in o.elements if e["identifier"] == uid), None)
        if pick is None:
            self.diag.add("yaml-issue", f"Unique Identifier '{uid}' is not a data element of the object",
                          o.id)
        return pick

    def supported_processes(self, res):
        """Process Objects a Data Object supports: inherited unmodified plus those it owns."""
        out = []
        for sp in res.raw.get("supported_processes") or []:
            p = self.lookup(sp["name"], f"{res.id} supported process")
            if p is None or p.kind != "Process":
                self.diag.add("yaml-issue", f"Supported process '{sp['name']}' is not a Process Object",
                              res.id)
            else:
                out.append(p)
        out.extend(p for p in self.objs.values() if p.kind == "Process" and self.owner_of(p) is res)
        return out


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class Generator:
    def __init__(self, model, diag):
        self.m = model
        self.diag = diag
        self.defs = {}
        self.common_used = set()
        self.placeholders = set()  # $defs keys whose content is not taken from the model
        self.external_used = {}

    # -- views -------------------------------------------------------------

    @staticmethod
    def view_of(op, owner):
        """View name of an operation: a standard view, else the operation Identifier as-is."""
        s = Model.op_suffix(op, owner)
        return s if s in STANDARD_VIEWS else op["identifier"]

    def views_for(self, o):
        if o.kind == "Component":
            return [None, "request"] if self.client_values(o) and self.in_resource(o) else [None]
        sfx = [Model.op_suffix(op, owner) for op, owner in o.operations]
        if o.kind == "Process":
            views = ["create", "read"]
            if "update" in sfx:
                views.append("update")
            for op, owner in o.operations:
                v = self.view_of(op, owner)
                if Model.definitions(op, "Input Data Elements") and v not in views:
                    views.append(v)
            if self.m.unique_id(o) is not None:
                views.append("reference")
            return views
        views = [v for v in ("create", "read", "update") if v in sfx]
        if "query" in sfx and "read" in views:
            views.append("query")
        if self.m.unique_id(o) is not None:
            views.append("reference")
        return views

    @staticmethod
    def def_name(o, view):
        return o.id if view is None else f"{o.id}.{view}"

    def has_def(self, o, view):
        return view in self.views_for(o)

    # -- top level ---------------------------------------------------------

    def build(self):
        ordered = []
        for kind in ("Component", "Process", "Resource"):
            for o in self.m.objs.values():
                if o.kind != kind:
                    continue
                if o.kind == "Component" and not o.elements:
                    self.diag.add("yaml-gap", "Object has no data elements", o.id)
                for view in self.views_for(o):
                    ordered.append((self.def_name(o, view), self.build_view(o, view)))
        defs = {}
        for name in self.m.common:
            self.common_used.add(common_key(name))
        for name in sorted(self.common_used):
            defs[name] = self.common_schema(name)
            self.diag.add("rule-gap", "Common Data Types have no Identifier, so Rule 27 does not name "
                                      "their $defs key; the draft's key is used", name)
        for name, profile in self.external_used.items():
            self.placeholders.add(name)
            defs[name] = {"type": "object",
                          "$comment": f"External type from {profile}: definition not available "
                                      f"in the object model export"}
            self.diag.add("yaml-gap", "External type definition is not exported; "
                                      "an open object placeholder is generated (Rule 15)",
                          f"{profile}:{name}")
        defs.update(ordered)
        self.check_processes()
        self.defs = defs
        return {"$schema": SCHEMA_URI, "$defs": defs}

    def common_schema(self, key):
        """Schema of a Common Data Type from its exported base type and restrictions."""
        ct = next((c for n, c in self.m.common.items() if common_key(n) == key), None)
        if ct is None:
            self.diag.add("yaml-gap", "Common Data Type is not exported; a plain string placeholder "
                                      "is generated", key)
            self.placeholders.add(key)
            return {"type": "string"}
        r = dict(ct.get("restrictions") or {})
        base = r.pop("base_type", "")
        if base in PRIMITIVES:
            schema = dict(PRIMITIVES[base])
        else:
            if base:
                self.diag.add("yaml-issue", f"Unknown base type '{base}'", key)
            elif key == "identifier":
                pass  # Rule 21: identifier fields are strings
            else:
                self.diag.add("yaml-gap", "Common Data Type has no base_type; string applied", key)
            schema = {"type": "string"}
        if not r:
            self.diag.add("yaml-gap", "Common Data Type syntax is given only as prose (no restrictions "
                                      "exported); no syntax keywords generated", key)
            self.placeholders.add(key)
        return self.restrict(schema, r, key)

    def restrict(self, schema, r, ctx):
        """Add the keywords of the exported value restrictions to a value schema."""
        for k, v in r.items():
            if k in STATUS_RESTRICTIONS:  # used by element_schema and status_target
                continue
            if k == "allowed_values":
                if schema.get("type") != "string":
                    self.diag.add("rule-gap", "Enumeration on a non-string value: Rule 22 covers string "
                                              "fields only; enum applied", ctx)
                schema["enum"] = list(v)
                continue
            self.diag.add("rule-gap", f"Restriction '{k}' has no JSON rule (Rule 22 covers enumerations "
                                      f"only); mapped to the matching JSON Schema keyword", ctx)
            if k == "range":
                if "min" in v:
                    schema["minimum"] = v["min"]
                if "max" in v:
                    schema["maximum"] = v["max"]
            elif k == "pattern":
                schema["pattern"] = v
            elif k == "min_length":
                schema["minLength"] = v
            elif k == "max_length":
                schema["maxLength"] = v
            else:
                self.diag.add("yaml-issue", f"Restriction '{k}' does not apply to this data type", ctx)
        return schema

    def apply_conditions(self, o, view, schema):
        """Cross-element conditions as if/then, where every element they name is in the view."""
        clauses = []
        for c in self.m.conditions(o):
            names = list(c.get("if") or {}) + list(c.get("require") or []) + list(c.get("forbid") or [])
            if not all(n in schema["properties"] for n in names):
                continue
            then = {}
            if c.get("require"):
                then["required"] = list(c["require"])
            if c.get("forbid"):
                forbid = [{"required": [n]} for n in c["forbid"]]
                then["not"] = forbid[0] if len(forbid) == 1 else {"anyOf": forbid}
            clauses.append({"if": {"properties": {k: {"const": v} for k, v in c["if"].items()},
                                   "required": list(c["if"])},
                            "then": then})
            self.diag.add("rule-gap", "Cross-element conditions have no JSON rule; if/then applied",
                          f"{o.id}.{view}")
        if len(clauses) == 1:
            schema.update(clauses[0])
        elif clauses:
            schema["allOf"] = clauses
        return schema

    def build_view(self, o, view):
        if view == "query":
            items = self.view_items(o, view)
            card = items[0]["cardinality"] if items else "0+"
            self.diag.add("rule-gap", f"An Output Object with cardinality '{card}' has no JSON rule; "
                                      "array of read representations applied following the draft", o.id)
            return {"type": "array", "items": {"$ref": f"#/$defs/{o.id}.read"}}
        props = {"@type": self.type_prop(o, view)}
        required = ["@type"]

        if view == "reference":
            uid = self.m.unique_id(o)
            props[uid["identifier"]] = self.element_schema(o, uid, view)
            required.append(uid["identifier"])
            return {"type": "object", "properties": props, "required": required}

        op_inputs = []
        for op, owner in o.operations:
            if self.view_of(op, owner) == view:
                op_inputs.extend(Model.definitions(op, "Input Data Elements"))
        if o.kind == "Process" and view not in ("create", "read", "update"):
            elements = []
        else:
            muts = self.view_mutabilities(o, view)
            elements = [e for e in o.elements if e["mutability"] in muts]

        for e in elements:
            self.add_element(o, e, view, props, required)
        for inp in op_inputs:
            # Input Data Elements have no Mutability (data-objects §1): client-provided content
            e = dict(inp)
            e.setdefault("mutability", "read-write")
            self.add_element(o, e, view, props, required)

        if view == "create" and o.kind == "Resource":
            prop = self.create_processes_prop(o)
            if prop is not None:
                props["processes"] = prop

        for p in o.raw.get("operations") or []:
            for par in Model.definitions(p, "Parameters"):
                self.diag.add("rule-gap", "Operation parameters have no JSON representation rule; "
                                          "not included in any schema",
                              f"{o.id}.{p['identifier']}.{par['identifier']}")
        return self.apply_conditions(o, view, {"type": "object", "properties": props, "required": required})

    def add_element(self, o, e, view, props, required):
        ident = e["identifier"]
        st = self.status_target(e)
        if st is not None and o.kind != "Resource":
            self.diag.add("rule-gap", "Status object embedded in an object with a single schema; the "
                                      "full set of status values applies in requests too", f"{o.id}.{ident}")
        elif st is not None:
            e = self.status_element(o, e, view, st)
            if e is None:
                return
        if ident.startswith("@"):
            self.diag.add("yaml-issue", "Data element name begins with '@' (reserved)", f"{o.id}.{ident}")
        props[ident] = self.element_schema(o, e, view)
        if e.get("direct_access"):
            self.direct_access(o, e)
        on_demand = e.get("visibility") == "onDemand"
        if on_demand:
            self.diag.add("rule-gap", "Visibility 'onDemand' has no JSON rule; the element is never "
                                      "required in read views (output only on request)", f"{o.id}.{ident}")
        if self.min_card(e["cardinality"]) >= 1 and not (on_demand and view == "read"):
            required.append(ident)

    # -- status objects ----------------------------------------------------

    @staticmethod
    def client_values(o):
        """Status values a client may set: the "client_values" of the object's elements.

        None when the object is not a status object (no element exports the client/server
        partition of its values)."""
        out = None
        for e in o.elements:
            r = e.get("restrictions") or {}
            if any(k in r for k in STATUS_RESTRICTIONS):
                out = (out or []) + list(r.get("client_values") or [])
        return out

    def in_resource(self, o):
        """Whether a Data Object embeds the object directly (and so sends it in requests)."""
        return any(self.status_target(e) is o for r in self.m.objs.values() if r.kind == "Resource"
                   for e in r.elements)

    def status_target(self, e):
        """Status Component Object that a data element embeds, or None."""
        dt = e["data_type"].strip().rstrip(".")
        m = ASSOC_RE.match(dt)
        t = self.m.lookup(m.group(2) if m else dt)
        if t is None or t.kind != "Component" or self.client_values(t) is None:
            return None
        return t

    # cardinality of a status element in requests (client may omit) and in read views
    OPTIONAL_CARD = {"1": "0-1", "1+": "0+"}
    REQUIRED_CARD = {"0-1": "1", "0+": "1+"}

    def status_element(self, o, e, view, st):
        """A status element adjusted for the view, or None when it is left out."""
        ctx = f"{o.id}.{e['identifier']}"
        self.diag.add("rule-gap", "No rule covers status objects in requests; client-settable values "
                                  "from the status values table applied", ctx)
        if view in REQUEST_VIEWS:
            if not self.client_values(st):
                return None
            if st.raw.get("status_not_required_for_client_request"):
                return dict(e, cardinality=self.OPTIONAL_CARD.get(e["cardinality"], e["cardinality"]))
        elif view == "read" and st.raw.get("at_least_one_status_by_server"):
            return dict(e, cardinality=self.REQUIRED_CARD.get(e["cardinality"], e["cardinality"]))
        return e

    def direct_access(self, o, e):
        ctx = f"{o.id}.{e['identifier']}"
        self.diag.add("rule-gap", "Direct Access (sub-resource addressing) has no JSON rule; "
                                  "the inline representation is generated unchanged", ctx)
        dt = e["data_type"].strip().rstrip(".")
        m = ASSOC_RE.match(dt)
        target = self.m.lookup(m.group(2) if m else dt)
        if target is None:
            self.diag.add("yaml-issue", "Direct Access on a data element that is not an association "
                                        "with an object", ctx)
        elif e["cardinality"] not in ("1", "0-1") and \
                any(self.m.unique_id(c) is None for c in [target] + target.descendants()):
            self.diag.add("yaml-issue", "Direct Access with cardinality greater than 1 requires the "
                                        "associated object to define a Unique Identifier", ctx)

    def check_processes(self):
        """The shared Processes Object vs. the processes each Data Object supports."""
        comp = self.m.objs.get("processes")
        if comp is None:
            return
        for r in self.m.objs.values():
            if r.kind != "Resource" or not any(e["identifier"] == "processes" for e in r.elements):
                continue
            supported = self.m.supported_processes(r)
            extra = []
            for e in comp.elements:
                m = ASSOC_RE.match(e["data_type"].strip())
                t = self.m.lookup(m.group(2) if m else e["data_type"])
                if t is not None and not any(p.is_a(t) for p in supported):
                    extra.append(e["identifier"])
            if extra:
                self.diag.add("rule-gap", "The Processes Object is shared by all Data Objects; no rule "
                                          "excludes processes a Data Object does not support",
                              f"{r.id}: {', '.join(extra)}")

    def type_prop(self, o, view):
        p = {"type": "string", "const": o.id}
        all_ro = bool(o.elements) and all(e["mutability"] == "read-only" for e in o.elements)
        if view == "read" or (view is None and all_ro):
            p["readOnly"] = True
        return p

    # Input/Output item that defines the elements of each view
    VIEW_IO = {"create": ("input", "Object"), "read": ("output", "Object"),
               "query": ("output", "Object")}
    DEFAULT_MUTS = {"create": {"create-only", "read-write"},
                    "read": {"create-only", "read-write", "read-only"}}

    def view_items(self, o, view, ops=None):
        """Input/Output items of the operations of a view that name the object itself."""
        side, kind = self.VIEW_IO[view]
        out = []
        for op, owner in ops if ops is not None else \
                [(op, ow) for op, ow in o.operations if self.view_of(op, ow) == view]:
            for item in self.m.io(op, owner, side):
                if item["kind"] == kind:
                    t = self.m.io_target(item, owner)
                    if t is not None and o.is_a(t):
                        out.append(item)
        return out

    def view_mutabilities(self, o, view):
        """Mutability values of the elements in a view, from the operations' Input/Output."""
        if view is None:  # a component has a single schema
            return self.DEFAULT_MUTS["read"]
        if view == "update":  # Rules 5-7: only read-write elements can be changed
            return {"read-write"}
        if view == "request":  # a status object sent by a client: everything it can set
            return {"create-only", "read-write"}
        items = self.view_items(o, view)
        if not items and view == "read":
            # a process without a Read operation: the representation its operations return
            items = self.view_items(o, view, o.operations)
        if not items:
            self.diag.add("heuristic", "No operation Input/Output describes this view; elements "
                                       "selected by mutability (create: create-only, read-write; "
                                       "read: all)", f"{o.id}.{view}")
            return self.DEFAULT_MUTS[view]
        return {m for item in items for m in item["elements"]}

    # -- elements ----------------------------------------------------------

    @staticmethod
    def min_card(card):
        return int(re.match(r"\d+", card).group(0)) if re.match(r"\d+", card) else 0

    def element_schema(self, o, e, view):
        ctx = f"{o.id}.{e['identifier']}"
        dt = e["data_type"].strip()
        if dt.endswith("."):
            self.diag.add("yaml-issue", "Data type value has a trailing period", ctx)
            dt = dt.rstrip(".")
        card = e["cardinality"]
        r = dict(e.get("restrictions") or {})
        if view == "request" and any(k in r for k in STATUS_RESTRICTIONS):
            r["allowed_values"] = list(r.get("client_values") or [])
        key_pattern, value_range = r.pop("key_pattern", None), r.pop("value_range", None)

        m = ASSOC_RE.match(dt)
        d = DICT_RE.match(dt)
        if (key_pattern or value_range) and not d and not (m and m.group(1) in DICTIONARY):
            self.diag.add("yaml-issue", "key_pattern/value_range on a data element that is not a "
                                        "Dictionary", ctx)
        if m:
            assoc, target = m.group(1), m.group(2)
            item = self.restrict(self.target_schema(target, assoc, view, ctx), r, ctx)
            if assoc in LABELLED:
                if not (self.is_object(target)):
                    self.diag.add("rule-gap", f"{assoc} of a primitive type: Rule 9/11 only cover "
                                              f"associations with objects", ctx)
                item = {"type": "object",
                        "properties": {"label": {"type": "string"}, "object": item},
                        "required": ["label", "object"]}
                schema = self.apply_cardinality(item, card, ctx, assoc)
            elif assoc in DICTIONARY:
                schema = self.dictionary(item, card, ctx, assoc)
            else:
                if assoc == "Aggregation" and card in ("1", "0-1"):
                    self.diag.add("rule-gap", "Aggregation with cardinality 1 or 0-1: "
                                              "Rule 8 only covers 0+ and 1+", ctx)
                schema = self.apply_cardinality(item, card, ctx, assoc)
        elif d:
            self.diag.add("rule-gap", "Dictionary[Type] primitive has no mapping in Primitive Type Mappings "
                                      "(mapped to object with additionalProperties)", ctx)
            item = self.target_schema(d.group(1), None, view, ctx)
            if value_range:
                r["range"] = value_range
            item = self.restrict(item, r, ctx)
            schema = self.dictionary(item, card, ctx, "Dictionary")
        else:
            # data-objects "Composition": notation "Composition[Type] or Type"
            target = self.m.lookup(dt)
            if target is not None and target.kind == "Resource" and not norm_name(dt)[1]:
                self.diag.add("rule-gap", "Bare 'Type' notation (= Composition[Type] in data-objects) is "
                                          "not mentioned in the Association Rules; embedded as composition",
                              ctx)
            item = self.restrict(self.target_schema(dt, "Composition", view, ctx), r, ctx)
            schema = self.apply_cardinality(item, card, ctx, "Composition")
        if key_pattern and isinstance(schema.get("additionalProperties"), dict):
            self.diag.add("rule-gap", "Restriction 'key_pattern' has no JSON rule (Rule 22 covers "
                                      "enumerations only); mapped to the matching JSON Schema keyword", ctx)
            schema["propertyNames"] = {"pattern": key_pattern}

        return self.annotate(schema, e["mutability"], view, ctx)

    def is_object(self, name):
        return self.m.lookup(name) is not None

    def apply_cardinality(self, item, card, ctx, assoc):
        if card in ("1", "0-1"):
            return dict(item)
        if card == "0+":
            return {"type": "array", "items": item}
        if card == "1+":
            return {"type": "array", "items": item, "minItems": 1}
        m = re.match(r"^(\d+)-(\d+)$", card)
        if m:
            self.diag.add("rule-gap", f"Cardinality '{card}' is not covered by Rules 1-4; "
                                      f"mapped to an array with minItems/maxItems", ctx)
            s = {"type": "array", "items": item}
            if int(m.group(1)) > 0:
                s["minItems"] = int(m.group(1))
            s["maxItems"] = int(m.group(2))
            return s
        self.diag.add("yaml-issue", f"Unknown cardinality notation '{card}'", ctx)
        return {"type": "array", "items": item}

    def dictionary(self, item, card, ctx, assoc):
        s = {"type": "object", "additionalProperties": item}
        if card == "1+":
            self.diag.add("rule-gap", f"{assoc} with cardinality 1+: Rules 10/12 do not define how "
                                      f"cardinality maps to a JSON object; minProperties 1 applied", ctx)
            s["minProperties"] = 1
        elif card not in ("0+", "0-1", "1"):
            self.diag.add("rule-gap", f"{assoc} with cardinality '{card}' has no mapping", ctx)
        return s

    def annotate(self, schema, mut, view, ctx):
        if mut == "read-only":
            schema["readOnly"] = True
        elif mut == "create-only":
            if view == "create":
                schema["writeOnly"] = True
            elif view == "read":
                self.diag.add("rule-gap", "Annotation of create-only elements in read responses is "
                                          "not defined (Rule 6 covers requests only); readOnly applied "
                                          "following the draft schemas", ctx)
                schema["readOnly"] = True
            elif view in (None, "request"):
                self.diag.add("rule-gap", "Create-only element in a component object: components have a "
                                          "single schema, Rule 6 (writeOnly in requests, excluded from "
                                          "update) cannot be applied; no annotation", ctx)
        elif mut not in ("read-write",):
            self.diag.add("yaml-issue", f"Unknown mutability '{mut}'", ctx)
        return schema

    # -- type resolution ---------------------------------------------------

    def target_schema(self, name, assoc, view, ctx):
        name = name.strip().rstrip(".")
        if name in PRIMITIVES:
            return dict(PRIMITIVES[name])
        if name in PRIMITIVES_NOT_IN_RULES:
            self.diag.add("rule-gap", f"Primitive type '{name}' is not listed in Primitive Type Mappings"
                          + ("; unevaluatedProperties: true applied (composable; Rule 24 names "
                             "additionalProperties: true)" if name == "Object" else ""), ctx)
            return dict(PRIMITIVES_NOT_IN_RULES[name])
        if name in COMMON_TYPES or name in self.m.common:
            self.common_used.add(common_key(name))
            return {"$ref": f"#/$defs/{common_key(name)}"}
        m = EXTERNAL_RE.match(name)
        if m:
            self.external_used[m.group(2)] = m.group(1)
            return {"$ref": f"#/$defs/{m.group(2)}"}

        o = self.m.lookup(name, ctx)
        if o is None:
            self.diag.add("yaml-issue", f"Unknown data type '{name}'", ctx)
            return {}
        is_ref = norm_name(name)[1]
        cands = [o] + o.descendants()
        refs = [{"$ref": f"#/$defs/{self.ref_name(c, assoc, view, is_ref, ctx)}"} for c in cands]
        if len(refs) == 1:
            return refs[0]
        self.diag.add("rule-gap", "Polymorphism (an object extending the referenced base object may be "
                                  "used in its place) has no JSON rule; oneOf over all candidates applied",
                      f"{ctx} -> {', '.join(c.id for c in cands)}")
        return {"oneOf": refs}

    def ref_name(self, o, assoc, view, is_ref, ctx):
        if o.kind == "Component":
            if view in REQUEST_VIEWS and self.has_def(o, "request"):
                return f"{o.id}.request"
            return o.id
        if is_ref or assoc not in COMPOSITIONS:
            # Rule 8: an aggregation carries at minimum the primary identifier
            if self.has_def(o, "reference"):
                return f"{o.id}.reference"
            self.diag.add("yaml-gap", f"Referenced {o.kind} Object has no derivable Unique Identifier; "
                                      "read view used", ctx)
            return f"{o.id}.read"
        if o.kind == "Resource":
            v = view if view in ("create", "read", "update") and self.has_def(o, view) else "read"
            return f"{o.id}.{v}"
        if assoc in COMPOSITIONS and view in ("create", "update") and self.has_def(o, view):
            return f"{o.id}.{view}"
        return f"{o.id}.read"

    def create_processes_prop(self, o):
        """'processes' of a create view: the Process Objects in the Create operation's Input."""
        cands = []
        for op, owner in o.operations:
            if self.view_of(op, owner) != "create":
                continue
            for item in self.m.io(op, owner, "input"):
                t = self.m.io_target(item, owner) if item["kind"] == "Object" else None
                if t is not None and t.kind == "Process":
                    cands.append(t)
        if not cands:
            return None
        if not any(e["identifier"] == "processes" for e in o.elements):
            self.diag.add("yaml-issue", "Create Input carries a Process Object, but the Data Object has "
                                        "no 'processes' data element", o.id)
        comp = self.m.objs.get("processes")
        slots = {}
        for c in cands:
            slot = None
            for e in comp.elements if comp is not None else []:
                m = ASSOC_RE.match(e["data_type"].strip())
                t = self.m.lookup(m.group(2) if m else e["data_type"])
                if t is not None and c.is_a(t):
                    slot = e["identifier"]
            if slot is None:
                self.diag.add("yaml-issue", f"Process Object '{c.id}' in the Create Input has no data "
                                            f"element in the Processes Object", o.id)
                continue
            slots.setdefault(slot, []).append({"$ref": f"#/$defs/{c.id}.create"})
        self.diag.add("rule-conflict", "Rule 18 requires process data in the 'processes' element of "
                                       "create requests, but 'processes' is read-only and Rule 5 forbids "
                                       "read-only properties in requests; Rule 18 applied",
                      o.id)
        return {"type": "object",
                "properties": {
                    "@type": {"type": "string", "const": "processes"},
                    **{slot: {"type": "array", "items": refs[0] if len(refs) == 1 else {"oneOf": refs}}
                       for slot, refs in slots.items()}},
                "required": ["@type"]}


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

LINE_WIDTH = 100


def _is_flat(v):
    """An object or array without nested objects (arrays of scalars allowed)."""
    if isinstance(v, dict):
        return all(not isinstance(x, dict) and _is_flat(x) for x in v.values())
    if isinstance(v, list):
        return all(not isinstance(x, (dict, list)) for x in v)
    return True


def _inline(v):
    if isinstance(v, dict):
        if not v:
            return "{}"
        return "{ " + ", ".join(f"{json.dumps(k)}: {_inline(x)}" for k, x in v.items()) + " }"
    if isinstance(v, list):
        return "[" + ", ".join(_inline(x) for x in v) + "]"
    return json.dumps(v, ensure_ascii=False)


def dump_compact(v, indent=0, prefix_len=0, step=2):
    """JSON in the style of the draft's schema blocks: flat objects and arrays on one line."""
    if _is_flat(v) or not isinstance(v, (dict, list)):
        s = _inline(v)
        if not isinstance(v, (dict, list)) or indent + prefix_len + len(s) <= LINE_WIDTH:
            return s
    pad, inner = " " * indent, " " * (indent + step)
    if isinstance(v, dict):
        items = [f"{inner}{json.dumps(k)}: "
                 f"{dump_compact(x, indent + step, len(json.dumps(k)) + 2, step)}" for k, x in v.items()]
        return "{\n" + ",\n".join(items) + "\n" + pad + "}"
    items = [inner + dump_compact(x, indent + step, 0, step) for x in v]
    return "[\n" + ",\n".join(items) + "\n" + pad + "]"


def dump(v, expanded=False):
    if expanded:
        return json.dumps(v, indent=2, ensure_ascii=False) + "\n"
    return dump_compact(v) + "\n"


def split_doc(name, defn, kind):
    """One definition shaped like a schema block of draft-ietf-rpp-json."""
    if kind in ("Process", "Resource"):
        return {"$schema": SCHEMA_URI, "$ref": f"#/$defs/{name}", "$defs": {name: defn}}
    return {"$defs": {name: defn}}


def iter_refs(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                yield v
            else:
                yield from iter_refs(v)
    elif isinstance(node, list):
        for v in node:
            yield from iter_refs(v)


def self_check(bundle):
    problems = []
    names = set(bundle["$defs"])
    for ref in iter_refs(bundle):
        if ref.startswith("#/$defs/") and ref[len("#/$defs/"):] not in names:
            problems.append(f"unresolved $ref {ref}")
    if HAS_JSONSCHEMA:
        try:
            Draft202012Validator.check_schema(bundle)
        except SchemaError as e:
            problems.append(f"invalid JSON Schema: {e.message}")
    else:
        problems.append("jsonschema not installed: meta-schema validation skipped")
    return problems


# ---------------------------------------------------------------------------
# Comparison with the draft
# ---------------------------------------------------------------------------

def draft_schema_blocks(lines):
    """(start, end, parsed block) of every ```json block in the "JSON Schema Definitions" chapter.

    lines[start:end] is the block content, without the fences; the block is {} if not valid JSON."""
    blocks = []
    h1 = ""
    in_code = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            if line.strip() == "```json" and h1 == "JSON Schema Definitions":
                start = i + 1
                j = i + 1
                while j < len(lines) and lines[j].strip() != "```":
                    j += 1
                try:
                    block = json.loads("\n".join(lines[start:j]))
                except json.JSONDecodeError:
                    block = {}
                blocks.append((start, j, block if isinstance(block, dict) else {}))
                i = j + 1
                continue
            in_code = not in_code
        elif not in_code:
            m = re.match(r"^#\s+(.*?)\s*(\{#.*\})?\s*$", line)
            if m:
                h1 = m.group(1)
        i += 1
    return blocks


def extract_draft_defs(md_path):
    """$defs of every schema block in the "JSON Schema Definitions" chapter."""
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    defs, dupes = {}, []
    for start, _, block in draft_schema_blocks(lines):
        for name, d in (block.get("$defs") or {}).items():
            if name in defs:
                dupes.append((name, start))
            defs[name] = (d, start)
    return defs, dupes


def replace_in_draft(bundle, kinds, placeholders, md_path, out_path, expanded=False):
    """Replace every draft schema block that has a generated counterpart; returns a report.

    A block is replaced by the generated definition under its Rule 27 key, shaped like
    --split. Blocks without a counterpart, with more than one $defs entry, or whose
    counterpart is already placed by an earlier block or is only a placeholder (an
    external type, a Common Data Type without exported syntax) are left untouched. The report
    ends with every generated definition that has no place in the draft."""
    gen = bundle["$defs"]
    text = Path(md_path).read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks = draft_schema_blocks(lines)
    ddefs, _ = extract_draft_defs(md_path)
    placed, replaced, untouched, edits = set(), [], [], []
    for start, end, block in blocks:
        names = list((block.get("$defs") or {}).keys())
        if len(names) != 1:
            untouched.append((start, ", ".join(names) or "(no $defs)",
                              "invalid JSON" if not block else f"{len(names)} $defs entries"))
            continue
        dname = names[0]
        gname = map_draft_name(dname, ddefs, gen)
        if gname is None:
            untouched.append((start, dname, "no generated counterpart"))
        elif gname in placeholders:
            placed.add(gname)
            untouched.append((start, dname, f"`{gname}` is generated only as a placeholder"))
        elif gname in placed:
            untouched.append((start, dname, f"`{gname}` already placed by an earlier block"))
        else:
            placed.add(gname)
            doc = split_doc(gname, gen[gname], kinds.get(gname, "Common"))
            edits.append((start, end, dump(doc, expanded).rstrip("\n").split("\n")))
            replaced.append((start, dname, gname))
    for start, end, new in reversed(edits):
        lines[start:end] = new
    Path(out_path).write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")

    out = [f"# Schema replacement in {md_path}" + (f" (written to {out_path})" if out_path != md_path else ""),
           "", f"## Replaced: {len(replaced)}", ""]
    out += [f"- line {s + 1}: `{d}` -> `{g}`" + ("" if d == g else " (key renamed)") for s, d, g in replaced]
    out += ["", f"## Left untouched: {len(untouched)}", ""]
    out += [f"- line {s + 1}: `{d}`: {why}" for s, d, why in untouched]
    unused = [n for n in gen if n not in placed]
    out += ["", f"## Unused generated schemas (no place in the draft): {len(unused)}", ""]
    for n in unused:
        out += [f"### `{n}`", "", "```json",
                dump(split_doc(n, gen[n], kinds.get(n, "Common")), expanded).rstrip("\n"), "```", ""]
    return "\n".join(out) + "\n"


def flatten_draft(defn, ddefs, notes, seen=None):
    """Merge allOf / oneOf / $ref-alias definitions into (properties, required)."""
    seen = seen or set()
    props, required = dict(defn.get("properties") or {}), list(defn.get("required") or [])
    for kw in ("additionalProperties", "unevaluatedProperties"):
        if kw in defn and defn[kw] is False:
            notes.add(f"{kw}: false")
    ref = defn.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/$defs/"):
        tgt = ref[len("#/$defs/"):]
        notes.add(f"$ref alias -> {tgt}")
        if tgt in ddefs and tgt not in seen:
            p, r = flatten_draft(ddefs[tgt][0], ddefs, notes, seen | {tgt})
            props = {**p, **props}
            required += r
    for member in defn.get("allOf") or []:
        notes.add("allOf")
        p, r = flatten_draft(member, ddefs, notes, seen)
        props.update(p)
        required += r
    branches = defn.get("oneOf") or []
    if branches:
        notes.add("oneOf")
        reqs = []
        for member in branches:
            p, r = flatten_draft(member, ddefs, notes, seen)
            for k, v in p.items():
                props.setdefault(k, v)
            reqs.append(set(r))
        required += sorted(set.intersection(*reqs))
    return props, sorted(set(required))


def draft_type_const(defn, ddefs, seen=None):
    notes = set()
    props, _ = flatten_draft(defn, ddefs, notes)
    t = props.get("@type") or {}
    return t.get("const")


def map_draft_name(name, ddefs, gen_defs):
    """Generated $defs key (Rule 27) corresponding to a draft $defs key.

    Matching is case-insensitive and tolerant of the draft's naming styles
    ("<x>Object", owner suffixes, operation names without the process stem), so
    that keys that differ from Rule 27 are still paired and can be reported."""
    if name in gen_defs:
        return name
    lower = {g.lower(): g for g in gen_defs}
    if name.lower() in lower:
        return lower[name.lower()]
    parts = name.split(".")
    tc = draft_type_const(ddefs[name][0], ddefs) if name in ddefs else None
    bases = [b for b in (tc, parts[0], parts[0][: -len("Object")] if parts[0].endswith("Object") else None)
             if b]
    if len(parts) >= 3:
        bases.insert(0, f"{parts[2]}{uc_first(parts[0])}")
    for base in bases:
        if len(parts) == 1:
            if base.lower() in lower:
                return lower[base.lower()]
            continue
        view = parts[1].lower()
        cands = [g for g in gen_defs if g.lower().startswith(base.lower() + ".")]
        for match in (lambda v: v == view, lambda v: v.endswith(view)):
            hit = next((g for g in cands if match(g.split(".", 1)[1].lower())), None)
            if hit:
                return hit
    return None


def shape(p, mapref):
    if not isinstance(p, dict):
        return p
    s = {}
    for k in ("type", "format", "readOnly", "writeOnly", "const", "enum", "pattern",
              "minimum", "maximum", "minLength", "maxLength", "minItems", "maxItems", "minProperties",
              "propertyNames",
              "unevaluatedProperties"):
        if k in p:
            s[k] = p[k]
    if "$ref" in p:
        s["$ref"] = mapref(p["$ref"])
    if "oneOf" in p:
        s["oneOf"] = sorted(mapref(x.get("$ref", "?")) for x in p["oneOf"])
    if "items" in p:
        s["items"] = shape(p["items"], mapref)
    if "additionalProperties" in p:
        s["additionalProperties"] = shape(p["additionalProperties"], mapref)
    if "properties" in p:
        s["properties"] = {k: shape(v, mapref) for k, v in p["properties"].items()}
    if "required" in p:
        s["required"] = sorted(p["required"])
    return s


def flat_paths(s, prefix=""):
    out = {}
    if isinstance(s, dict):
        for k, v in s.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and v:
                out.update(flat_paths(v, path))
            else:
                out[path] = v
    else:
        out[prefix] = s
    return out


CONSTRAINT_KEYS = {"enum", "pattern", "minimum", "maximum", "minLength", "maxLength",
                   "propertyNames", "maxItems", "const"}


def compare(bundle, md_path):
    gen = bundle["$defs"]
    ddefs, dupes = extract_draft_defs(md_path)
    mapping = {n: map_draft_name(n, ddefs, gen) for n in ddefs}

    def map_draft_ref(ref):
        n = ref[len("#/$defs/"):] if ref.startswith("#/$defs/") else ref
        return mapping.get(n) or f"<{n}>"

    def map_gen_ref(ref):
        return ref[len("#/$defs/"):] if ref.startswith("#/$defs/") else ref

    out = ["# Comparison: generated schemas vs. draft-ietf-rpp-json", ""]
    for name, line in dupes:
        out.append(f"- DUPLICATE draft $defs name `{name}` (block at line {line}); the later one wins")
    if dupes:
        out.append("")

    for dname, (ddef, line) in ddefs.items():
        gname = mapping[dname]
        out.append(f"## `{dname}` (draft line {line}) -> " + (f"`{gname}`" if gname else "NO COUNTERPART"))
        if gname and gname != dname:
            kind = "case only" if gname.lower() == dname.lower() else "name"
            out.append(f"- KEY MISMATCH ({kind}): draft `{dname}`, Rule 27 key `{gname}`")
        notes = set()
        dprops, dreq = flatten_draft(ddef, ddefs, notes)
        for n in sorted(notes):
            out.append(f"- draft structure: {n}")
        if not gname:
            out.append("")
            continue
        g = gen[gname]
        gprops, greq = g.get("properties") or {}, sorted(g.get("required") or [])
        only_d = [k for k in dprops if k not in gprops]
        only_g = [k for k in gprops if k not in dprops]
        if only_d:
            out.append(f"- properties only in draft: {', '.join(only_d)}")
        if only_g:
            out.append(f"- properties only in generated: {', '.join(only_g)}")
        if sorted(dreq) != greq:
            out.append(f"- required: draft={sorted(dreq)} generated={greq}")
        if not dprops and not gprops:  # a value type, e.g. a Common Data Type
            a = flat_paths(shape(ddef, map_draft_ref))
            b = flat_paths(shape(g, map_gen_ref))
            for path in sorted(set(a) | set(b)):
                if a.get(path) != b.get(path):
                    tag = " [prose constraint]" if path in CONSTRAINT_KEYS and path not in b else ""
                    out.append(f"- `{path}`: draft={json.dumps(a.get(path))} "
                               f"generated={json.dumps(b.get(path))}{tag}")
        for k in dprops:
            if k not in gprops:
                continue
            a = flat_paths(shape(dprops[k], map_draft_ref))
            b = flat_paths(shape(gprops[k], map_gen_ref))
            for path in sorted(set(a) | set(b)):
                if a.get(path) != b.get(path):
                    leaf = path.split(".")[-1]
                    tag = " [prose constraint]" if leaf in CONSTRAINT_KEYS and path not in b else ""
                    if k == "@type" and leaf == "const":
                        tag = " [@type value]"
                    out.append(f"- `{k}.{path}`: draft={json.dumps(a.get(path))} "
                               f"generated={json.dumps(b.get(path))}{tag}")
        out.append("")

    mismatched = [n for n, g in mapping.items() if g and g != n]
    out.insert(2, f"Draft keys that differ from the Rule 27 key: {len(mismatched)} of {len(ddefs)}"
                  f" (case only: {sum(mapping[n].lower() == n.lower() for n in mismatched)})\n")
    mapped = {v for v in mapping.values() if v}
    missing = [n for n in gen if n not in mapped]
    out.append("## Generated definitions without a draft counterpart")
    out.append("")
    out.append(", ".join(f"`{n}`" for n in missing) or "(none)")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", help="object model export (YAML)")
    ap.add_argument("-o", "--output", help="bundled schema output file (default: stdout)")
    ap.add_argument("--split", metavar="DIR", help="also write one file per definition")
    ap.add_argument("--compare", metavar="DRAFT", help="compare with the schemas in DRAFT (.md)")
    ap.add_argument("--compare-out", metavar="FILE", help="comparison output file (default: stdout)")
    ap.add_argument("--replace", metavar="DRAFT",
                    help="replace the schema blocks of DRAFT (.md) in place with their generated "
                         "counterparts and print the generated schemas left unused")
    ap.add_argument("--replace-out", metavar="FILE",
                    help="write the updated draft to FILE instead of DRAFT")
    ap.add_argument("--diagnostics", metavar="FILE", help="write diagnostics to FILE")
    ap.add_argument("-q", "--quiet", action="store_true", help="do not print diagnostics to stderr")
    ap.add_argument("--expanded", action="store_true",
                    help="one JSON value per line instead of the draft's compact style")
    args = ap.parse_args()

    data = yaml.safe_load(Path(args.model).read_text(encoding="utf-8"))
    diag = Diagnostics()
    model = Model(data, diag)
    gen = Generator(model, diag)
    bundle = gen.build()

    if args.replace_out and not args.replace:
        ap.error("--replace-out requires --replace")

    text = dump(bundle, args.expanded)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    elif not args.replace and (not args.compare or args.compare_out):
        sys.stdout.write(text)

    kinds = {gen.def_name(o, v): o.kind for o in model.objs.values() for v in gen.views_for(o)}
    if args.split:
        outdir = Path(args.split)
        outdir.mkdir(parents=True, exist_ok=True)
        for name, defn in bundle["$defs"].items():
            doc = split_doc(name, defn, kinds.get(name, "Common"))
            (outdir / f"{name}.json").write_text(dump(doc, args.expanded), encoding="utf-8")

    problems = self_check(bundle)
    for p in problems:
        print(f"SELF-CHECK: {p}", file=sys.stderr)

    rendered = diag.render()
    if args.diagnostics:
        Path(args.diagnostics).write_text("# Generator diagnostics\n\n" + rendered, encoding="utf-8")
    if not args.quiet:
        print(rendered, file=sys.stderr)

    if args.compare:
        cmp_text = compare(bundle, args.compare)
        if args.compare_out:
            Path(args.compare_out).write_text(cmp_text, encoding="utf-8")
        else:
            sys.stdout.write(cmp_text)

    if args.replace:  # after --compare, which may read the same draft
        sys.stdout.write(replace_in_draft(bundle, kinds, gen.placeholders, args.replace,
                                          args.replace_out or args.replace, args.expanded))

    return 1 if any(not p.startswith("jsonschema not installed") for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main())
