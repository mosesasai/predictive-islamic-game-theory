"""
Simulation 01: Prisoner's Dilemma — Classical Nash vs. Muhammad Equilibrium (Muwakhat)

This simulation demonstrates how the Islamic Utility Function transforms the Prisoner's
Dilemma from a defection-dominant game into a cooperation-dominant game.

Historical Context: The Muwakhat (Brotherhood) of Medina, where Ansar voluntarily shared
half their wealth with Muhajir refugees — an act that contradicts Nash prediction.

Reference: prophet_hypothesis.md — Hypothesis H1
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product

# ============================================================
# 1. CLASSICAL PRISONER'S DILEMMA
# ============================================================

# Standard PD payoffs: T > R > P > S
T, R, P, S = 5, 3, 1, 0

classical_payoff_matrix = {
    ('C', 'C'): (R, R),  # (3, 3)
    ('C', 'D'): (S, T),  # (0, 5)
    ('D', 'C'): (T, S),  # (5, 0)
    ('D', 'D'): (P, P),  # (1, 1)
}

def classical_utility(action_i, action_j):
    """Classical utility: purely material payoff."""
    return classical_payoff_matrix[(action_i, action_j)][0]

# ============================================================
# 2. ISLAMIC GAME THEORY (IGT) UTILITY FUNCTION
# ============================================================

# Divine Accounting payoffs for actions
omega = {
    ('C', 'C'): 10.0,   # Mutual cooperation: highest divine reward
    ('C', 'D'): 7.0,    # Cooperated despite partner's defection: rewarded for integrity
    ('D', 'C'): 2.0,    # Defected against cooperator: significant divine penalty
    ('D', 'D'): 1.0,    # Mutual defection: low divine payoff
}

def igt_utility(action_i, action_j, alpha, lambda_akh):
    """
    Islamic Utility Function:
    U_i = u_i^mat + alpha * u_j^mat + lambda * Omega_i(actions)

    Parameters:
        alpha: altruism coefficient (empathy for other's welfare)
        lambda_akh: akhirah sensitivity coefficient
    """
    mat_i = classical_payoff_matrix[(action_i, action_j)][0]
    mat_j = classical_payoff_matrix[(action_i, action_j)][1]
    omega_val = omega[(action_i, action_j)]

    return mat_i + alpha * mat_j + lambda_akh * omega_val

# ============================================================
# 3. FIND EQUILIBRIA
# ============================================================

def find_dominant_strategy(utility_func, **params):
    """Find dominant strategy for player 1 (symmetric game)."""
    strategies = ['C', 'D']
    results = {}

    for si in strategies:
        results[si] = {}
        for sj in strategies:
            results[si][sj] = utility_func(si, sj, **params)

    # Check if C dominates D
    c_dominates = all(results['C'][sj] >= results['D'][sj] for sj in strategies)
    d_dominates = all(results['D'][sj] >= results['C'][sj] for sj in strategies)

    return results, c_dominates, d_dominates

# ============================================================
# 4. SIMULATION: PARAMETER SWEEP
# ============================================================

def parameter_sweep(alpha_range, lambda_range, n_points=50):
    """Sweep alpha and lambda to find cooperation boundary."""
    alphas = np.linspace(alpha_range[0], alpha_range[1], n_points)
    lambdas = np.linspace(lambda_range[0], lambda_range[1], n_points)

    cooperation_region = np.zeros((n_points, n_points))

    for i, alpha in enumerate(alphas):
        for j, lam in enumerate(lambdas):
            # Check if Cooperation is dominant strategy under IGT
            u_cc = igt_utility('C', 'C', alpha, lam)
            u_dc = igt_utility('D', 'C', alpha, lam)
            u_cd = igt_utility('C', 'D', alpha, lam)
            u_dd = igt_utility('D', 'D', alpha, lam)

            # C dominates D if: U(C,C) >= U(D,C) AND U(C,D) >= U(D,D)
            if u_cc >= u_dc and u_cd >= u_dd:
                cooperation_region[j, i] = 1.0  # Full cooperation
            elif u_cc >= u_dc or u_cd >= u_dd:
                cooperation_region[j, i] = 0.5  # Partial cooperation incentive
            else:
                cooperation_region[j, i] = 0.0  # Defection dominant

    return alphas, lambdas, cooperation_region

# ============================================================
# 5. POPULATION SIMULATION: MUWAKHAT DYNAMICS
# ============================================================

def simulate_muwakhat(n_ansar=50, n_muhajir=50, alpha=0.5, lambda_akh=0.8,
                       initial_wealth_ansar=100, initial_wealth_muhajir=0,
                       sharing_fraction=0.5, n_rounds=20):
    """
    Simulate the Muwakhat (Brotherhood) dynamics.
    Each Ansar is paired with a Muhajir and decides whether to share wealth.

    Returns wealth trajectories under Classical GT vs IGT.
    """
    np.random.seed(42)

    # Classical GT: Ansar keep everything (defect is dominant)
    wealth_classical_ansar = np.full((n_rounds, n_ansar), initial_wealth_ansar, dtype=float)
    wealth_classical_muhajir = np.full((n_rounds, n_muhajir), initial_wealth_muhajir, dtype=float)

    # IGT: Ansar share according to Muwakhat (cooperate is dominant)
    wealth_igt_ansar = np.full((n_rounds, n_ansar), initial_wealth_ansar, dtype=float)
    wealth_igt_muhajir = np.full((n_rounds, n_muhajir), initial_wealth_muhajir, dtype=float)

    # Growth rate from trade (both benefit from larger market)
    base_growth = 0.05
    cooperation_bonus = 0.03  # Additional growth from integrated community

    for t in range(1, n_rounds):
        # CLASSICAL: No sharing, independent growth
        for i in range(n_ansar):
            wealth_classical_ansar[t, i] = wealth_classical_ansar[t-1, i] * (1 + base_growth)
        for i in range(n_muhajir):
            # Muhajir with zero wealth stay at zero (poverty trap)
            wealth_classical_muhajir[t, i] = wealth_classical_muhajir[t-1, i] * (1 + base_growth)

        # IGT: Muwakhat sharing in first round, then cooperative growth
        if t == 1:
            for i in range(min(n_ansar, n_muhajir)):
                shared = wealth_igt_ansar[0, i] * sharing_fraction
                wealth_igt_ansar[t, i] = (wealth_igt_ansar[0, i] - shared) * (1 + base_growth + cooperation_bonus)
                wealth_igt_muhajir[t, i] = shared * (1 + base_growth + cooperation_bonus)
        else:
            for i in range(n_ansar):
                wealth_igt_ansar[t, i] = wealth_igt_ansar[t-1, i] * (1 + base_growth + cooperation_bonus)
            for i in range(n_muhajir):
                wealth_igt_muhajir[t, i] = wealth_igt_muhajir[t-1, i] * (1 + base_growth + cooperation_bonus)

    return {
        'classical': {'ansar': wealth_classical_ansar, 'muhajir': wealth_classical_muhajir},
        'igt': {'ansar': wealth_igt_ansar, 'muhajir': wealth_igt_muhajir}
    }

# ============================================================
# 6. ANALYSIS AND RESULTS
# ============================================================

def compute_gini(wealth_array):
    """Compute Gini coefficient for a wealth distribution."""
    w = np.sort(wealth_array.flatten())
    w = w[w > 0]  # Remove zeros for meaningful Gini
    if len(w) == 0:
        return 1.0
    n = len(w)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * w) - (n + 1) * np.sum(w)) / (n * np.sum(w))

def main():
    print("=" * 70)
    print("SIMULATION 01: PRISONER'S DILEMMA — NASH vs. MUHAMMAD EQUILIBRIUM")
    print("Historical Case: The Muwakhat (Brotherhood) of Medina")
    print("=" * 70)

    # --- Part A: Classical PD Analysis ---
    print("\n--- Part A: Classical Prisoner's Dilemma ---")
    print(f"\nPayoff Matrix (Player 1):")
    print(f"              Cooperate    Defect")
    print(f"  Cooperate   {R}            {S}")
    print(f"  Defect      {T}            {P}")
    print(f"\nNash Equilibrium: (Defect, Defect) -> Payoff: ({P}, {P})")
    print(f"Social Optimum:   (Coop, Coop)     -> Payoff: ({R}, {R})")
    print(f"Price of Anarchy: {(R+R)/(P+P):.1f}x")

    # --- Part B: IGT Analysis ---
    print("\n--- Part B: IGT Analysis (Multiple Parameter Settings) ---")

    test_params = [
        (0.0, 0.0, "Classical (alpha=0, lambda=0)"),
        (0.3, 0.0, "Moderate altruism only"),
        (0.0, 0.3, "Moderate akhirah only"),
        (0.3, 0.3, "Moderate both"),
        (0.5, 0.8, "Muwakhat-level (strong believer)"),
        (1.0, 1.0, "Maximum IGT parameters"),
    ]

    print(f"\n{'Parameters':<35} {'U(C,C)':<10} {'U(D,C)':<10} {'U(C,D)':<10} {'U(D,D)':<10} {'Dominant':<12}")
    print("-" * 87)

    for alpha, lam, label in test_params:
        u_cc = igt_utility('C', 'C', alpha, lam)
        u_dc = igt_utility('D', 'C', alpha, lam)
        u_cd = igt_utility('C', 'D', alpha, lam)
        u_dd = igt_utility('D', 'D', alpha, lam)

        c_dom = (u_cc >= u_dc) and (u_cd >= u_dd)
        d_dom = (u_dc >= u_cc) and (u_dd >= u_cd)

        dom_str = "Cooperate" if c_dom else ("Defect" if d_dom else "Neither")
        print(f"{label:<35} {u_cc:<10.2f} {u_dc:<10.2f} {u_cd:<10.2f} {u_dd:<10.2f} {dom_str:<12}")

    # --- Part C: Population Simulation ---
    print("\n--- Part C: Muwakhat Population Simulation ---")
    results = simulate_muwakhat(alpha=0.5, lambda_akh=0.8)

    # Final period statistics
    final_round = -1

    classical_total = np.concatenate([
        results['classical']['ansar'][final_round],
        results['classical']['muhajir'][final_round]
    ])
    igt_total = np.concatenate([
        results['igt']['ansar'][final_round],
        results['igt']['muhajir'][final_round]
    ])

    print(f"\n{'Metric':<40} {'Classical GT':<15} {'IGT (Muwakhat)':<15}")
    print("-" * 70)
    print(f"{'Total community wealth':<40} {np.sum(classical_total):<15.1f} {np.sum(igt_total):<15.1f}")
    print(f"{'Mean wealth (Ansar)':<40} {np.mean(results['classical']['ansar'][final_round]):<15.1f} {np.mean(results['igt']['ansar'][final_round]):<15.1f}")
    print(f"{'Mean wealth (Muhajir)':<40} {np.mean(results['classical']['muhajir'][final_round]):<15.1f} {np.mean(results['igt']['muhajir'][final_round]):<15.1f}")
    print(f"{'Gini coefficient':<40} {compute_gini(classical_total):<15.4f} {compute_gini(igt_total):<15.4f}")
    print(f"{'Min wealth (any individual)':<40} {np.min(classical_total):<15.1f} {np.min(igt_total):<15.1f}")

    # --- Part D: Parameter Boundary ---
    print("\n--- Part D: Cooperation Boundary Analysis ---")
    alphas, lambdas, coop_region = parameter_sweep((0, 1.5), (0, 1.5))

    # Find minimum alpha needed at lambda=0 and vice versa
    for target_lambda in [0.0, 0.2, 0.5, 1.0]:
        lam_idx = np.argmin(np.abs(lambdas - target_lambda))
        coop_alphas = alphas[coop_region[lam_idx, :] >= 1.0]
        min_alpha = coop_alphas[0] if len(coop_alphas) > 0 else float('inf')
        print(f"  At lambda={target_lambda:.1f}: minimum alpha for cooperation = {min_alpha:.3f}")

    # --- Plot ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Cooperation region
    ax1 = axes[0]
    im = ax1.imshow(coop_region, extent=[0, 1.5, 0, 1.5], origin='lower',
                     cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax1.set_xlabel('Altruism coefficient (alpha)', fontsize=12)
    ax1.set_ylabel('Akhirah sensitivity (lambda)', fontsize=12)
    ax1.set_title('Cooperation Region in PD\n(Green = Cooperate dominant)', fontsize=12)
    ax1.plot([0], [0], 'rx', markersize=15, label='Classical GT (alpha=0,lambda=0)')
    ax1.plot([0.5], [0.8], 'w*', markersize=15, label='Muwakhat parameters')
    ax1.legend(loc='upper left', fontsize=9)
    plt.colorbar(im, ax=ax1, label='Cooperation level')

    # Plot 2: Wealth trajectories
    ax2 = axes[1]
    rounds = range(20)
    ax2.plot(rounds, np.mean(results['classical']['ansar'], axis=1),
             'r-', linewidth=2, label='Classical Ansar')
    ax2.plot(rounds, np.mean(results['classical']['muhajir'], axis=1),
             'r--', linewidth=2, label='Classical Muhajir')
    ax2.plot(rounds, np.mean(results['igt']['ansar'], axis=1),
             'g-', linewidth=2, label='IGT Ansar')
    ax2.plot(rounds, np.mean(results['igt']['muhajir'], axis=1),
             'g--', linewidth=2, label='IGT Muhajir')
    ax2.set_xlabel('Time Period', fontsize=12)
    ax2.set_ylabel('Mean Wealth', fontsize=12)
    ax2.set_title('Muwakhat Wealth Dynamics\n(Classical vs. IGT)', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Plot 3: Gini over time
    ax3 = axes[2]
    gini_classical = []
    gini_igt = []
    for t in rounds:
        c_total = np.concatenate([results['classical']['ansar'][t], results['classical']['muhajir'][t]])
        i_total = np.concatenate([results['igt']['ansar'][t], results['igt']['muhajir'][t]])
        gini_classical.append(compute_gini(c_total))
        gini_igt.append(compute_gini(i_total))
    ax3.plot(rounds, gini_classical, 'r-', linewidth=2, label='Classical GT')
    ax3.plot(rounds, gini_igt, 'g-', linewidth=2, label='IGT (Muwakhat)')
    ax3.set_xlabel('Time Period', fontsize=12)
    ax3.set_ylabel('Gini Coefficient', fontsize=12)
    ax3.set_title('Inequality Over Time\n(Lower = More Equal)', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 1)

    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_01_prisoners_dilemma_muwakhat.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n[OK] Figure saved: islamic_gt_codes/fig_01_prisoners_dilemma_muwakhat.png")
    print("\n--- CONCLUSION ---")
    print("The Islamic Utility Function transforms the Prisoner's Dilemma:")
    print("* Classical Nash: (Defect, Defect) — rational selfishness -> collective failure")
    print("* Muhammad Equilibrium: (Cooperate, Cooperate) — rational morality -> collective flourishing")
    print("* The Muwakhat demonstrates this: Ansar VOLUNTARILY shared, producing a wealthier,")
    print("  more equal community than Nash-predicted hoarding would have achieved.")

if __name__ == "__main__":
    main()
