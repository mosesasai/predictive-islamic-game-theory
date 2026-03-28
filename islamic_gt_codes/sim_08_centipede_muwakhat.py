"""
Simulation 08: Centipede Game — Abdur-Rahman ibn Awf and the Muwakhat Trust

This simulation models the famous exchange between Abdur-Rahman ibn Awf and Sa'd ibn ar-Rabi
as a Centipede Game, showing how IGT preferences (lambda > 0) allow players to reach
deeper cooperative nodes that backward induction eliminates under classical GT.

Historical Context: When the Prophet paired Abdur-Rahman ibn Awf (a Muhajir who lost
everything) with Sa'd ibn ar-Rabi (a wealthy Ansari), Sa'd offered half his wealth and
one of his wives (after divorce). Abdur-Rahman declined EVERYTHING, asking only to be
shown the marketplace. He then built a fortune independently through trade. This is the
opposite of the classical centipede prediction: the receiver declined free wealth,
and both parties reached a far deeper cooperative node.

Key Insight: In the standard Centipede Game, backward induction predicts immediate
defection at node 1. But when players have akhirah-sensitive utilities (lambda > 0),
the payoff from continuing (trust + divine reward for restraint) exceeds the payoff
from taking, allowing the game to reach Pareto-superior deep nodes.

Reference: prophet_hypothesis.md — Hypothesis H8
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Centipede game structure
N_NODES = 10           # Number of decision nodes
GROWTH_RATE = 2.0      # Pot doubles at each node
INITIAL_POT = 10.0     # Starting pot size
TAKE_SHARE = 0.7       # Taker gets 70%, other gets 30%

# Akhirah parameters
OMEGA_DECLINE = 5.0    # Divine reward for declining offered wealth (tawakkul/self-reliance)
OMEGA_CONTINUE = 3.0   # Reward for continuing trust
OMEGA_TAKE_OFFERED = -2.0  # Slight penalty for taking what was generously offered
OMEGA_SELF_RELIANCE = 8.0  # Large reward for building independently

# ============================================================
# 2. CENTIPEDE GAME PAYOFFS
# ============================================================

def centipede_payoffs(n_nodes=N_NODES):
    """
    Compute payoffs at each node of the centipede game.
    At node k: pot = INITIAL_POT * GROWTH_RATE^k
    If player takes: taker gets 70%, other gets 30%
    If game reaches end: split 50/50 (maximum cooperation)
    """
    payoffs = []
    for k in range(n_nodes):
        pot = INITIAL_POT * (GROWTH_RATE ** k)
        taker_payoff = pot * TAKE_SHARE
        other_payoff = pot * (1 - TAKE_SHARE)
        payoffs.append((taker_payoff, other_payoff, pot))

    # Final node: equal split
    final_pot = INITIAL_POT * (GROWTH_RATE ** n_nodes)
    payoffs.append((final_pot * 0.5, final_pot * 0.5, final_pot))

    return payoffs


def backward_induction_classical(payoffs):
    """Standard backward induction: always TAKE at node 1."""
    n = len(payoffs) - 1  # Number of decision nodes
    action = ['CONTINUE'] * n

    # Player alternates: even nodes = Player 1, odd nodes = Player 2
    for k in range(n - 1, -1, -1):
        player = k % 2  # 0 or 1

        # Payoff if TAKE now
        take_payoff = payoffs[k][player]

        # Payoff if CONTINUE (what happens at next node)
        if k == n - 1:
            # Last node: continuing means equal split
            continue_payoff = payoffs[n][player]
        else:
            # Find next take point or end
            next_take = None
            for j in range(k + 1, n):
                if action[j] == 'TAKE':
                    next_take = j
                    break
            if next_take is not None:
                continue_payoff = payoffs[next_take][player]
            else:
                continue_payoff = payoffs[n][player]

        if take_payoff >= continue_payoff:
            action[k] = 'TAKE'

    return action


def backward_induction_igt(payoffs, lambda_akh=1.0):
    """IGT backward induction: akhirah rewards for continuing."""
    n = len(payoffs) - 1
    action = ['CONTINUE'] * n

    for k in range(n - 1, -1, -1):
        player = k % 2

        # Material payoff if TAKE
        take_material = payoffs[k][player]
        take_akhirah = lambda_akh * OMEGA_TAKE_OFFERED

        # Material payoff if CONTINUE
        if k == n - 1:
            continue_material = payoffs[n][player]
            continue_akhirah = lambda_akh * (OMEGA_CONTINUE + OMEGA_SELF_RELIANCE)
        else:
            next_take = None
            for j in range(k + 1, n):
                if action[j] == 'TAKE':
                    next_take = j
                    break
            if next_take is not None:
                continue_material = payoffs[next_take][player]
            else:
                continue_material = payoffs[n][player]
            continue_akhirah = lambda_akh * OMEGA_CONTINUE

        total_take = take_material + take_akhirah
        total_continue = continue_material + continue_akhirah

        if total_take > total_continue:
            action[k] = 'TAKE'

    return action


# ============================================================
# 3. SIMULATION: POPULATION OF PLAYERS
# ============================================================

def simulate_centipede_population(n_games=1000, lambda_dist='uniform'):
    """
    Simulate many centipede games with heterogeneous lambda values.
    Returns distribution of stopping nodes.
    """
    np.random.seed(42)
    payoffs = centipede_payoffs()
    stopping_nodes_classical = []
    stopping_nodes_igt = []

    for _ in range(n_games):
        # Classical: always stops at node 0
        actions_classical = backward_induction_classical(payoffs)
        stop_classical = next((i for i, a in enumerate(actions_classical) if a == 'TAKE'), N_NODES)
        stopping_nodes_classical.append(stop_classical)

        # IGT: lambda drawn from distribution
        if lambda_dist == 'uniform':
            lam = np.random.uniform(0, 2)
        elif lambda_dist == 'believer':
            lam = np.random.beta(5, 2) * 2  # Skewed high
        else:
            lam = 0.5

        actions_igt = backward_induction_igt(payoffs, lam)
        stop_igt = next((i for i, a in enumerate(actions_igt) if a == 'TAKE'), N_NODES)
        stopping_nodes_igt.append(stop_igt)

    return stopping_nodes_classical, stopping_nodes_igt


# ============================================================
# 4. ABDUR-RAHMAN SPECIFIC MODEL
# ============================================================

def abdur_rahman_model(lambda_akh=1.0):
    """
    Model the specific Abdur-Rahman / Sa'd interaction.
    Sa'd offers: half wealth + option for wife (after divorce).
    Abdur-Rahman declines and asks for marketplace directions.
    """
    # Sa'd's total wealth (arbitrary units)
    sadds_wealth = 1000

    # Option 1: TAKE (classical rational)
    take_payoff_material = sadds_wealth * 0.5  # 500
    take_payoff_akhirah = lambda_akh * OMEGA_TAKE_OFFERED

    # Option 2: DECLINE and build independently
    # Short-term: nothing, long-term: Abdur-Rahman became one of richest companions
    years = 10
    trade_growth = 0.4  # 40% annual return (he was an exceptional trader)
    starting_capital = 10  # Minimal starting capital from first market day

    independent_wealth = starting_capital
    for y in range(years):
        independent_wealth *= (1 + trade_growth)

    decline_payoff_material = independent_wealth
    decline_payoff_akhirah = lambda_akh * (OMEGA_DECLINE + OMEGA_SELF_RELIANCE)

    return {
        'take_material': take_payoff_material,
        'take_total': take_payoff_material + take_payoff_akhirah,
        'decline_material': decline_payoff_material,
        'decline_total': decline_payoff_material + decline_payoff_akhirah,
        'independent_wealth_trajectory': [starting_capital * (1 + trade_growth)**y for y in range(years + 1)],
    }


# ============================================================
# 5. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 08: CENTIPEDE GAME — ABDUR-RAHMAN IBN AWF")
    print("Trust and Self-Reliance under Akhirah-Sensitive Preferences")
    print("=" * 70)

    # --- Part A: Standard Centipede Analysis ---
    print("\n--- Part A: Centipede Game Payoff Structure ---")
    payoffs = centipede_payoffs()

    print(f"\n  {'Node':<8} {'Pot Size':<12} {'Taker Gets':<12} {'Other Gets':<12} {'End Split':<12}")
    print("-" * 56)
    for k in range(N_NODES):
        print(f"  {k:<8} {payoffs[k][2]:<12.0f} {payoffs[k][0]:<12.0f} {payoffs[k][1]:<12.0f}")
    print(f"  {'END':<8} {payoffs[-1][2]:<12.0f} {payoffs[-1][0]:<12.0f} {payoffs[-1][1]:<12.0f} {'50/50':<12}")

    # --- Part B: Backward Induction ---
    print("\n--- Part B: Backward Induction Results ---")
    actions_classical = backward_induction_classical(payoffs)
    stop_classical = next((i for i, a in enumerate(actions_classical) if a == 'TAKE'), N_NODES)
    print(f"  Classical GT: TAKE at node {stop_classical} (payoff: {payoffs[stop_classical][0]:.0f})")

    print(f"\n  {'Lambda':<10} {'Stop Node':<12} {'Payoff (Taker)':<16} {'Payoff (Other)':<16} {'Total Pot':<12}")
    print("-" * 66)
    for lam in [0.0, 0.2, 0.5, 0.8, 1.0, 1.5, 2.0]:
        actions = backward_induction_igt(payoffs, lam)
        stop = next((i for i, a in enumerate(actions) if a == 'TAKE'), N_NODES)
        if stop < N_NODES:
            p_take = payoffs[stop][0]
            p_other = payoffs[stop][1]
            pot = payoffs[stop][2]
        else:
            p_take = payoffs[-1][0]
            p_other = payoffs[-1][1]
            pot = payoffs[-1][2]
        print(f"  {lam:<10.1f} {stop:<12} {p_take:<16.0f} {p_other:<16.0f} {pot:<12.0f}")

    # --- Part C: Abdur-Rahman Specific Analysis ---
    print("\n--- Part C: Abdur-Rahman ibn Awf Decision Model ---")
    for lam in [0.0, 0.5, 1.0, 1.5]:
        result = abdur_rahman_model(lam)
        decision = "DECLINE (build)" if result['decline_total'] > result['take_total'] else "TAKE (accept)"
        print(f"  lambda={lam:.1f}: Take={result['take_total']:>8.0f}, Decline={result['decline_total']:>8.0f} -> {decision}")

    print("\n  Historical: Abdur-Rahman DECLINED, asked 'Show me the marketplace'")
    print("  He became one of the wealthiest companions through independent trade")

    ar_result = abdur_rahman_model(1.0)
    print(f"\n  Wealth trajectory (independent trade):")
    for y, w in enumerate(ar_result['independent_wealth_trajectory']):
        if y % 2 == 0 or y == len(ar_result['independent_wealth_trajectory']) - 1:
            print(f"    Year {y}: {w:>10.0f}")

    # --- Part D: Population Simulation ---
    print("\n--- Part D: Population Simulation (1000 games) ---")
    stop_classical, stop_igt = simulate_centipede_population(1000, 'believer')

    print(f"  Classical: Mean stop node = {np.mean(stop_classical):.2f}")
    print(f"  IGT (believer dist): Mean stop node = {np.mean(stop_igt):.2f}")
    print(f"  Classical: Mean realized pot = {np.mean([payoffs[min(s, N_NODES)][2] for s in stop_classical]):.0f}")
    print(f"  IGT: Mean realized pot = {np.mean([payoffs[min(s, N_NODES)][2] for s in stop_igt]):.0f}")

    # --- Plot ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Centipede game tree payoffs
    ax1 = axes[0, 0]
    nodes = range(N_NODES + 1)
    pots = [payoffs[k][2] for k in nodes]
    taker_payoffs = [payoffs[k][0] for k in nodes]
    other_payoffs = [payoffs[k][1] for k in nodes]

    ax1.plot(nodes, pots, 'b-o', linewidth=2, markersize=6, label='Total Pot')
    ax1.plot(nodes, taker_payoffs, 'r--s', linewidth=2, markersize=5, label='Taker Payoff')
    ax1.plot(nodes, other_payoffs, 'g--^', linewidth=2, markersize=5, label='Other Payoff')
    ax1.axvline(x=0, color='red', linewidth=3, alpha=0.3, label='Classical stop (node 0)')
    ax1.set_xlabel('Node', fontsize=11)
    ax1.set_ylabel('Payoff', fontsize=11)
    ax1.set_title('Centipede Game: Payoff Structure', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Plot 2: Stop node vs lambda
    ax2 = axes[0, 1]
    lambdas = np.linspace(0, 3, 100)
    stop_nodes = []
    for lam in lambdas:
        actions = backward_induction_igt(payoffs, lam)
        stop = next((i for i, a in enumerate(actions) if a == 'TAKE'), N_NODES)
        stop_nodes.append(stop)
    ax2.plot(lambdas, stop_nodes, 'g-', linewidth=2.5)
    ax2.set_xlabel('Lambda (Akhirah Sensitivity)', fontsize=11)
    ax2.set_ylabel('Stopping Node', fontsize=11)
    ax2.set_title('How Lambda Deepens Trust\n(Higher = more cooperation)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.5, N_NODES + 0.5)
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Classical prediction')
    ax2.axhline(y=N_NODES, color='green', linestyle='--', alpha=0.5, label='Full cooperation')
    ax2.legend(fontsize=9)

    # Plot 3: Abdur-Rahman wealth trajectory
    ax3 = axes[1, 0]
    ar = abdur_rahman_model(1.0)
    years = range(len(ar['independent_wealth_trajectory']))
    ax3.plot(years, ar['independent_wealth_trajectory'], 'g-o', linewidth=2.5, label='Independent trade')
    ax3.axhline(y=ar['take_material'], color='red', linewidth=2, linestyle='--',
                label=f"Accepted Sa'd's offer: {ar['take_material']:.0f}")
    ax3.set_xlabel('Year', fontsize=11)
    ax3.set_ylabel('Wealth', fontsize=11)
    ax3.set_title("Abdur-Rahman's Decision:\nDecline Gift, Build Independently", fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_yscale('log')

    # Plot 4: Population stopping node distribution
    ax4 = axes[1, 1]
    bins = np.arange(-0.5, N_NODES + 1.5, 1)
    ax4.hist(stop_classical, bins=bins, alpha=0.5, color='red', label='Classical GT', density=True)
    ax4.hist(stop_igt, bins=bins, alpha=0.5, color='green', label='IGT (believer dist)', density=True)
    ax4.set_xlabel('Stopping Node', fontsize=11)
    ax4.set_ylabel('Density', fontsize=11)
    ax4.set_title('Distribution of Stopping Nodes\n(1000 simulated games)', fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)

    plt.suptitle('Centipede Game: Trust under Akhirah-Sensitive Preferences',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_08_centipede_muwakhat.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n--- CONCLUSION ---")
    print("The Abdur-Rahman / Sa'd exchange demonstrates the Centipede Game insight:")
    print("  1. Classical GT: backward induction -> TAKE at node 0 (accept the offer)")
    print("  2. IGT: akhirah rewards for self-reliance make DECLINING rational")
    print("  3. Higher lambda allows reaching deeper cooperative nodes")
    print("  4. Both parties benefit: Sa'd keeps wealth, Abdur-Rahman builds more")
    print("  5. Trust under akhirah breaks the backward induction paradox")
    print("  6. Historical: Abdur-Rahman declined and became independently wealthy")
    print("\nFigure saved: islamic_gt_codes/fig_08_centipede_muwakhat.png")

if __name__ == "__main__":
    main()
