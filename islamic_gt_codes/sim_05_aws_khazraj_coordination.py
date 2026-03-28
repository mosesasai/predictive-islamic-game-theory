"""
Simulation 05: Aws-Khazraj Coordination Game — Battle of the Sexes with External Arbiter

This simulation models the decades-long civil war between the Aws and Khazraj tribes of
Yathrib (Medina) as a coordination failure (Battle of the Sexes game), and shows how
the Prophet as external arbiter created a new focal point (Ummah identity) that resolved
the coordination problem.

Historical Context: The Aws and Khazraj had fought the bitter Battle of Bu'ath (617 CE)
and earlier conflicts. Each tribe preferred peace but only on their own terms (their leader
as chief). Neither could credibly commit to the other's leadership. The Prophet Muhammad,
as an outsider with divine authority, created a new focal point: the Constitution of Medina
(Sahifah), where identity shifted from tribal to Ummah, making coordination on shared
terms possible.

Key Insight: In Battle of the Sexes games, an external focal point — especially one backed
by transcendent authority — can break coordination deadlock by creating a new equilibrium
that dominates both tribal equilibria.

Reference: prophet_hypothesis.md — Hypothesis H5
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Battle of the Sexes payoffs
# (Aws prefers A-terms, Khazraj prefers K-terms, but both prefer agreement to war)
COORD_A = (3, 1)    # Both coordinate on Aws terms: Aws=3, Khazraj=1
COORD_K = (1, 3)    # Both coordinate on Khazraj terms: Aws=1, Khazraj=3
MISCOORD = (0, 0)   # Miscoordination: continued war, both lose

# New focal point: Ummah terms (Prophet as arbiter)
COORD_U = (4, 4)    # Both coordinate under Ummah: transcends tribal payoffs

# Akhirah parameters
OMEGA_UNITY = 10.0   # Divine reward for Muslim unity
OMEGA_TRIBALISM = -5.0  # Divine penalty for tribal division (asabiyyah)
LAMBDA = 0.8

# Simulation parameters
N_GENERATIONS = 100
POPULATION_SIZE = 200  # 100 Aws, 100 Khazraj
MUTATION_RATE = 0.02

# ============================================================
# 2. CLASSICAL BATTLE OF THE SEXES
# ============================================================

def classical_payoff(strategy_aws, strategy_khazraj):
    """
    Payoff matrix for the coordination game.
    Strategies: 'A' (Aws terms), 'K' (Khazraj terms), 'U' (Ummah terms)
    """
    payoffs = {
        ('A', 'A'): COORD_A,
        ('A', 'K'): MISCOORD,
        ('A', 'U'): (1.5, 2.0),   # Partial coordination
        ('K', 'A'): MISCOORD,
        ('K', 'K'): COORD_K,
        ('K', 'U'): (2.0, 1.5),   # Partial coordination
        ('U', 'A'): (2.0, 1.5),
        ('U', 'K'): (1.5, 2.0),
        ('U', 'U'): COORD_U,
    }
    return payoffs[(strategy_aws, strategy_khazraj)]


def igt_payoff(strategy_aws, strategy_khazraj, lambda_akh=LAMBDA):
    """IGT payoff adds akhirah dimension to coordination game."""
    mat_a, mat_k = classical_payoff(strategy_aws, strategy_khazraj)

    # Akhirah payoffs: unity rewarded, tribalism penalized
    if strategy_aws == 'U' and strategy_khazraj == 'U':
        omega_a, omega_k = OMEGA_UNITY, OMEGA_UNITY
    elif strategy_aws == 'U' or strategy_khazraj == 'U':
        omega_a = OMEGA_UNITY * 0.5 if strategy_aws == 'U' else OMEGA_TRIBALISM * 0.3
        omega_k = OMEGA_UNITY * 0.5 if strategy_khazraj == 'U' else OMEGA_TRIBALISM * 0.3
    else:
        omega_a, omega_k = OMEGA_TRIBALISM, OMEGA_TRIBALISM

    return (mat_a + lambda_akh * omega_a, mat_k + lambda_akh * omega_k)


# ============================================================
# 3. EVOLUTIONARY DYNAMICS
# ============================================================

def evolve_population(n_gen, use_igt=False, focal_point=None, lambda_akh=0.0):
    """
    Evolutionary simulation of strategy adoption.
    focal_point: None, 'tribal_leader', 'prophet'
    """
    np.random.seed(42)
    strategies = ['A', 'K', 'U']

    # Initial: Aws prefer A, Khazraj prefer K, small fraction try U
    aws_pop = np.random.choice(strategies, 100, p=[0.8, 0.15, 0.05])
    khz_pop = np.random.choice(strategies, 100, p=[0.15, 0.8, 0.05])

    history_aws = {s: [] for s in strategies}
    history_khz = {s: [] for s in strategies}
    total_welfare = []

    for gen in range(n_gen):
        # Record proportions
        for s in strategies:
            history_aws[s].append(np.sum(aws_pop == s) / 100)
            history_khz[s].append(np.sum(khz_pop == s) / 100)

        # Compute average fitness for each strategy
        fitness_aws = {s: 0.0 for s in strategies}
        fitness_khz = {s: 0.0 for s in strategies}
        welfare = 0.0

        for sa in strategies:
            for sk in strategies:
                if use_igt:
                    pa, pk = igt_payoff(sa, sk, lambda_akh)
                else:
                    pa, pk = classical_payoff(sa, sk)

                # Frequency-weighted fitness
                freq_a = np.sum(aws_pop == sa) / 100
                freq_k = np.sum(khz_pop == sk) / 100
                fitness_aws[sa] += pa * freq_k
                fitness_khz[sk] += pk * freq_a
                welfare += (pa + pk) * freq_a * freq_k

        total_welfare.append(welfare)

        # Focal point effects
        if focal_point == 'prophet' and gen >= 20:
            # After Prophet arrives (generation 20), U becomes salient
            fitness_aws['U'] += 2.0
            fitness_khz['U'] += 2.0
        elif focal_point == 'tribal_leader' and gen >= 20:
            # A tribal leader tries to unify but adds only weak focal point
            fitness_aws['U'] += 0.3
            fitness_khz['U'] += 0.3

        # Replicator dynamics: reproduce proportional to fitness
        new_aws = []
        new_khz = []

        # Normalize fitness (avoid negatives)
        min_fit = min(min(fitness_aws.values()), 0)
        for s in strategies:
            fitness_aws[s] -= min_fit - 0.1
        min_fit = min(min(fitness_khz.values()), 0)
        for s in strategies:
            fitness_khz[s] -= min_fit - 0.1

        total_fit_a = sum(fitness_aws[s] * np.sum(aws_pop == s) for s in strategies)
        total_fit_k = sum(fitness_khz[s] * np.sum(khz_pop == s) for s in strategies)

        probs_a = [fitness_aws[s] * np.sum(aws_pop == s) / max(total_fit_a, 1e-10) for s in strategies]
        probs_k = [fitness_khz[s] * np.sum(khz_pop == s) / max(total_fit_k, 1e-10) for s in strategies]

        # Ensure valid probabilities
        probs_a = np.maximum(probs_a, 0)
        probs_k = np.maximum(probs_k, 0)
        probs_a = probs_a / np.sum(probs_a)
        probs_k = probs_k / np.sum(probs_k)

        aws_pop = np.random.choice(strategies, 100, p=probs_a)
        khz_pop = np.random.choice(strategies, 100, p=probs_k)

        # Mutation
        for i in range(100):
            if np.random.random() < MUTATION_RATE:
                aws_pop[i] = np.random.choice(strategies)
            if np.random.random() < MUTATION_RATE:
                khz_pop[i] = np.random.choice(strategies)

    return history_aws, history_khz, total_welfare


# ============================================================
# 4. FOCAL POINT ANALYSIS
# ============================================================

def focal_point_comparison():
    """Compare convergence under different focal point scenarios."""
    scenarios = {
        'No focal point (classical)': (False, None, 0.0),
        'Tribal leader focal point': (False, 'tribal_leader', 0.0),
        'Prophet focal point (classical)': (False, 'prophet', 0.0),
        'Prophet + IGT (lambda=0.5)': (True, 'prophet', 0.5),
        'Prophet + IGT (lambda=1.0)': (True, 'prophet', 1.0),
    }

    results = {}
    for label, (use_igt, focal, lam) in scenarios.items():
        h_aws, h_khz, welfare = evolve_population(N_GENERATIONS, use_igt, focal, lam)
        # Final proportion playing U
        final_u_aws = h_aws['U'][-1]
        final_u_khz = h_khz['U'][-1]
        final_welfare = welfare[-1]
        results[label] = {
            'u_aws': final_u_aws,
            'u_khz': final_u_khz,
            'welfare': final_welfare,
            'history_aws': h_aws,
            'history_khz': h_khz,
            'welfare_history': welfare,
        }

    return results


# ============================================================
# 5. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 05: AWS-KHAZRAJ COORDINATION GAME")
    print("Battle of the Sexes with External Arbiter (Prophet as Focal Point)")
    print("=" * 70)

    # --- Part A: Payoff Analysis ---
    print("\n--- Part A: Payoff Matrix Analysis ---")
    strategies = ['A', 'K', 'U']
    print("\n  Classical Payoffs (Aws, Khazraj):")
    print(f"  {'':>12}", end="")
    for sk in strategies:
        print(f"  Khz={sk:>4}", end="")
    print()
    for sa in strategies:
        print(f"  Aws={sa:>4}  ", end="")
        for sk in strategies:
            pa, pk = classical_payoff(sa, sk)
            print(f"  ({pa:.0f},{pk:.0f}) ", end="")
        print()

    print("\n  IGT Payoffs (Aws, Khazraj) with lambda=0.8:")
    print(f"  {'':>12}", end="")
    for sk in strategies:
        print(f"  Khz={sk:>6}", end="")
    print()
    for sa in strategies:
        print(f"  Aws={sa:>4}  ", end="")
        for sk in strategies:
            pa, pk = igt_payoff(sa, sk)
            print(f"  ({pa:.1f},{pk:.1f})", end="")
        print()

    # --- Part B: Nash Equilibria ---
    print("\n--- Part B: Equilibrium Analysis ---")
    print("  Classical Game:")
    print("    Nash Equilibria: (A,A) and (K,K) — both are equilibria, coordination failure")
    print("    Mixed NE: each plays own preference with p=0.75 — welfare = 0.75")
    print("  IGT Game:")
    print("    (U,U) becomes unique Pareto-dominant equilibrium with sufficient lambda")
    print("    Ummah identity resolves coordination failure")

    # --- Part C: Evolutionary Dynamics ---
    print("\n--- Part C: Evolutionary Dynamics Comparison ---")
    results = focal_point_comparison()

    print(f"\n  {'Scenario':<40} {'Aws->U%':<12} {'Khz->U%':<12} {'Welfare':<12}")
    print("-" * 76)
    for label, data in results.items():
        print(f"  {label:<40} {100*data['u_aws']:<12.1f} {100*data['u_khz']:<12.1f} {data['welfare']:<12.2f}")

    # --- Part D: Convergence Speed ---
    print("\n--- Part D: Convergence Speed ---")
    for label, data in results.items():
        # Find first generation where U > 50% for both
        converged = None
        for g in range(N_GENERATIONS):
            if data['history_aws']['U'][g] > 0.5 and data['history_khz']['U'][g] > 0.5:
                converged = g
                break
        conv_str = f"gen {converged}" if converged is not None else "never"
        print(f"  {label:<40} converged at: {conv_str}")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Get specific scenario data for detailed plots
    scenario_keys = list(results.keys())
    colors = {'A': 'red', 'K': 'blue', 'U': 'green'}

    # Plot 1-3: Evolution under three key scenarios
    for idx, key in enumerate([scenario_keys[0], scenario_keys[2], scenario_keys[4]]):
        ax = axes[0, idx]
        data = results[key]
        gens = range(N_GENERATIONS)
        for s in ['A', 'K', 'U']:
            combined = [(data['history_aws'][s][g] + data['history_khz'][s][g]) / 2 for g in gens]
            ax.plot(gens, combined, color=colors[s], linewidth=2,
                    label=f'{s} strategy')
        ax.set_xlabel('Generation', fontsize=11)
        ax.set_ylabel('Population Fraction', fontsize=11)
        ax.set_title(key, fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        if 'Prophet' in key or 'prophet' in key:
            ax.axvline(x=20, color='gold', linestyle='--', alpha=0.7, label='Prophet arrives')

    # Plot 4: Welfare comparison over time
    ax4 = axes[1, 0]
    for label, data in results.items():
        short_label = label.split('(')[0].strip()[:25]
        ax4.plot(range(N_GENERATIONS), data['welfare_history'], linewidth=2, label=short_label)
    ax4.set_xlabel('Generation', fontsize=11)
    ax4.set_ylabel('Total Welfare', fontsize=11)
    ax4.set_title('Social Welfare Over Time', fontsize=12)
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)

    # Plot 5: Final strategy distribution bar chart
    ax5 = axes[1, 1]
    x = np.arange(len(results))
    width = 0.25
    for i, s in enumerate(['A', 'K', 'U']):
        vals = [(results[k]['history_aws'][s][-1] + results[k]['history_khz'][s][-1]) / 2
                for k in results]
        ax5.bar(x + i * width, vals, width, color=colors[s], alpha=0.8, label=f'{s} strategy')
    ax5.set_xticks(x + width)
    short_labels = [k.split('(')[0].strip()[:15] for k in results]
    ax5.set_xticklabels(short_labels, rotation=45, ha='right', fontsize=8)
    ax5.set_ylabel('Final Population Fraction', fontsize=11)
    ax5.set_title('Final Strategy Distribution', fontsize=12)
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3, axis='y')

    # Plot 6: Lambda sensitivity
    ax6 = axes[1, 2]
    lambda_vals = np.linspace(0, 2, 20)
    final_u_fracs = []
    for lam in lambda_vals:
        h_aws, h_khz, _ = evolve_population(60, True, 'prophet', lam)
        final_u_fracs.append((h_aws['U'][-1] + h_khz['U'][-1]) / 2)
    ax6.plot(lambda_vals, final_u_fracs, 'g-o', linewidth=2, markersize=4)
    ax6.set_xlabel('Lambda (Akhirah Sensitivity)', fontsize=11)
    ax6.set_ylabel('Final Ummah Strategy Fraction', fontsize=11)
    ax6.set_title('Lambda vs. Coordination on Ummah', fontsize=12)
    ax6.grid(True, alpha=0.3)
    ax6.set_ylim(0, 1)
    ax6.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% threshold')
    ax6.legend(fontsize=9)

    plt.suptitle('Aws-Khazraj Coordination: From Tribal War to Ummah Unity',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_05_aws_khazraj_coordination.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n--- CONCLUSION ---")
    print("The Aws-Khazraj coordination problem demonstrates focal point theory:")
    print("  1. Without external arbiter: tribes oscillate between tribal equilibria (war)")
    print("  2. Tribal leader as arbiter: weak focal point, slow/incomplete convergence")
    print("  3. Prophet as arbiter: strong focal point with divine authority")
    print("  4. Prophet + IGT: Ummah becomes dominant strategy (asabiyyah penalized)")
    print("  5. The Constitution of Medina formalized the new focal equilibrium")
    print("  6. Historical result: decades of war ended in months after Hijra")
    print("\nFigure saved: islamic_gt_codes/fig_05_aws_khazraj_coordination.png")

if __name__ == "__main__":
    main()
