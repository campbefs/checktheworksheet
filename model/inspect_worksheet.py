#!/usr/bin/env python3
"""Pull the calculation logic out of the CJ-D 304 Guidelines Worksheet.

WHY THIS EXISTS
---------------
Everything in model/guidelines.py that is marked INFERRED is inferred only because we
did not have the Worksheet. The Trial Court publishes an *electronic* version and the
Task Force "strongly encouraged" its use -- which means it is almost certainly a fillable
AcroForm PDF whose fields auto-calculate. Auto-calculating PDFs carry the arithmetic as
embedded JavaScript. If it is there, this prints it, and the order of operations stops
being a guess.

WHAT IT EXTRACTS, best case to worst
  1. Embedded JavaScript  -> the literal formulas (Line 3e = ..., Line 7e = ..., etc.)
  2. AcroForm field names, types, values, and per-field calculate/format actions
  3. Field calculation ORDER (the /CO array) -- tells you the sequence of computation
  4. Plain page text -> line numbering and labels even if the file is flat/scanned

Usage:
    .venv/bin/python model/inspect_worksheet.py <path-to-CJ-D-304.pdf>
"""

import re
import sys
import zlib


def _txt(o):
    try:
        from pypdf.generic import TextStringObject, ByteStringObject
        if isinstance(o, (TextStringObject, ByteStringObject)):
            return str(o)
    except Exception:
        pass
    if isinstance(o, bytes):
        return o.decode("latin-1", "ignore")
    return str(o) if o is not None else ""


def _stream(o):
    """Return decoded stream text for a JS action, which may be a string or a stream."""
    try:
        data = o.get_data()
        try:
            data = zlib.decompress(data)
        except Exception:
            pass
        return data.decode("latin-1", "ignore")
    except Exception:
        return _txt(o)


def dump_javascript(reader):
    print("=" * 78)
    print("1. EMBEDDED JAVASCRIPT  (the formulas, if present)")
    print("=" * 78)
    found = []

    # (a) document-level JS in the Names tree
    try:
        root = reader.trailer["/Root"]
        names = root.get("/Names", {})
        js = names.get("/JavaScript") if hasattr(names, "get") else None
        if js:
            arr = js.get_object().get("/Names", [])
            for i in range(0, len(arr) - 1, 2):
                label = _txt(arr[i])
                act = arr[i + 1].get_object()
                code = _stream(act.get("/JS")) if hasattr(act, "get") else ""
                if code:
                    found.append((f"document-level: {label}", code))
    except Exception as e:
        print(f"  (document-level scan failed: {e})")

    # (b) per-field calculate / format / validate actions
    try:
        fields = reader.get_fields() or {}
        for name, f in fields.items():
            obj = f.get("/_States_", None)  # placeholder to keep pypdf happy
            aa = None
            try:
                aa = f.indirect_reference.get_object().get("/AA")
            except Exception:
                aa = f.get("/AA") if hasattr(f, "get") else None
            if not aa:
                continue
            for key, label in (("/C", "calculate"), ("/F", "format"), ("/V", "validate")):
                act = aa.get(key)
                if act is None:
                    continue
                code = _stream(act.get_object().get("/JS"))
                if code:
                    found.append((f"{name} [{label}]", code))
    except Exception as e:
        print(f"  (field-action scan failed: {e})")

    # Adobe ships boilerplate version-check JS in every Acrobat form. Filter it out
    # so real calculation code is not buried under a hundred lines of noise.
    noise = re.compile(r"ADBE|VersChk|XFACheck|viewerVersion|Need_New_Version", re.I)
    real = [(l, c) for l, c in found if not noise.search(l)]
    boiler = len(found) - len(real)
    if boiler:
        print(f"  (filtered {boiler} Adobe boilerplate script(s))")
    found = real

    if not found:
        print("  NO CALCULATION JAVASCRIPT FOUND.")
        print("  => Either the file is flat/scanned, or calculations are not embedded.")
        print("  => Fall back to section 4 (page text) for line numbers and labels.")
    for label, code in found:
        print(f"\n--- {label} ---")
        print(code.strip()[:4000])
    return found


def dump_xfa(reader):
    """LiveCycle/XFA forms keep their arithmetic in an XML packet, not in /AA actions.
    Field names like form1[0].Page1[0].Line3e[0] are the tell. This pulls the
    <calculate> and <validate> scripts out of that XML -- which for a court worksheet
    is the actual order of operations."""
    print("\n" + "=" * 78)
    print("1b. XFA CALCULATION SCRIPTS  (LiveCycle forms keep formulas here)")
    print("=" * 78)
    try:
        acro = reader.trailer["/Root"].get("/AcroForm")
        xfa = acro.get_object().get("/XFA") if acro else None
        if not xfa:
            print("  No /XFA packet. (Form is a classic AcroForm, or flat.)")
            return
        parts = []
        arr = xfa.get_object()
        if isinstance(arr, list):
            for i in range(0, len(arr) - 1, 2):
                nm = _txt(arr[i])
                parts.append((nm, _stream(arr[i + 1].get_object())))
        else:
            parts.append(("xfa", _stream(arr)))
        blob = "\n".join(c for _, c in parts)
        print(f"  XFA packet(s): {[n for n, _ in parts]}  ({len(blob):,} chars)")
        with open("data/extracted/cjd304-xfa.xml", "w", errors="ignore") as fh:
            fh.write(blob)
        print("  full XML saved -> data/extracted/cjd304-xfa.xml")
        scripts = re.findall(
            r"<(calculate|validate)[^>]*>(.*?)</\1>", blob, re.S | re.I)
        print(f"\n  {len(scripts)} <calculate>/<validate> block(s):")
        for kind, body in scripts[:80]:
            code = re.sub(r"<[^>]+>", " ", body)
            code = re.sub(r"\s+", " ", code).strip()
            if code:
                print(f"    [{kind}] {code[:300]}")
    except Exception as e:
        print(f"  XFA scan failed: {e}")


def dump_fields(reader):
    print("\n" + "=" * 78)
    print("2. FORM FIELDS  (names, types, current values)")
    print("=" * 78)
    try:
        fields = reader.get_fields() or {}
    except Exception as e:
        print(f"  could not read fields: {e}")
        return {}
    if not fields:
        print("  No AcroForm fields -- the file is flat or scanned.")
        return {}
    print(f"  {len(fields)} field(s)\n")
    for name, f in sorted(fields.items()):
        ft = _txt(f.get("/FT", ""))
        val = _txt(f.get("/V", ""))
        print(f"  {name:<48} {ft:<8} {val}")
    return fields


def dump_calc_order(reader):
    print("\n" + "=" * 78)
    print("3. CALCULATION ORDER  (/CO -- the sequence the form computes in)")
    print("=" * 78)
    try:
        acro = reader.trailer["/Root"].get("/AcroForm")
        co = acro.get_object().get("/CO") if acro else None
        if not co:
            print("  No /CO array. (Normal if there are no calculated fields.)")
            return
        for i, ref in enumerate(co, 1):
            o = ref.get_object()
            print(f"  {i:>3}. {_txt(o.get('/T',''))}")
    except Exception as e:
        print(f"  could not read: {e}")


def dump_text(reader):
    print("\n" + "=" * 78)
    print("4. PAGE TEXT  (line numbers and labels)")
    print("=" * 78)
    for i, page in enumerate(reader.pages, 1):
        t = (page.extract_text() or "").strip()
        print(f"\n--- page {i} ---")
        print(re.sub(r"\n{2,}", "\n", t)[:6000] if t else "  (no extractable text)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    from pypdf import PdfReader
    path = sys.argv[1]
    reader = PdfReader(path)
    print(f"\nFILE: {path}\nPAGES: {len(reader.pages)}\n")
    dump_javascript(reader)
    dump_xfa(reader)
    dump_fields(reader)
    dump_calc_order(reader)
    dump_text(reader)
    return 0


if __name__ == "__main__":
    sys.exit(main())
