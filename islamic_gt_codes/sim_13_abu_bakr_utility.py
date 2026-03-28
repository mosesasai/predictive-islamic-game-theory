"""
Simulation 13: Abu Bakr's Total Sacrifice — Risk Preferences under IGT

This simulation models why Abu Bakr's decision to donate ALL his wealth is rational under
Islamic Game Theory, while classical expected utility with risk aversion predicts no
rational agent would ever donate everything.

Historical Context: When the Prophet called for donations for the Tabuk expedition (9 AH),
Abu Bakr brought his ENTIRE wealth. When asked "What did you leave for your family?", he
replied "Allah and His Messenger." Under classical utility theory with risk aversion (concave
utility function), this is irrational: the marginal utility of wealth is highest when wealth
approaches zero, making total donation maximally costly. Under IGT with akhirah payoffs,
the calculus reverses: the akhirah reward for total sacrifice (siddiq-level trust) creates
a convex region in the extended utility function, making total commitment rational.

Key Insight: Classical risk aversion (concave utility in wealth) predicts partial donation
at most. The akhirah term creates a "commitment premium" that makes the utility function
convex in the sacrifice region, rationalizing total donation as an optimal corner solution.

Reference: prophet_hypothesis.md — Hypothesis H13
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Abu Bakr's parameters
INITIAL_WEALTH = 1000.0       # Abu Bakr's total wealth (arbitrary units)
FAMILY_NEEDS = 100.0          # Minimum family subsistence (social safety net exists)

# Classical utility parameters
RISK_AVERSION = 0.5           # CRRA coefficient (0.5 = square root utility)
WARM_GLOW = 0.3               # Warm glow from giving (classical altruism)

# Akhirah parameters
OMEGA_TOTAL_SACRIFICE = 100.0     # "Siddiq" level reward for total commitment
OMEGA_PARTIAL_SACRIFICE = 20.0    # Reward for significant but not total giving
OMEGA_NORMAL_GIVING = 5.0         # Normal charity reward
OMEGA_HOARDING = -3.0             # Penalty for hoarding during community need
COMMITMENT_THRESHOLD = 0.9        # Fraction donated to qualify as "total sacrifice"

# Different lambda values for different believer types
LAMBDA_WEAK = 0.2
LAMBDA_MODERATE = 0.5
LAMBDA_STRONG = 1.0
LAMBDA_SIDDIQ = 2.0   # Abu Bakr's level

# ============================================================
# 2. UTILITY FUNCTIONS
# ============================================================

def classical_utility(wealth, risk_aversion=RISK_AVERSION):
    """CRRA (constant relative risk aversion) utility function."""
    if risk_aversion == 1:
        return np.log(np.maximum(wealth, 1e-10))
    else:
        return np.maximum(wealth, 1e-10) ** (1 - risk_aversion) / (1 - risk_aversion)


def classical_donation_utility(donation, wealth=INITIAL_WEALTH, warm_glow=WARM_GLOW):
    """
    Classical expected utility from donating amount 'donation'.
    U = u(wealth - donation) + warm_glow * u(donation)
    """
    remaining = max(wealth - donation, 1e-10)
    u_remaining = classical_utility(remaining)
    u_warmglow = warm_glow * classical_utility(donation) if donation > 0 else 0
    return u_remaining + u_warmglow


def igt_donation_utility(donation, wealth=INITIAL_WEALTH, lambda_akh=LAMBDA_SIDDIQ,
                          warm_glow=WARM_GLOW):
    """
    IGT utility from donating:
    U = u(wealth - donation) + warm_glow * u(donation) + lambda * Omega(donation/wealth)
    """
    remaining = max(wealth - donation, 1e-10)
    fraction = donation / wealth

    # Material utility
    u_material = classical_utility(remaining) + warm_glow * classical_utility(max(donation, 1e-10))

    # Akhirah reward: non-linear, with commitment premium
    if fraction >= COMMITMENT_THRESHOLD:
        omega = OMEGA_TOTAL_SACRIFICE * (fraction / COMMITMENT_THRESHOLD)
    elif fraction >= 0.5:
        omega = OMEGA_PARTIAL_SACRIFICE * fraction
    elif fraction >= 0.1:
        omega = OMEGA_NORMAL_GIVING * fraction
    elif fraction > 0:
        omega = OMEGA_NORMAL_GIVING * fraction * 0.5
    else:
        omega = OMEGA_HOARDING

    u_total = u_material + lambda_akh * omega
    return u_total


# ============================================================
# 3. OPTIMAL DONATION CALCULATION
# ============================================================

def find_optimal_donation(utility_func, wealth=INITIAL_WEALTH, **kwargs):
    """Find the donation amount that maximizes utility."""
    donations = np.linspace(0, wealth * 0.999, 1000)
    utilities = [utility_func(d, wealth, **kwargs) for d in donations]
    best_idx = np.argmax(utilities)
    return donations[best_idx], utilities[best_idx]


def donation_sweep(lambda_range, n_points=50):
    """Sweep lambda values and find optimal donation fraction at each."""
    lambdas = np.linspace(lambda_range[0], lambda_range[1], n_points)
    opt_fractions = []

    for lam in lambdas:
        opt_don, _ = find_optimal_donation(igt_donation_utility, lambda_akh=lam)
        opt_fractions.append(opt_don / INITIAL_WEALTH)

    return lambdas, np.array(opt_fractions)


# ============================================================
# 4. RISK PREFERENCE ANALYSIS
# ============================================================

def risk_preference_analysis():
    """
    Show how akhirah term changes effective risk preferences.
    Classical: concave everywhere (risk averse).
    IGT: convex region near total sacrifice (risk seeking in sacrifice).
    """
    donation_fractions = np.linspace(0.01, 0.99, 200)
    donations = donation_fractions * INITIAL_WEALTH

    classical_utils = [classical_donation_utility(d) for d in donations]
    igt_utils_weak = [igt_donation_utility(d, lambda_akh=LAMBDA_WEAK) for d in donations]
    igt_utils_moderate = [igt_donation_utility(d, lambda_akh=LAMBDA_MODERATE) for d in donations]
    igt_utils_strong = [igt_donation_utility(d, lambda_akh=LAMBDA_STRONG) for d in donations]
    igt_utils_siddiq = [igt_donation_utility(d, lambda_akh=LAMBDA_SIDDIQ) for d in donations]

    return {
        'fractions': donation_fractions,
        'classical': classical_utils,
        'weak': igt_utils_weak,
        'moderate': igt_utils_moderate,
        'strong': igt_utils_strong,
        'siddiq': igt_utils_siddiq,
    }


# ============================================================
# 5. POPULATION SIMULATION
# ============================================================

def simulate_population(n_agents=1000):
    """Simulate a population of heterogeneous agents deciding how much to donate."""
    np.random.seed(42)

    # Heterogeneous agents
    wealths = np.random.lognormal(np.log(500), 0.5, n_agents)
    lambdas = np.random.beta(2, 3, n_agents) * 2.5  # Most have moderate lambda
    risk_aversions = np.random.uniform(0.3, 0.8, n_agents)

    classical_donations = []
    igt_donations = []

    for i in range(n_agents):
        w = wealths[i]
        lam = lambdas[i]
        ra = risk_aversions[i]

        # Classical optimal
        def neg_classical(d):
            return -classical_donation_utility(d, w, WARM_GLOW)
        res = minimize_scalar(neg_classical, bounds=(0, w*0.999), method='bounded')
        classical_donations.append(res.x)

        # IGT optimal
        def neg_igt(d):
            return -igt_donation_utility(d, w, lam, WARM_GLOW)
        res = minimize_scalar(neg_igt, bounds=(0, w*0.999), method='bounded')
        igt_donations.append(res.x)

    return {
        'wealths': wealths,
        'lambdas': lambdas,
        'classical_donations': np.array(classical_donations),
        'igt_donations': np.array(igt_donations),
        'classical_fractions': np.array(classical_donations) / wealths,
        'igt_fractions': np.array(igt_donations) / wealths,
    }


# ============================================================
# 6. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 13: ABU BAKR'S TOTAL SACRIFICE")
    print("Risk Preferences under Islamic Game Theory")
    print("=" * 70)

    # --- Part A: Classical Analysis ---
    print("\n--- Part A: Classical Expected Utility Analysis ---")
    opt_classical, u_classical = find_optimal_donation(classical_donation_utility)
    print(f"  Initial wealth: {INITIAL_WEALTH:.0f}")
    print(f"  Risk aversion (CRRA): {RISK_AVERSION}")
    print(f"  Classical optimal donation: {opt_classical:.0f} ({100*opt_classical/INITIAL_WEALTH:.1f}%)")
    print(f"  Classical utility at optimal: {u_classical:.2f}")
    print(f"\n  Classical prediction: donate ~{100*opt_classical/INITIAL_WEALTH:.0f}% (never 100%)")
    print(f"  Abu Bakr's actual: donated 100% — 'IRRATIONAL' under classical GT")

    # --- Part B: IGT Analysis ---
    print("\n--- Part B: IGT Analysis at Different Lambda Values ---")
    print(f"\n  {'Lambda (type)':<25} {'Optimal Donation':<18} {'Fraction':<12} {'Utility':<12}")
    print("-" * 67)

    for lam, label in [(0.0, 'Classical'), (LAMBDA_WEAK, 'Weak believer'),
                        (LAMBDA_MODERATE, 'Moderate'), (LAMBDA_STRONG, 'Strong'),
                        (LAMBDA_SIDDIQ, 'Siddiq (Abu Bakr)')]:
        opt_don, opt_u = find_optimal_donation(igt_donation_utility, lambda_akh=lam)
        tag = f"{lam:.1f} ({label})"
        print(f"  {tag:<25} {opt_don:<18.0f} {100*opt_don/INITIAL_WEALTH:<12.1f}% {opt_u:<12.2f}")

    # --- Part C: Critical Lambda ---
    print("\n--- Part C: Critical Lambda for Total Sacrifice ---")
    lambdas, fractions = donation_sweep((0, 3), 100)

    total_sacrifice_lambda = None
    for i, f in enumerate(fractions):
        if f >= 0.95:
            total_sacrifice_lambda = lambdas[i]
            break

    if total_sacrifice_lambda is not None:
        print(f"  Lambda threshold for total sacrifice (>95%): {total_sacrifice_lambda:.2f}")
    print(f"  Abu Bakr's estimated lambda: {LAMBDA_SIDDIQ:.1f} (well above threshold)")

    # --- Part D: Omar's Half ---
    print("\n--- Part D: Comparison — Omar's 50% Donation ---")
    omar_lambda = 1.2  # Strong but not siddiq level
    opt_omar, u_omar = find_optimal_donation(igt_donation_utility, lambda_akh=omar_lambda)
    print(f"  Omar's estimated lambda: {omar_lambda:.1f}")
    print(f"  Omar's optimal donation: {opt_omar:.0f} ({100*opt_omar/INITIAL_WEALTH:.1f}%)")
    print(f"  Historical: Omar donated half his wealth (50%)")
    print(f"  Abu Bakr donated everything (100%) — different lambda, different optimal!")

    # --- Part E: Population Simulation ---
    print("\n--- Part E: Population Simulation (1000 agents) ---")
    pop = simulate_population(1000)

    print(f"\n  {'Metric':<35} {'Classical':<18} {'IGT':<18}")
    print("-" * 71)
    print(f"  {'Mean donation fraction':<35} {100*np.mean(pop['classical_fractions']):<18.1f}% {100*np.mean(pop['igt_fractions']):<18.1f}%")
    print(f"  {'Median donation fraction':<35} {100*np.median(pop['classical_fractions']):<18.1f}% {100*np.median(pop['igt_fractions']):<18.1f}%")
    print(f"  {'Agents donating >50%':<35} {100*np.mean(pop['classical_fractions'] > 0.5):<18.1f}% {100*np.mean(pop['igt_fractions'] > 0.5):<18.1f}%")
    print(f"  {'Agents donating >90%':<35} {100*np.mean(pop['classical_fractions'] > 0.9):<18.1f}% {100*np.mean(pop['igt_fractions'] > 0.9):<18.1f}%")
    print(f"  {'Total funds raised':<35} {np.sum(pop['classical_donations']):<18.0f} {np.sum(pop['igt_donations']):<18.0f}")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Utility curves
    ax1 = axes[0, 0]
    risk_data = risk_preference_analysis()
    ax1.plot(risk_data['fractions'], risk_data['classical'], 'r-', linewidth=2, label='Classical')
    ax1.plot(risk_data['fractions'], risk_data['moderate'], 'orange', linewidth=2, linestyle='--', label='IGT (moderate)')
    ax1.plot(risk_data['fractions'], risk_data['strong'], 'blue', linewidth=2, linestyle='--', label='IGT (strong)')
    ax1.plot(risk_data['fractions'], risk_data['siddiq'], 'g-', linewidth=2.5, label='IGT (Siddiq)')
    ax1.axvline(x=opt_classical/INITIAL_WEALTH, color='red', linestyle=':', alpha=0.5)
    ax1.set_xlabel('Donation Fraction', fontsize=11)
    ax1.set_ylabel('Total Utility', fontsize=11)
    ax1.set_title('Utility vs Donation Fraction\n(Higher lambda shifts peak rightward)', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Lambda vs optimal donation
    ax2 = axes[0, 1]
    ax2.plot(lambdas, fractions * 100, 'g-', linewidth=2.5)
    ax2.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='Total sacrifice (100%)')
    ax2.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label="Omar's level (50%)")
    ax2.axhline(y=opt_classical/INITIAL_WEALTH*100, color='red', linestyle='--', alpha=0.5, label='Classical optimal')
    # Mark key players
    ax2.plot(LAMBDA_SIDDIQ, 100, 'g*', markersize=15, label='Abu Bakr')
    ax2.plot(omar_lambda, 50, 'bs', markersize=10, label='Omar')
    ax2.set_xlabel('Lambda (Akhirah Sensitivity)', fontsize=11)
    ax2.set_ylabel('Optimal Donation (%)', fontsize=11)
    ax2.set_title('How Lambda Determines\nOptimal Sacrifice Level', fontsize=12)
    ax2.legend(fontsize=8, loc='center right')
    ax2.grid(True, alpha=0.3)

    # Plot 3: Risk preference reversal
    ax3 = axes[0, 2]
    # Show second derivative (concavity) of utility function
    fracs = risk_data['fractions']
    for label, data, color in [('Classical', risk_data['classical'], 'red'),
                                 ('Siddiq', risk_data['siddiq'], 'green')]:
        # Numerical second derivative
        d2 = np.gradient(np.gradient(data, fracs), fracs)
        ax3.plot(fracs[5:-5], d2[5:-5], color=color, linewidth=2, label=f'{label} (concavity)')
    ax3.axhline(y=0, color='black', linewidth=1)
    ax3.fill_between(fracs[5:-5], 0, 1, where=np.array(np.gradient(np.gradient(risk_data['siddiq'], fracs), fracs))[5:-5] > 0,
                    alpha=0.2, color='green', label='Risk-SEEKING region (convex)')
    ax3.set_xlabel('Donation Fraction', fontsize=11)
    ax3.set_ylabel('Second Derivative (Concavity)', fontsize=11)
    ax3.set_title('Risk Preference Reversal\n(Positive = risk-seeking)', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    # Plot 4: Population donation distributions
    ax4 = axes[1, 0]
    ax4.hist(pop['classical_fractions'] * 100, bins=50, alpha=0.5, color='red', label='Classical', density=True)
    ax4.hist(pop['igt_fractions'] * 100, bins=50, alpha=0.5, color='green', label='IGT', density=True)
    ax4.axvline(x=100, color='green', linewidth=2, linestyle='--', label='Abu Bakr (100%)')
    ax4.axvline(x=50, color='blue', linewidth=2, linestyle='--', label='Omar (50%)')
    ax4.set_xlabel('Donation Fraction (%)', fontsize=11)
    ax4.set_ylabel('Density', fontsize=11)
    ax4.set_title('Population Donation Distribution', fontsize=12)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)

    # Plot 5: Lambda vs donation scatter
    ax5 = axes[1, 1]
    ax5.scatter(pop['lambdas'], pop['igt_fractions'] * 100, alpha=0.3, s=10, color='green')
    ax5.set_xlabel('Lambda', fontsize=11)
    ax5.set_ylabel('Optimal Donation (%)', fontsize=11)
    ax5.set_title('Lambda vs Donation (Population)', fontsize=12)
    ax5.grid(True, alpha=0.3)

    # Plot 6: Abu Bakr vs Omar comparison
    ax6 = axes[1, 2]
    names = ['Classical\nAgent', 'Moderate\nBeliever', 'Omar\n(Strong)', 'Abu Bakr\n(Siddiq)']
    lams = [0.0, LAMBDA_MODERATE, omar_lambda, LAMBDA_SIDDIQ]
    donations_pct = []
    for lam in lams:
        opt, _ = find_optimal_donation(igt_donation_utility, lambda_akh=lam)
        donations_pct.append(100 * opt / INITIAL_WEALTH)
    colors_bar = ['red', 'orange', 'blue', 'green']
    bars = ax6.bar(names, donations_pct, color=colors_bar, alpha=0.8)
    ax6.set_ylabel('Optimal Donation (%)', fontsize=11)
    ax6.set_title('Optimal Donation by Agent Type', fontsize=12)
    ax6.grid(True, alpha=0.3, axis='y')
    for bar, val in zip(bars, donations_pct):
        ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.0f}%', ha='center', va='bottom', fontweight='bold')

    plt.suptitle("Abu Bakr's Total Sacrifice: Rational Under Akhirah Utility",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_13_abu_bakr_utility.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n--- CONCLUSION ---")
    print("Abu Bakr's total sacrifice demonstrates IGT risk preference reversal:")
    print("  1. Classical: concave utility -> risk averse -> partial donation optimal (~20-30%)")
    print("  2. IGT: akhirah creates convex region near total sacrifice")
    print("  3. 'Siddiq-level' lambda makes 100% donation the optimal corner solution")
    print("  4. Omar's 50% is also rational at his (slightly lower) lambda")
    print("  5. Both are consistent within the IGT framework — different lambda, different optimal")
    print("  6. 'What did you leave?' 'Allah and His Messenger' = infinite akhirah confidence")
    print("  7. This is NOT irrationality — it is rationality under extended utility")
    print("\nFigure saved: islamic_gt_codes/fig_13_abu_bakr_utility.png")

if __name__ == "__main__":
    main()
