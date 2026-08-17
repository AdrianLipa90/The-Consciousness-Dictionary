from pathlib import Path
from consciousness_dictionary.registry import Lexicon

ROOT=Path(__file__).resolve().parents[1]
lex=Lexicon.load(ROOT/"ontology/registry/v0_2",ROOT/"ontology/relations/extra_relations.jsonl")
out=ROOT/"build/DICTIONARY_FULL.md"; out.parent.mkdir(exist_ok=True)
lines=["# The Consciousness Dictionary — generated V0.2 alpha","",f"**{len(lex.terms)} canonical terms.**",""]
for t in sorted(lex.terms.values(),key=lambda x:x.phase_index):
    r=t.raw
    lines += [f"## {t.term_id} — {t.canonical_name}","",f"**Class:** `{t.formal_class}`  ",f"**Status:** `{t.epistemic_status}`  ",f"**Phase index:** `{t.phase_index}`  ",f"**Category:** {t.category}","",r["definition"],""]
    if r.get("dependencies"): lines += ["**Depends on:** "+", ".join(f"`{x}`" for x in r["dependencies"]),""]
    if r.get("not_equivalent_to"): lines += ["**Not equivalent to:** "+", ".join(f"`{x}`" for x in r["not_equivalent_to"]),""]
    if r.get("equations"): lines += ["**Equations:** "+", ".join(f"`{x}`" for x in r["equations"]),""]
    if r.get("source_anchors"): lines += ["**Sources:** "+"; ".join(r["source_anchors"]),""]
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(out)
