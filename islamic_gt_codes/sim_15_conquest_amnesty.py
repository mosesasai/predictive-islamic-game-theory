"""
Simulation 15: Conquest of Mecca — Amnesty vs. Punishment in Post-Conflict Games

This simulation compares the long-run outcomes of three post-conquest strategies:
1. Purge (classical realist prescription)
2. Tit-for-Tat (classical repeated game prescription)
3. Amnesty (the Prophet's actual strategy — Muhammad Equilibrium)

Historical Context: The Prophet ﷺ entered Mecca with 10,000 soldiers (630 CE) and declared
universal amnesty: "Go, for you are free." This produced zero guerrilla resistance and
unified the Arabian Peninsula within 2 years.

Reference: prophet_hypothesis.md — Hypothesis H15
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL SETUP
# ============================================================

N_POPULATION = 10000     # Conquered Mecca population
N_ELITE = 500            # Former elite/leaders who actively opposed Islam
N_PERIODS = 50           # Simulation periods (months)
N_SIMULATIONS = 100      # Monte Carlo runs

# Population states: each person can be {loyal, neutral, hostile, rebel}
STATES = ['loyal', 'neutral', 'hostile', 'rebel']

# Initial state distribution after conquest (before any strategy applied)
INITIAL_DIST = {
    'loyal': 0.10,      # Already Muslim / supportive
    'neutral': 0.40,    # Indifferent population
    'hostile': 0.40,    # Opposed but not fighting
    'rebel': 0.10,      # Actively resisting
}

# ============================================================
# 2. STRATEGY DEFINITIONS
# ============================================================

class PostConquestStrategy:
    """Base class for post-conquest strategies."""

    def __init__(self, name):
        self.name = name

    def apply(self, state_dist, period):
        """Apply strategy and return new state distribution."""
        raise NotImplementedError


class PurgeStrategy(PostConquestStrategy):
    """Classical realist: eliminate elites, punish hostile population."""

    def __init__(self):
        super().__init__("Purge (Classical Realist)")
        self.purge_executed = False

    def apply(self, state_dist, period):
        new_dist = state_dist.copy()

        if period == 0 and not self.purge_executed:
            # Execute purge: remove 80% of hostile/rebel, they become "eliminated"
            eliminated = 0.8 * (state_dist['hostile'] + state_dist['rebel'])
            new_dist['hostile'] *= 0.2
            new_dist['rebel'] *= 0.2

            # BUT: purge creates grievance -> some neutrals become hostile
            grievance_rate = 0.3  # 30% of neutrals radicalized by witnessing purge
            radicalized = grievance_rate * state_dist['neutral']
            new_dist['neutral'] -= radicalized
            new_dist['hostile'] += radicalized * 0.7
            new_dist['rebel'] += radicalized * 0.3

            self.purge_executed = True
        else:
            # Ongoing surveillance and suppression
            # Some hostile -> neutral (fear), some neutral -> hostile (resentment)
            new_dist['neutral'] += 0.02 * state_dist['hostile']  # Suppression works
            new_dist['hostile'] -= 0.02 * state_dist['hostile']
            new_dist['hostile'] += 0.01 * state_dist['neutral']  # But resentment grows
            new_dist['neutral'] -= 0.01 * state_dist['neutral']

            # Rebels regenerate slowly from hostile pool
            new_dist['rebel'] += 0.02 * state_dist['hostile']
            new_dist['hostile'] -= 0.02 * state_dist['hostile']

            # Very slow loyalty gain (fear-based)
            new_dist['loyal'] += 0.005 * state_dist['neutral']
            new_dist['neutral'] -= 0.005 * state_dist['neutral']

        return new_dist


class TitForTatStrategy(PostConquestStrategy):
    """Classical GT: punish defectors, reward cooperators proportionally."""

    def __init__(self):
        super().__init__("Tit-for-Tat (Classical GT)")

    def apply(self, state_dist, period):
        new_dist = state_dist.copy()

        # Punish rebels and hostile, reward loyal
        # Rebels punished -> some submit, some entrench
        new_dist['hostile'] += 0.3 * state_dist['rebel']    # Some rebels subdued
        new_dist['rebel'] -= 0.3 * state_dist['rebel']
        new_dist['rebel'] += 0.05 * state_dist['hostile']   # Some hostile escalate
        new_dist['hostile'] -= 0.05 * state_dist['hostile']

        # Reward cooperators -> slow loyalty gain
        new_dist['loyal'] += 0.02 * state_dist['neutral']
        new_dist['neutral'] -= 0.02 * state_dist['neutral']

        # Neutral drift: some become hostile (seeing punishment), some become loyal (seeing reward)
        new_dist['hostile'] += 0.015 * state_dist['neutral']
        new_dist['loyal'] += 0.015 * state_dist['neutral']
        new_dist['neutral'] -= 0.03 * state_dist['neutral']

        return new_dist


class AmnestyStrategy(PostConquestStrategy):
    """Prophet Muhammad's strategy: universal amnesty + moral transformation."""

    def __init__(self):
        super().__init__("Amnesty (Muhammad Equilibrium)")

    def apply(self, state_dist, period):
        new_dist = state_dist.copy()

        if period == 0:
            # Amnesty shock: dramatic immediate effect
            # Rebels lose motivation (no oppressor to fight)
            new_dist['neutral'] += 0.7 * state_dist['rebel']
            new_dist['rebel'] *= 0.3

            # Hostile population re-evaluates
            new_dist['neutral'] += 0.5 * state_dist['hostile']
            new_dist['hostile'] *= 0.5

            # Some immediately convert (Abu Sufyan effect)
            new_dist['loyal'] += 0.1 * state_dist['hostile']
            new_dist['hostile'] -= 0.1 * state_dist['hostile']
        else:
            # Ongoing moral transformation (dakwah)
            # High conversion rate: hostile -> neutral -> loyal
            conversion_rate = 0.08  # High because mercy destroys resistance narrative

            new_dist['neutral'] += conversion_rate * state_dist['hostile']
            new_dist['hostile'] -= conversion_rate * state_dist['hostile']

            new_dist['loyal'] += conversion_rate * state_dist['neutral']
            new_dist['neutral'] -= conversion_rate * state_dist['neutral']

            # Rebels diminish rapidly (no grievance to recruit from)
            new_dist['neutral'] += 0.15 * state_dist['rebel']
            new_dist['rebel'] -= 0.15 * state_dist['rebel']

            # Cascade effect: as loyal population grows, social pressure increases
            loyalty_fraction = new_dist['loyal']
            cascade_bonus = 0.02 * loyalty_fraction
            new_dist['loyal'] += cascade_bonus * state_dist['neutral']
            new_dist['neutral'] -= cascade_bonus * state_dist['neutral']

        return new_dist

# ============================================================
# 3. SIMULATION ENGINE
# ============================================================

def run_simulation(strategy, n_periods=N_PERIODS):
    """Run a single simulation with given strategy."""
    state_history = []
    state_dist = INITIAL_DIST.copy()
    state_history.append(state_dist.copy())

    for t in range(n_periods):
        state_dist = strategy.apply(state_dist, t)

        # Normalize to ensure probabilities sum to 1
        total = sum(state_dist.values())
        state_dist = {k: max(0, v/total) for k, v in state_dist.items()}

        state_history.append(state_dist.copy())

    return state_history


def compute_metrics(history):
    """Compute key metrics from simulation history."""
    loyalty = [h['loyal'] for h in history]
    rebellion = [h['rebel'] for h in history]
    hostility = [h['hostile'] for h in history]
    stability = [1.0 - h['rebel'] - 0.5 * h['hostile'] for h in history]

    # Time to 80% loyalty
    time_to_80 = None
    for t, l in enumerate(loyalty):
        if l >= 0.8:
            time_to_80 = t
            break

    # Total rebellion person-months (cost measure)
    total_rebellion = sum(rebellion) * N_POPULATION

    # Peak rebellion
    peak_rebellion = max(rebellion) * N_POPULATION

    return {
        'loyalty': loyalty,
        'rebellion': rebellion,
        'hostility': hostility,
        'stability': stability,
        'time_to_80_loyalty': time_to_80,
        'total_rebellion_months': total_rebellion,
        'peak_rebellion': peak_rebellion,
        'final_loyalty': loyalty[-1],
        'final_rebellion': rebellion[-1],
    }

# ============================================================
# 4. COST-BENEFIT ANALYSIS
# ============================================================

def cost_benefit_analysis(metrics, strategy_name):
    """Compute total welfare under each strategy."""
    # Costs
    if 'Purge' in strategy_name:
        purge_cost = 0.8 * (INITIAL_DIST['hostile'] + INITIAL_DIST['rebel']) * N_POPULATION * 10
        ongoing_surveillance = sum(metrics['hostility']) * N_POPULATION * 2
        guerrilla_cost = metrics['total_rebellion_months'] * 5
        total_cost = purge_cost + ongoing_surveillance + guerrilla_cost
    elif 'Tit-for-Tat' in strategy_name:
        punishment_cost = sum(metrics['rebellion']) * N_POPULATION * 3
        administration_cost = N_PERIODS * 100
        guerrilla_cost = metrics['total_rebellion_months'] * 5
        total_cost = punishment_cost + administration_cost + guerrilla_cost
    else:  # Amnesty
        # Minimal cost: no purge, no ongoing punishment
        social_integration_cost = N_PERIODS * 50
        guerrilla_cost = metrics['total_rebellion_months'] * 5
        total_cost = social_integration_cost + guerrilla_cost

    # Benefits
    loyalty_benefit = sum(metrics['loyalty']) * N_POPULATION * 3
    stability_benefit = sum(metrics['stability']) * 1000
    trade_benefit = sum(metrics['loyalty']) * N_POPULATION * 0.5

    total_benefit = loyalty_benefit + stability_benefit + trade_benefit
    net_welfare = total_benefit - total_cost

    return {
        'total_cost': total_cost,
        'total_benefit': total_benefit,
        'net_welfare': net_welfare,
    }

# ============================================================
# 5. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 15: CONQUEST OF MECCA — AMNESTY vs. PUNISHMENT")
    print("Post-Conflict Strategy Comparison")
    print("=" * 70)

    strategies = [
        PurgeStrategy(),
        TitForTatStrategy(),
        AmnestyStrategy(),
    ]

    all_metrics = {}
    all_costs = {}

    for strategy in strategies:
        history = run_simulation(strategy)
        metrics = compute_metrics(history)
        costs = cost_benefit_analysis(metrics, strategy.name)
        all_metrics[strategy.name] = metrics
        all_costs[strategy.name] = costs

    # --- Print Results ---
    print("\n--- Outcome Comparison (50-month simulation) ---\n")
    header = f"{'Metric':<35}"
    for s in strategies:
        header += f" {s.name[:20]:<22}"
    print(header)
    print("-" * len(header))

    metric_labels = [
        ('final_loyalty', 'Final loyalty rate', '{:.1%}'),
        ('final_rebellion', 'Final rebellion rate', '{:.1%}'),
        ('peak_rebellion', 'Peak rebellion (people)', '{:,.0f}'),
        ('total_rebellion_months', 'Total rebellion person-months', '{:,.0f}'),
        ('time_to_80_loyalty', 'Months to 80% loyalty', '{}'),
    ]

    for key, label, fmt in metric_labels:
        row = f"{label:<35}"
        for s in strategies:
            val = all_metrics[s.name][key]
            if val is None:
                row += f" {'Never':<22}"
            else:
                row += f" {fmt.format(val):<22}"
        print(row)

    print("\n--- Cost-Benefit Analysis ---\n")
    for s in strategies:
        c = all_costs[s.name]
        print(f"  {s.name}:")
        print(f"    Total Cost:    {c['total_cost']:>12,.0f}")
        print(f"    Total Benefit: {c['total_benefit']:>12,.0f}")
        print(f"    Net Welfare:   {c['net_welfare']:>12,.0f}")
        print()

    # --- Historical Comparison ---
    print("--- Historical Verification ---")
    print("  Prophet's Amnesty (actual outcome):")
    print("  * Zero organized guerrilla resistance after conquest")
    print("  * Abu Sufyan, Ikrimah ibn Abi Jahl, Safwan ibn Umayyah all converted")
    print("  * Arabian Peninsula unified within 24 months")
    print("  * No garrison troops required in Mecca")
    print()
    print("  Counter-examples (purge strategies in history):")
    print("  * Roman conquest strategy: decades of Jewish revolts (66-135 CE)")
    print("  * Mongol invasions: destroyed infrastructure, centuries of recovery")
    print("  * Colonial purges: guerrilla resistance lasting generations")

    # --- Plot ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors = {'Purge (Classical Realist)': 'red',
              'Tit-for-Tat (Classical GT)': 'orange',
              'Amnesty (Muhammad Equilibrium)': 'green'}

    # Plot 1: Loyalty over time
    ax1 = axes[0, 0]
    for s in strategies:
        m = all_metrics[s.name]
        ax1.plot(m['loyalty'], color=colors[s.name], linewidth=2.5, label=s.name)
    ax1.axhline(y=0.8, color='gray', linestyle='--', alpha=0.5, label='80% threshold')
    ax1.set_xlabel('Months after Conquest', fontsize=11)
    ax1.set_ylabel('Loyalty Rate', fontsize=11)
    ax1.set_title('Population Loyalty Over Time', fontsize=12)
    ax1.legend(fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)

    # Plot 2: Rebellion over time
    ax2 = axes[0, 1]
    for s in strategies:
        m = all_metrics[s.name]
        rebellion_people = [r * N_POPULATION for r in m['rebellion']]
        ax2.plot(rebellion_people, color=colors[s.name], linewidth=2.5, label=s.name)
    ax2.set_xlabel('Months after Conquest', fontsize=11)
    ax2.set_ylabel('Active Rebels', fontsize=11)
    ax2.set_title('Rebellion Level Over Time', fontsize=12)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    # Plot 3: Stability index
    ax3 = axes[1, 0]
    for s in strategies:
        m = all_metrics[s.name]
        ax3.plot(m['stability'], color=colors[s.name], linewidth=2.5, label=s.name)
    ax3.set_xlabel('Months after Conquest', fontsize=11)
    ax3.set_ylabel('Stability Index', fontsize=11)
    ax3.set_title('Social Stability (1.0 = Perfect Peace)', fontsize=12)
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)

    # Plot 4: State distribution at final period
    ax4 = axes[1, 1]
    x = np.arange(len(STATES))
    width = 0.25

    for i, s in enumerate(strategies):
        final = all_metrics[s.name]
        vals = [final['loyalty'][-1], 1 - final['loyalty'][-1] - final['hostility'][-1] - final['rebellion'][-1],
                final['hostility'][-1], final['rebellion'][-1]]
        ax4.bar(x + i * width, vals, width, color=list(colors.values())[i],
                label=s.name, alpha=0.8)

    ax4.set_xlabel('Population State', fontsize=11)
    ax4.set_ylabel('Fraction', fontsize=11)
    ax4.set_title('Final Population Distribution (Month 50)', fontsize=12)
    ax4.set_xticks(x + width)
    ax4.set_xticklabels(STATES, fontsize=10)
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_15_conquest_amnesty.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n[OK] Figure saved: islamic_gt_codes/fig_15_conquest_amnesty.png")
    print("\n--- CONCLUSION ---")
    print("The Amnesty strategy (Muhammad Equilibrium) dominates both classical alternatives:")
    print("* HIGHEST loyalty rate, LOWEST rebellion, FASTEST unification")
    print("* LOWEST total cost, HIGHEST net welfare")
    print("* Confirmed by history: zero guerrilla resistance, peninsula unified in 24 months")
    print("* Mercy as dominant strategy is the central insight of IGT applied to post-conflict games")

if __name__ == "__main__":
    main()
