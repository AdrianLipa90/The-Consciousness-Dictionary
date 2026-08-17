# The Consciousness Dictionary — V0.2 alpha

The canonical executable dictionary contains **548 complete term cards** in the compact registry under `ontology/registry/v0_2/`. Storage is column-normalized with explicit codebooks; `Lexicon.load()` reconstructs the full records deterministically.

Generate a single human-readable dictionary with:

```text
PYTHONPATH=src python3 tools/render_dictionary.py
```

The generated file is `build/DICTIONARY_FULL.md`. Formal equations, distinction tables and ontology graphs are maintained separately so they remain reusable by software as well as readable by humans.
