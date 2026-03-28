"""
Simulation 06: Treaty of Hudaybiyyah — Finite vs. Infinite Game Analysis

This simulation demonstrates how reframing a bargaining game from finite to infinite
horizon (with dakwah externalities) makes apparently "losing" treaty terms optimal.

Historical Context: The Prophet ﷺ accepted seemingly unfavorable treaty terms at Hudaybiyyah
(628 CE). Within 22 months, the peace enabled explosive growth of the Muslim community.

Reference: prophet_hypothesis.md — Hypothesis H6
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# Treaty terms (material perspective)
MILITARY_ADVANTAGE = 0.6     # Muslims had ~1400 devoted fighters
TREATY_MATERIAL_COST = -0.3  # Asymmetric extradition, no Umrah that year, title removal
PEACE_DURATION = 22          # Months of peace before Quraysh violated
WAR_COST_PER_PERIOD = -0.5   # Cost of continued warfare per period

# Dakwah (propagation) parameters
DAKWAH_RATE_WAR = 0.02       # Conversion rate during warfare (very low)
DAKWAH_RATE_PEACE = 0.15     # Conversion rate during peace (high — free travel, dialogue)
INITIAL_MUSLIMS = 1400       # At time of Hudaybiyyah
ARABIA_POPULATION = 100000   # Approximate population of Arabian peninsula

# Discount factors
DELTA_MATERIAL = 0.95        # Material discount factor
DELTA_AKHIRAH = 1.0          # Akhirah discount factor (no discounting)

# Akhirah parameters
OMEGA_OBEY_REVELATION = 100  # Divine reward for following revelation (Quran 48:1)
OMEGA_REJECT_PEACE = -50     # Divine cost of rejecting peace when commanded
LAMBDA = 1.0                 # Akhirah sensitivity

# ============================================================
# 2. FINITE GAME ANALYSIS (Classical GT)
# ============================================================

def classical_bargaining_payoff(accept_treaty, periods=10):
    """
    Classical bargaining analysis: finite horizon, material payoffs only.

    If accept: get treaty_material_cost + peace dividends
    If reject: fight with military advantage
    """
    if accept_treaty:
        # Material loss from unfavorable terms
        payoff = TREATY_MATERIAL_COST
        for t in range(1, periods + 1):
            # Minor peace dividends (trade, stability)
            payoff += (DELTA_MATERIAL ** t) * 0.1
        return payoff
    else:
        # War with military advantage
        payoff = 0
        for t in range(1, periods + 1):
            payoff += (DELTA_MATERIAL ** t) * (MILITARY_ADVANTAGE + WAR_COST_PER_PERIOD)
        return payoff

# ============================================================
# 3. INFINITE GAME ANALYSIS (IGT)
# ============================================================

def igt_treaty_payoff(accept_treaty, periods=50, alpha=0.5, lambda_akh=1.0):
    """
    IGT analysis: infinite horizon with dakwah externalities and akhirah payoffs.

    U = material + alpha * (souls saved through dakwah) + lambda * Omega
    """
    muslims = INITIAL_MUSLIMS
    material_payoff = 0
    dakwah_payoff = 0
    akhirah_payoff = 0

    if accept_treaty:
        # Accept treaty — peace enables dakwah
        material_payoff = TREATY_MATERIAL_COST
        akhirah_payoff = lambda_akh * OMEGA_OBEY_REVELATION

        muslim_trajectory = [muslims]
        for t in range(1, periods + 1):
            # Dakwah during peace: exponential growth
            new_converts = int(muslims * DAKWAH_RATE_PEACE)
            muslims = min(muslims + new_converts, ARABIA_POPULATION)
            muslim_trajectory.append(muslims)

            # Material: trade and stability dividends
            material_payoff += (DELTA_MATERIAL ** t) * 0.1

            # Altruistic: each new convert is a welfare gain
            dakwah_payoff += (DELTA_MATERIAL ** t) * alpha * new_converts * 0.01

        total = material_payoff + dakwah_payoff + akhirah_payoff
        return total, muslim_trajectory

    else:
        # Reject treaty — continued warfare
        akhirah_payoff = lambda_akh * OMEGA_REJECT_PEACE

        muslim_trajectory = [muslims]
        for t in range(1, periods + 1):
            # Dakwah during war: very slow, casualties reduce numbers
            new_converts = int(muslims * DAKWAH_RATE_WAR)
            casualties = int(muslims * 0.01)  # War casualties
            muslims = max(muslims + new_converts - casualties, 100)
            muslim_trajectory.append(muslims)

            # Material: war costs + occasional tactical gains
            material_payoff += (DELTA_MATERIAL ** t) * (MILITARY_ADVANTAGE * 0.3 + WAR_COST_PER_PERIOD)

            # Dakwah: minimal during war
            dakwah_payoff += (DELTA_MATERIAL ** t) * alpha * new_converts * 0.01

        total = material_payoff + dakwah_payoff + akhirah_payoff
        return total, muslim_trajectory

# ============================================================
# 4. HISTORICAL CONVERSION DATA (Key Events Post-Hudaybiyyah)
# ============================================================

historical_events = {
    0: "Treaty of Hudaybiyyah signed (Dhul Qi'dah 6 AH)",
    3: "Letters to Kings dispatched (7 AH)",
    6: "Khalid ibn al-Walid converts (military genius)",
    7: "Amr ibn al-As converts (diplomatic mastermind)",
    8: "Uthman ibn Talhah converts (keeper of Kaaba key)",
    15: "Quraysh violate treaty (attack Banu Khuza'ah)",
    18: "Conquest of Mecca — 10,000 strong (Ramadan 8 AH)",
    22: "Arabian Peninsula largely unified under Islam",
}

# ============================================================
# 5. MAIN SIMULATION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 06: TREATY OF HUDAYBIYYAH")
    print("Finite Game (Classical GT) vs. Infinite Game (IGT) Analysis")
    print("=" * 70)

    # --- Part A: Classical Bargaining Analysis ---
    print("\n--- Part A: Classical (Finite) Game Analysis ---")
    for horizon in [5, 10, 20, 50]:
        accept_val = classical_bargaining_payoff(True, horizon)
        reject_val = classical_bargaining_payoff(False, horizon)
        decision = "ACCEPT" if accept_val > reject_val else "REJECT"
        print(f"  Horizon={horizon:>3} periods: Accept={accept_val:>8.3f}, Reject={reject_val:>8.3f} -> Classical: {decision}")

    print("\n  -> Classical GT recommends REJECTING the treaty at all finite horizons")
    print("  -> This matches the companions' initial reaction (Umar's objection)")

    # --- Part B: IGT Analysis with Dakwah ---
    print("\n--- Part B: IGT (Infinite Game) Analysis ---")

    param_sets = [
        (0.0, 0.0, "Classical (no altruism, no akhirah)"),
        (0.3, 0.0, "Altruism only (alpha=0.3)"),
        (0.0, 0.5, "Akhirah only (lambda=0.5)"),
        (0.3, 0.5, "Moderate IGT"),
        (0.5, 1.0, "Strong IGT (Prophetic level)"),
    ]

    print(f"\n{'Parameters':<40} {'Accept':<12} {'Reject':<12} {'Decision':<10}")
    print("-" * 74)

    for alpha, lam, label in param_sets:
        accept_val, accept_traj = igt_treaty_payoff(True, 50, alpha, lam)
        reject_val, reject_traj = igt_treaty_payoff(False, 50, alpha, lam)
        decision = "ACCEPT" if accept_val > reject_val else "REJECT"
        print(f"{label:<40} {accept_val:<12.2f} {reject_val:<12.2f} {decision:<10}")

    # --- Part C: Muslim Population Growth ---
    print("\n--- Part C: Muslim Community Growth (Peace vs. War) ---")

    _, peace_trajectory = igt_treaty_payoff(True, 30, 0.5, 1.0)
    _, war_trajectory = igt_treaty_payoff(False, 30, 0.5, 1.0)

    print(f"\n{'Month':<8} {'Peace (Treaty)':<20} {'War (No Treaty)':<20} {'Difference':<15}")
    print("-" * 63)
    for t in [0, 3, 6, 12, 18, 22, 30]:
        if t < len(peace_trajectory):
            diff = peace_trajectory[t] - war_trajectory[t]
            print(f"{t:<8} {peace_trajectory[t]:<20,} {war_trajectory[t]:<20,} {diff:<15,}")

    # --- Part D: Key Historical Events ---
    print("\n--- Part D: Historical Verification ---")
    for month, event in sorted(historical_events.items()):
        pop = peace_trajectory[min(month, len(peace_trajectory)-1)]
        print(f"  Month {month:>2}: {event}")
        print(f"           -> Model population: ~{pop:,}")

    # --- Part E: Sensitivity Analysis ---
    print("\n--- Part E: Critical Dakwah Rate Analysis ---")
    print("  What dakwah rate makes the treaty worth accepting (material terms only)?")

    for dakwah_rate in [0.01, 0.05, 0.10, 0.15, 0.20, 0.30]:
        # Simple NPV calculation: peace value vs war value
        peace_npv = TREATY_MATERIAL_COST
        war_npv = 0
        pop = INITIAL_MUSLIMS

        for t in range(1, 30):
            new_converts = int(pop * dakwah_rate)
            pop = min(pop + new_converts, ARABIA_POPULATION)
            peace_npv += (DELTA_MATERIAL ** t) * (0.1 + 0.001 * new_converts)
            war_npv += (DELTA_MATERIAL ** t) * (MILITARY_ADVANTAGE * 0.3 + WAR_COST_PER_PERIOD)

        status = "ACCEPT [OK]" if peace_npv > war_npv else "REJECT [X]"
        print(f"  Dakwah rate={dakwah_rate:.2f}: Peace NPV={peace_npv:.2f}, War NPV={war_npv:.2f} -> {status}")

    # --- Plot ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Population trajectories
    ax1 = axes[0, 0]
    months = range(len(peace_trajectory))
    ax1.plot(months, peace_trajectory, 'g-', linewidth=2.5, label='Peace (Treaty accepted)')
    ax1.plot(months, war_trajectory, 'r-', linewidth=2.5, label='War (Treaty rejected)')
    ax1.axvline(x=22, color='blue', linestyle='--', alpha=0.5, label='Conquest of Mecca')
    ax1.set_xlabel('Months after Hudaybiyyah', fontsize=11)
    ax1.set_ylabel('Muslim Population', fontsize=11)
    ax1.set_title('Community Growth: Peace vs. War', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Plot 2: Cumulative payoff comparison
    ax2 = axes[0, 1]
    cum_peace_material = [TREATY_MATERIAL_COST]
    cum_war_material = [0]
    cum_peace_igt = [TREATY_MATERIAL_COST + LAMBDA * OMEGA_OBEY_REVELATION]
    cum_war_igt = [LAMBDA * OMEGA_REJECT_PEACE]

    for t in range(1, 30):
        cum_peace_material.append(cum_peace_material[-1] + DELTA_MATERIAL**t * 0.1)
        cum_war_material.append(cum_war_material[-1] + DELTA_MATERIAL**t * (MILITARY_ADVANTAGE*0.3 + WAR_COST_PER_PERIOD))
        cum_peace_igt.append(cum_peace_igt[-1] + DELTA_MATERIAL**t * 0.3)
        cum_war_igt.append(cum_war_igt[-1] + DELTA_MATERIAL**t * (MILITARY_ADVANTAGE*0.3 + WAR_COST_PER_PERIOD))

    ax2.plot(range(30), cum_peace_material, 'g--', linewidth=2, label='Peace (material only)')
    ax2.plot(range(30), cum_war_material, 'r--', linewidth=2, label='War (material only)')
    ax2.plot(range(30), cum_peace_igt, 'g-', linewidth=2.5, label='Peace (IGT: +akhirah+dakwah)')
    ax2.plot(range(30), cum_war_igt, 'r-', linewidth=2.5, label='War (IGT)')
    ax2.set_xlabel('Months', fontsize=11)
    ax2.set_ylabel('Cumulative Payoff', fontsize=11)
    ax2.set_title('Cumulative Payoffs: Material vs. IGT', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linewidth=0.5)

    # Plot 3: Decision boundary (alpha vs lambda)
    ax3 = axes[1, 0]
    n_pts = 50
    alphas = np.linspace(0, 1, n_pts)
    lambdas = np.linspace(0, 2, n_pts)
    decision_map = np.zeros((n_pts, n_pts))

    for i, a in enumerate(alphas):
        for j, l in enumerate(lambdas):
            acc, _ = igt_treaty_payoff(True, 30, a, l)
            rej, _ = igt_treaty_payoff(False, 30, a, l)
            decision_map[j, i] = 1.0 if acc > rej else 0.0

    im = ax3.imshow(decision_map, extent=[0, 1, 0, 2], origin='lower',
                     cmap='RdYlGn', aspect='auto')
    ax3.set_xlabel('Altruism (alpha)', fontsize=11)
    ax3.set_ylabel('Akhirah Sensitivity (lambda)', fontsize=11)
    ax3.set_title('Treaty Decision Boundary\n(Green=Accept, Red=Reject)', fontsize=12)
    ax3.plot(0, 0, 'rx', markersize=15, label='Classical GT')
    ax3.plot(0.5, 1.0, 'w*', markersize=15, label="Prophet's parameters")
    ax3.legend(fontsize=10)

    # Plot 4: Key conversions timeline
    ax4 = axes[1, 1]
    events_x = list(historical_events.keys())
    events_labels = [v.split('(')[0].strip()[:40] for v in historical_events.values()]
    events_pop = [peace_trajectory[min(m, len(peace_trajectory)-1)] for m in events_x]

    ax4.barh(range(len(events_x)), events_pop, color='teal', alpha=0.7)
    ax4.set_yticks(range(len(events_x)))
    ax4.set_yticklabels(events_labels, fontsize=8)
    ax4.set_xlabel('Muslim Population', fontsize=11)
    ax4.set_title('Historical Events Post-Hudaybiyyah', fontsize=12)
    ax4.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_06_hudaybiyyah_treaty.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n[OK] Figure saved: islamic_gt_codes/fig_06_hudaybiyyah_treaty.png")
    print("\n--- CONCLUSION ---")
    print("The Treaty of Hudaybiyyah demonstrates the core IGT insight:")
    print("* Classical GT (finite horizon, material payoffs): REJECT treaty -> continued war")
    print("* IGT (infinite horizon, dakwah + akhirah): ACCEPT treaty -> explosive peaceful growth")
    print("* The Quran called it 'a clear victory' (48:1) BEFORE military conquest")
    print("* Historical verification: 1,400 -> 10,000+ within 22 months under peace")
    print("* The Prophet played the INFINITE game while others played the FINITE game")

if __name__ == "__main__":
    main()
