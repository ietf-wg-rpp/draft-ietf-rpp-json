#!/usr/bin/env python3
"""
gen_json_schema.py

Builds JSON Schema (draft 2020-12) definitions for the RPP data objects from
the structured object model export of draft-ietf-rpp-data-objects (YAML),
following the JSON Representation Rules of draft-ietf-rpp-json.

Usage:
    python3 gen_json_schema.py MODEL.yaml [-o OUT.json] [--split DIR]
                               [--compare DRAFT.md] [--compare-out FILE]
                               [--diagnostics FILE] [--expanded] [-q]

  MODEL.yaml        object model export (e.g. .work/draft-ietf-rpp-data-objects.yaml)
  -o OUT.json       write the bundled schema (all $defs) to OUT.json (default: stdout)
  --split DIR       additionally write one file per definition, shaped like the
                    schema blocks in draft-ietf-rpp-json
  --compare DRAFT   compare generated definitions with the schemas in the
                    "JSON Schema Definitions" chapter of DRAFT
  --compare-out F   write the comparison to F instead of stdout
  --diagnostics F   write generator diagnostics (rule gaps, YAML gaps, heuristics) to F
  -q                do not print diagnostics to stderr

Generation decisions (precedence: draft rules > YAML content > draft schema shape):

  * $defs names derive from the YAML identifier: components "<id>", resources
    "<id>.create|read|update|reference", processes "<id>.create|read" plus one
    view per operation carrying input data elements (e.g. "<id>.reject").
  * Inheritance ("extends") is flattened (draft section "Inheritance").
  * Polymorphism: a reference to a base object accepts every object extending
    it, expressed as "oneOf" over the candidates (each fixed by its "@type").
  * Prose constraints are NOT converted to keywords; only the structured
    attributes (cardinality, mutability, data type) are used.
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
    "Object":                      {"type": "object", "additionalProperties": True},
    "Fully Qualified Domain Name": {"type": "string", "format": "hostname"},
}

# Common Data Types: name -> $defs name. Their syntax is not in the YAML export.
COMMON_TYPES = {
    "Identifier":        "identifier",
    "Client Identifier": "clientIdentifier",
    "Phone Number":      "phoneNumber",
}

ASSOC_RE = re.compile(r"^(Aggregation|Composition|LabelledAggregation|DictionaryAggregation|"
                      r"LabelledComposition|DictionaryComposition)\[(.+)\]$")
DICT_RE = re.compile(r"^Dictionary\[(.+)\]$")
EXTERNAL_RE = re.compile(r"^External:([^:]+):(.+)$")

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
        """Normalised operation name: "transferReject" on transferProcess -> "reject"."""
        oid = op["identifier"]
        stem = owner.stem() if owner.kind == "Process" else ""
        if stem and oid.startswith(stem) and len(oid) > len(stem):
            return lc_first(oid[len(stem):])
        return oid

    def owner_of(self, proc):
        """Owner resource of an object-specific process, derived from its identifier."""
        for base in proc.ancestors():
            suffix = uc_first(base.id)
            if base.kind == "Process" and proc.id.endswith(suffix) and proc.id != base.id:
                prefix = proc.id[: -len(suffix)]
                for r in self.objs.values():
                    if r.kind == "Resource" and r.id.startswith(prefix):
                        self.diag.add("yaml-gap",
                                      "Owner Data Object of an object-specific Process Object "
                                      "is not exported; derived from the identifier prefix",
                                      f"{proc.id} -> {r.id}")
                        return r
        return None

    def unique_id(self, o):
        """Unique Identifier element; not exported in the YAML, so derived heuristically."""
        cands = [e for e in o.elements if e["cardinality"] == "1"]
        pick = None
        if o.kind == "Process":
            pick = next((e for e in o.elements if e["identifier"] == "processId"), None)
        if pick is None:
            pick = next((e for e in cands if e["data_type"].rstrip(".")
                         in ("Identifier", "Fully Qualified Domain Name")), None)
        if pick is None:
            pick = next((e for e in cands if e["identifier"] in ("id", "name")), None)
        if pick is not None:
            self.diag.add("yaml-gap",
                          "'Unique Identifier' object attribute is not exported; "
                          "derived heuristically for the reference view",
                          f"{o.id} -> {pick['identifier']}")
        return pick


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class Generator:
    def __init__(self, model, diag):
        self.m = model
        self.diag = diag
        self.defs = {}
        self.common_used = set()
        self.external_used = {}

    # -- views -------------------------------------------------------------

    def views_for(self, o):
        if o.kind == "Component":
            return [None]
        sfx = [Model.op_suffix(op, owner) for op, owner in o.operations]
        if o.kind == "Process":
            views = ["create", "read"]
            if "update" in sfx:
                views.append("update")
            for op, owner in o.operations:
                s = Model.op_suffix(op, owner)
                if op.get("inputs") and s not in views:
                    views.append(s)
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
        for name in sorted(self.common_used):
            defs[name] = {"type": "string",
                          "$comment": "Common Data Type: syntax not available in the object model export"}
            self.diag.add("yaml-gap", "Common Data Types (syntax, length, pattern) are not exported; "
                                      "a plain string placeholder is generated", name)
        for name, profile in self.external_used.items():
            defs[name] = {"type": "object",
                          "$comment": f"External type from {profile}: definition not available "
                                      f"in the object model export"}
            self.diag.add("yaml-gap", "External type definition is not exported; "
                                      "an open object placeholder is generated (Rule 15)",
                          f"{profile}:{name}")
        defs.update(ordered)
        self.defs = defs
        return {"$schema": SCHEMA_URI, "$defs": defs}

    def build_view(self, o, view):
        if view == "query":
            self.diag.add("rule-gap", "Query response representation is not defined by a rule; "
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
            if Model.op_suffix(op, owner) == view:
                op_inputs.extend(op.get("inputs") or [])
        if o.kind == "Process" and view not in ("create", "read", "update"):
            elements = []
        else:
            elements = [e for e in o.elements if self.included(e, view)]

        for e in elements:
            self.add_element(o, e, view, props, required)
        for inp in op_inputs:
            e = dict(inp)
            e.setdefault("mutability", (inp.get("extra_attributes") or {}).get("mutability", "read-write"))
            self.add_element(o, e, view, props, required)

        if view == "create" and o.kind == "Resource" and \
                any(e["identifier"] == "processes" for e in o.elements):
            props["processes"] = self.create_processes_prop(o)

        for p in o.raw.get("operations") or []:
            for par in p.get("params") or []:
                self.diag.add("rule-gap", "Operation parameters have no JSON representation rule; "
                                          "not included in any schema",
                              f"{o.id}.{p['identifier']}.{par['identifier']}")
        return {"type": "object", "properties": props, "required": required}

    def add_element(self, o, e, view, props, required):
        ident = e["identifier"]
        if ident.startswith("@"):
            self.diag.add("yaml-issue", "Data element name begins with '@' (reserved)", f"{o.id}.{ident}")
        props[ident] = self.element_schema(o, e, view)
        if self.min_card(e["cardinality"]) >= 1:
            required.append(ident)

    def type_prop(self, o, view):
        p = {"type": "string", "const": o.id}
        all_ro = bool(o.elements) and all(e["mutability"] == "read-only" for e in o.elements)
        if view == "read" or (view is None and all_ro):
            p["readOnly"] = True
        return p

    @staticmethod
    def included(e, view):
        mut = e["mutability"]
        if view == "create":
            return mut in ("create-only", "read-write")
        if view == "update":
            return mut == "read-write"
        return True

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

        m = ASSOC_RE.match(dt)
        d = DICT_RE.match(dt)
        if m:
            assoc, target = m.group(1), m.group(2)
            item = self.target_schema(target, assoc, view, ctx)
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
            schema = self.dictionary(item, card, ctx, "Dictionary")
        else:
            # data-objects "Composition": notation "Composition[Type] or Type"
            target = self.m.lookup(dt)
            if target is not None and target.kind == "Resource" and not norm_name(dt)[1]:
                self.diag.add("rule-gap", "Bare 'Type' notation (= Composition[Type] in data-objects) is "
                                          "not mentioned in the Association Rules; embedded as composition",
                              ctx)
            item = self.target_schema(dt, "Composition", view, ctx)
            schema = self.apply_cardinality(item, card, ctx, "Composition")

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
            elif view is None:
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
                          + (" (Rule 24 only permits additionalProperties: true for it)"
                             if name == "Object" else ""), ctx)
            return dict(PRIMITIVES_NOT_IN_RULES[name])
        if name in COMMON_TYPES:
            self.common_used.add(COMMON_TYPES[name])
            return {"$ref": f"#/$defs/{COMMON_TYPES[name]}"}
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
            return o.id
        if o.kind == "Resource":
            if is_ref or assoc not in COMPOSITIONS:
                if self.has_def(o, "reference"):
                    return f"{o.id}.reference"
                self.diag.add("yaml-gap", "Referenced Data Object has no derivable Unique Identifier; "
                                          "read view used", ctx)
                return f"{o.id}.read"
            v = view if view in ("create", "read", "update") and self.has_def(o, view) else "read"
            return f"{o.id}.{v}"
        if assoc in COMPOSITIONS and view in ("create", "update") and self.has_def(o, view):
            return f"{o.id}.{view}"
        return f"{o.id}.read"

    def create_processes_prop(self, o):
        base = self.m.objs.get("createProcess")
        specific = [p for p in self.m.objs.values()
                    if base is not None and p is not base and p.is_a(base) and self.m.owner_of(p) is o]
        cands = specific or ([base] if base is not None else [])
        refs = [{"$ref": f"#/$defs/{c.id}.create"} for c in cands]
        self.diag.add("rule-conflict", "Rule 18 requires process data in the 'processes' element of "
                                       "create requests, but 'processes' is read-only and Rule 5 forbids "
                                       "read-only properties in requests; Rule 18 applied",
                      o.id)
        return {"type": "object",
                "properties": {
                    "@type": {"type": "string", "const": "processes"},
                    "createProcess": {"type": "array",
                                      "items": refs[0] if len(refs) == 1 else {"oneOf": refs}}},
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

def extract_draft_defs(md_path):
    """$defs of every schema block in the "JSON Schema Definitions" chapter."""
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    defs, dupes = {}, []
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
                for name, d in (block.get("$defs") or {}).items():
                    if name in defs:
                        dupes.append((name, start))
                    defs[name] = (d, start)
                i = j + 1
                continue
            in_code = not in_code
        elif not in_code:
            m = re.match(r"^#\s+(.*?)\s*(\{#.*\})?\s*$", line)
            if m:
                h1 = m.group(1)
        i += 1
    return defs, dupes


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
    """Generated $defs name corresponding to a draft $defs name."""
    if name in gen_defs:
        return name
    parts = name.split(".")
    tc = draft_type_const(ddefs[name][0], ddefs) if name in ddefs else None
    base = tc or parts[0]
    if len(parts) >= 3:
        specific = f"{parts[2]}{uc_first(parts[0])}.{parts[1]}"
        if specific in gen_defs:
            return specific
    cand = base if len(parts) == 1 else f"{base}.{parts[1]}"
    return cand if cand in gen_defs else None


def shape(p, mapref):
    if not isinstance(p, dict):
        return p
    s = {}
    for k in ("type", "format", "readOnly", "writeOnly", "const", "enum", "pattern",
              "minimum", "maximum", "minItems", "maxItems", "minProperties", "propertyNames",
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


CONSTRAINT_KEYS = {"enum", "pattern", "minimum", "maximum", "propertyNames", "maxItems", "const"}


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

    text = dump(bundle, args.expanded)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    elif not args.compare or args.compare_out:
        sys.stdout.write(text)

    if args.split:
        outdir = Path(args.split)
        outdir.mkdir(parents=True, exist_ok=True)
        kinds = {gen.def_name(o, v): o.kind for o in model.objs.values() for v in gen.views_for(o)}
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

    return 1 if any(not p.startswith("jsonschema not installed") for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main())
