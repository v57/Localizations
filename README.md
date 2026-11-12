# Localizations

Translations of the v57 apps and kits, kept out of their repositories. Apps ship English and a few languages and
download the others from here when the user asks (PlatformLanguages in [v57/Platform](https://github.com/v57/Platform),
Settings ▸ Languages in every app). The design: `Ideas/Localization.md` in the v57 folder.

## Layout

```
manifest.json                                what apps read first: every source's languages and files
<Source>/Localizable.xcstrings               the catalog, every language (edit this)
<Source>/<lang>.lproj/Localizable.strings    compiled from it by Scripts/build (apps download these)
<Source>/<lang>.lproj/Localizable.stringsdict
```

A source is one set of strings: an app (`Markdown`, `Shell`) or a kit every app links (`ComponentKit`, `VaultUI`). An
app downloads its own source and its kits' and looks a key up in that order. A source may have more tables than
`Localizable` (any `*.xcstrings` in its folder).

Keys are the English text, so a file fits every version of an app: a new string shows in English until it's
translated here, and a typo fix reaches every installed copy without a release.

## Changing translations

Dev's Localization tab writes the catalogs. By hand: open `<Source>/Localizable.xcstrings` in Xcode, then

```bash
Scripts/build
```

which compiles every catalog (Xcode's `xcstringstool`, the source language left out) and rewrites `manifest.json`.
Commit the catalog together with what the script wrote. English is the key itself except for counts: the script also
merges every catalog's English plural variants ("%lld servers" → "1 server") into one table in the Platform checkout
beside this one (`Sources/PlatformLanguages/English`), which every app answers them from; commit it there when it
changed. Pull requests with fixed translations are welcome.

Apps check every line they download: a translation whose format specifiers (`%@`, `%lld`, `%1$@`…) don't fit the key's
is dropped and shows in English.
