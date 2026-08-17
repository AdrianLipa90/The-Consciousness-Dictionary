"""Transparent affect inference for the executable Consciousness Dictionary.

This module operationalizes the RIFC / Relational Geometry of Qualia affect field
A_t(x) = (v, a, u, tau, alpha, r) as a text-conditioned estimate.

Canonical boundary:
    AFFECT_INFERENCE != AFFECT_MODULATION != TRUTH != DIAGNOSIS

The detector is deterministic and auditable. It uses explicit lexical and
surface-form cues in Polish and English. The optional temporal tracker stores
estimates and hashes rather than raw input text.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import exp, pi, tanh
import re
from typing import Sequence

from .rifc import AffectiveField

TAU = 2.0 * pi
KAPPA = 0.6931471805599453 / (24.0 * pi)
_TOKEN_RE = re.compile(r"[^\W_]+(?:['’-][^\W_]+)?", re.UNICODE)

# Engineering heuristics, not psychological laws.
_CUES: tuple[tuple[str, dict[str, float]], ...] = (
    ("bardzo lubię", {"valence": 1.0, "reward": 1.1}),
    ("lubię", {"valence": 0.7, "reward": 0.9}),
    ("uwielbiam", {"valence": 1.1, "reward": 1.0, "arousal": 0.25}),
    ("cieszę się", {"valence": 1.0, "reward": 0.6, "arousal": 0.15}),
    ("świetnie", {"valence": 0.8, "reward": 0.35}),
    ("super", {"valence": 0.7, "reward": 0.35, "arousal": 0.15}),
    ("chcę", {"reward": 0.75, "urgency": 0.1}),
    ("wolę", {"reward": 0.9}),
    ("zależy mi", {"attachment": 0.55, "reward": 0.55}),
    ("i like", {"valence": 0.7, "reward": 0.9}),
    ("i love", {"valence": 1.0, "reward": 0.8, "attachment": 0.75}),
    ("i prefer", {"reward": 0.9}),
    ("i want", {"reward": 0.75, "urgency": 0.1}),
    ("i'm glad", {"valence": 0.9, "reward": 0.5}),
    ("i am glad", {"valence": 0.9, "reward": 0.5}),
    ("kocham", {"valence": 0.9, "attachment": 1.25, "arousal": 0.2}),
    ("tęsknię", {"valence": -0.25, "attachment": 1.15, "arousal": 0.2}),
    ("bliska osoba", {"attachment": 0.8}),
    ("bliski mi", {"attachment": 0.85}),
    ("przywiąz", {"attachment": 0.9}),
    ("miss you", {"valence": -0.2, "attachment": 1.1}),
    ("care about", {"attachment": 0.95, "reward": 0.25}),
    ("important to me", {"attachment": 0.75, "reward": 0.35}),
    ("wkurw", {"valence": -1.0, "arousal": 0.85, "urgency": 0.25}),
    ("kurwa", {"valence": -0.55, "arousal": 0.65, "urgency": 0.15}),
    ("dość", {"valence": -0.55, "arousal": 0.45}),
    ("wściek", {"valence": -1.0, "arousal": 1.0}),
    ("zły", {"valence": -0.7, "arousal": 0.45}),
    ("frustr", {"valence": -0.7, "arousal": 0.6}),
    ("angry", {"valence": -0.9, "arousal": 0.85}),
    ("furious", {"valence": -1.0, "arousal": 1.0}),
    ("frustrated", {"valence": -0.75, "arousal": 0.65}),
    ("hate", {"valence": -0.95, "arousal": 0.7}),
    ("natychmiast", {"urgency": 1.25, "arousal": 0.35}),
    ("pilnie", {"urgency": 1.1, "arousal": 0.25}),
    ("teraz", {"urgency": 0.45}),
    ("jak najszybciej", {"urgency": 1.0, "arousal": 0.2}),
    ("od razu", {"urgency": 0.8}),
    ("asap", {"urgency": 1.2, "arousal": 0.25}),
    ("immediately", {"urgency": 1.2, "arousal": 0.3}),
    ("urgent", {"urgency": 1.1, "arousal": 0.25}),
    ("right now", {"urgency": 0.8, "arousal": 0.15}),
    ("boję się", {"valence": -0.8, "arousal": 0.75, "threat": 1.0}),
    ("mam strach", {"valence": -0.7, "arousal": 0.65, "threat": 0.9}),
    ("zagroż", {"valence": -0.55, "arousal": 0.45, "threat": 0.9}),
    ("niebezpiecz", {"valence": -0.6, "arousal": 0.5, "threat": 0.9}),
    ("skrzywd", {"valence": -0.7, "arousal": 0.65, "threat": 1.0}),
    ("zabij", {"valence": -0.9, "arousal": 0.9, "threat": 1.25}),
    ("groźb", {"valence": -0.7, "arousal": 0.7, "threat": 1.15}),
    ("groż", {"valence": -0.7, "arousal": 0.7, "threat": 1.15}),
    ("i am afraid", {"valence": -0.8, "arousal": 0.75, "threat": 1.0}),
    ("i'm afraid", {"valence": -0.8, "arousal": 0.75, "threat": 1.0}),
    ("threat", {"valence": -0.55, "arousal": 0.45, "threat": 0.95}),
    ("danger", {"valence": -0.6, "arousal": 0.5, "threat": 0.95}),
    ("hurt", {"valence": -0.55, "arousal": 0.55, "threat": 0.75}),
    ("kill", {"valence": -0.9, "arousal": 0.9, "threat": 1.25}),
)

_DIMENSIONS = ("valence", "arousal", "urgency", "threat", "attachment", "reward")

@dataclass(frozen=True)
class AffectEvidence:
    cue: str
    start: int
    end: int
    contributions: tuple[tuple[str, float], ...]
    kind: str = "lexical"

@dataclass(frozen=True)
class AffectEstimate:
    field: AffectiveField
    confidence: float
    surface_labels: tuple[str, ...]
    evidence: tuple[AffectEvidence, ...]
    text_sha256: str
    method: str = "transparent_lexical_surface_v1"
    truth_authority: bool = False
    semantic_authority: bool = False
    diagnostic_authority: bool = False
    modulation_authority: bool = False

    def as_dict(self) -> dict:
        return {
            "affect": {
                "valence": self.field.valence,
                "arousal": self.field.arousal,
                "urgency": self.field.urgency,
                "threat_relevance": self.field.threat_relevance,
                "attachment_relevance": self.field.attachment_relevance,
                "reward_relevance": self.field.reward_relevance,
            },
            "confidence": self.confidence,
            "surface_labels": list(self.surface_labels),
            "evidence": [
                {"cue": e.cue, "start": e.start, "end": e.end,
                 "contributions": dict(e.contributions), "kind": e.kind}
                for e in self.evidence
            ],
            "text_sha256": self.text_sha256,
            "method": self.method,
            "truth_authority": self.truth_authority,
            "semantic_authority": self.semantic_authority,
            "diagnostic_authority": self.diagnostic_authority,
            "modulation_authority": self.modulation_authority,
        }

@dataclass(frozen=True)
class TrackedAffectState:
    instantaneous: AffectEstimate
    smoothed: AffectiveField
    observations: int
    phase36: tuple[float, ...]
    path_change: float


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))

def _clip11(x: float) -> float:
    return max(-1.0, min(1.0, float(x)))

def _saturate_signed(x: float, scale: float = 1.65) -> float:
    return _clip11(tanh(float(x) / scale))

def _saturate_positive(x: float, scale: float = 1.55) -> float:
    return _clip01(1.0 - exp(-max(0.0, float(x)) / scale))

def _labels(field: AffectiveField, confidence: float) -> tuple[str, ...]:
    if confidence < 0.18:
        return ("insufficient-evidence",)
    out: list[str] = []
    if field.urgency >= 0.55:
        out.append("urgency-salient")
    if field.threat_relevance >= 0.55:
        out.append("threat-salient")
    if field.attachment_relevance >= 0.50:
        out.append("attachment-salient")
    if field.reward_relevance >= 0.50:
        out.append("preference-reward-salient")
    if field.valence <= -0.35 and field.arousal >= 0.40:
        out.append("negative-high-arousal")
    elif field.valence >= 0.35 and field.arousal >= 0.25:
        out.append("positive-activated")
    elif field.valence >= 0.35:
        out.append("positive-valence")
    elif field.valence <= -0.35:
        out.append("negative-valence")
    if not out:
        out.append("mixed-or-low-intensity")
    return tuple(out)

class AffectDetector:
    """Deterministic, inspectable affect inference from text surface cues.

    Numerical outputs are operational estimates, not measurements of a hidden mental
    state. A low-confidence result is UNKNOWN rather than silently neutral.
    """
    def __init__(self, cues: Sequence[tuple[str, dict[str, float]]] | None = None):
        self._cues = tuple(cues) if cues is not None else _CUES

    def detect(self, text: str) -> AffectEstimate:
        raw_text = str(text)
        lower = raw_text.casefold()
        scores = {d: 0.0 for d in _DIMENSIONS}
        evidence: list[AffectEvidence] = []
        for cue, contribution in self._cues:
            needle = cue.casefold()
            start_at = 0
            while True:
                idx = lower.find(needle, start_at)
                if idx < 0:
                    break
                for dim, value in contribution.items():
                    scores[dim] += float(value)
                evidence.append(AffectEvidence(
                    cue=raw_text[idx:idx+len(cue)], start=idx, end=idx+len(cue),
                    contributions=tuple(sorted((k, float(v)) for k, v in contribution.items()))
                ))
                start_at = idx + max(1, len(needle))
        exclam = raw_text.count("!")
        if exclam:
            contribution = {"arousal": min(0.65, 0.12 * exclam), "urgency": min(0.30, 0.05 * exclam)}
            for dim, value in contribution.items():
                scores[dim] += value
            evidence.append(AffectEvidence("!", 0, 0, tuple(sorted(contribution.items())), "punctuation"))
        tokens = _TOKEN_RE.findall(raw_text)
        caps = [t for t in tokens if len(t) >= 3 and t.isupper() and any(c.isalpha() for c in t)]
        if caps:
            contribution = {"arousal": min(0.55, 0.10 * len(caps))}
            scores["arousal"] += contribution["arousal"]
            evidence.append(AffectEvidence("ALL_CAPS", 0, 0, tuple(contribution.items()), "surface"))
        field = AffectiveField(
            valence=round(_saturate_signed(scores["valence"]), 6),
            arousal=round(_saturate_positive(scores["arousal"]), 6),
            urgency=round(_saturate_positive(scores["urgency"]), 6),
            threat_relevance=round(_saturate_positive(scores["threat"]), 6),
            attachment_relevance=round(_saturate_positive(scores["attachment"]), 6),
            reward_relevance=round(_saturate_positive(scores["reward"]), 6),
        )
        cue_mass = sum(sum(abs(v) for _, v in e.contributions) for e in evidence)
        confidence = round(_clip01(1.0 - exp(-cue_mass / 3.5)), 6) if cue_mass else 0.0
        return AffectEstimate(
            field=field,
            confidence=confidence,
            surface_labels=_labels(field, confidence),
            evidence=tuple(evidence),
            text_sha256=sha256(raw_text.encode("utf-8")).hexdigest(),
        )

def affect_phase36(field: AffectiveField) -> tuple[float, ...]:
    """Engineering 6D->36D PhaseNav-shaped mapping for trajectory diagnostics only."""
    six = ((field.valence + 1.0) / 2.0, field.arousal, field.urgency,
           field.threat_relevance, field.attachment_relevance, field.reward_relevance)
    out = []
    for block in range(6):
        offset = (KAPPA * TAU * block) % TAU
        for x in six:
            out.append((TAU * _clip01(x) + offset) % TAU)
    return tuple(out)

def _phase_path_change(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("dimension mismatch")
    if not a:
        return 0.0
    def delta(x: float, y: float) -> float:
        return (y - x + pi) % TAU - pi
    return (sum(delta(x, y) ** 2 for x, y in zip(a, b)) / len(a)) ** 0.5

class AffectTracker:
    """Temporal affect estimate with bounded history and no raw-text retention."""
    def __init__(self, detector: AffectDetector | None = None, memory: float = 0.65, history_limit: int = 32):
        if not 0.0 <= memory < 1.0:
            raise ValueError("memory must be in [0,1)")
        if history_limit < 1:
            raise ValueError("history_limit must be positive")
        self.detector = detector or AffectDetector()
        self.memory = float(memory)
        self.history_limit = int(history_limit)
        self._history: list[TrackedAffectState] = []

    @property
    def history(self) -> tuple[TrackedAffectState, ...]:
        return tuple(self._history)

    def update(self, text: str) -> TrackedAffectState:
        est = self.detector.detect(text)
        now = est.field
        if self._history:
            prev = self._history[-1].smoothed
            m = self.memory
            vals = tuple(m*x + (1.0-m)*y for x, y in zip(prev.as_tuple(), now.as_tuple()))
            smoothed = AffectiveField(*[round(v, 6) for v in vals])
            previous_phase = self._history[-1].phase36
        else:
            smoothed = now
            previous_phase = affect_phase36(now)
        phase = affect_phase36(smoothed)
        change = round(_phase_path_change(previous_phase, phase), 6) if self._history else 0.0
        state = TrackedAffectState(est, smoothed, len(self._history) + 1, phase, change)
        self._history.append(state)
        if len(self._history) > self.history_limit:
            del self._history[:-self.history_limit]
        return state
