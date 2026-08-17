from pathlib import Path
from consciousness_dictionary.registry import Lexicon
from consciousness_dictionary.query import phase_similarity

root=Path(__file__).resolve().parents[1]
lex=Lexicon.load(root/'ontology/registry',root/'ontology/relations/relations.jsonl')
print(lex.get('Qualia'))
print(phase_similarity(lex,'Qualia',limit=8))
