# Simulator Coupling Audit — Complete Cross-Variable Matrix

## Variables

| Abbrev | Variable | Type | Code Location |
|--------|----------|------|---------------|
| T | trust_score | Belief state | ps.py |
| D | disappointment_memory | Emotion memory | ps.py |
| S | satisfaction_memory | Emotion memory | ps.py |
| QE | quality_expectation | Belief state | ps.py |
| PS | price_sensitivity | Preference | ps.py |
| Des | expressed_desire_level | Motivational | main.py |
| Loy | loyalty_propensity | Trait/state | ps.py |
| Reg | regret_propensity | Trait | humans.py |

## Full Coupling Matrix

| From → To | Research | Simulator Status | Code Location | Fix |
|-----------|----------|-----------------|---------------|-----|
| S → T | ↑ strong (Garbarino & Johnson 1999) | ✅ EXISTS | ps.py:395-396 | — |
| D → T | ↓ strong (Zeelenberg & Pieters 2004) | ✅ EXISTS (3x asymmetric) | ps.py:386-387 | — |
| D → Loy | ↓ strong (Zeelenberg & Pieters 1999) | ✅ EXISTS | ps.py:429-434 | — |
| QE → D threshold | ↑ moderate (Oliver 1980 EDT) | ✅ EXISTS | ps.py:333,376 | — |
| D → QE | ↓ moderate (Tykocinski & Steinberg 2005) | ✅ EXISTS | ps.py:389-390 | — |
| S → QE | ↑ moderate, asymmetric (LaBarbera & Mazursky 1983) | ✅ EXISTS (1/3 rate) | ps.py:398-399 | — |
| QE ↔ PS | ↔ moderate (Dodds, Monroe & Grewal 1991) | ✅ EXISTS | ps.py:338-341 | — |
| T → funnel | ↑ strong (multiple) | ✅ EXISTS | commerce.py (multiple) | — |
| **D → Des** | **⊥ none** | **❌ EXISTED (WRONG)** | **main.py:617-631** | **Fix 1: REMOVED** |
| **T → PS** | **↓ strong (Erdem & Swait 2004)** | **✅ ADDED** | **ps.py:apply_coupling_modulations** | **Fix 2** |
| **Loy → PS** | **↓ strong (Krishnamurthi & Raj 1991)** | **✅ ADDED** | **ps.py:apply_coupling_modulations** | **Fix 3** |
| **T → Des** | **↑ moderate (Chaudhuri & Holbrook 2001)** | **✅ ADDED** | **main.py:_update_desire_after_exposure** | **Fix 4** |
| **S → Des** | **↑ moderate (Garbarino & Johnson 1999)** | **✅ ADDED** | **main.py:_update_desire_after_exposure** | **Fix 5** |
| **Des → QE** | **↑ weak (Brehm 1966)** | **✅ ADDED** | **ps.py:apply_coupling_modulations** | **Fix 6** |
| Reg → T | ⊥ none | ⚠️ Indirect via alignment | ps.py:179 | Acceptable (personality matching, not causal) |

## Couplings Verified as Absent (Correct)

| From → To | Research | Status |
|-----------|----------|--------|
| Reg → Des | ⊥ none | ✅ Absent |
| PS → T | ⊥ none | ✅ Absent |
| PS → Des | ⊥ none | ✅ Absent |
| S → PS | ⊥ none | ✅ Absent (only through T→PS now) |
| Des → T | ⊥ none | ✅ Absent |
| Loy → T | ⊥ none | ✅ Absent |
| Loy → Des | ⊥ none | ✅ Absent (only through Loy→PS) |

## Known Limitation: Regret r²

The regret r² regression (0.270 → 0.133) is NOT a coupling error. `regret_propensity` is a stable personality trait, not event-level experienced regret. The 3x trust asymmetry now explains more variance in hesitation and refund behavior, crowding out regret's signal. This is a pipeline signal-to-noise issue requiring SQL changes (out of scope).
