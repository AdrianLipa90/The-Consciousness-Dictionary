from __future__ import annotations
import heapq
import math
from .registry import Lexicon
from .phasenav_native import (
    PhaseState,
    relational_coherence,
    relational_phase,
    angular_distance,
    informational_action,
)

BLOCKED_PATH_RELATIONS={'NOT_EQUIVALENT_TO'}

def _state(t): return PhaseState.from_term(t.term_id,t.phase_index,t.raw)

def _external_vector36(vector) -> tuple[float, ...]:
    v=tuple(float(x) for x in vector)
    if len(v)!=36: raise ValueError('external PhaseNav state must have exactly 36 components')
    if not all(math.isfinite(x) for x in v): raise ValueError('external PhaseNav state contains non-finite values')
    return v

def external_phase_projection(lexicon: Lexicon, vector, limit: int=16) -> list[dict]:
    """Rank canonical terms against an external 36D PhaseNav state.

    This is a computational retrieval projection for NEXUS-like consumers. Phase
    similarity, salience, or rank does not create semantic equivalence, truth,
    capability, or epistemic authority.
    """
    qv=_external_vector36(vector)
    if limit<=0: return []
    rows=[]
    for t in lexicon.terms.values():
        tv=_state(t).vector
        coherence=relational_coherence(qv,tv)
        rows.append({
            'term_id':t.term_id,
            'name':t.canonical_name,
            'phase_index':t.phase_index,
            'coherence':coherence,
            'phase':relational_phase(qv,tv),
            'angular_distance':angular_distance(qv,tv),
            'informational_action':informational_action(qv,tv),
            'semantic_equivalence':False,
            'authority_grant':False,
        })
    rows.sort(key=lambda r:(-r['coherence'],r['informational_action'],r['angular_distance'],r['term_id']))
    return rows[:min(int(limit),len(rows))]

def phase_similarity(lexicon: Lexicon, key: str, limit: int=10) -> list[dict]:
    q=lexicon.get(key); qv=_state(q).vector
    rows=[]
    for t in lexicon.terms.values():
        if t.term_id==q.term_id: continue
        tv=_state(t).vector
        rows.append({'term_id':t.term_id,'name':t.canonical_name,'coherence':relational_coherence(qv,tv),'angular_distance':angular_distance(qv,tv),'semantic_equivalence':False})
    rows.sort(key=lambda r:(-r['coherence'],r['angular_distance'],r['term_id']))
    return rows[:limit]

def declared_neighbors(lexicon: Lexicon, key: str, include_negative: bool=False) -> list[dict]:
    q=lexicon.get(key); qv=_state(q).vector; rows=[]
    for e in lexicon.outgoing.get(q.term_id,[]):
        if e.relation=='NOT_EQUIVALENT_TO' and not include_negative: continue
        t=lexicon.terms[e.target]; tv=_state(t).vector
        rows.append({'term_id':t.term_id,'name':t.canonical_name,'relation':e.relation,'coherence':relational_coherence(qv,tv),'angular_distance':angular_distance(qv,tv)})
    return rows

def constrained_phase_path(lexicon: Lexicon, start: str, end: str, allowed_relations: set[str]|None=None) -> list[str]:
    """Dijkstra path on declared ontology edges; PhaseNav geometry supplies edge cost only."""
    s=lexicon.get(start).term_id; target=lexicon.get(end).term_id
    dist={s:0.0}; prev={}; heap=[(0.0,s)]
    while heap:
        cost,u=heapq.heappop(heap)
        if cost!=dist.get(u): continue
        if u==target: break
        us=_state(lexicon.terms[u]).vector
        for e in lexicon.outgoing.get(u,[]):
            if e.relation in BLOCKED_PATH_RELATIONS: continue
            if allowed_relations and e.relation not in allowed_relations: continue
            if e.target not in lexicon.terms: continue
            vs=_state(lexicon.terms[e.target]).vector
            w=angular_distance(us,vs)+informational_action(us,vs)
            nc=cost+w
            if nc<dist.get(e.target,float('inf')):
                dist[e.target]=nc; prev[e.target]=u; heapq.heappush(heap,(nc,e.target))
    if target not in dist: return []
    path=[target]
    while path[-1]!=s:path.append(prev[path[-1]])
    path.reverse(); return path

def declared_path(lexicon: Lexicon, start: str, end: str, allowed_relations: set[str]|None=None) -> list[str]:
    s=lexicon.get(start).term_id; target=lexicon.get(end).term_id
    queue=[s]; prev={s:None}
    for cur in queue:
        if cur==target: break
        for e in lexicon.outgoing.get(cur,[]):
            if e.relation in BLOCKED_PATH_RELATIONS: continue
            if allowed_relations and e.relation not in allowed_relations: continue
            if e.target not in prev:
                prev[e.target]=cur; queue.append(e.target)
    if target not in prev: return []
    path=[]; cur=target
    while cur is not None: path.append(cur); cur=prev[cur]
    return list(reversed(path))
