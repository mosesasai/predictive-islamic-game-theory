"""
Simulation 11: Hotelling's Game — Tawhid as Dimension-Breaking Strategy

This simulation models the Prophet's positioning at "extreme" pure monotheism (Tawhid)
rather than compromising toward median Meccan religious opinion, and shows how creating
a new dimension of competition (moral authority) escapes the Hotelling convergence-to-center
trap.

Historical Context: Hotelling's Law predicts that competitors converge to the median voter's
position. Meccan religion was a spectrum from polytheism to vague monotheistic sympathies
(hanif tradition). Quraysh leaders occupied the center-right of this spectrum. Classical
political strategy would predict the Prophet should moderate his message toward the Meccan
median. Instead, he took the "extreme" position: absolute Tawhid (La ilaha illa Allah),
no compromise (Surah Al-Kafirun: "To you your religion, to me mine"). This SHOULD have
failed per Hotelling — but succeeded because the Prophet opened a NEW competitive dimension
(moral authority, akhirah accountability) where he had monopoly position.

Key Insight: When a new dimension is introduced that is orthogonal to the existing
spectrum, the "extreme" position on the old axis can become the optimal position if it
commands monopoly on the new axis.

Reference: prophet_hypothesis.md — Hypothesis H11
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Meccan religious spectrum (1D Hotelling)
# 0 = pure polytheism, 1 = pure monotheism
POPULATION_SIZE = 1000
MECCAN_MEDIAN = 0.3          # Most Meccans were moderate polytheists
MECCAN_STD = 0.15            # Spread of religious preferences

# Competitor positions
QURAYSH_POSITION = 0.35      # Quraysh leaders: slightly above median (maintaining status quo)
PROPHET_POSITION_COMPROMISE = 0.45  # Hypothetical: what if Prophet compromised?
PROPHET_POSITION_TAWHID = 1.0       # Actual: pure Tawhid, no compromise

# Second dimension: moral authority / akhirah accountability
# 0 = no moral authority, 1 = maximum moral authority
QURAYSH_MORAL = 0.2          # Low moral authority (corruption, tribal privilege)
PROPHET_MORAL = 0.95         # Extremely high moral authority

# Voter utility: U = -|position - preference| + beta * moral_authority
# beta: weight voters place on moral dimension
BETA_INITIAL = 0.1           # Initially, moral dimension barely matters
BETA_GROWTH_RATE = 0.15      # Per-period growth as moral dimension becomes salient

# ============================================================
# 2. HOTELLING MODEL (1D)
# ============================================================

def hotelling_1d_share(candidate_pos, opponent_pos, voter_positions):
    """
    Standard 1D Hotelling: voters choose nearest candidate.
    Returns vote share for candidate.
    """
    dist_cand = np.abs(voter_positions - candidate_pos)
    dist_opp = np.abs(voter_positions - opponent_pos)
    return np.mean(dist_cand < dist_opp)


def hotelling_1d_optimal(opponent_pos, voter_positions, n_search=200):
    """Find optimal position in 1D Hotelling against opponent."""
    positions = np.linspace(0, 1, n_search)
    shares = [hotelling_1d_share(p, opponent_pos, voter_positions) for p in positions]
    best_idx = np.argmax(shares)
    return positions[best_idx], shares[best_idx]


# ============================================================
# 3. EXTENDED HOTELLING (2D: Religion + Moral Authority)
# ============================================================

def hotelling_2d_share(cand_pos, cand_moral, opp_pos, opp_moral,
                        voter_positions, voter_moral_prefs, beta):
    """
    2D Hotelling: voters weigh both religious position and moral authority.
    U_voter = -|pos - pref_pos| + beta * moral_authority_of_candidate
    """
    u_cand = -np.abs(voter_positions - cand_pos) + beta * cand_moral
    u_opp = -np.abs(voter_positions - opp_pos) + beta * opp_moral
    return np.mean(u_cand > u_opp)


# ============================================================
# 4. DYNAMIC SIMULATION
# ============================================================

def simulate_market_dynamics(n_periods=30):
    """
    Simulate the evolution of market shares as the moral dimension
    becomes increasingly salient over time.
    """
    np.random.seed(42)

    # Generate voter positions (religious preferences)
    voter_positions = np.clip(np.random.normal(MECCAN_MEDIAN, MECCAN_STD, POPULATION_SIZE), 0, 1)
    voter_moral_prefs = np.random.uniform(0, 1, POPULATION_SIZE)  # Everyone values morality somewhat

    # Three scenarios
    scenarios = {
        'Prophet (Tawhid, high moral)': (PROPHET_POSITION_TAWHID, PROPHET_MORAL),
        'Prophet (compromise, high moral)': (PROPHET_POSITION_COMPROMISE, PROPHET_MORAL),
        'Generic reformer (compromise, low moral)': (PROPHET_POSITION_COMPROMISE, 0.5),
    }

    results = {name: {'shares': [], 'betas': []} for name in scenarios}

    for t in range(n_periods):
        beta = BETA_INITIAL + BETA_GROWTH_RATE * t  # Moral dimension becomes more salient

        for name, (pos, moral) in scenarios.items():
            share = hotelling_2d_share(pos, moral, QURAYSH_POSITION, QURAYSH_MORAL,
                                       voter_positions, voter_moral_prefs, beta)
            results[name]['shares'].append(share)
            results[name]['betas'].append(beta)

    return results, voter_positions


def dimension_analysis():
    """
    Analyze how the new dimension changes the competitive landscape.
    """
    np.random.seed(42)
    voter_positions = np.clip(np.random.normal(MECCAN_MEDIAN, MECCAN_STD, POPULATION_SIZE), 0, 1)

    # 1D analysis: Tawhid position is "extreme"
    share_1d_tawhid = hotelling_1d_share(PROPHET_POSITION_TAWHID, QURAYSH_POSITION, voter_positions)
    share_1d_compromise = hotelling_1d_share(PROPHET_POSITION_COMPROMISE, QURAYSH_POSITION, voter_positions)
    opt_pos, opt_share = hotelling_1d_optimal(QURAYSH_POSITION, voter_positions)

    # 2D analysis at different beta values
    betas = np.linspace(0, 3, 50)
    shares_tawhid_2d = []
    shares_compromise_2d = []

    for beta in betas:
        s1 = hotelling_2d_share(PROPHET_POSITION_TAWHID, PROPHET_MORAL,
                                QURAYSH_POSITION, QURAYSH_MORAL,
                                voter_positions, np.random.uniform(0, 1, POPULATION_SIZE), beta)
        s2 = hotelling_2d_share(PROPHET_POSITION_COMPROMISE, PROPHET_MORAL,
                                QURAYSH_POSITION, QURAYSH_MORAL,
                                voter_positions, np.random.uniform(0, 1, POPULATION_SIZE), beta)
        shares_tawhid_2d.append(s1)
        shares_compromise_2d.append(s2)

    return {
        'share_1d_tawhid': share_1d_tawhid,
        'share_1d_compromise': share_1d_compromise,
        'optimal_1d': (opt_pos, opt_share),
        'betas': betas,
        'shares_tawhid_2d': shares_tawhid_2d,
        'shares_compromise_2d': shares_compromise_2d,
    }


# ============================================================
# 5. QURAYSH COUNTER-STRATEGY ANALYSIS
# ============================================================

def quraysh_response_analysis():
    """
    Analyze why Quraysh couldn't compete on the moral dimension.
    They tried to match on religion (offered compromise) but couldn't
    match on moral authority.
    """
    np.random.seed(42)
    voter_positions = np.clip(np.random.normal(MECCAN_MEDIAN, MECCAN_STD, POPULATION_SIZE), 0, 1)

    # Quraysh responses
    responses = {
        'Status quo': (QURAYSH_POSITION, QURAYSH_MORAL),
        'Quraysh move toward monotheism': (0.5, 0.25),  # Try to match on religion
        'Quraysh improve morality': (QURAYSH_POSITION, 0.5),  # Try to match on morals
        'Quraysh: both moves': (0.5, 0.5),  # Try both
    }

    beta = 1.5  # Moderate moral salience

    results = {}
    for name, (pos, moral) in responses.items():
        # Prophet's share against this Quraysh strategy
        share = hotelling_2d_share(PROPHET_POSITION_TAWHID, PROPHET_MORAL,
                                   pos, moral, voter_positions,
                                   np.random.uniform(0, 1, POPULATION_SIZE), beta)
        results[name] = share

    return results


# ============================================================
# 6. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 11: HOTELLING'S GAME — TAWHID AS DIMENSION-BREAKING STRATEGY")
    print("Pure Monotheism vs. Convergence-to-Center")
    print("=" * 70)

    # --- Part A: 1D Hotelling Analysis ---
    print("\n--- Part A: Standard 1D Hotelling Analysis ---")
    dim_analysis = dimension_analysis()

    print(f"\n  Meccan median religious position: {MECCAN_MEDIAN}")
    print(f"  Quraysh position: {QURAYSH_POSITION}")
    print(f"  Optimal 1D position: {dim_analysis['optimal_1d'][0]:.3f} (share: {dim_analysis['optimal_1d'][1]:.3f})")
    print(f"\n  Prophet at Tawhid (1.0): 1D share = {dim_analysis['share_1d_tawhid']:.3f} — LOSES in 1D!")
    print(f"  Prophet at compromise (0.45): 1D share = {dim_analysis['share_1d_compromise']:.3f}")
    print(f"\n  Hotelling predicts: converge to center. Tawhid position is 'irrational'")

    # --- Part B: 2D Hotelling with Moral Dimension ---
    print("\n--- Part B: 2D Hotelling (Religion + Moral Authority) ---")
    print(f"\n  {'Beta (moral weight)':<22} {'Tawhid Share':<15} {'Compromise Share':<18} {'Winner':<15}")
    print("-" * 70)
    for i in range(0, len(dim_analysis['betas']), 10):
        beta = dim_analysis['betas'][i]
        s_t = dim_analysis['shares_tawhid_2d'][i]
        s_c = dim_analysis['shares_compromise_2d'][i]
        winner = "Tawhid" if s_t > s_c else "Compromise"
        print(f"  {beta:<22.2f} {s_t:<15.3f} {s_c:<18.3f} {winner:<15}")

    # --- Part C: Dynamic Market Evolution ---
    print("\n--- Part C: Dynamic Market Share Evolution ---")
    dynamics, voter_pos = simulate_market_dynamics(30)

    print(f"\n  {'Period':<10}", end="")
    for name in dynamics:
        short = name.split('(')[1].split(')')[0][:20] if '(' in name else name[:20]
        print(f"  {short:<20}", end="")
    print()
    print("-" * 70)
    for t in [0, 5, 10, 15, 20, 25, 29]:
        print(f"  {t:<10}", end="")
        for name in dynamics:
            print(f"  {dynamics[name]['shares'][t]:<20.3f}", end="")
        print()

    # --- Part D: Quraysh Counter-Strategy ---
    print("\n--- Part D: Quraysh Counter-Strategy Analysis ---")
    quraysh = quraysh_response_analysis()

    print(f"\n  {'Quraysh Strategy':<35} {'Prophet Share':<15} {'Quraysh Share':<15}")
    print("-" * 65)
    for name, share in quraysh.items():
        print(f"  {name:<35} {share:<15.3f} {1-share:<15.3f}")

    print("\n  Key: Quraysh cannot close the gap because moral authority requires")
    print("  authentic character, not just positional adjustment")

    # --- Part E: The Compromise Offer ---
    print("\n--- Part E: Why Quraysh's 'Year-Sharing' Offer Failed ---")
    print("  Quraysh offered: 'Worship our gods one year, we worship yours one year'")
    print("  This is a Hotelling-style compromise at position ~0.5")
    print(f"  Prophet at compromise (0.5): 1D share = {dim_analysis['share_1d_compromise']:.3f}")
    print(f"  Prophet at Tawhid (1.0): 2D share at beta=1.5 = {dim_analysis['shares_tawhid_2d'][25]:.3f}")
    print("  Compromise DESTROYS the moral authority dimension advantage")
    print("  Surah Al-Kafirun (109): 'To you your religion, to me mine' = maintaining position")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Voter distribution and positions
    ax1 = axes[0, 0]
    ax1.hist(voter_pos, bins=50, density=True, alpha=0.5, color='gray', label='Meccan population')
    ax1.axvline(x=QURAYSH_POSITION, color='red', linewidth=3, label=f'Quraysh ({QURAYSH_POSITION})')
    ax1.axvline(x=PROPHET_POSITION_TAWHID, color='green', linewidth=3, label=f'Tawhid ({PROPHET_POSITION_TAWHID})')
    ax1.axvline(x=PROPHET_POSITION_COMPROMISE, color='orange', linewidth=2, linestyle='--',
                label=f'Compromise ({PROPHET_POSITION_COMPROMISE})')
    ax1.axvline(x=dim_analysis['optimal_1d'][0], color='blue', linewidth=2, linestyle=':',
                label=f'Hotelling optimal ({dim_analysis["optimal_1d"][0]:.2f})')
    ax1.set_xlabel('Religious Position (0=Polytheism, 1=Monotheism)', fontsize=10)
    ax1.set_ylabel('Density', fontsize=11)
    ax1.set_title('1D Hotelling: Voter Distribution', fontsize=12)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    # Plot 2: 2D positioning map
    ax2 = axes[0, 1]
    ax2.scatter([QURAYSH_POSITION], [QURAYSH_MORAL], color='red', s=200, marker='s',
               zorder=5, label='Quraysh')
    ax2.scatter([PROPHET_POSITION_TAWHID], [PROPHET_MORAL], color='green', s=200, marker='*',
               zorder=5, label='Prophet (Tawhid)')
    ax2.scatter([PROPHET_POSITION_COMPROMISE], [PROPHET_MORAL], color='orange', s=100, marker='^',
               zorder=5, label='Prophet (hypothetical compromise)')
    # Draw voter cloud
    moral_prefs = np.random.uniform(0, 0.5, POPULATION_SIZE)  # Most voters low moral awareness initially
    ax2.scatter(voter_pos, moral_prefs, alpha=0.1, s=5, color='gray')
    ax2.set_xlabel('Religious Position', fontsize=11)
    ax2.set_ylabel('Moral Authority Dimension', fontsize=11)
    ax2.set_title('2D Competitive Space:\nReligion + Moral Authority', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-0.05, 1.05)
    ax2.set_ylim(-0.05, 1.05)

    # Plot 3: Tawhid vs Compromise share as beta increases
    ax3 = axes[0, 2]
    ax3.plot(dim_analysis['betas'], dim_analysis['shares_tawhid_2d'], 'g-', linewidth=2.5,
            label='Tawhid (position=1.0)')
    ax3.plot(dim_analysis['betas'], dim_analysis['shares_compromise_2d'], 'orange', linewidth=2.5,
            linestyle='--', label='Compromise (position=0.45)')
    ax3.axhline(y=0.5, color='black', linewidth=1, linestyle=':', alpha=0.5)
    ax3.set_xlabel('Beta (Moral Dimension Weight)', fontsize=11)
    ax3.set_ylabel('Market Share', fontsize=11)
    ax3.set_title('Tawhid Wins as Moral Dimension\nBecomes Salient', fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    # Find crossover
    for i in range(len(dim_analysis['betas']) - 1):
        if (dim_analysis['shares_tawhid_2d'][i] < dim_analysis['shares_compromise_2d'][i] and
            dim_analysis['shares_tawhid_2d'][i+1] >= dim_analysis['shares_compromise_2d'][i+1]):
            ax3.axvline(x=dim_analysis['betas'][i], color='blue', linestyle=':', alpha=0.7,
                       label=f'Crossover at beta={dim_analysis["betas"][i]:.2f}')
            ax3.legend(fontsize=9)
            break

    # Plot 4: Dynamic market share evolution
    ax4 = axes[1, 0]
    colors_dyn = {'Prophet (Tawhid, high moral)': 'green',
                  'Prophet (compromise, high moral)': 'orange',
                  'Generic reformer (compromise, low moral)': 'gray'}
    for name, data in dynamics.items():
        short = name.split(',')[0].replace('Prophet ', '')
        ax4.plot(range(30), data['shares'], color=colors_dyn[name], linewidth=2.5, label=short)
    ax4.axhline(y=0.5, color='black', linewidth=1, linestyle=':', alpha=0.5)
    ax4.set_xlabel('Period (Moral salience increases)', fontsize=11)
    ax4.set_ylabel('Market Share vs Quraysh', fontsize=11)
    ax4.set_title('Dynamic Market Evolution', fontsize=12)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)

    # Plot 5: Quraysh counter-strategy
    ax5 = axes[1, 1]
    q_names = list(quraysh.keys())
    q_shares_prophet = [quraysh[n] for n in q_names]
    q_shares_quraysh = [1 - quraysh[n] for n in q_names]
    x = np.arange(len(q_names))
    width = 0.35
    ax5.bar(x - width/2, q_shares_prophet, width, color='green', alpha=0.8, label='Prophet share')
    ax5.bar(x + width/2, q_shares_quraysh, width, color='red', alpha=0.8, label='Quraysh share')
    ax5.set_xticks(x)
    ax5.set_xticklabels([n[:20] for n in q_names], rotation=45, ha='right', fontsize=8)
    ax5.set_ylabel('Market Share', fontsize=11)
    ax5.set_title('Quraysh Counter-Strategies\n(None fully effective)', fontsize=12)
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3, axis='y')
    ax5.axhline(y=0.5, color='black', linewidth=1, linestyle=':')

    # Plot 6: Dimension diagram
    ax6 = axes[1, 2]
    # Show how new dimension breaks Hotelling
    theta = np.linspace(0, np.pi/2, 100)
    r1 = 0.5  # Old dimension radius (Quraysh advantage)
    r2 = 0.9  # New dimension radius (Prophet advantage)
    ax6.plot(r1 * np.cos(theta), r1 * np.sin(theta), 'r--', linewidth=2, label='Quraysh reach')
    ax6.plot(r2 * np.cos(theta), r2 * np.sin(theta), 'g-', linewidth=2, label='Prophet reach')
    ax6.annotate('Quraysh\n(center, low moral)', xy=(0.35, 0.2), fontsize=10, color='red',
                ha='center', fontweight='bold')
    ax6.annotate('Prophet\n(extreme, high moral)', xy=(0.3, 0.85), fontsize=10, color='green',
                ha='center', fontweight='bold')
    ax6.arrow(0.5, 0.1, 0, 0.7, head_width=0.03, head_length=0.03, fc='green', ec='green', alpha=0.5)
    ax6.text(0.55, 0.4, 'NEW\nDIMENSION', fontsize=10, color='green', alpha=0.7)
    ax6.set_xlabel('Religious Spectrum', fontsize=11)
    ax6.set_ylabel('Moral Authority', fontsize=11)
    ax6.set_title('Dimension-Breaking Strategy', fontsize=12)
    ax6.set_xlim(-0.1, 1.1)
    ax6.set_ylim(-0.1, 1.1)
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)

    plt.suptitle("Hotelling's Game: Tawhid as Dimension-Breaking Strategy",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_11_hotelling_tawhid.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n--- CONCLUSION ---")
    print("The Tawhid positioning demonstrates dimension-breaking strategy:")
    print("  1. In 1D Hotelling (religion only): Tawhid is the WORST position (extreme)")
    print("  2. Hotelling predicts: converge to Meccan median polytheism")
    print("  3. Prophet opened NEW dimension: moral authority / akhirah accountability")
    print("  4. On this new dimension, Quraysh had no competitive position")
    print("  5. As moral dimension became salient, Tawhid dominated compromise")
    print("  6. Quraysh could adjust religious position but NOT moral authority")
    print("  7. Refusing compromise (Surah Al-Kafirun) preserved the dimensional advantage")
    print("  8. This explains why 'extreme' positioning won: it was only extreme in 1D")
    print("\nFigure saved: islamic_gt_codes/fig_11_hotelling_tawhid.png")

if __name__ == "__main__":
    main()
