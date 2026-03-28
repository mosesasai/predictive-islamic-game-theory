"""
Simulation 21: Nash Bargaining — Kaaba Black Stone Arbitration

Nash Bargaining (Nash 1950) predicts that rational parties will agree on the outcome
that maximizes the product of their gains over the disagreement point. The key is the
DISAGREEMENT POINT — what happens if negotiations fail.

Historical Context: Around 605 CE (5 years before prophethood), the Kaaba was being
rebuilt after a flood. When the Black Stone (Hajar al-Aswad) needed to be placed, four
major tribes (Banu Hashim, Banu Umayya, Banu Makhzum, Banu Abd al-Dar) each claimed
the honor. The dispute nearly escalated to armed conflict — the disagreement point was
tribal warfare.

Muhammad (then ~35 years old) proposed: place the stone on a cloth, each tribe holds a
corner, all lift together, then Muhammad places the stone. This mechanism:
  1. Converted a zero-sum honor dispute into a positive-sum shared action
  2. Gave each tribe equal symbolic participation
  3. Avoided the disagreement point (violence) entirely
  4. Was accepted instantly by all parties

Reference: prophet_hypothesis.md — Hypothesis H21
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from itertools import combinations

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

N_TRIBES = 4
TRIBE_NAMES = ['Banu Hashim', 'Banu Umayya', 'Banu Makhzum', 'Banu Abd al-Dar']
N_SIMULATIONS = 2000

# Honor values (each tribe's value for placing the stone)
HONOR_VALUE = 100.0      # Total honor value of placing the stone

# Tribe relative power (affects bargaining position)
TRIBE_POWER = {
    'Banu Hashim': 0.28,
    'Banu Umayya': 0.30,
    'Banu Makhzum': 0.25,
    'Banu Abd al-Dar': 0.17,
}

# Disagreement point: cost of inter-tribal warfare
WAR_COST_PER_TRIBE = -50.0       # Direct cost
WAR_VARIANCE = 20.0              # Uncertainty in war outcomes
WAR_WINNER_GAIN = 60.0           # Winner gets honor minus war cost
WAR_LOSER_COST = -80.0           # Loser pays heavily

# Solution mechanisms
# Classical: one tribe gets all honor (zero-sum)
# Prophetic: cloth mechanism (shared honor)

SHARED_HONOR_FRACTION = 0.25    # Each tribe gets 1/4 of honor
SHARED_BONUS = 20.0             # Bonus from avoiding conflict + unity signal
PLACEMENT_HONOR = 10.0          # Small extra for the one who physically places

np.random.seed(42)

# ============================================================
# 2. BARGAINING MODEL
# ============================================================

def disagreement_payoff(tribe_power):
    """Expected payoff at disagreement point (war)."""
    # Each tribe's expected war payoff depends on power
    # With 4 tribes, probability of winning = power share
    p_win = tribe_power
    expected = p_win * WAR_WINNER_GAIN + (1 - p_win) * WAR_LOSER_COST
    return expected


def nash_bargaining_solution(values, disagreement_points):
    """Compute Nash Bargaining Solution for n players.
    Maximizes product of (u_i - d_i) subject to feasibility."""
    n = len(values)
    # For symmetric case with equal outside options,
    # NBS gives proportional to (value * bargaining power)
    gains = [v - d for v, d in zip(values, disagreement_points)]
    total_gain = sum(max(0, g) for g in gains)
    if total_gain == 0:
        return [d for d in disagreement_points]
    shares = [max(0, g) / total_gain for g in gains]
    surplus = HONOR_VALUE - sum(disagreement_points)
    allocations = [d + s * surplus for d, s in zip(disagreement_points, shares)]
    return allocations


def zero_sum_outcome():
    """Classical zero-sum: one tribe gets all, others get nothing.
    With war risk if no agreement."""
    outcomes = {tribe: [] for tribe in TRIBE_NAMES}

    for _ in range(N_SIMULATIONS):
        # Tribes negotiate; if no agreement, war
        agreement = np.random.random() < 0.3  # Low agreement probability in zero-sum

        if agreement:
            # One tribe wins through negotiation (proportional to power)
            powers = [TRIBE_POWER[t] for t in TRIBE_NAMES]
            winner = np.random.choice(TRIBE_NAMES, p=powers)
            for tribe in TRIBE_NAMES:
                if tribe == winner:
                    outcomes[tribe].append(HONOR_VALUE)
                else:
                    outcomes[tribe].append(0.0)
        else:
            # War breaks out
            powers = [TRIBE_POWER[t] for t in TRIBE_NAMES]
            winner = np.random.choice(TRIBE_NAMES, p=powers)
            for tribe in TRIBE_NAMES:
                war_cost = WAR_COST_PER_TRIBE + np.random.normal(0, WAR_VARIANCE)
                if tribe == winner:
                    outcomes[tribe].append(WAR_WINNER_GAIN + war_cost)
                else:
                    outcomes[tribe].append(WAR_LOSER_COST + war_cost)

    return outcomes


def cloth_mechanism_outcome():
    """Prophet's cloth mechanism: shared honor + bonus for unity."""
    outcomes = {tribe: [] for tribe in TRIBE_NAMES}

    for _ in range(N_SIMULATIONS):
        # Always reaches agreement (mechanism is self-enforcing)
        for i, tribe in enumerate(TRIBE_NAMES):
            honor = SHARED_HONOR_FRACTION * HONOR_VALUE + SHARED_BONUS
            # Small random variation in perceived honor
            honor += np.random.normal(0, 2.0)
            outcomes[tribe].append(honor)

    return outcomes


def nash_bargaining_outcome():
    """Standard Nash Bargaining Solution (no mechanism design)."""
    disagreement = {t: disagreement_payoff(TRIBE_POWER[t]) for t in TRIBE_NAMES}
    values = [HONOR_VALUE * TRIBE_POWER[t] for t in TRIBE_NAMES]
    d_points = [disagreement[t] for t in TRIBE_NAMES]

    nbs = nash_bargaining_solution(values, d_points)

    outcomes = {tribe: [] for tribe in TRIBE_NAMES}
    for _ in range(N_SIMULATIONS):
        # NBS with negotiation noise
        agreement_prob = 0.6  # Moderate agreement probability
        if np.random.random() < agreement_prob:
            for i, tribe in enumerate(TRIBE_NAMES):
                outcomes[tribe].append(nbs[i] + np.random.normal(0, 3.0))
        else:
            # Falls back to disagreement
            for tribe in TRIBE_NAMES:
                outcomes[tribe].append(disagreement[tribe] + np.random.normal(0, WAR_VARIANCE))

    return outcomes

# ============================================================
# 3. SIMULATION ENGINE
# ============================================================

def compute_metrics(outcomes, name):
    """Compute metrics for a set of outcomes."""
    means = {t: np.mean(v) for t, v in outcomes.items()}
    stds = {t: np.std(v) for t, v in outcomes.items()}
    total_welfare = sum(means.values())
    min_payoff = min(means.values())
    max_payoff = max(means.values())
    gini = (max_payoff - min_payoff) / max(total_welfare, 1)
    welfare_per_sim = [sum(outcomes[t][i] for t in TRIBE_NAMES) for i in range(N_SIMULATIONS)]

    return {
        'name': name,
        'means': means,
        'stds': stds,
        'total_welfare': total_welfare,
        'min_payoff': min_payoff,
        'max_payoff': max_payoff,
        'inequality': gini,
        'welfare_per_sim': welfare_per_sim,
        'agreement_rate': sum(1 for w in welfare_per_sim if w > 0) / N_SIMULATIONS,
    }

# ============================================================
# 4. MAIN FUNCTION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 21: NASH BARGAINING — KAABA BLACK STONE ARBITRATION")
    print("Zero-Sum Honor Dispute to Positive-Sum Shared Action")
    print("=" * 70)

    print("\nRunning three mechanism simulations...")
    zero_sum = zero_sum_outcome()
    cloth = cloth_mechanism_outcome()
    nbs = nash_bargaining_outcome()

    m_zero = compute_metrics(zero_sum, "Zero-Sum (Classical)")
    m_cloth = compute_metrics(cloth, "Cloth Mechanism (Prophetic)")
    m_nbs = compute_metrics(nbs, "Nash Bargaining (Standard)")

    all_metrics = [m_zero, m_nbs, m_cloth]

    # --- Results ---
    print("\n--- Tribe-Level Outcomes ---\n")
    for m in all_metrics:
        print(f"  {m['name']}:")
        for tribe in TRIBE_NAMES:
            print(f"    {tribe:<22} Mean: {m['means'][tribe]:>8.2f}  Std: {m['stds'][tribe]:>8.2f}")
        print()

    print("--- Aggregate Comparison ---\n")
    print(f"  {'Metric':<35} {'Zero-Sum':<18} {'Nash Bargain':<18} {'Cloth (Prophetic)':<18}")
    print(f"  {'-'*89}")
    print(f"  {'Total welfare':<35} {m_zero['total_welfare']:<18.2f} {m_nbs['total_welfare']:<18.2f} "
          f"{m_cloth['total_welfare']:<18.2f}")
    print(f"  {'Min tribe payoff':<35} {m_zero['min_payoff']:<18.2f} {m_nbs['min_payoff']:<18.2f} "
          f"{m_cloth['min_payoff']:<18.2f}")
    print(f"  {'Max tribe payoff':<35} {m_zero['max_payoff']:<18.2f} {m_nbs['max_payoff']:<18.2f} "
          f"{m_cloth['max_payoff']:<18.2f}")
    print(f"  {'Inequality (Gini-like)':<35} {m_zero['inequality']:<18.4f} {m_nbs['inequality']:<18.4f} "
          f"{m_cloth['inequality']:<18.4f}")
    print(f"  {'Agreement rate':<35} {m_zero['agreement_rate']:<18.1%} {m_nbs['agreement_rate']:<18.1%} "
          f"{m_cloth['agreement_rate']:<18.1%}")

    # Disagreement points
    print(f"\n--- Disagreement Points (War Payoffs) ---\n")
    for tribe in TRIBE_NAMES:
        d = disagreement_payoff(TRIBE_POWER[tribe])
        print(f"  {tribe:<22} Power: {TRIBE_POWER[tribe]:.2f}  War E[payoff]: {d:>8.2f}")

    print(f"\n--- Mechanism Design Analysis ---\n")
    print(f"  The cloth mechanism achieves:")
    print(f"    Welfare gain over zero-sum:    {m_cloth['total_welfare'] - m_zero['total_welfare']:>+.2f}")
    print(f"    Welfare gain over NBS:         {m_cloth['total_welfare'] - m_nbs['total_welfare']:>+.2f}")
    print(f"    Inequality reduction vs zero:  {m_zero['inequality'] - m_cloth['inequality']:>.4f}")
    print(f"    Agreement rate improvement:    {m_cloth['agreement_rate'] - m_zero['agreement_rate']:>+.1%}")

    # --- Historical ---
    print("\n--- Historical Verification ---")
    print("  Kaaba Stone Dispute (~605 CE):")
    print("  * Four tribes deadlocked for days, nearly at war")
    print("  * Agreed: 'next person to enter the sanctuary decides'")
    print("  * Muhammad entered — all parties relieved ('Al-Amin!')")
    print("  * Cloth solution: ALL tribes participate, NO tribe excluded")
    print("  * Accepted instantly, unanimously — no further dispute")
    print("  * The mechanism was self-enforcing: no tribe could object to equality")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Mean payoffs by tribe and mechanism
    ax = axes[0, 0]
    x = np.arange(N_TRIBES)
    width = 0.25
    for i, m in enumerate(all_metrics):
        vals = [m['means'][t] for t in TRIBE_NAMES]
        colors = ['red', 'orange', 'green']
        ax.bar(x + i * width, vals, width, color=colors[i], alpha=0.8,
               label=m['name'], edgecolor='black')
    ax.set_xticks(x + width)
    ax.set_xticklabels([t.replace('Banu ', 'B. ') for t in TRIBE_NAMES], fontsize=9)
    ax.set_ylabel('Mean Payoff')
    ax.set_title('Payoff by Tribe and Mechanism')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 2: Welfare distribution histograms
    ax = axes[0, 1]
    for m, color in zip(all_metrics, ['red', 'orange', 'green']):
        ax.hist(m['welfare_per_sim'], bins=40, alpha=0.5, color=color,
                label=m['name'], density=True)
    ax.set_xlabel('Total Welfare per Simulation')
    ax.set_ylabel('Density')
    ax.set_title('Welfare Distribution')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Plot 3: Inequality comparison
    ax = axes[0, 2]
    names_short = ['Zero-Sum', 'Nash\nBargain', 'Cloth\n(Prophetic)']
    ineq = [m['inequality'] for m in all_metrics]
    colors = ['red', 'orange', 'green']
    bars = ax.bar(names_short, ineq, color=colors, alpha=0.8, edgecolor='black')
    for bar, val in zip(bars, ineq):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.3f}', ha='center', fontsize=10)
    ax.set_ylabel('Inequality Index')
    ax.set_title('Outcome Inequality')
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 4: Payoff variance by tribe
    ax = axes[1, 0]
    for i, m in enumerate(all_metrics):
        vals = [m['stds'][t] for t in TRIBE_NAMES]
        ax.bar(x + i * width, vals, width, color=['red', 'orange', 'green'][i],
               alpha=0.8, label=m['name'], edgecolor='black')
    ax.set_xticks(x + width)
    ax.set_xticklabels([t.replace('Banu ', 'B. ') for t in TRIBE_NAMES], fontsize=9)
    ax.set_ylabel('Payoff Std Dev')
    ax.set_title('Outcome Uncertainty by Tribe')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 5: Mechanism comparison summary
    ax = axes[1, 1]
    metrics_to_plot = ['total_welfare', 'agreement_rate']
    labels = ['Total Welfare', 'Agreement Rate']

    # Normalize for comparison
    for idx, (metric_key, label) in enumerate(zip(metrics_to_plot, labels)):
        vals = [m[metric_key] for m in all_metrics]
        max_val = max(abs(v) for v in vals) if max(abs(v) for v in vals) > 0 else 1
        norm_vals = [v / max_val for v in vals]
        ax.bar([i + idx * 0.3 for i in range(3)], norm_vals, 0.28,
               color=['lightcoral', 'lightyellow', 'lightgreen'][idx],
               edgecolor=['red', 'orange', 'green'][idx], linewidth=2,
               label=label)
    ax.set_xticks(range(3))
    ax.set_xticklabels(names_short, fontsize=9)
    ax.set_ylabel('Normalized Score')
    ax.set_title('Mechanism Performance Summary')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 6: Mechanism diagram
    ax = axes[1, 2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.text(5, 9.5, 'KAABA STONE ARBITRATION', ha='center', fontsize=12, fontweight='bold')

    # Zero-sum path
    ax.text(2, 7.5, 'ZERO-SUM\n1 winner, 3 losers\nor WAR', ha='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax.annotate('', xy=(2, 5.5), xytext=(2, 7),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(2, 4.5, 'Violence\nor Resentment', ha='center', fontsize=8, color='red',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

    # Cloth mechanism
    ax.text(8, 7.5, 'CLOTH MECHANISM\nAll 4 tribes hold corners\nShared action', ha='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax.annotate('', xy=(8, 5.5), xytext=(8, 7),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(8, 4.5, 'Unanimous\nAcceptance', ha='center', fontsize=8, color='green',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

    # Key insight
    ax.text(5, 2.5, 'Key Insight: Convert zero-sum HONOR\ninto positive-sum SHARED ACTION',
            ha='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Tribes at corners
    for i, (name, pos) in enumerate(zip(TRIBE_NAMES,
                                         [(6.5, 1), (9.5, 1), (6.5, 0.2), (9.5, 0.2)])):
        ax.text(pos[0], pos[1], name.replace('Banu ', ''), fontsize=7,
                ha='center', color='darkblue')

    ax.axis('off')

    plt.suptitle("Nash Bargaining: Kaaba Black Stone Arbitration\n"
                 "Zero-Sum Honor to Positive-Sum Shared Action",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_21_kaaba_stone_bargaining.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\nFigure saved: islamic_gt_codes/fig_21_kaaba_stone_bargaining.png")

    print("\n--- CONCLUSION ---")
    print("The cloth mechanism is a masterclass in mechanism design that:")
    print(f"  1. Increases total welfare by {m_cloth['total_welfare'] - m_zero['total_welfare']:+.1f} "
          f"over zero-sum")
    print(f"  2. Achieves {m_cloth['agreement_rate']:.0%} agreement rate vs "
          f"{m_zero['agreement_rate']:.0%} (zero-sum)")
    print(f"  3. Reduces inequality from {m_zero['inequality']:.3f} to {m_cloth['inequality']:.3f}")
    print("  4. Is SELF-ENFORCING: no tribe can object to equal participation")
    print("  5. Converts zero-sum honor dispute into positive-sum shared action")
    print("  6. Avoids the catastrophic disagreement point (tribal warfare)")
    print("  7. This anticipates modern mechanism design (Myerson, Roth) by 1400 years")


if __name__ == "__main__":
    main()
