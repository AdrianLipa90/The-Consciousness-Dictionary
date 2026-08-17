import math
from consciousness_dictionary.affect_detection import AffectDetector, AffectTracker, affect_phase36


def test_unknown_is_not_silently_neutral():
    e=AffectDetector().detect('Tabela ma trzy kolumny i dwa wiersze.')
    assert e.confidence == 0.0
    assert e.surface_labels == ('insufficient-evidence',)
    assert e.truth_authority is False
    assert e.diagnostic_authority is False


def test_polish_preference_positive():
    e=AffectDetector().detect('Bardzo lubię ten kierunek i wolę tę wersję.')
    assert e.field.valence > 0.35
    assert e.field.reward_relevance > 0.5
    assert 'preference-reward-salient' in e.surface_labels


def test_polish_urgency_negative_high_arousal():
    e=AffectDetector().detect('Kurwa, zrób to NATYCHMIAST!!!')
    assert e.field.valence < -0.25
    assert e.field.arousal > 0.5
    assert e.field.urgency > 0.5
    assert 'urgency-salient' in e.surface_labels
    assert e.field.threat_relevance < 0.5


def test_threat_relevance_is_salience_not_truth():
    e=AffectDetector().detect('To brzmi jak groźba i może być niebezpieczne.')
    assert e.field.threat_relevance > 0.5
    assert e.truth_authority is False
    assert e.semantic_authority is False


def test_attachment_relevance():
    e=AffectDetector().detect('Kocham ją i bardzo mi na niej zależy.')
    assert e.field.attachment_relevance > 0.5
    assert 'attachment-salient' in e.surface_labels


def test_phase36_is_finite_and_exactly_36():
    e=AffectDetector().detect('I prefer this and I am glad.')
    v=affect_phase36(e.field)
    assert len(v)==36
    assert all(math.isfinite(x) and 0.0 <= x < 2*math.pi for x in v)


def test_tracker_smoothes_and_does_not_store_raw_text():
    t=AffectTracker(memory=0.5)
    t.update('I love this.')
    b=t.update('This is urgent!')
    assert len(t.history)==2
    assert b.observations==2
    assert b.path_change >= 0
    assert hasattr(b.instantaneous, 'text_sha256')
    assert not hasattr(b.instantaneous, 'raw_text')


def test_english_fear_cue():
    e=AffectDetector().detect("I'm afraid this is dangerous.")
    assert e.field.threat_relevance > 0.5
    assert e.field.valence < 0
