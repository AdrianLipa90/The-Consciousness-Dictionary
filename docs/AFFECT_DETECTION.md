# Affect Detection Runtime

## Scope

This module operationalizes the RIFC / Relational Geometry of Qualia affect field

`A_t(x) = (v, a, u, tau, alpha, r)`

as a transparent text-conditioned estimate:

- `v`: valence in `[-1,1]`
- `a`: arousal in `[0,1]`
- `u`: urgency in `[0,1]`
- `tau`: threat relevance in `[0,1]`
- `alpha`: attachment relevance in `[0,1]`
- `r`: reward / preference relevance in `[0,1]`

## Hard boundary

`AFFECT_INFERENCE != AFFECT_MODULATION != TRUTH != DIAGNOSIS`

The detector reports observable linguistic/surface evidence and a confidence value. It does not claim privileged access to a person's internal state. Low evidence is reported as `insufficient-evidence`, not silently converted to neutral affect.

Every `AffectEstimate` carries:

- `truth_authority = false`
- `semantic_authority = false`
- `diagnostic_authority = false`
- `modulation_authority = false`

Affect may inform salience handling, but it cannot alter factual validity or evidence status.

## Detection method

`transparent_lexical_surface_v1` is deterministic and inspectable. It currently uses explicit Polish and English lexical cues plus weak punctuation / ALL-CAPS arousal cues. Every cue is returned with its span and numerical contribution.

This is an engineering implementation, not a psychological law or validated clinical instrument.

## Temporal tracking

`AffectTracker` maintains a bounded smoothed trajectory. It stores estimates and SHA-256 hashes rather than raw input text.

The diagnostic mapping `affect_phase36()` embeds six affect coordinates into a 36D PhaseNav-shaped vector for trajectory comparison. This mapping is explicitly computational and does not establish an identity between affect and PhaseNav geometry.

## Example

```python
from consciousness_dictionary import AffectDetector, AffectTracker

detector = AffectDetector()
estimate = detector.detect('Bardzo lubię ten kierunek i wolę tę wersję.')
print(estimate.as_dict())

tracker = AffectTracker()
tracker.update('I love this.')
state = tracker.update('This is urgent!')
print(state.smoothed)
print(state.path_change)
```

CLI:

```text
PYTHONPATH=src python3 -m consciousness_dictionary.cli affect "Kurwa, zrób to NATYCHMIAST!!!"
```

## Validation

Dedicated tests cover: unknown/low-evidence handling, Polish preference cues, high-arousal urgency, threat relevance without truth authority, attachment relevance, 36D mapping finiteness, bounded temporal tracking without raw-text retention, and English fear cues.
