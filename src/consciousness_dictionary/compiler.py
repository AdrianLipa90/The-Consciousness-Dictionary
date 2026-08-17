from __future__ import annotations
import hashlib, json
from pathlib import Path
from .registry import Lexicon
from .phasenav_native import PhaseState, relational_coherence, relational_phase, angular_distance, informational_action, berry_connection, relation_delta

def compile_states(lexicon: Lexicon) -> list[dict]:
    out=[]
    for t in sorted(lexicon.terms.values(), key=lambda x:x.phase_index):
        s=PhaseState.from_term(t.term_id,t.phase_index,t.raw)
        out.append({"term_id":t.term_id,"canonical_name":t.canonical_name,"phase_index":t.phase_index,"vector_36d":list(s.vector),"order_parameter":s.order_parameter,"semantic_mass":s.semantic_mass,"epistemic_status":t.epistemic_status})
    return out

def compile_relation_observables(lexicon: Lexicon, states: list[dict]) -> list[dict]:
    by={s["term_id"]:s for s in states}; out=[]
    for e in lexicon.relations:
        if e.source not in by or e.target not in by: continue
        a=by[e.source]["vector_36d"]; b=by[e.target]["vector_36d"]
        out.append({"source":e.source,"relation":e.relation,"target":e.target,"phase_coherence":relational_coherence(a,b),"phase":relational_phase(a,b),"angular_distance":angular_distance(a,b),"informational_action":informational_action(a,b),"berry_connection":berry_connection(a,b),"delta_36d":list(relation_delta(a,b)),"semantic_authority":False})
    return out

def write_compiled(lexicon: Lexicon, out_dir: str|Path) -> dict:
    p=Path(out_dir); p.mkdir(parents=True,exist_ok=True)
    states=compile_states(lexicon); rels=compile_relation_observables(lexicon,states)
    sf=p/"TERM_STATES_36D.jsonl"; rf=p/"RELATION_OBSERVABLES.jsonl"
    sf.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in states),encoding="utf-8")
    rf.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in rels),encoding="utf-8")
    def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
    manifest={"states":len(states),"relations":len(rels),"state_sha256":sha(sf),"relation_sha256":sha(rf),"semantic_boundary":"Phase similarity is never semantic equivalence or epistemic authority."}
    (p/"COMPILE_RECEIPT.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return manifest
