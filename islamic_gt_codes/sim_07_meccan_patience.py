"""
Simulation 07: 13 Years of Meccan Patience — Asymmetric Repeated Game

This simulation models the 13-year Meccan period (610-622 CE) as an asymmetric repeated game
where a weaker player (early Muslims) chooses between patience and retaliation under
persistent persecution.

Historical Context: For 13 years in Mecca, Muslims endured boycotts, torture, murder of
members (Sumayyah, Yasir), economic embargo, and social ostracism. Classical GT would
predict either capitulation or violent retaliation. Instead, the Prophet prescribed patience
(sabr), which: (1) built moral capital and credibility, (2) avoided escalation spirals that
would destroy the movement, (3) attracted converts through moral exemplarity, and
(4) preserved the community for the explosive growth post-Hijra.

Key Insight: In asymmetric repeated games, the weaker player's patience is not weakness but
optimal strategy when akhirah payoffs reward endurance and the long-run payoff from
movement survival exceeds short-run gains from retaliation.

Reference: prophet_hypothesis.md — Hypothesis H7
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Power asymmetry
QURAYSH_POWER = 10.0
MUSLIM_POWER_INITIAL = 1.0
MUSLIM_POWER_GROWTH = 0.08   # Natural growth per year from converts

# Strategies for weaker player
# Patience: absorb persecution, build moral capital
# Retaliation: fight back, risk escalation

# Payoffs per period
PERSECUTION_COST = -2.0       # Cost of being persecuted
PATIENCE_MORAL_CAPITAL = 1.5  # Moral capital gained per period of patience
RETALIATION_COST = -3.0       # Cost of retaliating (crackdown intensifies)
RETALIATION_DAMAGE = -1.0     # Damage inflicted on oppressor

# Escalation dynamics
ESCALATION_RATE = 1.5         # Oppressor escalates after retaliation
DE_ESCALATION_RATE = 0.9      # Oppressor slightly de-escalates after patience

# Movement survival threshold
SURVIVAL_THRESHOLD = 0.2      # Below this, movement is destroyed

# Akhirah parameters
OMEGA_PATIENCE = 8.0          # "Indeed the patient will be given their reward without measure" (39:10)
OMEGA_RETALIATE_WHEN_WEAK = 2.0  # Some reward for defending, but less than patience
OMEGA_DESTROYED = -5.0        # Movement destroyed = mission failed

# Post-migration explosion
MEDINA_GROWTH_MULTIPLIER = 5.0  # Growth rate explodes after successful migration

# ============================================================
# 2. REPEATED GAME ENGINE
# ============================================================

def simulate_13_years(strategy='patience', lambda_akh=0.0, n_years=25):
    """
    Simulate the Meccan period under different strategies.

    strategy: 'patience', 'retaliation', 'tit_for_tat', 'threshold'
    Returns trajectories of key variables.
    """
    np.random.seed(42)

    # State variables
    muslim_power = MUSLIM_POWER_INITIAL
    quraysh_aggression = 3.0    # Initial persecution level
    moral_capital = 0.0
    community_size = 40.0       # Initial believers
    cumulative_payoff = 0.0
    alive = True
    migrated = False

    # Trajectories
    traj = {
        'power': [], 'aggression': [], 'moral_capital': [],
        'community': [], 'payoff': [], 'alive': [],
        'igt_payoff': [],
    }

    for year in range(n_years):
        # Record state
        traj['power'].append(muslim_power)
        traj['aggression'].append(quraysh_aggression)
        traj['moral_capital'].append(moral_capital)
        traj['community'].append(community_size)
        traj['alive'].append(alive)

        if not alive:
            traj['payoff'].append(cumulative_payoff)
            traj['igt_payoff'].append(cumulative_payoff + lambda_akh * OMEGA_DESTROYED)
            continue

        # Determine action
        power_ratio = muslim_power / QURAYSH_POWER

        if strategy == 'patience':
            action = 'patient'
        elif strategy == 'retaliation':
            action = 'retaliate'
        elif strategy == 'tit_for_tat':
            action = 'retaliate' if quraysh_aggression > 5.0 else 'patient'
        elif strategy == 'threshold':
            # Retaliate only when strong enough
            action = 'retaliate' if power_ratio > 0.3 else 'patient'
        else:
            action = 'patient'

        # Compute period payoff
        if action == 'patient':
            period_payoff = PERSECUTION_COST * quraysh_aggression / 5.0
            moral_capital += PATIENCE_MORAL_CAPITAL
            akhirah_payoff = lambda_akh * OMEGA_PATIENCE

            # Quraysh de-escalate slightly (persecution fatigue)
            quraysh_aggression *= DE_ESCALATION_RATE
            # But add random spikes (e.g., boycott, torture events)
            if np.random.random() < 0.2:
                quraysh_aggression += np.random.exponential(1.0)

            # Community grows through moral example
            convert_rate = 0.05 + 0.02 * moral_capital / (1 + moral_capital)
            community_size *= (1 + convert_rate)

        else:  # retaliate
            period_payoff = RETALIATION_COST + RETALIATION_DAMAGE * power_ratio
            moral_capital *= 0.5  # Lose moral high ground
            akhirah_payoff = lambda_akh * OMEGA_RETALIATE_WHEN_WEAK

            # Quraysh ESCALATE severely
            quraysh_aggression *= ESCALATION_RATE
            # Community splits — some leave due to violence
            community_size *= 0.85

            # Risk of destruction
            if quraysh_aggression > 15.0 and power_ratio < 0.2:
                if np.random.random() < 0.4:
                    alive = False
                    period_payoff += lambda_akh * OMEGA_DESTROYED

        # Power grows with community
        muslim_power = MUSLIM_POWER_INITIAL + 0.1 * community_size

        # Migration opportunity at year 13 (if alive and moral capital sufficient)
        if year == 12 and alive and moral_capital > 5.0:
            migrated = True
            community_size *= 2.0  # Ansar join
            muslim_power *= 3.0
            moral_capital += 10.0  # Successful hijra adds credibility

        # Post-migration growth
        if migrated and year > 12:
            community_size *= (1 + 0.15)  # Much faster growth in Medina
            muslim_power *= 1.1

        cumulative_payoff += period_payoff
        traj['payoff'].append(cumulative_payoff)
        traj['igt_payoff'].append(cumulative_payoff + akhirah_payoff)

    return traj


# ============================================================
# 3. ESCALATION SPIRAL ANALYSIS
# ============================================================

def escalation_analysis(n_sims=500):
    """Monte Carlo: probability of movement destruction under each strategy."""
    np.random.seed(42)
    strategies = ['patience', 'retaliation', 'tit_for_tat', 'threshold']
    survival_rates = {}
    final_sizes = {}

    for strat in strategies:
        survived = 0
        sizes = []
        for sim in range(n_sims):
            np.random.seed(sim)
            traj = simulate_13_years(strat, lambda_akh=0.0, n_years=25)
            if traj['alive'][-1]:
                survived += 1
                sizes.append(traj['community'][-1])
            else:
                sizes.append(0)
        survival_rates[strat] = survived / n_sims
        final_sizes[strat] = sizes

    return survival_rates, final_sizes


# ============================================================
# 4. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 07: 13 YEARS OF MECCAN PATIENCE")
    print("Asymmetric Repeated Game — Patience vs. Retaliation")
    print("=" * 70)

    # --- Part A: Strategy Comparison ---
    print("\n--- Part A: Strategy Trajectories (Single Run) ---")
    strategies = ['patience', 'retaliation', 'tit_for_tat', 'threshold']
    trajectories = {}

    for strat in strategies:
        traj = simulate_13_years(strat, lambda_akh=0.8, n_years=25)
        trajectories[strat] = traj

    print(f"\n  {'Strategy':<20} {'Survived?':<12} {'Final Size':<15} {'Moral Capital':<15} {'Cum. Payoff':<15}")
    print("-" * 77)
    for strat in strategies:
        t = trajectories[strat]
        survived = "YES" if t['alive'][-1] else "NO"
        final_size = t['community'][-1] if t['alive'][-1] else 0
        moral_cap = t['moral_capital'][-1]
        payoff = t['payoff'][-1]
        print(f"  {strat:<20} {survived:<12} {final_size:<15.0f} {moral_cap:<15.1f} {payoff:<15.2f}")

    # --- Part B: Monte Carlo Survival Analysis ---
    print("\n--- Part B: Monte Carlo Survival Analysis (n=500) ---")
    survival_rates, final_sizes = escalation_analysis(500)

    print(f"\n  {'Strategy':<20} {'Survival Rate':<18} {'Mean Final Size':<18} {'Median Final Size':<18}")
    print("-" * 74)
    for strat in strategies:
        mean_size = np.mean(final_sizes[strat])
        median_size = np.median(final_sizes[strat])
        print(f"  {strat:<20} {100*survival_rates[strat]:<18.1f} {mean_size:<18.0f} {median_size:<18.0f}")

    print("\n  Historical outcome: Prophet chose patience -> community survived 13 years")
    print("  -> successful Hijra -> explosive growth -> 10,000+ at Conquest of Mecca")

    # --- Part C: Moral Capital as Strategic Asset ---
    print("\n--- Part C: Moral Capital Accumulation ---")
    patience_traj = trajectories['patience']
    for year in [0, 3, 6, 9, 12, 15, 20, 24]:
        if year < len(patience_traj['moral_capital']):
            mc = patience_traj['moral_capital'][year]
            cs = patience_traj['community'][year]
            period = "Mecca" if year < 13 else "Medina"
            print(f"  Year {year:>2} ({period:>6}): Moral capital = {mc:>6.1f}, Community size = {cs:>8.0f}")

    # --- Part D: IGT vs Classical Payoff ---
    print("\n--- Part D: Cumulative Payoff (Classical vs IGT) ---")
    for lam in [0.0, 0.3, 0.5, 0.8, 1.0]:
        pat_traj = simulate_13_years('patience', lambda_akh=lam, n_years=25)
        ret_traj = simulate_13_years('retaliation', lambda_akh=lam, n_years=25)
        pat_final = pat_traj['igt_payoff'][-1] if pat_traj['alive'][-1] else pat_traj['igt_payoff'][-1]
        ret_final = ret_traj['igt_payoff'][-1] if ret_traj['alive'][-1] else ret_traj['igt_payoff'][-1]
        better = "PATIENCE" if pat_final > ret_final else "RETALIATE"
        print(f"  lambda={lam:.1f}: Patience={pat_final:>8.1f}, Retaliate={ret_final:>8.1f} -> {better}")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    colors = {'patience': 'green', 'retaliation': 'red', 'tit_for_tat': 'orange', 'threshold': 'blue'}
    years = range(25)

    # Plot 1: Community size trajectories
    ax1 = axes[0, 0]
    for strat in strategies:
        t = trajectories[strat]
        ax1.plot(years, t['community'], color=colors[strat], linewidth=2, label=strat.replace('_', ' ').title())
    ax1.axvline(x=13, color='gold', linestyle='--', alpha=0.7, linewidth=2, label='Hijra (year 13)')
    ax1.set_xlabel('Year', fontsize=11)
    ax1.set_ylabel('Community Size', fontsize=11)
    ax1.set_title('Community Growth by Strategy', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Plot 2: Quraysh aggression level
    ax2 = axes[0, 1]
    for strat in strategies:
        t = trajectories[strat]
        ax2.plot(years, t['aggression'], color=colors[strat], linewidth=2, label=strat.replace('_', ' ').title())
    ax2.set_xlabel('Year', fontsize=11)
    ax2.set_ylabel('Quraysh Aggression Level', fontsize=11)
    ax2.set_title('Escalation Dynamics', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Plot 3: Moral capital
    ax3 = axes[0, 2]
    for strat in strategies:
        t = trajectories[strat]
        ax3.plot(years, t['moral_capital'], color=colors[strat], linewidth=2, label=strat.replace('_', ' ').title())
    ax3.set_xlabel('Year', fontsize=11)
    ax3.set_ylabel('Moral Capital', fontsize=11)
    ax3.set_title('Moral Capital Accumulation', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    # Plot 4: Cumulative payoff
    ax4 = axes[1, 0]
    for strat in strategies:
        t = trajectories[strat]
        ax4.plot(years, t['payoff'], color=colors[strat], linewidth=2, label=strat.replace('_', ' ').title())
    ax4.set_xlabel('Year', fontsize=11)
    ax4.set_ylabel('Cumulative Material Payoff', fontsize=11)
    ax4.set_title('Cumulative Payoff Over Time', fontsize=12)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='black', linewidth=0.5)

    # Plot 5: Survival probability (bar chart)
    ax5 = axes[1, 1]
    strat_labels = [s.replace('_', ' ').title() for s in strategies]
    surv_vals = [survival_rates[s] * 100 for s in strategies]
    bars = ax5.bar(strat_labels, surv_vals, color=[colors[s] for s in strategies], alpha=0.8)
    ax5.set_ylabel('Survival Rate (%)', fontsize=11)
    ax5.set_title('Movement Survival by Strategy\n(500 Monte Carlo simulations)', fontsize=12)
    ax5.grid(True, alpha=0.3, axis='y')
    for bar, val in zip(bars, surv_vals):
        ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.0f}%', ha='center', va='bottom', fontweight='bold')

    # Plot 6: Final community size distributions
    ax6 = axes[1, 2]
    for strat in strategies:
        sizes = [s for s in final_sizes[strat] if s > 0]
        if sizes:
            ax6.hist(sizes, bins=30, alpha=0.4, color=colors[strat],
                    label=strat.replace('_', ' ').title(), density=True)
    ax6.set_xlabel('Final Community Size', fontsize=11)
    ax6.set_ylabel('Density', fontsize=11)
    ax6.set_title('Distribution of Final Community Size\n(Conditional on Survival)', fontsize=12)
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)

    plt.suptitle('13 Years of Meccan Patience: Asymmetric Repeated Game',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_07_meccan_patience.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n--- CONCLUSION ---")
    print("The 13-year Meccan period demonstrates optimal strategy for the weaker player:")
    print("  1. Patience dominates retaliation in long-run survival probability")
    print("  2. Retaliation triggers escalation spirals that destroy the movement")
    print("  3. Moral capital from patience attracts converts and builds credibility")
    print("  4. IGT (akhirah payoffs) makes patience rational even under severe persecution")
    print("  5. Patience preserved the movement for post-Hijra explosive growth")
    print("  6. Historical: 13 years of patience -> 40 believers to 10,000+ in 23 years")
    print("\nFigure saved: islamic_gt_codes/fig_07_meccan_patience.png")

if __name__ == "__main__":
    main()
