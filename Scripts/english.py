"""Merges every source's compiled English .stringsdict tables into one per table name: argv[1] is the output folder
(it gets `en.lproj/<Table>.stringsdict`, binary plists), the rest are the compiled files, best source first.

English needs only its plural variants (`%lld servers` → "1 server" / "2 servers"): every other English line is the key
itself, which the code already holds. Apps get these tables from PlatformLanguages (`../Platform`), which answers
them behind the app's own strings and behind a translation that lacks a key, so a count reads "1 server" in every
app, Debug or Release, without each app bundling English. Keys are the English text, so the sources share one table;
a key two sources write differently keeps the first source's and is reported.
"""
import os
import plistlib
import sys

output, paths = sys.argv[1], sys.argv[2:]
tables = {}
for path in paths:
    table = os.path.basename(path)
    with open(path, "rb") as handle:
        entries = plistlib.load(handle)
    merged = tables.setdefault(table, {})
    for key, value in entries.items():
        if key in merged and merged[key] != value:
            print(f"english.py: {path}: {key!r} differs from an earlier source's; kept the earlier one", file=sys.stderr)
            continue
        merged.setdefault(key, value)

folder = os.path.join(output, "en.lproj")
os.makedirs(folder, exist_ok=True)
for name in os.listdir(folder):
    if name.endswith(".stringsdict") and name not in tables:
        os.remove(os.path.join(folder, name))
for table, entries in sorted(tables.items()):
    data = plistlib.dumps(dict(sorted(entries.items())), fmt=plistlib.FMT_BINARY, sort_keys=True)
    target = os.path.join(folder, table)
    try:
        with open(target, "rb") as handle:
            if handle.read() == data:
                continue
    except FileNotFoundError:
        pass
    with open(target, "wb") as handle:
        handle.write(data)
    print(f"{target}: {len(entries)} keys")
