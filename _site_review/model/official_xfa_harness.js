#!/usr/bin/env node
'use strict';
/*
 * official_xfa_harness.js
 *
 * Executes the ACTUAL calculate-event JavaScript embedded in CJ-D 304's XFA template
 * (data/extracted/cjd304-xfa.xml), rather than a re-implementation of it. This is the
 * "run the Commonwealth's own form" cross-check for model/worksheet.py.
 *
 * Approach (regex-based; no XML library, no dependencies):
 *   1. Find every <field name="X" ...> / <exclGroup name="X" ...> open tag and its
 *      byte offset in the document.
 *   2. Find every non-self-closing <calculate>...<script>...</script></calculate>
 *      block and its byte offset, and associate it with the NEAREST PRECEDING
 *      field/exclGroup name -- the same structure `pypdf`/XFA designer produces:
 *      each field's own <calculate> immediately follows its own opening tag.
 *   3. Find the three named script objects the calculate scripts call into
 *      (CheckIfInputsPopulated, CheckIfChildrenInputsPopulated, CalcChildCare) and
 *      build them into real JS objects exposing every top-level function they declare.
 *   4. Build ONE shared namespace object (a Proxy) where every known field name is a
 *      property holding {rawValue: ...}. Page_1..Page_4 are all bound to that SAME
 *      object, so `Page_2.Value_3a_pA` and a bare `Value_3a_pA` resolve to the same
 *      node -- this collapses the mirrored read-only fields the real form repeats on
 *      pages 2-4 (CaseName, DocketNumber, Value_1c_pA/pB) into one node, which is a
 *      simplification of true XFA scoping but is harmless: those mirrors carry no
 *      numeric logic of their own, only "this.rawValue = Page_1.X.rawValue" copies.
 *   5. Wrap each field's calculate script in `with (NS) { ... }` so its bare field
 *      references resolve through the namespace, and invoke it with `this` bound to
 *      that field's own node -- exactly as XFA does when a calculate event fires.
 *   6. Seed input fields from the JSON argument, then iterate every calculate script
 *      in document order, repeatedly, until no rawValue changes (fixed point), capped
 *      at 50 passes. This is necessary because the form's own scripts are mutually
 *      referential in places (e.g. Value_3a_pA can read Value_2c_adjustInc_pA, which
 *      in turn reads Page_3.Value_6f_pB, which is only known after 6e/6g are computed
 *      downstream of 3a) -- the real form is edited interactively over many events;
 *      one static run needs several passes to reach the same fixed point.
 *
 * Usage:
 *   node official_xfa_harness.js <path-to-cjd304-xfa.xml> <path-to-inputs.json>
 *
 * Prints every Value_* (and RadioButtonList / SS_* / na_box_* / grey_box_*) field's
 * final rawValue as JSON to stdout.
 */

const fs = require('fs');

function unescapeXml(s) {
  return s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&');
}

function loadXml(path) {
  return fs.readFileSync(path, 'utf8');
}

// ---------------------------------------------------------------------------
// 1. Field / exclGroup name declarations, with byte offset.
// ---------------------------------------------------------------------------
function collectNamePositions(xml) {
  const re = /<(field|exclGroup)\b([^>]*)>/g;
  const out = [];
  let m;
  while ((m = re.exec(xml)) !== null) {
    const attrs = m[2];
    const nameMatch = attrs.match(/\bname="([^"]+)"/);
    if (nameMatch) out.push({ pos: m.index, name: nameMatch[1] });
  }
  out.sort((a, b) => a.pos - b.pos);
  return out;
}

// Which fields are numericEdit widgets, per the XFA <ui> child that immediately
// follows each field's opening tag (<ui><numericEdit/></ui> vs <textEdit/> vs
// <checkButton/>). This matters because several calculate scripts build a
// percentage via `.toFixed(2)`, which in real JS returns a STRING -- e.g.
// Value_6d_pB.rawValue = (6c/3a).toFixed(2) -> "0.04". A later script does
// `(Value_6d_pB.rawValue + 0.10) * ...`. If rawValue really were a JS string,
// `+` would be STRING CONCATENATION ("0.04" + 0.10 -> "0.040.1"), producing
// NaN once multiplied. Adobe's XFA runtime does not have this bug: a
// numericEdit field's rawValue is normalized back to its bound numeric type on
// assignment, regardless of what expression produced the assigned value, so a
// script that assigns a formatted string to a numeric field's rawValue reads
// back a number next time. That normalization is reproduced here: any numeric
// field that receives a numeric-looking string has it coerced to a Number.
function collectNumericFieldNames(xml, namePositions) {
  const numeric = new Set();
  for (const { pos, name } of namePositions) {
    const window = xml.slice(pos, pos + 600);
    const uiMatch = window.match(/<(numericEdit|textEdit|checkButton|dateTimeEdit|choiceList)\b/);
    if (uiMatch && uiMatch[1] === 'numericEdit') numeric.add(name);
  }
  return numeric;
}

function makeNearestNameLookup(namePositions) {
  const positions = namePositions.map((p) => p.pos);
  return function nearestName(pos) {
    let lo = 0;
    let hi = positions.length - 1;
    let ans = null;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (positions[mid] <= pos) {
        ans = namePositions[mid].name;
        lo = mid + 1;
      } else {
        hi = mid - 1;
      }
    }
    return ans;
  };
}

// ---------------------------------------------------------------------------
// 2. Calculate-script blocks (skip self-closing <calculate override="error"/>,
//    which never has a <script> child -- those belong to unrelated pagination
//    fields (MasterPageIndex etc.) outside Page_1..Page_4 and are not reached by
//    this regex anyway, since it requires a <script> to follow immediately).
// ---------------------------------------------------------------------------
function collectCalcScripts(xml) {
  const re = /<calculate([^>]*)>\s*<script[^>]*>([\s\S]*?)<\/script\s*>/g;
  const out = [];
  let m;
  while ((m = re.exec(xml)) !== null) {
    out.push({ pos: m.index, body: unescapeXml(m[2]) });
  }
  return out;
}

// ---------------------------------------------------------------------------
// 3. Named script objects (variables subform): CheckIfInputsPopulated,
//    CheckIfChildrenInputsPopulated, CalcChildCare, and others not on the
//    calculation path (ClearComputedFields, ClearInputs, ColorFieldsValidation,
//    CheckIfChildrenCreditsPopulated) -- harmless to build, unused.
// ---------------------------------------------------------------------------
function collectNamedScriptObjects(xml) {
  const re = /<script contentType="application\/x-javascript" name="([^"]+)"\s*>([\s\S]*?)<\/script\s*>/g;
  const out = {};
  let m;
  while ((m = re.exec(xml)) !== null) {
    out[m[1]] = unescapeXml(m[2]);
  }
  return out;
}

// Find only TOP-LEVEL `function name(...)` declarations in a script body (brace
// depth 0), skipping string/comment content so braces inside them don't confuse
// the depth counter. CheckIfInputsPopulated nests a `color1f` helper inside
// validateInput1f() -- that name must NOT be returned, since it is out of scope
// at the top level (a naive whole-body regex found it and crashed with a
// ReferenceError when it appeared in the returned object literal).
function topLevelFunctionNames(body) {
  const names = [];
  let depth = 0;
  let i = 0;
  const n = body.length;
  const fnDeclRe = /^function\s+([A-Za-z_$][\w$]*)\s*\(/;
  while (i < n) {
    const two = body.slice(i, i + 2);
    if (two === '//') {
      const end = body.indexOf('\n', i);
      i = end === -1 ? n : end + 1;
      continue;
    }
    if (two === '/*') {
      const end = body.indexOf('*/', i + 2);
      i = end === -1 ? n : end + 2;
      continue;
    }
    const ch = body[i];
    if (ch === '"' || ch === "'" || ch === '`') {
      let j = i + 1;
      while (j < n && body[j] !== ch) {
        if (body[j] === '\\') j += 1;
        j += 1;
      }
      i = j + 1;
      continue;
    }
    if (ch === '{') {
      depth += 1;
      i += 1;
      continue;
    }
    if (ch === '}') {
      depth -= 1;
      i += 1;
      continue;
    }
    if (depth === 0 && body.startsWith('function', i)) {
      const m = fnDeclRe.exec(body.slice(i));
      if (m) names.push(m[1]);
    }
    i += 1;
  }
  return names;
}

function buildScriptObject(body, NS) {
  const names = new Set(topLevelFunctionNames(body));
  const returnExpr = '{' + Array.from(names).map((n) => `${n}: ${n}`).join(', ') + '}';
  const src = `${body}\nreturn ${returnExpr};`;
  // These object bodies only ever reference fields via explicit Page_N.X.rawValue,
  // never bare -- so no `with` wrapper is needed here, only Page_1..4 bound to NS.
  const factory = new Function('NS', 'Page_1', 'Page_2', 'Page_3', 'Page_4', src);
  return factory(NS, NS, NS, NS, NS);
}

// ---------------------------------------------------------------------------
// 4. The shared namespace. `has` is restricted to known field names (or the
//    form's own naming conventions) so that `with (NS) { ... }` does NOT
//    shadow script-object names, Math/Number, or the scripts' own local `var`s.
// ---------------------------------------------------------------------------
const FIELD_PREFIX_RE = /^(Value_|grey_box_|na_box_|RadioButtonList$|SS_benefit$|SS_parent$|CaseName$|DocketNumber$|DatePrepared$|NameOfPreparer$|Box1$|Box2$|Box3$|yes$|no$)/;

const NUMERIC_STRING_RE = /^-?\d+(\.\d+)?$/;

function makeFieldNode(isNumeric) {
  let raw = null;
  return {
    get rawValue() {
      return raw;
    },
    set rawValue(v) {
      if (isNumeric && typeof v === 'string' && NUMERIC_STRING_RE.test(v.trim())) {
        raw = Number(v);
      } else {
        raw = v;
      }
    },
  };
}

function buildNamespace(declaredNames, numericFieldNames) {
  const known = new Set(declaredNames);
  const target = {};
  return new Proxy(target, {
    has(t, prop) {
      if (typeof prop !== 'string') return prop in t;
      return known.has(prop) || FIELD_PREFIX_RE.test(prop);
    },
    get(t, prop) {
      if (typeof prop !== 'string') return t[prop];
      if (!known.has(prop) && !FIELD_PREFIX_RE.test(prop)) return undefined;
      if (!(prop in t)) t[prop] = makeFieldNode(numericFieldNames.has(prop));
      return t[prop];
    },
  });
}

function buildCalcFn(body) {
  const src = `with (NS) {\n${body}\n}`;
  return new Function(
    'NS',
    'CheckIfInputsPopulated',
    'CheckIfChildrenInputsPopulated',
    'CalcChildCare',
    'Page_1',
    'Page_2',
    'Page_3',
    'Page_4',
    src
  );
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const xmlPath = process.argv[2];
  const inputPath = process.argv[3];
  if (!xmlPath || !inputPath) {
    process.stderr.write('usage: node official_xfa_harness.js <xfa.xml> <inputs.json>\n');
    process.exit(2);
  }
  const xml = loadXml(xmlPath);
  const inputs = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

  const namePositions = collectNamePositions(xml);
  const declaredNames = namePositions.map((p) => p.name);
  const nearestName = makeNearestNameLookup(namePositions);

  const calcScripts = collectCalcScripts(xml);
  const fieldCalcs = []; // {name, body, pos} in document order
  for (const c of calcScripts) {
    const name = nearestName(c.pos);
    if (name) fieldCalcs.push({ name, body: c.body, pos: c.pos });
  }
  fieldCalcs.sort((a, b) => a.pos - b.pos);

  const numericFieldNames = collectNumericFieldNames(xml, namePositions);
  const NS = buildNamespace(declaredNames, numericFieldNames);

  const namedObjSrc = collectNamedScriptObjects(xml);
  const scriptObjs = {};
  for (const [name, body] of Object.entries(namedObjSrc)) {
    scriptObjs[name] = buildScriptObject(body, NS);
  }
  const CheckIfInputsPopulated = scriptObjs.CheckIfInputsPopulated || {};
  const CheckIfChildrenInputsPopulated = scriptObjs.CheckIfChildrenInputsPopulated || {};
  const CalcChildCare = scriptObjs.CalcChildCare || {};

  // Seed inputs directly onto the namespace (bypassing calc, exactly as a user
  // typing into the PDF would).
  for (const [name, value] of Object.entries(inputs)) {
    NS[name].rawValue = value;
  }

  // Compile every field's calculate function once.
  const compiled = fieldCalcs.map((fc) => ({
    name: fc.name,
    fn: buildCalcFn(fc.body),
  }));

  const MAX_PASSES = 50;
  let pass = 0;
  let changed = true;
  const warnings = [];
  while (changed && pass < MAX_PASSES) {
    changed = false;
    pass += 1;
    for (const { name, fn } of compiled) {
      const fieldObj = NS[name];
      const before = fieldObj.rawValue;
      try {
        fn.call(fieldObj, NS, CheckIfInputsPopulated, CheckIfChildrenInputsPopulated, CalcChildCare, NS, NS, NS, NS);
      } catch (e) {
        warnings.push(`field ${name} pass ${pass}: ${e.message}`);
        continue;
      }
      const after = fieldObj.rawValue;
      if (after !== before) {
        // NaN !== NaN is always true; guard against a false "still changing" loop.
        if (!(typeof after === 'number' && typeof before === 'number' && Number.isNaN(after) && Number.isNaN(before))) {
          changed = true;
        }
      }
    }
  }

  const result = {};
  for (const name of declaredNames) {
    if (/^(Value_|RadioButtonList$|SS_benefit$|SS_parent$)/.test(name)) {
      result[name] = NS[name].rawValue;
    }
  }
  result.__meta__ = { passes: pass, converged: !changed, warnings };

  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

main();
