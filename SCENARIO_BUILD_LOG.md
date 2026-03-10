# Scenario Build Log — 50-Scenario Behavioral Test Suite

**Date:** 2026-03-10
**Status:** BUILT — pending smoke tests and CI run

## Summary

- **Existing configs:** 11
- **New configs built:** 39
- **Total:** 50 (33 TRAIN + 17 TEST)

## Seed Registry

| Config | Seed | Set | Template Base |
|---|---|---|---|
| gt_healthy_growth | 42 | TRAIN | — |
| gt_bad_acquisition | 43 | TRAIN | — |
| gt_discount_addiction | 46 | TRAIN | — |
| gt_silent_churn | 47 | TRAIN | — |
| gt_extreme_good | 44 | TRAIN | — |
| gt_extreme_bad | 45 | TRAIN | — |
| gt_seasonal_brand | 301 | TRAIN | — |
| gt_reformed_discounter | 302 | TRAIN | — |
| gt_quality_collapse | 303 | TEST | — |
| gt_loyal_niche | 304 | TRAIN | — |
| gt_moderate_middle | 305 | TRAIN | — |
| gt_beauty_replenishment | 401 | TRAIN | healthy_growth |
| gt_fast_fashion_returns | 402 | TRAIN | healthy_growth |
| gt_supplement_habit | 403 | TRAIN | healthy_growth |
| gt_furniture_onedone | 404 | TEST | healthy_growth |
| gt_pet_loyalty | 405 | TRAIN | loyal_niche |
| gt_electronics_gift | 406 | TRAIN | seasonal_brand |
| gt_baby_lifecycle | 407 | TEST | healthy_growth |
| gt_fitness_newyear | 408 | TRAIN | healthy_growth |
| gt_viral_launch | 409 | TEST | bad_acquisition |
| gt_steady_compounder | 410 | TRAIN | healthy_growth |
| gt_maturity_plateau | 411 | TRAIN | moderate_middle |
| gt_slow_erosion | 412 | TEST | silent_churn |
| gt_brand_collapse | 413 | TEST | quality_collapse |
| gt_strategic_turnaround | 414 | TRAIN | reformed_discounter |
| gt_ultra_premium | 416 | TRAIN | loyal_niche |
| gt_strategic_promoter | 417 | TRAIN | healthy_growth |
| gt_deep_discount_trap | 419 | TEST | discount_addiction |
| gt_premium_to_discount | 421 | TEST | quality_collapse |
| gt_post_viral_hangover | 423 | TRAIN | bad_acquisition |
| gt_supply_chain_shock | 424 | TEST | quality_collapse |
| gt_offseason_crash | 425 | TRAIN | seasonal_brand |
| gt_post_boycott | 439 | TEST | quality_collapse |
| gt_bimodal_customers | 427 | TRAIN | healthy_growth |
| gt_whale_dependent | 428 | TEST | loyal_niche |
| gt_aging_cohort | 430 | TEST | silent_churn |
| gt_founder_community | 431 | TRAIN | loyal_niche |
| gt_habit_formation | 438 | TRAIN | healthy_growth |
| gt_subscription_churn | 432 | TRAIN | healthy_growth |
| gt_bracketing_fashion | 433 | TEST | healthy_growth |
| gt_guilt_regret | 434 | TRAIN | bad_acquisition |
| gt_bfcm_onetimer | 435 | TEST | seasonal_brand |
| gt_gifting_category | 436 | TRAIN | seasonal_brand |
| gt_trading_down | 437 | TRAIN | silent_churn |
| gt_wellness_obsessive | 440 | TEST | healthy_growth |
| gt_bnpl_impulse | 491 | TRAIN | healthy_growth |
| gt_tiktok_primary | 492 | TEST | bad_acquisition |
| gt_hypochondriac_supp | 493 | TRAIN | healthy_growth |
| gt_gen_cohort_diverge | 494 | TEST | healthy_growth |
| gt_economic_stress | 495 | TRAIN | silent_churn |

## Train/Test Split

### TRAIN (33)
gt_healthy_growth, gt_discount_addiction, gt_bad_acquisition, gt_silent_churn, gt_extreme_good, gt_extreme_bad, gt_seasonal_brand, gt_reformed_discounter, gt_loyal_niche, gt_moderate_middle, gt_beauty_replenishment, gt_fast_fashion_returns, gt_supplement_habit, gt_pet_loyalty, gt_electronics_gift, gt_fitness_newyear, gt_steady_compounder, gt_maturity_plateau, gt_strategic_turnaround, gt_ultra_premium, gt_strategic_promoter, gt_post_viral_hangover, gt_offseason_crash, gt_bimodal_customers, gt_founder_community, gt_habit_formation, gt_subscription_churn, gt_guilt_regret, gt_gifting_category, gt_trading_down, gt_bnpl_impulse, gt_hypochondriac_supp, gt_economic_stress

### TEST (17)
gt_quality_collapse, gt_furniture_onedone, gt_baby_lifecycle, gt_viral_launch, gt_slow_erosion, gt_brand_collapse, gt_deep_discount_trap, gt_premium_to_discount, gt_supply_chain_shock, gt_post_boycott, gt_whale_dependent, gt_aging_cohort, gt_bracketing_fashion, gt_bfcm_onetimer, gt_wellness_obsessive, gt_tiktok_primary, gt_gen_cohort_diverge

## Skip List (6 research scenarios covered by existing)

| Research # | Existing Config | Reason |
|---|---|---|
| #15 Seasonal Sawtooth | gt_seasonal_brand | Same Q4-heavy extreme seasonality |
| #18 Discount-Reliant | gt_discount_addiction | Same discount dependency profile |
| #20 Discount→Premium | gt_reformed_discounter | Same pivot arc |
| #22 Acute Quality Crisis | gt_quality_collapse | Same crisis pattern |
| #26 Loyalist Niche | gt_loyal_niche | Same ultra-devoted profile |
| #29 High-Churn Acquisition | gt_bad_acquisition | Same leaky-bucket model |

## Risky Configs Requiring Smoke Test

1. **gt_electronics_gift** — First use of `month_inflow_mult` parameter
2. **gt_bracketing_fashion** — 50% refund with 3 coordinated trust-protection overrides
3. **gt_viral_launch** — First use of `phase_inflow_mult` override
4. **gt_bfcm_onetimer** — Extreme `month_inflow_mult` values (4.0x)

## Technical Notes

- `phase_inflow_mult` defaults in code: {launch:0.5, growth:1.2, maturation:0.8, saturation:0.5, decline:0.4}
- `month_inflow_mult` defaults to empty dict (no seasonal inflow modulation)
- `refund_direct_trust_penalty` default: 0.08 (bypasses EMA)
- Trust floor: `max(0.1, trust_floor_from_refunds - cumulative_refund_rate_ema)`
- Phase transitions are emergent (threshold-based), not time-scripted
- Subscription churn (#32) approximated via high repeat_mult + short purchase_inactivity
- Whale concentration (#28) via spending_propensity_sigma=1.4 + small customer base

## Phase Transition Timing (Approximate)

Phase timing depends on growth_velocity_threshold and maturation_penetration_pct:
- Fast (velocity 4-6): Growth in ~months 3-6
- Medium (velocity 8-10): Growth in ~months 6-10
- Slow (velocity 12-15): Growth in ~months 10-14
- Maturation: penetration_pct 0.08=early, 0.15=mid, 0.18=late

Actual transitions will be documented post-run from god-mode exports.
