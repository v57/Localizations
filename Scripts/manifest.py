"""Prints manifest.json for the repository at argv[1]: every source's languages and their files, with sizes and
SHA-256 hashes. Apps read it to list the languages they can download, to show a download's size and to tell whether
their copy of a language is current.

{"version": 1, "sources": {"Markdown": {"de": {"Localizable.strings": {"bytes": 1234, "sha256": "…"}, …}, …}, …}}
"""
import hashlib
import json
import os
import sys

root = sys.argv[1]
sources = {}
for source in sorted(os.listdir(root)):
    folder = os.path.join(root, source)
    if source.startswith(".") or source == "Scripts" or not os.path.isdir(folder):
        continue
    languages = {}
    for lproj in sorted(os.listdir(folder)):
        if not lproj.endswith(".lproj"):
            continue
        files = {}
        for name in sorted(os.listdir(os.path.join(folder, lproj))):
            if not (name.endswith(".strings") or name.endswith(".stringsdict")):
                continue
            with open(os.path.join(folder, lproj, name), "rb") as handle:
                data = handle.read()
            files[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        if files:
            languages[lproj[: -len(".lproj")]] = files
    if languages:
        sources[source] = languages
json.dump({"version": 1, "sources": sources}, sys.stdout, indent=1, sort_keys=True, ensure_ascii=False)
print()
