#!/usr/bin/env python3
"""
Generate 55 parameter-sweep scenario configs for empirical calibration.

48 via Latin Hypercube Sampling (8D primary + correlated secondary params)
 7 adversarial edge-case configs

Output: configs/gt_sweep_001.yaml – gt_sweep_055.yaml
        SWEEP_DESIGN_LOG.md
"""

import copy
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import yaml
from scipy.stats.qmc import LatinHypercube

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONFIGS_DIR = ROOT / "configs"
TEMPLATE_PATH = CONFIGS_DIR / "gt_healthy_growth.yaml"
OUTPUT_LOG = ROOT / "SWEEP_DESIGN_LOG.md"

# ---------------------------------------------------------------------------
# 8 primary LHS dimensions: [low, high]
# ---------------------------------------------------------------------------
PRIMARY_DIMS = {
    0: ("base_refund_rate",                           0.03,  0.38),
    1: ("discount_probability",                       0.05,  0.75),
    2: ("population_dynamics.daily_inflow_base",      20,    120),
    3: ("population_dynamics.inflow_decay_rate",      0.0002, 0.003),
    4: ("memory.brand_memory_decay_rate",             0.002, 0.050),
    5: ("memory.brand_memory_decay_after_days",       15,    160),
    6: ("brand_lifecycle.growth_velocity_threshold",  4,     15),
    7: ("population_dynamics.quality_drift_rate",     0.00004, 0.001),
}

L_BOUNDS = [PRIMARY_DIMS[i][1] for i in range(8)]
U_BOUNDS = [PRIMARY_DIMS[i][2] for i in range(8)]

# ---------------------------------------------------------------------------
# Phase-effect profiles
# ---------------------------------------------------------------------------
PHASE_PROFILES = {
    "healthy": None,
    "aggressive_growth": {
        "launch":     {"ctr_mult": 0.90, "cvr_mult": 0.80, "refund_mult": 1.1, "repeat_mult": 0.6, "cpa_mult": 0.9},
        "growth":     {"ctr_mult": 1.20, "cvr_mult": 1.15, "refund_mult": 0.8, "repeat_mult": 1.4, "cpa_mult": 1.0},
        "maturation": {"ctr_mult": 1.05, "cvr_mult": 1.10, "refund_mult": 0.85, "repeat_mult": 1.3, "cpa_mult": 1.1},
        "saturation": {"ctr_mult": 0.90, "cvr_mult": 0.85, "refund_mult": 1.0, "repeat_mult": 1.0, "cpa_mult": 1.3},
        "decline":    {"ctr_mult": 0.80, "cvr_mult": 0.70, "refund_mult": 1.2, "repeat_mult": 0.7, "cpa_mult": 1.5},
    },
    "crisis_arc": {
        "launch":     {"ctr_mult": 1.0,  "cvr_mult": 1.0,  "refund_mult": 1.0, "repeat_mult": 1.0, "cpa_mult": 1.0},
        "growth":     {"ctr_mult": 1.1,  "cvr_mult": 1.05, "refund_mult": 0.9, "repeat_mult": 1.2, "cpa_mult": 1.0},
        "maturation": {"ctr_mult": 0.80, "cvr_mult": 0.70, "refund_mult": 1.8, "repeat_mult": 0.4, "cpa_mult": 1.5},
        "saturation": {"ctr_mult": 0.60, "cvr_mult": 0.50, "refund_mult": 2.2, "repeat_mult": 0.2, "cpa_mult": 2.0},
        "decline":    {"ctr_mult": 0.45, "cvr_mult": 0.35, "refund_mult": 2.5, "repeat_mult": 0.1, "cpa_mult": 2.5},
    },
    "turnaround": {
        "launch":     {"ctr_mult": 1.0,  "cvr_mult": 1.0,  "refund_mult": 1.0, "repeat_mult": 1.0, "cpa_mult": 1.0},
        "growth":     {"ctr_mult": 1.0,  "cvr_mult": 0.95, "refund_mult": 1.5, "repeat_mult": 0.8, "cpa_mult": 1.1},
        "maturation": {"ctr_mult": 0.85, "cvr_mult": 0.80, "refund_mult": 2.0, "repeat_mult": 0.5, "cpa_mult": 1.4},
        "saturation": {"ctr_mult": 0.95, "cvr_mult": 0.90, "refund_mult": 0.7, "repeat_mult": 1.1, "cpa_mult": 1.2},
        "decline":    {"ctr_mult": 0.90, "cvr_mult": 0.85, "refund_mult": 0.5, "repeat_mult": 1.0, "cpa_mult": 1.3},
    },
    "stagnant": {
        "launch":     {"ctr_mult": 0.95, "cvr_mult": 0.95, "refund_mult": 1.05, "repeat_mult": 0.9, "cpa_mult": 1.05},
        "growth":     {"ctr_mult": 0.97, "cvr_mult": 0.97, "refund_mult": 1.03, "repeat_mult": 0.95, "cpa_mult": 1.03},
        "maturation": {"ctr_mult": 0.95, "cvr_mult": 0.93, "refund_mult": 1.05, "repeat_mult": 0.9, "cpa_mult": 1.08},
        "saturation": {"ctr_mult": 0.92, "cvr_mult": 0.90, "refund_mult": 1.08, "repeat_mult": 0.85, "cpa_mult": 1.12},
        "decline":    {"ctr_mult": 0.88, "cvr_mult": 0.85, "refund_mult": 1.10, "repeat_mult": 0.80, "cpa_mult": 1.18},
    },
    "volatile": {
        "launch":     {"ctr_mult": 1.15, "cvr_mult": 1.10, "refund_mult": 0.8, "repeat_mult": 1.3, "cpa_mult": 0.9},
        "growth":     {"ctr_mult": 0.75, "cvr_mult": 0.70, "refund_mult": 1.6, "repeat_mult": 0.5, "cpa_mult": 1.4},
        "maturation": {"ctr_mult": 1.10, "cvr_mult": 1.05, "refund_mult": 0.9, "repeat_mult": 1.2, "cpa_mult": 1.1},
        "saturation": {"ctr_mult": 0.70, "cvr_mult": 0.65, "refund_mult": 1.8, "repeat_mult": 0.4, "cpa_mult": 1.8},
        "decline":    {"ctr_mult": 0.95, "cvr_mult": 0.90, "refund_mult": 1.0, "repeat_mult": 0.9, "cpa_mult": 1.2},
    },
}

PROFILE_NAMES = list(PHASE_PROFILES.keys())  # deterministic order


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def set_nested(d, dotpath, value):
    """Set a value in a nested dict using dot-separated path."""
    keys = dotpath.split(".")
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value


def get_nested(d, dotpath, default=None):
    """Get a value from nested dict using dot-separated path."""
    keys = dotpath.split(".")
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


def extract_primary_params(config):
    """Extract the 8 primary params from a config dict. Returns array of length 8."""
    vals = []
    for i in range(8):
        path = PRIMARY_DIMS[i][0]
        default = 0.30 if path == "discount_probability" else None
        v = get_nested(config, path, default)
        if v is None:
            v = (PRIMARY_DIMS[i][1] + PRIMARY_DIMS[i][2]) / 2  # mid-range fallback
        vals.append(float(v))
    return np.array(vals)


def normalize_params(params):
    """Normalize to [0,1] using sweep ranges."""
    lo = np.array(L_BOUNDS)
    hi = np.array(U_BOUNDS)
    return (params - lo) / (hi - lo)


def load_existing_configs():
    """Load all existing gt_*.yaml configs (excluding gt_sweep_*) and extract primary params."""
    configs = []
    for f in sorted(CONFIGS_DIR.glob("gt_*.yaml")):
        if "gt_sweep_" in f.name:
            continue
        with open(f) as fh:
            cfg = yaml.safe_load(fh)
        configs.append((f.name, extract_primary_params(cfg)))
    return configs


def compute_secondary_params(primary_scaled, rng):
    """Derive secondary params from primary dims + noise."""
    # Normalize primary dims to [0,1]
    lo = np.array(L_BOUNDS)
    hi = np.array(U_BOUNDS)
    norms = (primary_scaled - lo) / (hi - lo)

    refund_norm = norms[0]
    disc_norm = norms[1]
    inflow_norm = norms[2]
    decay_norm = norms[4]
    decay_after_norm = norms[5]
    drift_rate_norm = norms[7]

    def noise(range_span):
        return rng.uniform(-0.15 * range_span, 0.15 * range_span)

    secondary = {}

    # base_ctr: inverse of refund
    secondary["base_ctr"] = clamp(
        0.042 - (refund_norm * 0.020) + noise(0.042 - 0.015),
        0.015, 0.042)

    # base_conversion: positive with discount
    secondary["base_conversion"] = clamp(
        0.020 + (disc_norm * 0.025) + noise(0.055 - 0.020),
        0.020, 0.055)

    # num_customers: positive with inflow
    secondary["num_customers"] = int(clamp(
        300 + (inflow_norm * 300) + noise(400),
        300, 700))

    # spending_propensity_sigma: independent uniform
    secondary["distribution_realism.spending_propensity_sigma"] = round(
        rng.uniform(0.35, 1.5), 3)

    # discount_only_fullprice_penalty: positive with discount
    secondary["memory.discount_only_fullprice_penalty"] = clamp(
        0.3 + (disc_norm * 0.3) + noise(0.4),
        0.3, 0.7)

    # discount_dependency_cvr_penalty: positive with discount
    secondary["long_term_accumulators.discount_dependency_cvr_penalty"] = clamp(
        0.15 + (disc_norm * 0.25) + noise(0.35),
        0.15, 0.50)

    # pool_expiry_days: inverse of decay_rate
    secondary["population_dynamics.pool_expiry_days"] = int(clamp(
        400 - (decay_norm * 250) + noise(300),
        100, 400))

    # pressure_ramp_rate: positive with refund
    secondary["feedback_loops.pressure_ramp_rate"] = clamp(
        0.01 + (refund_norm * 0.03) + noise(0.04),
        0.01, 0.05)

    # Memory regression params correlated with decay dimensions
    secondary["memory.satisfaction_memory_decay_rate"] = clamp(
        0.001 + (decay_norm * 0.005) + noise(0.007),
        0.001, 0.008)

    secondary["memory.disappointment_memory_decay_rate"] = clamp(
        0.002 + (decay_norm * 0.006) + noise(0.008),
        0.002, 0.010)

    secondary["memory.loyalty_regression_rate"] = clamp(
        0.001 + (decay_norm * 0.003) + noise(0.004),
        0.001, 0.005)

    secondary["memory.purchase_inactivity_decay_after_days"] = int(clamp(
        20 + (decay_after_norm * 50) + noise(70),
        20, 90))

    secondary["population_dynamics.quality_drift_cap"] = clamp(
        0.05 + (drift_rate_norm * 0.25) + noise(0.35),
        0.05, 0.40)

    return secondary


# ---------------------------------------------------------------------------
# Flow-style YAML representer for phase_effects inner dicts
# ---------------------------------------------------------------------------
class FlowDict(dict):
    """Dict subclass that renders in YAML flow style."""
    pass


def flow_dict_representer(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data, flow_style=True)


yaml.add_representer(FlowDict, flow_dict_representer)


def make_flow_phase_effects(pe):
    """Convert phase_effects dict to use FlowDict for inner dicts."""
    if pe is None:
        return None
    result = {}
    for phase, mults in pe.items():
        result[phase] = FlowDict(mults)
    return result


# ---------------------------------------------------------------------------
# Build a single config from template
# ---------------------------------------------------------------------------
def build_config(template, primary_vals, secondary_vals, profile_name, seed, index, split):
    """Build a complete config dict from template + swept params."""
    cfg = copy.deepcopy(template)

    # Set seed
    cfg["seed"] = seed

    # Set primary params
    for i in range(8):
        path = PRIMARY_DIMS[i][0]
        val = primary_vals[i]
        # Round appropriately
        if path in ("population_dynamics.daily_inflow_base",
                     "memory.brand_memory_decay_after_days",
                     "brand_lifecycle.growth_velocity_threshold"):
            val = int(round(val))
        else:
            val = round(float(val), 6)
        set_nested(cfg, path, val)

    # Set secondary params
    for path, val in secondary_vals.items():
        if isinstance(val, (int, np.integer)):
            val = int(val)
        else:
            val = round(float(val), 6)
        set_nested(cfg, path, val)

    # Set phase_effects
    profile = PHASE_PROFILES.get(profile_name)
    if profile is not None:
        cfg.setdefault("brand_lifecycle", {})
        cfg["brand_lifecycle"]["phase_effects"] = make_flow_phase_effects(profile)
    else:
        # Remove phase_effects if present in template
        if "brand_lifecycle" in cfg and "phase_effects" in cfg.get("brand_lifecycle", {}):
            del cfg["brand_lifecycle"]["phase_effects"]

    # Ensure diagnostic_output
    cfg["diagnostic_output"] = True

    # Build header comment
    header = (
        f"# Sweep scenario {index:03d} | seed={seed} | split={split} | profile={profile_name}\n"
        f"# Primary: refund={primary_vals[0]:.3f} disc_prob={primary_vals[1]:.3f} "
        f"inflow={primary_vals[2]:.0f} inflow_decay={primary_vals[3]:.5f}\n"
        f"#          mem_decay={primary_vals[4]:.4f} mem_after={primary_vals[5]:.0f} "
        f"growth_vel={primary_vals[6]:.0f} qual_drift={primary_vals[7]:.6f}\n"
    )

    return cfg, header


# ---------------------------------------------------------------------------
# Adversarial configs
# ---------------------------------------------------------------------------
def build_adversarial_configs(template, rng):
    """Build 7 adversarial configs (indices 49-55)."""
    adversarial = []

    # 49: High refund + high repeat
    primary = np.array([0.25, 0.30, 60, 0.001, 0.010, 90, 8, 0.0002])
    secondary = compute_secondary_params(primary, rng)
    profile_name = "aggressive_growth"
    # Boost repeat_mult in growth/maturation
    profile = copy.deepcopy(PHASE_PROFILES["aggressive_growth"])
    profile["growth"]["repeat_mult"] = 1.5
    profile["maturation"]["repeat_mult"] = 1.5
    adversarial.append((primary, secondary, "aggressive_growth", profile,
                         "High refund + high repeat: can high refunds coexist with loyalty?"))

    # 50: Zero discount + decline
    primary = np.array([0.10, 0.02, 30, 0.003, 0.015, 60, 10, 0.0004])
    secondary = compute_secondary_params(primary, rng)
    adversarial.append((primary, secondary, "stagnant", None,
                         "Zero discount + decline: premium decline without discount explanation"))

    # 51: Ultra-fast decay
    primary = np.array([0.04, 0.30, 50, 0.001, 0.050, 15, 8, 0.0003])
    secondary = compute_secondary_params(primary, rng)
    # Override regression rates to 3x default
    secondary["memory.satisfaction_memory_decay_rate"] = 0.009
    secondary["memory.disappointment_memory_decay_rate"] = 0.012
    secondary["memory.loyalty_regression_rate"] = 0.006
    adversarial.append((primary, secondary, "volatile", None,
                         "Ultra-fast decay: rapidly evolving psychological states"))

    # 52: Mid-sim inversion
    primary = np.array([0.12, 0.35, 70, 0.001, 0.010, 90, 8, 0.0002])
    secondary = compute_secondary_params(primary, rng)
    custom_profile = {
        "launch":     {"ctr_mult": 1.15, "cvr_mult": 1.10, "refund_mult": 0.8, "repeat_mult": 1.3, "cpa_mult": 0.9},
        "growth":     {"ctr_mult": 1.15, "cvr_mult": 1.10, "refund_mult": 0.8, "repeat_mult": 1.3, "cpa_mult": 0.9},
        "maturation": {"ctr_mult": 0.90, "cvr_mult": 0.85, "refund_mult": 1.2, "repeat_mult": 0.8, "cpa_mult": 1.2},
        "saturation": {"ctr_mult": 0.50, "cvr_mult": 0.45, "refund_mult": 2.5, "repeat_mult": 0.2, "cpa_mult": 2.0},
        "decline":    {"ctr_mult": 0.50, "cvr_mult": 0.40, "refund_mult": 2.5, "repeat_mult": 0.1, "cpa_mult": 2.5},
    }
    adversarial.append((primary, secondary, "mid_sim_inversion", custom_profile,
                         "Mid-sim inversion: direction change detection"))

    # 53: Minimum viable signal
    primary = np.array([0.08, 0.25, 15, 0.001, 0.010, 90, 8, 0.0002])
    secondary = compute_secondary_params(primary, rng)
    secondary["num_customers"] = 200
    adversarial.append((primary, secondary, "healthy", None,
                         "Minimum viable signal: formula stability with sparse data"))

    # 54: Maximum everything
    primary = np.array([0.35, 0.70, 120, 0.002, 0.045, 30, 5, 0.0009])
    secondary = compute_secondary_params(primary, rng)
    adversarial.append((primary, secondary, "crisis_arc", None,
                         "Maximum everything: simultaneous stress on all dimensions"))

    # 55: Slow-and-stable
    primary = np.array([0.05, 0.20, 40, 0.0003, 0.003, 150, 12, 0.00005])
    secondary = compute_secondary_params(primary, rng)
    secondary["memory.loyalty_regression_rate"] = 0.0008
    adversarial.append((primary, secondary, "healthy", None,
                         "Slow-and-stable: ultra-stable long-memory brand"))

    return adversarial


# ---------------------------------------------------------------------------
# Train/test split
# ---------------------------------------------------------------------------
def assign_splits(n_lhs, n_adversarial):
    """
    LHS samples: sort by refund, assign every 3rd-4th to test.
    Adversarial: 5 TRAIN (49,51,52,54,55), 2 TEST (50,53).
    Returns list of 'TRAIN'/'TEST' for all 55 samples.
    """
    splits = ["TRAIN"] * (n_lhs + n_adversarial)

    # For LHS (indices 0..47): stratified by refund
    # We'll assign ~16 test from LHS => need about 16 from 48
    # But plan says 39 TRAIN, 16 TEST total.
    # Adversarial: 5 TRAIN + 2 TEST = 7. So LHS: 34 TRAIN + 14 TEST = 48.
    # Sort LHS indices by refund, pick every ~3.4th for test
    # Actually plan says 39 TRAIN total, 16 TEST total
    # Adversarial: 5 TRAIN, 2 TEST
    # LHS: 34 TRAIN, 14 TEST
    lhs_test_count = 14
    # We'll pick every floor(48/14) ≈ 3rd from sorted order
    test_indices_in_lhs = set()
    step = 48 / lhs_test_count
    for j in range(lhs_test_count):
        idx = int(round(j * step + step / 2))
        idx = min(idx, 47)
        test_indices_in_lhs.add(idx)

    # These are indices in the refund-sorted order
    # We need to map back: this is done during generation
    return test_indices_in_lhs


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------
def main():
    print("Loading template...")
    with open(TEMPLATE_PATH) as f:
        template = yaml.safe_load(f)

    print("Loading existing configs for dedup...")
    existing = load_existing_configs()
    existing_params_norm = np.array([normalize_params(p) for _, p in existing])
    print(f"  Found {len(existing)} existing configs")

    # LHS sampling
    print("Generating 48 LHS samples (8D)...")
    rng = np.random.default_rng(2026)
    sampler = LatinHypercube(d=8, seed=2026)
    raw = sampler.random(n=48)

    # Scale to parameter ranges
    lo = np.array(L_BOUNDS)
    hi = np.array(U_BOUNDS)
    scaled = raw * (hi - lo) + lo

    # Deduplication
    print("Deduplicating against existing configs...")
    accepted = []
    rejection_count = 0

    for i in range(48):
        sample = scaled[i]
        sample_norm = normalize_params(sample)

        # Check distance to existing configs
        min_dist_existing = np.min(np.linalg.norm(existing_params_norm - sample_norm, axis=1))

        # Also check distance to already-accepted samples
        if accepted:
            accepted_norms = np.array([normalize_params(s) for s in accepted])
            min_dist_accepted = np.min(np.linalg.norm(accepted_norms - sample_norm, axis=1))
            min_dist = min(min_dist_existing, min_dist_accepted)
        else:
            min_dist = min_dist_existing

        threshold = 0.15
        attempts = 0
        while min_dist < threshold and attempts < 200:
            # Resample this point with jitter
            jitter = rng.uniform(-0.1, 0.1, size=8)
            sample_new = sample + jitter * (hi - lo)
            sample_new = np.clip(sample_new, lo, hi)
            sample_norm_new = normalize_params(sample_new)

            min_dist_existing = np.min(np.linalg.norm(existing_params_norm - sample_norm_new, axis=1))
            if accepted:
                accepted_norms = np.array([normalize_params(s) for s in accepted])
                min_dist_accepted = np.min(np.linalg.norm(accepted_norms - sample_norm_new, axis=1))
                min_dist = min(min_dist_existing, min_dist_accepted)
            else:
                min_dist = min_dist_existing

            if min_dist >= threshold:
                sample = sample_new
                sample_norm = sample_norm_new
                break

            attempts += 1
            rejection_count += 1

        if attempts >= 200:
            # Lower threshold
            threshold = 0.10
            if min_dist < threshold:
                warnings.warn(f"Sample {i}: could not achieve min distance 0.10 after 200 attempts "
                              f"(best: {min_dist:.3f}). Accepting anyway.")
            print(f"  WARNING: Sample {i} lowered threshold to 0.10 (dist={min_dist:.3f})")

        accepted.append(sample)

    print(f"  Accepted 48 samples ({rejection_count} total rejections)")

    # Sort by refund rate for stratified split
    refund_order = np.argsort([s[0] for s in accepted])
    sorted_accepted = [accepted[refund_order[i]] for i in range(48)]
    lhs_test_indices = assign_splits(48, 7)

    # Build LHS configs
    all_configs = []  # (index_1based, primary, secondary, profile_name, split, description, custom_pe)
    for rank, orig_idx in enumerate(range(48)):
        sample = sorted_accepted[rank]
        secondary = compute_secondary_params(sample, rng)
        profile_name = PROFILE_NAMES[rank % len(PROFILE_NAMES)]
        split = "TEST" if rank in lhs_test_indices else "TRAIN"
        idx = rank + 1  # 1-based
        all_configs.append((idx, sample, secondary, profile_name, split, "LHS sample", None))

    # Build adversarial configs
    adv = build_adversarial_configs(template, rng)
    adv_splits = {49: "TRAIN", 50: "TEST", 51: "TRAIN", 52: "TRAIN",
                  53: "TEST", 54: "TRAIN", 55: "TRAIN"}
    for j, (primary, secondary, profile_name, custom_pe, desc) in enumerate(adv):
        idx = 49 + j
        split = adv_splits[idx]
        all_configs.append((idx, primary, secondary, profile_name, split, desc, custom_pe))

    # Verify test set has >=3 phase profiles
    test_profiles = set()
    for idx, _, _, pn, sp, _, _ in all_configs:
        if sp == "TEST":
            test_profiles.add(pn)
    print(f"  Test set phase profiles: {test_profiles} ({len(test_profiles)} unique)")
    assert len(test_profiles) >= 3, f"Test set only has {len(test_profiles)} profiles, need >=3"

    # Count splits
    n_train = sum(1 for c in all_configs if c[4] == "TRAIN")
    n_test = sum(1 for c in all_configs if c[4] == "TEST")
    print(f"  Split: {n_train} TRAIN, {n_test} TEST")

    # Write YAML files
    print("Writing 55 YAML configs...")
    param_rows = []  # For design log
    for idx, primary, secondary, profile_name, split, desc, custom_pe in all_configs:
        seed = 500 + idx  # seeds 501-555
        cfg, header = build_config(template, primary, secondary, profile_name, seed, idx, split)

        # Handle custom phase_effects for adversarial configs
        if custom_pe is not None:
            cfg.setdefault("brand_lifecycle", {})
            cfg["brand_lifecycle"]["phase_effects"] = make_flow_phase_effects(custom_pe)

        filename = f"gt_sweep_{idx:03d}.yaml"
        filepath = CONFIGS_DIR / filename

        yaml_str = yaml.dump(cfg, default_flow_style=False, sort_keys=False, allow_unicode=True)

        with open(filepath, "w") as f:
            f.write(header)
            f.write(yaml_str)

        param_rows.append({
            "index": idx,
            "seed": seed,
            "split": split,
            "profile": profile_name,
            "desc": desc,
            "refund": primary[0],
            "disc_prob": primary[1],
            "inflow": primary[2],
            "inflow_decay": primary[3],
            "mem_decay": primary[4],
            "mem_after": primary[5],
            "growth_vel": primary[6],
            "qual_drift": primary[7],
        })

    # Validation pass
    print("\nValidation pass...")
    seeds_seen = set()
    errors = []
    for idx in range(1, 56):
        filename = f"gt_sweep_{idx:03d}.yaml"
        filepath = CONFIGS_DIR / filename
        if not filepath.exists():
            errors.append(f"{filename}: FILE MISSING")
            continue

        with open(filepath) as f:
            cfg = yaml.safe_load(f)

        # Check seed uniqueness
        s = cfg.get("seed")
        if s in seeds_seen:
            errors.append(f"{filename}: duplicate seed {s}")
        seeds_seen.add(s)

        # Check all template keys exist
        for key in template:
            if key not in cfg:
                errors.append(f"{filename}: missing top-level key '{key}'")

        # Check primary params in range
        for i in range(8):
            path = PRIMARY_DIMS[i][0]
            val = get_nested(cfg, path)
            lo_val = PRIMARY_DIMS[i][1]
            hi_val = PRIMARY_DIMS[i][2]
            if val is not None:
                # Adversarial configs may be slightly outside LHS range by design
                if idx <= 48 and (val < lo_val * 0.95 or val > hi_val * 1.05):
                    errors.append(f"{filename}: {path}={val} outside [{lo_val}, {hi_val}]")

    # Check seed range
    expected_seeds = set(range(501, 556))
    if seeds_seen != expected_seeds:
        missing = expected_seeds - seeds_seen
        extra = seeds_seen - expected_seeds
        if missing:
            errors.append(f"Missing seeds: {missing}")
        if extra:
            errors.append(f"Unexpected seeds: {extra}")

    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("  All 55 configs validated successfully!")

    # Summary stats
    print("\nParameter summary (LHS samples only, indices 1-48):")
    lhs_rows = [r for r in param_rows if r["index"] <= 48]
    for col in ["refund", "disc_prob", "inflow", "inflow_decay", "mem_decay", "mem_after", "growth_vel", "qual_drift"]:
        vals = [r[col] for r in lhs_rows]
        print(f"  {col:15s}: min={min(vals):.6f}  max={max(vals):.6f}  mean={np.mean(vals):.6f}")

    # Write design log
    print(f"\nWriting {OUTPUT_LOG}...")
    write_design_log(param_rows, rejection_count, existing)

    print("\nDone!")


def write_design_log(param_rows, rejection_count, existing_configs):
    """Write SWEEP_DESIGN_LOG.md with full documentation."""
    lines = []
    lines.append("# Sweep Design Log\n")
    lines.append(f"Generated: 55 parameter-sweep scenarios for empirical calibration\n")
    lines.append(f"LHS seed: 2026 | Dimensions: 8 primary + 13 secondary\n")
    lines.append(f"Dedup rejections: {rejection_count}\n")
    lines.append(f"Existing configs used for dedup: {len(existing_configs)}\n")
    lines.append("")

    # Parameter grid
    lines.append("## Primary Parameter Grid\n")
    lines.append("| Dim | Parameter | Low | High |")
    lines.append("|-----|-----------|-----|------|")
    for i in range(8):
        lines.append(f"| {i} | `{PRIMARY_DIMS[i][0]}` | {PRIMARY_DIMS[i][1]} | {PRIMARY_DIMS[i][2]} |")
    lines.append("")

    # Phase profiles
    lines.append("## Phase Effect Profiles\n")
    lines.append("6 profiles assigned cyclically: " + ", ".join(PROFILE_NAMES))
    lines.append("")

    # Train/test assignment
    lines.append("## Train/Test Split\n")
    n_train = sum(1 for r in param_rows if r["split"] == "TRAIN")
    n_test = sum(1 for r in param_rows if r["split"] == "TEST")
    lines.append(f"- TRAIN: {n_train}")
    lines.append(f"- TEST: {n_test}")
    lines.append(f"- Stratification: sorted by base_refund_rate, every ~3.4th assigned to TEST")
    lines.append("")

    # Adversarial descriptions
    lines.append("## Adversarial Configs (49-55)\n")
    for r in param_rows:
        if r["index"] >= 49:
            lines.append(f"- **gt_sweep_{r['index']:03d}** (seed {r['seed']}, {r['split']}): {r['desc']}")
    lines.append("")

    # Full parameter matrix
    lines.append("## Full Parameter Matrix\n")
    lines.append("| # | Seed | Split | Profile | Refund | DiscProb | Inflow | InfDecay | MemDecay | MemAfter | GrowthVel | QualDrift |")
    lines.append("|---|------|-------|---------|--------|----------|--------|----------|----------|----------|-----------|-----------|")
    for r in param_rows:
        lines.append(
            f"| {r['index']:03d} | {r['seed']} | {r['split']} | {r['profile']} | "
            f"{r['refund']:.3f} | {r['disc_prob']:.3f} | {r['inflow']:.0f} | "
            f"{r['inflow_decay']:.5f} | {r['mem_decay']:.4f} | {r['mem_after']:.0f} | "
            f"{r['growth_vel']:.0f} | {r['qual_drift']:.6f} |"
        )
    lines.append("")

    with open(OUTPUT_LOG, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
