"""
Simulation 03: Stag Hunt — The Aqaba Pledges

The Stag Hunt models the trust problem: high-payoff cooperation requires mutual commitment.
The Aqaba Pledges demonstrate how the Naqib (leader) system and akhirah payoffs
solved the coordination problem.

Reference: prophet_hypothesis.md — Hypothesis H3
"""

import numpy as np
import matplotlib.pyplot as plt

# Stag Hunt payoffs
STAG_BOTH = 10     # Both commit: high reward (successful Hijra)
STAG_ALONE = -5    # Committed alone: captured, killed
HARE_BOTH = 3      # Both hedge: low-level faith, no migration
HARE_VS_STAG = 3   # Hedged while other committed: safe but small gain

def classical_expected_payoff(prob_other_stag):
    """Expected payoff under classical GT given belief about partner."""
    stag_eu = prob_other_stag * STAG_BOTH + (1 - prob_other_stag) * STAG_ALONE
    hare_eu = prob_other_stag * HARE_VS_STAG + (1 - prob_other_stag) * HARE_BOTH
    return stag_eu, hare_eu

def igt_expected_payoff(prob_other_stag, alpha=0.3, lambda_akh=0.5):
    """IGT expected payoff with altruism and akhirah."""
    omega_stag = 15.0  # Akhirah reward for commitment to faith
    omega_hare = 2.0   # Minimal akhirah reward for hedging

    stag_eu_mat = prob_other_stag * STAG_BOTH + (1 - prob_other_stag) * STAG_ALONE
    hare_eu_mat = prob_other_stag * HARE_VS_STAG + (1 - prob_other_stag) * HARE_BOTH

    # Add akhirah
    stag_eu = stag_eu_mat + lambda_akh * omega_stag
    hare_eu = hare_eu_mat + lambda_akh * omega_hare

    # Add altruistic component (commitment helps the community)
    stag_eu += alpha * prob_other_stag * 5
    hare_eu += alpha * prob_other_stag * 1

    return stag_eu, hare_eu

def simulate_naqib_effect(n_people=73, n_naqibs=12, base_belief=0.4, naqib_boost=0.15):
    """Simulate how the Naqib system shifts beliefs about coordination."""
    # Without Naqibs: each person has base_belief that others will commit
    beliefs_without = np.full(n_people, base_belief)

    # With Naqibs: observable commitment by leaders raises beliefs
    beliefs_with = np.full(n_people, base_belief)
    naqib_indices = np.random.choice(n_people, n_naqibs, replace=False)
    beliefs_with[naqib_indices] = 0.95  # Naqibs are committed

    # Others observe Naqibs' commitment -> their beliefs increase
    for i in range(n_people):
        if i not in naqib_indices:
            # Number of Naqibs in "visible range" (same tribe)
            visible_naqibs = np.random.poisson(2)
            beliefs_with[i] = min(0.95, base_belief + visible_naqibs * naqib_boost)

    return beliefs_without, beliefs_with

def main():
    print("=" * 70)
    print("SIMULATION 03: STAG HUNT — THE AQABA PLEDGES")
    print("=" * 70)

    # Critical belief threshold: where Stag becomes preferred
    print("\n--- Belief Thresholds for Stag (Commitment) ---")
    probs = np.linspace(0, 1, 100)

    for label, payoff_func, params in [
        ("Classical GT", classical_expected_payoff, {}),
        ("IGT (alpha=0.3, lambda=0.3)", igt_expected_payoff, {"alpha": 0.3, "lambda_akh": 0.3}),
        ("IGT (alpha=0.5, lambda=0.8)", igt_expected_payoff, {"alpha": 0.5, "lambda_akh": 0.8}),
    ]:
        threshold = None
        for p in probs:
            stag_eu, hare_eu = payoff_func(p, **params)
            if stag_eu >= hare_eu:
                threshold = p
                break
        print(f"  {label}: Stag preferred when P(others commit) >= {threshold:.2f}" if threshold else
              f"  {label}: Stag always preferred (dominant strategy)")

    # Naqib system effect
    print("\n--- Naqib System Effect ---")
    beliefs_without, beliefs_with = simulate_naqib_effect()

    stag_without = sum(1 for b in beliefs_without
                       if classical_expected_payoff(b)[0] > classical_expected_payoff(b)[1])
    stag_with = sum(1 for b in beliefs_with
                    if classical_expected_payoff(b)[0] > classical_expected_payoff(b)[1])

    print(f"  Without Naqibs: {stag_without}/73 choose Stag (commit)")
    print(f"  With 12 Naqibs: {stag_with}/73 choose Stag (commit)")
    print(f"  Historical: 73/73 pledged at Aqaba (100% commitment)")

    # With IGT
    stag_igt = sum(1 for b in beliefs_with
                   if igt_expected_payoff(b, 0.5, 0.8)[0] > igt_expected_payoff(b, 0.5, 0.8)[1])
    print(f"  With Naqibs + IGT: {stag_igt}/73 choose Stag")

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: Expected payoffs vs belief
    ax1 = axes[0]
    stag_c, hare_c = zip(*[classical_expected_payoff(p) for p in probs])
    stag_i, hare_i = zip(*[igt_expected_payoff(p, 0.5, 0.8) for p in probs])

    ax1.plot(probs, stag_c, 'r-', linewidth=2, label='Stag (Classical)')
    ax1.plot(probs, hare_c, 'r--', linewidth=2, label='Hare (Classical)')
    ax1.plot(probs, stag_i, 'g-', linewidth=2, label='Stag (IGT)')
    ax1.plot(probs, hare_i, 'g--', linewidth=2, label='Hare (IGT)')
    ax1.set_xlabel('Belief: P(Others Commit)', fontsize=11)
    ax1.set_ylabel('Expected Payoff', fontsize=11)
    ax1.set_title('Stag Hunt: Classical vs. IGT', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Belief distributions
    ax2 = axes[1]
    ax2.hist(beliefs_without, bins=20, alpha=0.5, color='red', label='Without Naqibs', density=True)
    ax2.hist(beliefs_with, bins=20, alpha=0.5, color='green', label='With 12 Naqibs', density=True)
    ax2.set_xlabel('Belief about Others Committing', fontsize=11)
    ax2.set_ylabel('Density', fontsize=11)
    ax2.set_title('Naqib System Shifts Beliefs', fontsize=12)
    ax2.legend(fontsize=10)

    # Plot 3: Commitment cascade
    ax3 = axes[2]
    cascade_rounds = 10
    n_committed_no_naqib = [0]
    n_committed_naqib = [12]
    n_committed_igt = [12]

    for r in range(cascade_rounds):
        # Without Naqib: slow cascade
        p = n_committed_no_naqib[-1] / 73
        new = sum(1 for _ in range(73 - n_committed_no_naqib[-1])
                  if np.random.random() < p * 0.5)
        n_committed_no_naqib.append(min(73, n_committed_no_naqib[-1] + new))

        # With Naqib: faster cascade
        p = n_committed_naqib[-1] / 73
        new = sum(1 for _ in range(73 - n_committed_naqib[-1])
                  if np.random.random() < p * 0.7)
        n_committed_naqib.append(min(73, n_committed_naqib[-1] + new))

        # With Naqib + IGT: fastest cascade
        p = n_committed_igt[-1] / 73
        new = sum(1 for _ in range(73 - n_committed_igt[-1])
                  if np.random.random() < min(0.95, p * 0.9 + 0.2))
        n_committed_igt.append(min(73, n_committed_igt[-1] + new))

    ax3.plot(n_committed_no_naqib, 'r-o', label='No Naqibs, Classical')
    ax3.plot(n_committed_naqib, 'orange', marker='s', label='12 Naqibs, Classical')
    ax3.plot(n_committed_igt, 'g-^', label='12 Naqibs + IGT')
    ax3.axhline(y=73, color='blue', linestyle='--', alpha=0.5, label='Full commitment (73)')
    ax3.set_xlabel('Round', fontsize=11)
    ax3.set_ylabel('Number Committed', fontsize=11)
    ax3.set_title('Commitment Cascade', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_03_stag_hunt_aqaba.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n[OK] Figure saved: islamic_gt_codes/fig_03_stag_hunt_aqaba.png")

if __name__ == "__main__":
    main()
