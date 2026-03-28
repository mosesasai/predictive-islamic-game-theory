"""
Simulation 02: Hilf al-Fudul — Voluntary Enforcement Coalitions vs. Free-Riding

Multi-player Prisoner's Dilemma where clans choose to join or abstain from
a voluntary justice pact. Classical GT predicts free-riding; IGT predicts joining.

Reference: prophet_hypothesis.md — Hypothesis H2
"""

import numpy as np
import matplotlib.pyplot as plt

N_CLANS = 8
ENFORCEMENT_COST = 3.0
SECURITY_BENEFIT = 5.0
REPUTATION_BENEFIT = 2.0
FREE_RIDER_BENEFIT = 2.0  # Benefit from others' enforcement without joining

def classical_payoff(join, n_joiners, n_clans=N_CLANS):
    """Classical material payoff for a clan."""
    if join:
        if n_joiners >= 3:  # Minimum viable coalition
            return SECURITY_BENEFIT + REPUTATION_BENEFIT - ENFORCEMENT_COST
        else:
            return -ENFORCEMENT_COST  # Lonely enforcer
    else:
        if n_joiners >= 3:
            return FREE_RIDER_BENEFIT  # Free ride on others
        else:
            return 0  # No pact, no benefit

def igt_payoff(join, n_joiners, alpha=0.3, lambda_akh=0.5, n_clans=N_CLANS):
    """IGT payoff including altruism and akhirah."""
    material = classical_payoff(join, n_joiners, n_clans)

    # Altruistic: benefit from others' protection
    others_protected = n_joiners / n_clans * 10
    altruistic = alpha * others_protected if join else 0

    # Akhirah: divine reward for standing with the oppressed
    omega_join = 8.0   # Reward for justice commitment
    omega_abstain = 1.0  # No reward for inaction when capable
    akhirah = lambda_akh * (omega_join if join else omega_abstain)

    return material + altruistic + akhirah

def simulate_coalition_formation(payoff_func, n_sims=1000, **params):
    """Simulate iterated best-response coalition formation."""
    results = []
    for _ in range(n_sims):
        # Start with random decisions
        decisions = np.random.choice([True, False], size=N_CLANS)

        for _ in range(20):  # Convergence iterations
            new_decisions = decisions.copy()
            for i in range(N_CLANS):
                n_others_join = sum(decisions) - (1 if decisions[i] else 0)
                payoff_join = payoff_func(True, n_others_join + 1, **params)
                payoff_abstain = payoff_func(False, n_others_join, **params)
                new_decisions[i] = payoff_join > payoff_abstain

            if np.array_equal(decisions, new_decisions):
                break
            decisions = new_decisions

        results.append(sum(decisions))

    return results

def main():
    print("=" * 70)
    print("SIMULATION 02: HILF AL-FUDUL — VOLUNTARY JUSTICE COALITION")
    print("=" * 70)

    # Classical GT
    classical_results = simulate_coalition_formation(classical_payoff)
    print(f"\nClassical GT:")
    print(f"  Mean joiners: {np.mean(classical_results):.1f} / {N_CLANS}")
    print(f"  Pact forms (>=3): {sum(1 for r in classical_results if r >= 3)/len(classical_results)*100:.0f}%")

    # IGT with varying parameters
    param_sets = [
        (0.1, 0.1, "Low IGT"),
        (0.3, 0.3, "Moderate IGT"),
        (0.5, 0.5, "Strong IGT"),
        (0.5, 0.8, "Historical (Hilf al-Fudul)"),
    ]

    print(f"\nIGT Results:")
    for alpha, lam, label in param_sets:
        igt_results = simulate_coalition_formation(igt_payoff, alpha=alpha, lambda_akh=lam)
        print(f"  {label} (alpha={alpha}, lambda={lam}): Mean={np.mean(igt_results):.1f}, "
              f"Pact forms={sum(1 for r in igt_results if r >= 3)/len(igt_results)*100:.0f}%")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Payoff comparison
    ax1 = axes[0]
    n_range = range(N_CLANS + 1)
    join_classical = [classical_payoff(True, n) for n in n_range]
    abstain_classical = [classical_payoff(False, n) for n in n_range]
    join_igt = [igt_payoff(True, n, 0.5, 0.8) for n in n_range]
    abstain_igt = [igt_payoff(False, n, 0.5, 0.8) for n in n_range]

    ax1.plot(n_range, join_classical, 'r-o', label='Join (Classical)')
    ax1.plot(n_range, abstain_classical, 'r--o', label='Abstain (Classical)')
    ax1.plot(n_range, join_igt, 'g-s', label='Join (IGT)')
    ax1.plot(n_range, abstain_igt, 'g--s', label='Abstain (IGT)')
    ax1.set_xlabel('Number of Clans Joining', fontsize=11)
    ax1.set_ylabel('Payoff', fontsize=11)
    ax1.set_title('Payoff to Join vs. Abstain', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Coalition size distribution
    ax2 = axes[1]
    ax2.hist(classical_results, bins=range(N_CLANS+2), alpha=0.5, color='red',
             label='Classical GT', density=True, align='left')
    igt_hist = simulate_coalition_formation(igt_payoff, alpha=0.5, lambda_akh=0.8)
    ax2.hist(igt_hist, bins=range(N_CLANS+2), alpha=0.5, color='green',
             label='IGT (alpha=0.5, lambda=0.8)', density=True, align='left')
    ax2.axvline(x=3, color='blue', linestyle='--', label='Min viable coalition')
    ax2.set_xlabel('Number of Clans Joining', fontsize=11)
    ax2.set_ylabel('Probability', fontsize=11)
    ax2.set_title('Coalition Size Distribution', fontsize=12)
    ax2.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_02_hilf_al_fudul.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n[OK] Figure saved: islamic_gt_codes/fig_02_hilf_al_fudul.png")

if __name__ == "__main__":
    main()
