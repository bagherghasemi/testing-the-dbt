# Sweep Design Log

Generated: 55 parameter-sweep scenarios for empirical calibration

LHS seed: 2026 | Dimensions: 8 primary + 13 secondary

Dedup rejections: 0

Existing configs used for dedup: 50


## Primary Parameter Grid

| Dim | Parameter | Low | High |
|-----|-----------|-----|------|
| 0 | `base_refund_rate` | 0.03 | 0.38 |
| 1 | `discount_probability` | 0.05 | 0.75 |
| 2 | `population_dynamics.daily_inflow_base` | 20 | 120 |
| 3 | `population_dynamics.inflow_decay_rate` | 0.0002 | 0.003 |
| 4 | `memory.brand_memory_decay_rate` | 0.002 | 0.05 |
| 5 | `memory.brand_memory_decay_after_days` | 15 | 160 |
| 6 | `brand_lifecycle.growth_velocity_threshold` | 4 | 15 |
| 7 | `population_dynamics.quality_drift_rate` | 4e-05 | 0.001 |

## Phase Effect Profiles

6 profiles assigned cyclically: healthy, aggressive_growth, crisis_arc, turnaround, stagnant, volatile

## Train/Test Split

- TRAIN: 39
- TEST: 16
- Stratification: sorted by base_refund_rate, every ~3.4th assigned to TEST

## Adversarial Configs (49-55)

- **gt_sweep_049** (seed 549, TRAIN): High refund + high repeat: can high refunds coexist with loyalty?
- **gt_sweep_050** (seed 550, TEST): Zero discount + decline: premium decline without discount explanation
- **gt_sweep_051** (seed 551, TRAIN): Ultra-fast decay: rapidly evolving psychological states
- **gt_sweep_052** (seed 552, TRAIN): Mid-sim inversion: direction change detection
- **gt_sweep_053** (seed 553, TEST): Minimum viable signal: formula stability with sparse data
- **gt_sweep_054** (seed 554, TRAIN): Maximum everything: simultaneous stress on all dimensions
- **gt_sweep_055** (seed 555, TRAIN): Slow-and-stable: ultra-stable long-memory brand

## Full Parameter Matrix

| # | Seed | Split | Profile | Refund | DiscProb | Inflow | InfDecay | MemDecay | MemAfter | GrowthVel | QualDrift |
|---|------|-------|---------|--------|----------|--------|----------|----------|----------|-----------|-----------|
| 001 | 501 | TRAIN | healthy | 0.032 | 0.494 | 40 | 0.00274 | 0.0436 | 140 | 14 | 0.000326 |
| 002 | 502 | TRAIN | aggressive_growth | 0.041 | 0.188 | 31 | 0.00220 | 0.0243 | 58 | 6 | 0.000167 |
| 003 | 503 | TEST | crisis_arc | 0.049 | 0.351 | 88 | 0.00040 | 0.0096 | 111 | 10 | 0.000543 |
| 004 | 504 | TRAIN | turnaround | 0.052 | 0.134 | 120 | 0.00076 | 0.0239 | 90 | 5 | 0.000874 |
| 005 | 505 | TRAIN | stagnant | 0.060 | 0.663 | 43 | 0.00216 | 0.0043 | 68 | 6 | 0.000852 |
| 006 | 506 | TEST | volatile | 0.073 | 0.092 | 79 | 0.00127 | 0.0073 | 126 | 13 | 0.000909 |
| 007 | 507 | TRAIN | healthy | 0.077 | 0.139 | 85 | 0.00235 | 0.0021 | 112 | 7 | 0.000587 |
| 008 | 508 | TRAIN | aggressive_growth | 0.084 | 0.281 | 35 | 0.00062 | 0.0331 | 138 | 5 | 0.000358 |
| 009 | 509 | TRAIN | crisis_arc | 0.094 | 0.299 | 33 | 0.00071 | 0.0056 | 17 | 7 | 0.000989 |
| 010 | 510 | TEST | turnaround | 0.099 | 0.214 | 77 | 0.00210 | 0.0251 | 101 | 9 | 0.000410 |
| 011 | 511 | TRAIN | stagnant | 0.109 | 0.160 | 105 | 0.00228 | 0.0124 | 33 | 13 | 0.000099 |
| 012 | 512 | TRAIN | volatile | 0.117 | 0.613 | 93 | 0.00092 | 0.0357 | 71 | 4 | 0.000150 |
| 013 | 513 | TEST | healthy | 0.123 | 0.249 | 90 | 0.00239 | 0.0185 | 124 | 5 | 0.000203 |
| 014 | 514 | TRAIN | aggressive_growth | 0.127 | 0.746 | 110 | 0.00026 | 0.0474 | 19 | 11 | 0.000763 |
| 015 | 515 | TRAIN | crisis_arc | 0.137 | 0.401 | 43 | 0.00052 | 0.0390 | 56 | 11 | 0.000124 |
| 016 | 516 | TEST | turnaround | 0.142 | 0.687 | 53 | 0.00156 | 0.0088 | 104 | 13 | 0.000396 |
| 017 | 517 | TRAIN | stagnant | 0.149 | 0.238 | 69 | 0.00148 | 0.0379 | 37 | 15 | 0.000790 |
| 018 | 518 | TRAIN | volatile | 0.155 | 0.053 | 23 | 0.00296 | 0.0495 | 64 | 10 | 0.000371 |
| 019 | 519 | TRAIN | healthy | 0.168 | 0.294 | 74 | 0.00153 | 0.0219 | 130 | 6 | 0.000825 |
| 020 | 520 | TEST | aggressive_growth | 0.170 | 0.465 | 29 | 0.00251 | 0.0067 | 149 | 13 | 0.000631 |
| 021 | 521 | TRAIN | crisis_arc | 0.180 | 0.454 | 98 | 0.00288 | 0.0324 | 115 | 9 | 0.000296 |
| 022 | 522 | TRAIN | turnaround | 0.183 | 0.695 | 27 | 0.00244 | 0.0390 | 27 | 5 | 0.000252 |
| 023 | 523 | TEST | stagnant | 0.196 | 0.712 | 62 | 0.00142 | 0.0103 | 32 | 8 | 0.000489 |
| 024 | 524 | TRAIN | volatile | 0.200 | 0.111 | 101 | 0.00133 | 0.0414 | 86 | 10 | 0.000693 |
| 025 | 525 | TRAIN | healthy | 0.206 | 0.424 | 82 | 0.00279 | 0.0120 | 107 | 4 | 0.000939 |
| 026 | 526 | TRAIN | aggressive_growth | 0.214 | 0.313 | 60 | 0.00111 | 0.0229 | 42 | 12 | 0.000198 |
| 027 | 527 | TEST | crisis_arc | 0.222 | 0.339 | 106 | 0.00107 | 0.0281 | 47 | 12 | 0.000561 |
| 028 | 528 | TRAIN | turnaround | 0.233 | 0.566 | 50 | 0.00187 | 0.0176 | 73 | 7 | 0.000436 |
| 029 | 529 | TRAIN | stagnant | 0.234 | 0.645 | 21 | 0.00206 | 0.0342 | 44 | 15 | 0.000077 |
| 030 | 530 | TEST | volatile | 0.244 | 0.659 | 46 | 0.00101 | 0.0362 | 77 | 11 | 0.000725 |
| 031 | 531 | TRAIN | healthy | 0.251 | 0.538 | 67 | 0.00036 | 0.0318 | 143 | 5 | 0.000605 |
| 032 | 532 | TRAIN | aggressive_growth | 0.258 | 0.172 | 57 | 0.00045 | 0.0202 | 49 | 14 | 0.000956 |
| 033 | 533 | TRAIN | crisis_arc | 0.266 | 0.591 | 55 | 0.00263 | 0.0457 | 148 | 13 | 0.000304 |
| 034 | 534 | TEST | turnaround | 0.272 | 0.383 | 49 | 0.00284 | 0.0291 | 154 | 14 | 0.000040 |
| 035 | 535 | TRAIN | stagnant | 0.279 | 0.387 | 38 | 0.00116 | 0.0147 | 83 | 8 | 0.000514 |
| 036 | 536 | TRAIN | volatile | 0.290 | 0.551 | 109 | 0.00165 | 0.0450 | 119 | 6 | 0.000448 |
| 037 | 537 | TEST | healthy | 0.294 | 0.734 | 71 | 0.00079 | 0.0154 | 99 | 12 | 0.000713 |
| 038 | 538 | TRAIN | aggressive_growth | 0.303 | 0.437 | 115 | 0.00266 | 0.0486 | 160 | 8 | 0.000279 |
| 039 | 539 | TRAIN | crisis_arc | 0.308 | 0.364 | 95 | 0.00254 | 0.0161 | 94 | 9 | 0.000667 |
| 040 | 540 | TEST | turnaround | 0.318 | 0.581 | 117 | 0.00180 | 0.0461 | 129 | 10 | 0.000753 |
| 041 | 541 | TRAIN | stagnant | 0.323 | 0.517 | 24 | 0.00086 | 0.0198 | 79 | 12 | 0.000814 |
| 042 | 542 | TRAIN | volatile | 0.330 | 0.624 | 73 | 0.00195 | 0.0134 | 135 | 10 | 0.000894 |
| 043 | 543 | TRAIN | healthy | 0.337 | 0.257 | 113 | 0.00167 | 0.0276 | 52 | 11 | 0.000112 |
| 044 | 544 | TEST | aggressive_growth | 0.347 | 0.481 | 103 | 0.00190 | 0.0425 | 62 | 9 | 0.000478 |
| 045 | 545 | TRAIN | crisis_arc | 0.354 | 0.066 | 65 | 0.00057 | 0.0262 | 93 | 8 | 0.000532 |
| 046 | 546 | TRAIN | turnaround | 0.362 | 0.504 | 58 | 0.00124 | 0.0036 | 152 | 8 | 0.000238 |
| 047 | 547 | TEST | stagnant | 0.366 | 0.208 | 93 | 0.00176 | 0.0303 | 22 | 7 | 0.000640 |
| 048 | 548 | TRAIN | volatile | 0.377 | 0.103 | 84 | 0.00025 | 0.0405 | 29 | 14 | 0.000980 |
| 049 | 549 | TRAIN | aggressive_growth | 0.250 | 0.300 | 60 | 0.00100 | 0.0100 | 90 | 8 | 0.000200 |
| 050 | 550 | TEST | stagnant | 0.100 | 0.020 | 30 | 0.00300 | 0.0150 | 60 | 10 | 0.000400 |
| 051 | 551 | TRAIN | volatile | 0.040 | 0.300 | 50 | 0.00100 | 0.0500 | 15 | 8 | 0.000300 |
| 052 | 552 | TRAIN | mid_sim_inversion | 0.120 | 0.350 | 70 | 0.00100 | 0.0100 | 90 | 8 | 0.000200 |
| 053 | 553 | TEST | healthy | 0.080 | 0.250 | 15 | 0.00100 | 0.0100 | 90 | 8 | 0.000200 |
| 054 | 554 | TRAIN | crisis_arc | 0.350 | 0.700 | 120 | 0.00200 | 0.0450 | 30 | 5 | 0.000900 |
| 055 | 555 | TRAIN | healthy | 0.050 | 0.200 | 40 | 0.00030 | 0.0030 | 150 | 12 | 0.000050 |
