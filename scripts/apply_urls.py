#!/usr/bin/env python3
"""Apply image URLs from url.csv (source of truth) to src/data/models/*.json.

Handles name syntax noise: extra spaces, trailing single-letter suffixes,
accents and small typos (Sigle/Single, Fiordaliso/Fioraliso).
Stores every available URL per color variant in `imageUrls`.
"""
import csv, json, glob, re, unicodedata, collections, difflib, sys, os

CSV = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-uploads/url.csv"
ROOT = os.path.join(os.path.dirname(__file__), "..")


def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm_name(s):
    s = " ".join(deaccent(s).split()).lower()
    s = re.sub(r"\s+[a-z]$", "", s)  # drop trailing variant letter (e.g. "Latteria A")
    return s


def norm_code(s):
    return " ".join(str(s).split())


by_key = collections.defaultdict(list)   # (name, code) -> [urls]
by_name = collections.defaultdict(list)  # name -> [urls]

with open(CSV, encoding="utf-8-sig") as f:
    for row in list(csv.reader(f, delimiter=";"))[1:]:
        if len(row) < 2 or not row[1].strip():
            continue
        m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", row[0].strip())
        if not m:
            continue
        n, code, url = norm_name(m.group(1)), norm_code(m.group(2)), row[1].strip()
        if url not in by_key[(n, code)]:
            by_key[(n, code)].append(url)
        if url not in by_name[n]:
            by_name[n].append(url)

all_names = list(by_name)
_cache = {}


def resolve_name(n):
    if n in by_name:
        return n
    if n in _cache:
        return _cache[n]
    match = difflib.get_close_matches(n, all_names, n=1, cutoff=0.85)
    res = match[0] if match else None
    _cache[n] = res
    return res


def lookup(name, code):
    n = resolve_name(norm_name(name))
    if not n:
        return []
    c = norm_code(code)
    urls = list(by_key.get((n, c), []))
    if not urls:
        # partial code overlap (multi-code entries)
        parts = set(c.split())
        for (kn, kc), v in by_key.items():
            if kn == n and parts & set(kc.split()):
                for u in v:
                    if u not in urls:
                        urls.append(u)
    if not urls:
        urls = list(by_name[n])
    return urls


stats = collections.Counter()
for path in sorted(glob.glob(os.path.join(ROOT, "src/data/models/*.json"))):
    d = json.load(open(path, encoding="utf-8"))
    changed = False
    for c in d.get("colors", []):
        urls = lookup(d["name"], c.get("code", ""))
        if urls:
            if c.get("imageUrl") != urls[0] or c.get("imageUrls") != urls:
                changed = True
            c["imageUrl"] = urls[0]
            c["imageUrls"] = urls
            stats["colors_ok"] += 1
        else:
            stats["colors_missing"] += 1
    rn = resolve_name(norm_name(d["name"]))
    gallery = list(by_name.get(rn, [])) if rn else []
    if d.get("gallery") != gallery:
        changed = True
    d["gallery"] = gallery
    stats["gallery_imgs"] += len(gallery)

    for look in d.get("looks", []):
        for it in look.get("items", []):
            urls = lookup(it.get("name", ""), it.get("code", ""))
            if urls:
                if it.get("imageUrl") != urls[0]:
                    changed = True
                it["imageUrl"] = urls[0]
                stats["items_ok"] += 1
            else:
                stats["items_missing"] += 1
    if changed:
        stats["files"] += 1
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")

print(stats)
