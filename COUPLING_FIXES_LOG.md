# Coupling Fixes Log — v3

## Fix 1: REMOVE Disappointment → Desire (direct collapse)

**Research basis**: Disappointment ↔ Desire = ⊥/none. Disappointment is other-attributed; desire is a motivational state. Independent constructs.
**Code removed**: `_apply_disappointment_desire_collapse()` call at main.py ~line 1186.
**Replacement**: Trust-mediated path — Disappointment → Trust erosion (ps.py:387, existing) → Trust → Desire modulation (Fix 4, new).
**Config removed**: `disappointment_desire_threshold` (0.35), `disappointment_desire_collapse` (0.85).

---

## Fix 2: ADD Trust → Price Sensitivity (inverse, STRONG)

**Research**: Erdem & Swait 2004. Trust creates perceived brand uniqueness → reduces price comparison relevance.
**File**: `generators/psychological_state.py` — `apply_coupling_modulations()`
**Mechanism**: Daily continuous modulation for ALL customers. `ps += strength * (0.5 - trust)`. High trust pushes PS down; low trust pushes PS up.
**Config**: `coupling.trust_price_sensitivity_strength` = **0.005** (default)
**Math**: trust=0.8 for 30 days: PS shifts −0.045. trust=0.2 for 30 days: PS shifts +0.045.

---

## Fix 3: ADD Loyalty → Price Sensitivity (inverse, STRONG)

**Research**: Krishnamurthi & Raj 1991. Loyal customers assign idiosyncratic value → resist price switching.
**File**: Same function as Fix 2.
**Mechanism**: `ps += strength * (0.5 - loyalty)`.
**Config**: `coupling.loyalty_price_sensitivity_strength` = **0.003** (default)

---

## Fix 4: ADD Trust → Desire modulation (MODERATE)

**Research**: Chaudhuri & Holbrook 2001. Trust reduces perceived risk → enables desire expression.
**File**: `main.py` — `_update_desire_after_exposure()`
**Mechanism**: Desire lift from exposure multiplied by `(1 - mod + mod * trust)`. Range: [0.5, 1.0] at default mod=0.5.
**Config**: `coupling.trust_desire_modulation` = **0.5** (default)
**Effect**: trust=1.0 → full desire lift. trust=0.0 → 50% desire lift. Replaces removed Disappointment→Desire collapse with correct causal chain.

---

## Fix 5: ADD Satisfaction → Desire boost (MODERATE)

**Research**: Garbarino & Johnson 1999. Past satisfaction creates positive affect → sustains desire.
**File**: `main.py` — `_update_desire_after_exposure()`
**Mechanism**: `add *= (1 + sat_memory * boost)`. Capped at satisfaction_memory=1.0 to prevent runaway.
**Config**: `coupling.satisfaction_desire_boost` = **0.1** (default)

---

## Fix 6: ADD Desire → Quality Expectations inflation (WEAK)

**Research**: Brehm 1966, Festinger 1957. Desire inflates quality beliefs via confirmation bias.
**File**: `generators/psychological_state.py` — `apply_coupling_modulations()`
**Mechanism**: `qe += desire * strength` daily.
**Config**: `coupling.desire_quality_expectation_inflation` = **0.0005** (default)
**Math**: Typical desire 0.2 → +0.0001/day, +0.036/year. Genuinely weak — subtle treadmill effect.

---

## New Config Namespace: `coupling`

All new parameters live under a `coupling` key in config:

| Parameter | Default | Fix |
|-----------|---------|-----|
| `trust_price_sensitivity_strength` | 0.005 | 2 |
| `loyalty_price_sensitivity_strength` | 0.003 | 3 |
| `trust_desire_modulation` | 0.5 | 4 |
| `satisfaction_desire_boost` | 0.1 | 5 |
| `desire_quality_expectation_inflation` | 0.0005 | 6 |

All can be zeroed out to disable individual couplings for isolated testing.
