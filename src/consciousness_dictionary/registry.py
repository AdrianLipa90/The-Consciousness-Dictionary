from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, Iterator

@dataclass(frozen=True)
class Term:
    term_id: str
    canonical_name: str
    definition: str
    formal_class: str
    epistemic_status: str
    phase_index: int
    category: str
    raw: dict

@dataclass(frozen=True)
class Relation:
    source: str
    relation: str
    target: str
    status: str = "DECLARED"

class Lexicon:
    def __init__(self, terms: Iterable[dict], relations: Iterable[dict] = ()):
        self.terms = {}
        self.by_name = {}
        for raw in terms:
            t=Term(raw['term_id'],raw['canonical_name'],raw['definition'],raw.get('formal_class',''),raw.get('epistemic_status',''),int(raw['phase_index']),raw.get('category',''),raw)
            if t.term_id in self.terms: raise ValueError(f'duplicate term id: {t.term_id}')
            key=t.canonical_name.casefold()
            if key in self.by_name: raise ValueError(f'duplicate canonical name: {t.canonical_name}')
            self.terms[t.term_id]=t; self.by_name[key]=t.term_id
        # DEPENDS_ON and NOT_EQUIVALENT_TO are canonically derived from term cards.
        derived=[]
        for t in self.terms.values():
            for target in t.raw.get('dependencies',[]):
                derived.append(Relation(t.term_id,'DEPENDS_ON',target,'DECLARED'))
            for target in t.raw.get('not_equivalent_to',[]):
                derived.append(Relation(t.term_id,'NOT_EQUIVALENT_TO',target,'DECLARED'))
        explicit=[Relation(**r) for r in relations]
        seen=set(); self.relations=[]
        for e in derived+explicit:
            key=(e.source,e.relation,e.target,e.status)
            if key not in seen:
                seen.add(key); self.relations.append(e)
        self.outgoing={tid:[] for tid in self.terms}
        self.incoming={tid:[] for tid in self.terms}
        for e in self.relations:
            self.outgoing.setdefault(e.source,[]).append(e)
            self.incoming.setdefault(e.target,[]).append(e)

    @classmethod
    def load(cls, registry: str|Path, relations: str|Path|None=None) -> "Lexicon":
        def jsonl(path):
            with Path(path).open(encoding='utf-8') as f:
                return [json.loads(line) for line in f if line.strip()]
        rp=Path(registry)
        if rp.is_dir():
            idx=json.loads((rp/'index.json').read_text(encoding='utf-8'))
            terms=[]
            if idx.get('schema') == 'clx2/compact-registry/v0.2':
                cb=idx['codebooks']; cols=idx['columns']
                for shard in idx['shards']:
                    rows=json.loads((rp/shard['path']).read_text(encoding='utf-8'))
                    for row in rows:
                        x=dict(zip(cols,row)); extras=x.pop('extras',{}) or {}
                        raw={
                            'term_id':x['term_id'],'canonical_name':x['canonical_name'],'definition':x['definition'],
                            'formal_class':cb['formal_classes'][x['formal_class_code']],
                            'epistemic_status':cb['epistemic_statuses'][x['epistemic_status_code']],
                            'phase_index':x['phase_index'],'category':cb['categories'][x['category_code']],
                            'dependencies':x['dependencies'],'not_equivalent_to':x['not_equivalent_to'],
                            'equations':x['equations'],'source_anchors':[cb['sources'][i] for i in x['source_codes']],
                            'aliases':[],'counterexamples':[],'examples':[],'notes':'','observables':[],
                            'operationalization':'','realization':'','revision_condition':'','symbol':''
                        }
                        raw.update(extras); raw['namespace']=raw['term_id'].split('-')[1]
                        terms.append(raw)
            else:
                for part in idx['parts']:
                    terms.extend(jsonl(rp/part['path']))
        else:
            terms=jsonl(rp)
        # Apply ordered append-only canonical correction patches after reconstructing the base registry.
        if rp.is_dir():
            patch_dir = rp / 'patches'
            if patch_dir.exists():
                by_id = {x['term_id']: x for x in terms}
                for patch_path in sorted(patch_dir.glob('*.json')):
                    patch = json.loads(patch_path.read_text(encoding='utf-8'))
                    tid = patch['term_id']
                    if tid not in by_id:
                        raise ValueError(f'patch targets missing term: {tid}')
                    if patch.get('operation') != 'replace_field':
                        raise ValueError(f'unsupported registry patch operation: {patch.get("operation")}')
                    by_id[tid][patch['field']] = patch['value']
                terms = list(by_id.values())
        return cls(terms, jsonl(relations) if relations and Path(relations).exists() else [])

    def get(self, key: str) -> Term:
        if key in self.terms: return self.terms[key]
        tid=self.by_name.get(key.casefold())
        if tid is None: raise KeyError(key)
        return self.terms[tid]

    def neighbors(self, key: str, relation: str|None=None, incoming: bool=False) -> list[Term]:
        t=self.get(key); edges=(self.incoming if incoming else self.outgoing).get(t.term_id,[])
        if relation: edges=[e for e in edges if e.relation==relation]
        ids=[e.source if incoming else e.target for e in edges]
        return [self.terms[x] for x in ids if x in self.terms]
