from __future__ import annotations
import argparse, json
from pathlib import Path
from .registry import Lexicon
from .compiler import write_compiled
from .query import phase_similarity, declared_path, declared_neighbors, constrained_phase_path
from .validate import validate
from .phasenav_native import PhaseState

def default_paths():
    root=Path(__file__).resolve().parents[2]
    return root/'ontology/registry/v0_2', root/'ontology/relations/extra_relations.jsonl', root/'ontology/formulas/formulas.json'

def main(argv=None):
    ap=argparse.ArgumentParser(prog='consciousness-dictionary')
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('stats')
    p=sub.add_parser('term'); p.add_argument('key')
    p=sub.add_parser('vector'); p.add_argument('key')
    p=sub.add_parser('similar'); p.add_argument('key'); p.add_argument('-n',type=int,default=10)
    p=sub.add_parser('path'); p.add_argument('start'); p.add_argument('end')
    p=sub.add_parser('phase-path'); p.add_argument('start'); p.add_argument('end')
    p=sub.add_parser('neighbors'); p.add_argument('key'); p.add_argument('--include-negative',action='store_true')
    p=sub.add_parser('formula'); p.add_argument('formula_id')
    p=sub.add_parser('validate')
    p=sub.add_parser('compile'); p.add_argument('--out',default='build')
    ns=ap.parse_args(argv); reg,rels,forms=default_paths(); lex=Lexicon.load(reg,rels)
    if ns.cmd=='stats': print(json.dumps({'terms':len(lex.terms),'relations':len(lex.relations)},indent=2))
    elif ns.cmd=='term': print(json.dumps(lex.get(ns.key).raw,ensure_ascii=False,indent=2))
    elif ns.cmd=='vector':
        t=lex.get(ns.key); s=PhaseState.from_term(t.term_id,t.phase_index,t.raw); print(json.dumps({'term_id':t.term_id,'phase_index':t.phase_index,'vector_36d':s.vector,'R':s.order_parameter,'semantic_mass':s.semantic_mass},indent=2))
    elif ns.cmd=='similar': print(json.dumps(phase_similarity(lex,ns.key,ns.n),ensure_ascii=False,indent=2))
    elif ns.cmd=='path': print(json.dumps(declared_path(lex,ns.start,ns.end),indent=2))
    elif ns.cmd=='phase-path': print(json.dumps(constrained_phase_path(lex,ns.start,ns.end),indent=2))
    elif ns.cmd=='neighbors': print(json.dumps(declared_neighbors(lex,ns.key,ns.include_negative),ensure_ascii=False,indent=2))
    elif ns.cmd=='formula':
        table={x['formula_id']:x for x in json.loads(forms.read_text())['formulas']}; print(json.dumps(table[ns.formula_id],ensure_ascii=False,indent=2))
    elif ns.cmd=='validate':
        formula_ids={x['formula_id'] for x in json.loads(forms.read_text())['formulas']}; print(json.dumps(validate(lex,formula_ids),ensure_ascii=False,indent=2))
    elif ns.cmd=='compile': print(json.dumps(write_compiled(lex,ns.out),indent=2))

if __name__=='__main__': main()
