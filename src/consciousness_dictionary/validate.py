from __future__ import annotations
from collections import Counter
from .registry import Lexicon

KNOWN_STATUSES={
'DEFINITION','WORKING_DEFINITION','RIFC_WORKING_DEFINITION','MODEL_DEFINITION','MODEL_CLASS','MODEL_HYPOTHESIS','CONSTITUTIVE_HYPOTHESIS','HYPOTHESIS','OPEN_HYPOTHESIS','OPEN_ONTOLOGY','IMPLEMENTED','IMPLEMENTED_DEFINITION','IMPLEMENTATION_PRINCIPLE','MODEL_PRINCIPLE','WORKING_CANONICAL_DEFINITION','METHODOLOGICAL_DEFINITION','METHODOLOGICAL_PRINCIPLE','ESTABLISHED_MATH_PHYSICS','ESTABLISHED_GEOMETRY','EXACT_BINARY_RESULT','INTERPRETATION','SPECULATIVE_EXTENSION','EVIDENTIAL_BOUNDARY','DERIVED_OR_EXACT_MODEL_RESULT','EVIDENTIAL_FRAMEWORK','THEORETICAL_POSITION'
}

def validate(lexicon: Lexicon, formula_ids: set[str]|None=None) -> dict:
    failures=[]; warnings=[]
    ids=set(lexicon.terms)
    phases=[]
    for t in lexicon.terms.values():
        r=t.raw; phases.append(t.phase_index)
        for dep in r.get('dependencies',[]):
            if dep not in ids: failures.append(f'{t.term_id}: missing dependency {dep}')
        for neq in r.get('not_equivalent_to',[]):
            if neq not in ids: warnings.append(f'{t.term_id}: unresolved not-equivalent target {neq}')
        if t.epistemic_status not in KNOWN_STATUSES: warnings.append(f'{t.term_id}: unregistered status {t.epistemic_status}')
        if not r.get('source_anchors'): warnings.append(f'{t.term_id}: no source anchor')
        if formula_ids is not None:
            for eq in r.get('equations',[]):
                if eq not in formula_ids: failures.append(f'{t.term_id}: missing formula {eq}')
    dup_phase=[k for k,v in Counter(phases).items() if v>1]
    if dup_phase: failures.append(f'duplicate phase indices: {dup_phase[:10]}')
    for e in lexicon.relations:
        if e.source not in ids or e.target not in ids: failures.append(f'broken edge {e}')
    graph={tid:[] for tid in ids}
    for t in lexicon.terms.values(): graph[t.term_id]=[d for d in t.raw.get('dependencies',[]) if d in ids]
    temp=set(); perm=set(); cycles=[]
    def dfs(n,stack):
        if n in perm:return
        if n in temp:
            cycles.append(stack[stack.index(n):]+[n]); return
        temp.add(n); stack.append(n)
        for d in graph[n]: dfs(d,stack)
        stack.pop(); temp.remove(n); perm.add(n)
    for n in ids:
        if n not in perm: dfs(n,[])
    if cycles: failures.append(f'dependency cycles: {cycles[:3]}')
    return {'status':'PASS' if not failures else 'FAIL','terms':len(ids),'relations':len(lexicon.relations),'failures':failures,'warnings':warnings,'warning_count':len(warnings)}
