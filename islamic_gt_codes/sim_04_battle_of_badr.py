"""
Simulation 04: Battle of Badr — Incomplete Information Game with Divine Certainty

This simulation models the Battle of Badr (624 CE) as a game of incomplete information
where divine revelation provides a certainty advantage that overcomes numerical inferiority.

Historical Context: 313 poorly-equipped Muslim fighters faced ~1000 well-armed Quraysh.
Classical military analysis predicts decisive Quraysh victory. However, Quranic revelation
(8:9-10) promised divine support, giving Muslims pure-strategy commitment while Quraysh
played mixed strategies under uncertainty. The moral certainty from high lambda (akhirah
sensitivity) eliminated hesitation and produced unified tactical execution.

Key Insight: In games of incomplete information, certainty of purpose (pure strategy from
revelation) dominates mixed-strategy hedging, especially when the uncertain side's
mixed strategy induces coordination failures.

Reference: prophet_hypothesis.md — Hypothesis H4
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Force sizes
MUSLIMS = 313
QURAYSH = 1000

# Base combat effectiveness per soldier (normalized)
BASE_EFFECTIVENESS = 1.0

# Morale and commitment multipliers
CERTAINTY_MULTIPLIER = 2.5    # Pure strategy commitment bonus (no hesitation, unified action)
MIXED_STRATEGY_PENALTY = 0.6  # Coordination loss from mixed strategies (internal disagreement)

# Quraysh internal factions (incomplete information problem)
QURAYSH_HAWKS = 0.4           # Fraction wanting aggressive attack (Abu Jahl)
QURAYSH_DOVES = 0.3           # Fraction wanting negotiation/retreat (Utbah ibn Rabiah)
QURAYSH_UNCERTAIN = 0.3       # Fraction undecided

# Akhirah parameters
OMEGA_FIGHT_FOR_TRUTH = 20.0  # Shahada (martyrdom) reward
OMEGA_FLEE = -10.0            # Fleeing from righteous battle
OMEGA_FIGHT_OPPRESSION = -5.0 # Fighting to oppress

# Lanchester combat model parameters
ATTRITION_RATE = 0.003        # Base attrition coefficient

# ============================================================
# 2. CLASSICAL MIXED STRATEGY MODEL (QURAYSH PERSPECTIVE)
# ============================================================

def quraysh_mixed_strategy_effectiveness(n_simulations=1000):
    """
    Quraysh played a mixed strategy due to internal disagreement.
    Hawks wanted aggressive assault, Doves wanted to retreat after a show of force.
    This internal conflict reduced effective coordination.
    """
    np.random.seed(42)
    outcomes = []

    for _ in range(n_simulations):
        # Each Quraysh soldier independently decides commitment level
        commitments = np.zeros(QURAYSH)
        for i in range(QURAYSH):
            r = np.random.random()
            if r < QURAYSH_HAWKS:
                commitments[i] = 1.0      # Full commitment (hawks)
            elif r < QURAYSH_HAWKS + QURAYSH_DOVES:
                commitments[i] = 0.3      # Half-hearted (doves)
            else:
                commitments[i] = 0.5 + 0.3 * np.random.random()  # Uncertain, variable

        effective_force = np.sum(commitments) * BASE_EFFECTIVENESS * MIXED_STRATEGY_PENALTY
        outcomes.append(effective_force)

    return np.array(outcomes)


def muslim_pure_strategy_effectiveness():
    """
    Muslims played a pure strategy: total commitment from divine certainty.
    No mixed strategy, no hesitation, unified tactical execution.
    """
    # Every soldier at full commitment with certainty multiplier
    effective_force = MUSLIMS * BASE_EFFECTIVENESS * CERTAINTY_MULTIPLIER
    return effective_force


# ============================================================
# 3. IGT UTILITY: WHY PURE STRATEGY IS RATIONAL
# ============================================================

def soldier_utility_classical(fight, win_prob):
    """Classical expected utility for a soldier."""
    if fight:
        return win_prob * 10.0 + (1 - win_prob) * (-20.0)  # Win glory or die
    else:
        return 2.0  # Flee/desert — survive but no gain

def soldier_utility_igt(fight, win_prob, lambda_akh=1.0, righteous=True):
    """IGT utility includes akhirah payoffs."""
    omega = OMEGA_FIGHT_FOR_TRUTH if righteous else OMEGA_FIGHT_OPPRESSION
    if fight:
        material = win_prob * 10.0 + (1 - win_prob) * (-20.0)
        akhirah = lambda_akh * omega  # Fighting for truth always rewarded
        return material + akhirah
    else:
        material = 2.0
        akhirah = lambda_akh * OMEGA_FLEE if righteous else 0.0
        return material + akhirah


# ============================================================
# 4. LANCHESTER COMBAT MODEL
# ============================================================

def lanchester_battle(force_a, force_b, eff_a, eff_b, dt=0.1, max_steps=2000):
    """
    Lanchester's Square Law combat model.
    dA/dt = -beta * B, dB/dt = -alpha * A
    where alpha, beta are effectiveness-weighted attrition rates.
    """
    a_traj = [force_a]
    b_traj = [force_b]

    a, b = float(force_a), float(force_b)
    alpha = ATTRITION_RATE * eff_a  # A's ability to destroy B
    beta = ATTRITION_RATE * eff_b   # B's ability to destroy A

    for _ in range(max_steps):
        da = -beta * b * dt
        db = -alpha * a * dt
        a = max(0, a + da)
        b = max(0, b + db)
        a_traj.append(a)
        b_traj.append(b)
        if a <= 0 or b <= 0:
            break

    winner = 'A' if a > b else 'B'
    return np.array(a_traj), np.array(b_traj), winner


# ============================================================
# 5. MONTE CARLO SIMULATION
# ============================================================

def run_battle_simulations(n_sims=2000):
    """Run Monte Carlo simulations comparing classical vs IGT predictions."""
    np.random.seed(42)

    # Get Quraysh mixed strategy distribution
    quraysh_eff_dist = quraysh_mixed_strategy_effectiveness(n_sims)
    muslim_eff = muslim_pure_strategy_effectiveness()

    classical_results = []  # Raw numbers, no morale effects
    igt_results = []        # With commitment/morale effects

    for i in range(n_sims):
        # Classical prediction: pure numbers
        _, _, winner_classical = lanchester_battle(
            MUSLIMS, QURAYSH,
            BASE_EFFECTIVENESS, BASE_EFFECTIVENESS
        )
        classical_results.append(winner_classical)

        # IGT prediction: commitment effects
        quraysh_eff_per_soldier = quraysh_eff_dist[i] / QURAYSH
        _, _, winner_igt = lanchester_battle(
            MUSLIMS, QURAYSH,
            CERTAINTY_MULTIPLIER,
            quraysh_eff_per_soldier * MIXED_STRATEGY_PENALTY
        )
        igt_results.append(winner_igt)

    return classical_results, igt_results


# ============================================================
# 6. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 04: BATTLE OF BADR")
    print("Incomplete Information Game with Divine Certainty Advantage")
    print("=" * 70)

    # --- Part A: Force Comparison ---
    print("\n--- Part A: Force Comparison ---")
    print(f"  Muslim forces:  {MUSLIMS} soldiers")
    print(f"  Quraysh forces: {QURAYSH} soldiers")
    print(f"  Numerical ratio: {QURAYSH/MUSLIMS:.1f}:1 Quraysh advantage")

    muslim_eff = muslim_pure_strategy_effectiveness()
    quraysh_eff_dist = quraysh_mixed_strategy_effectiveness(2000)
    quraysh_eff_mean = np.mean(quraysh_eff_dist)

    print(f"\n  Muslim effective force (pure strategy):   {muslim_eff:.0f}")
    print(f"  Quraysh effective force (mixed strategy): {quraysh_eff_mean:.0f} (mean)")
    print(f"  Effective ratio: {muslim_eff/quraysh_eff_mean:.2f}:1")

    # --- Part B: Individual Soldier Decision ---
    print("\n--- Part B: Individual Soldier's Fight/Flee Decision ---")
    print(f"\n  {'Win Prob':<12} {'Classical(Fight)':<18} {'Classical(Flee)':<18} {'IGT(Fight)':<15} {'IGT(Flee)':<15} {'Classical':<12} {'IGT':<12}")
    print("-" * 102)

    for win_prob in [0.1, 0.2, 0.3, 0.5, 0.7]:
        cf = soldier_utility_classical(True, win_prob)
        cn = soldier_utility_classical(False, win_prob)
        igf = soldier_utility_igt(True, win_prob, lambda_akh=1.0, righteous=True)
        ign = soldier_utility_igt(False, win_prob, lambda_akh=1.0, righteous=True)
        c_dec = "FIGHT" if cf > cn else "FLEE"
        i_dec = "FIGHT" if igf > ign else "FLEE"
        print(f"  {win_prob:<12.1f} {cf:<18.2f} {cn:<18.2f} {igf:<15.2f} {ign:<15.2f} {c_dec:<12} {i_dec:<12}")

    print("\n  Key: Under classical GT, soldiers flee unless win probability > 0.73")
    print("  Under IGT with akhirah, soldiers fight even at very low win probabilities")

    # --- Part C: Monte Carlo Battle Outcomes ---
    print("\n--- Part C: Monte Carlo Battle Simulations (n=2000) ---")
    classical_results, igt_results = run_battle_simulations(2000)

    classical_muslim_wins = sum(1 for r in classical_results if r == 'A')
    igt_muslim_wins = sum(1 for r in igt_results if r == 'A')

    print(f"\n  {'Model':<35} {'Muslim Wins':<15} {'Quraysh Wins':<15} {'Muslim Win %':<15}")
    print("-" * 80)
    print(f"  {'Classical (numbers only)':<35} {classical_muslim_wins:<15} {2000-classical_muslim_wins:<15} {100*classical_muslim_wins/2000:<15.1f}")
    print(f"  {'IGT (commitment + mixed strat)':<35} {igt_muslim_wins:<15} {2000-igt_muslim_wins:<15} {100*igt_muslim_wins/2000:<15.1f}")
    print(f"  {'Historical outcome':<35} {'1':<15} {'0':<15} {'100.0':<15}")

    # --- Part D: Lambda Sensitivity ---
    print("\n--- Part D: How Lambda (Akhirah Sensitivity) Affects Commitment ---")
    print(f"\n  {'Lambda':<10} {'Fight Utility':<15} {'Flee Utility':<15} {'Decision':<12} {'Commitment %':<15}")
    print("-" * 67)

    for lam in [0.0, 0.2, 0.5, 0.8, 1.0, 1.5, 2.0]:
        fu = soldier_utility_igt(True, 0.3, lambda_akh=lam, righteous=True)
        flu = soldier_utility_igt(False, 0.3, lambda_akh=lam, righteous=True)
        dec = "FIGHT" if fu > flu else "FLEE"
        # Commitment proportion in a population with heterogeneous lambda
        commit_pct = min(100, max(0, 50 + 40 * (fu - flu) / max(abs(fu - flu), 0.01)))
        if fu > flu:
            commit_pct = 100.0
        else:
            commit_pct = max(0, 100 * (1 - (flu - fu) / 20))
        print(f"  {lam:<10.1f} {fu:<15.2f} {flu:<15.2f} {dec:<12} {commit_pct:<15.0f}")

    # --- Part E: Lanchester Trajectory ---
    print("\n--- Part E: Representative Battle Trajectory ---")
    a_traj, b_traj, winner = lanchester_battle(
        MUSLIMS, QURAYSH,
        CERTAINTY_MULTIPLIER,
        np.mean(quraysh_eff_dist) / QURAYSH * MIXED_STRATEGY_PENALTY
    )
    print(f"  Battle duration: {len(a_traj)} time steps")
    print(f"  Muslim survivors: {a_traj[-1]:.0f}")
    print(f"  Quraysh survivors: {b_traj[-1]:.0f}")
    print(f"  Winner: {'Muslims' if winner == 'A' else 'Quraysh'}")

    # Historical comparison
    print(f"\n  Historical: ~14 Muslim martyrs, ~70 Quraysh killed, ~70 captured")

    # --- Plot ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Effective force distributions
    ax1 = axes[0, 0]
    ax1.hist(quraysh_eff_dist, bins=50, alpha=0.6, color='red', label='Quraysh (mixed strategy)', density=True)
    ax1.axvline(x=muslim_eff, color='green', linewidth=3, label=f'Muslim (pure strategy): {muslim_eff:.0f}')
    ax1.axvline(x=quraysh_eff_mean, color='red', linewidth=2, linestyle='--', label=f'Quraysh mean: {quraysh_eff_mean:.0f}')
    ax1.axvline(x=QURAYSH, color='darkred', linewidth=2, linestyle=':', label=f'Quraysh raw numbers: {QURAYSH}')
    ax1.set_xlabel('Effective Combat Force', fontsize=11)
    ax1.set_ylabel('Density', fontsize=11)
    ax1.set_title('Effective Force: Pure vs. Mixed Strategy', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Battle trajectory
    ax2 = axes[0, 1]
    time_steps = np.arange(len(a_traj))
    ax2.plot(time_steps, a_traj, 'g-', linewidth=2.5, label='Muslim forces')
    ax2.plot(time_steps, b_traj, 'r-', linewidth=2.5, label='Quraysh forces')
    ax2.set_xlabel('Time Steps', fontsize=11)
    ax2.set_ylabel('Remaining Forces', fontsize=11)
    ax2.set_title('Lanchester Battle Trajectory (IGT Model)', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linewidth=0.5)

    # Plot 3: Fight/Flee decision under different lambda
    ax3 = axes[1, 0]
    lambdas = np.linspace(0, 2, 100)
    fight_utils = [soldier_utility_igt(True, 0.3, lam, True) for lam in lambdas]
    flee_utils = [soldier_utility_igt(False, 0.3, lam, True) for lam in lambdas]
    ax3.plot(lambdas, fight_utils, 'g-', linewidth=2.5, label='Fight (righteous cause)')
    ax3.plot(lambdas, flee_utils, 'r--', linewidth=2.5, label='Flee')
    # Find crossover
    crossover = None
    for i in range(len(lambdas) - 1):
        if fight_utils[i] < flee_utils[i] and fight_utils[i+1] >= flee_utils[i+1]:
            crossover = lambdas[i]
            break
    if crossover is not None:
        ax3.axvline(x=crossover, color='blue', linestyle=':', linewidth=2,
                    label=f'Commitment threshold: lambda={crossover:.2f}')
    ax3.set_xlabel('Lambda (Akhirah Sensitivity)', fontsize=11)
    ax3.set_ylabel('Expected Utility', fontsize=11)
    ax3.set_title('Fight vs. Flee Decision\n(Win prob = 0.3, Righteous cause)', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    # Plot 4: Win probability heatmap (numbers vs commitment)
    ax4 = axes[1, 1]
    force_ratios = np.linspace(0.1, 1.0, 50)   # Muslim/Quraysh ratio
    commitment_mults = np.linspace(1.0, 4.0, 50)  # Muslim commitment multiplier
    win_map = np.zeros((50, 50))

    for i, ratio in enumerate(force_ratios):
        for j, mult in enumerate(commitment_mults):
            m_force = int(QURAYSH * ratio)
            _, _, w = lanchester_battle(m_force, QURAYSH, mult, MIXED_STRATEGY_PENALTY * 0.6)
            win_map[j, i] = 1.0 if w == 'A' else 0.0

    im = ax4.imshow(win_map, extent=[0.1, 1.0, 1.0, 4.0], origin='lower',
                     cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax4.plot(MUSLIMS/QURAYSH, CERTAINTY_MULTIPLIER, 'w*', markersize=15, label='Badr parameters')
    ax4.set_xlabel('Force Ratio (Muslim/Quraysh)', fontsize=11)
    ax4.set_ylabel('Commitment Multiplier', fontsize=11)
    ax4.set_title('Victory Region\n(Green = Muslim victory)', fontsize=12)
    ax4.legend(fontsize=10, loc='upper left')
    plt.colorbar(im, ax=ax4, label='Win probability')

    plt.suptitle('Battle of Badr: Divine Certainty as Strategic Advantage', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_04_battle_of_badr.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n--- CONCLUSION ---")
    print("The Battle of Badr demonstrates how moral certainty transforms strategic outcomes:")
    print("  1. Classical GT (numbers only): 313 vs 1000 -> decisive Quraysh victory")
    print("  2. IGT with commitment: divine revelation creates pure-strategy advantage")
    print("  3. Quraysh internal disagreement (hawks vs doves) produces mixed-strategy penalty")
    print("  4. High lambda makes fighting rational even at low win probabilities")
    print("  5. The certainty-commitment advantage overcomes 3:1 numerical disadvantage")
    print("\nFigure saved: islamic_gt_codes/fig_04_battle_of_badr.png")

if __name__ == "__main__":
    main()
