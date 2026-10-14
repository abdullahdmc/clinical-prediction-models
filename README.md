# Infection Model Tracker

Prognostic and diagnostic models for sepsis, severe infection and febrile illness, organised by the outcome they predict. Each model sheet gives components, cut-offs, the original article and updates, outcome definitions, published performance and links to online calculators.

**Website:** https://abdullahdmc.github.io/clinical-prediction-models/

Research reference only, not for direct clinical use. Check scores against the original publication before using them in patient care.

## Repository layout

| Path | What it is |
|---|---|
| `docs/` | The published site (`index.html` + `data.json`), served by GitHub Pages |
| `build/src/content.py`, `content2.py` | Curated model sheets: **edit these to change site content** |
| `build/template.html` | Page layout, styles and script |
| `build/build_site.py` | Builds `docs/` from the content files |
| `build/test_render.js` | Renders every page with a stubbed DOM to catch errors |
| `data/` | Head-to-head AUC extraction and small search outputs |
| `scripts/` | Search, mining and workbook scripts from the October 2026 PubMed search |

Not in the repository (kept locally): the gap-analysis workbook, the full PubMed download (168 MB), downloaded PDFs and cached abstracts.

## Rebuild

```bash
python -I build/build_site.py
node build/test_render.js
```

The build fetches citation details from PubMed, so it needs an internet connection.

## Source labels

Every model sheet shows where its details come from: *checked against original* (tables of the original article), *from original abstract*, *secondary source* (standard published version, e.g. a guideline or MDCalc) or *pending PDF*.

## Update policy

Updated once a year in October, or on request:

1. Re-run the PubMed query in `scripts/query2.txt` from the last update date.
2. Mine new named models and recent development/validation studies (`scripts/mine.py`, `scripts/newmodels.py`).
3. Add or update sheets in `build/src/content*.py`; set `UPDATED` in `build/build_site.py`.
4. Rebuild, run the render test, commit and push.
