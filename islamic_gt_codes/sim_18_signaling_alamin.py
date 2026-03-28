"""
Simulation 18: Signaling Game — 40 Years of Al-Amin Reputation as Costly Separating Signal

In signaling games (Spence 1973), a sender with private information takes a costly action
to credibly communicate their type. A separating equilibrium exists when the signal cost
differs enough between types that only the genuine type can afford to send it.

Historical Context: Before his prophethood, Muhammad was known as "Al-Amin" (The
Trustworthy) and "Al-Sadiq" (The Truthful) for 40 years (570-610 CE). He never lied,
never cheated in trade, returned the Kaaba deposits even after declaring prophethood,
and maintained impeccable character in a society that closely observed personal conduct.

Game-Theoretic Model: Two types of potential prophets:
  - Type P (genuine prophet): naturally honest, cost of consistent honesty = low
  - Type S (strategic deceiver / power-seeker): must SUPPRESS natural opportunism,
    cost of consistent honesty = very high (and increasing over time)

After 40 years of perfect honesty, the signal becomes overwhelmingly credible because
no strategic deceiver would invest 40 years of costly signaling for a future payoff
that was unknowable in advance.

Reference: prophet_hypothesis.md — Hypothesis H18
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

N_YEARS = 50             # Simulation horizon (40 pre-prophethood + 10 post)
PROPHETHOOD_YEAR = 40    # Year of claim
N_SIMULATIONS = 1000     # Monte Carlo runs for population model

# Type P (genuine prophet): honesty is natural, low cost
TYPE_P_ANNUAL_COST = 0.5        # Low cost per year of honest behavior
TYPE_P_COST_GROWTH = 0.0        # No growth — honesty is intrinsic

# Type S (strategic deceiver): honesty is costly performance
TYPE_S_ANNUAL_COST = 2.0        # High base cost of suppressing opportunism
TYPE_S_COST_GROWTH = 0.08       # Cost grows — harder to maintain facade over time
TYPE_S_DISCOUNT_RATE = 0.05     # Deceiver discounts future (impatient)

# Credibility function parameters
CREDIBILITY_BASE = 0.1          # Starting credibility at year 0
CREDIBILITY_RATE = 0.06         # Annual credibility growth from consistent signal
CREDIBILITY_BONUS_POST_CLAIM = 0.15  # Jump when claim is consistent with track record

# Population belief parameters
PRIOR_PROPHET_PROB = 0.01       # Prior: very unlikely someone is genuine prophet
SIGNAL_LIKELIHOOD_RATIO = 1.15  # Each year of honesty updates beliefs

# Payoffs for deception (if deceiver succeeds)
DECEPTION_PAYOFF = 100.0        # One-time payoff if believed
# But deceiver doesn't know WHEN to claim, so expected payoff is discounted

np.random.seed(42)

# ============================================================
# 2. SIGNALING COST MODEL
# ============================================================

def type_p_cumulative_cost(years):
    """Cumulative cost for genuine prophet type."""
    return TYPE_P_ANNUAL_COST * years


def type_s_cumulative_cost(years):
    """Cumulative cost for strategic deceiver type."""
    costs = 0
    for y in range(int(years)):
        annual = TYPE_S_ANNUAL_COST * (1 + TYPE_S_COST_GROWTH) ** y
        costs += annual
    return costs


def type_s_expected_payoff(years_invested, remaining_horizon=10):
    """Expected payoff for deceiver: payoff discounted by years invested."""
    # Deceiver didn't know at age 20 that he'd claim at age 40
    # So at each year, expected payoff of continuing = small probability of future gain
    future_payoff = DECEPTION_PAYOFF * (1 / (1 + TYPE_S_DISCOUNT_RATE)) ** remaining_horizon
    return future_payoff - type_s_cumulative_cost(years_invested)


def credibility_function(years_of_signal, post_claim=False):
    """Credibility as function of signal duration."""
    cred = CREDIBILITY_BASE + CREDIBILITY_RATE * years_of_signal
    if post_claim and years_of_signal >= PROPHETHOOD_YEAR:
        cred += CREDIBILITY_BONUS_POST_CLAIM
    # Logistic saturation
    cred = 1.0 / (1.0 + np.exp(-5 * (cred - 0.5)))
    return min(cred, 0.99)


def bayesian_belief_update(years_of_signal):
    """Update population belief using Bayes' rule after observing years of honesty."""
    prior = PRIOR_PROPHET_PROB
    # Likelihood ratio accumulates multiplicatively
    lr = SIGNAL_LIKELIHOOD_RATIO ** years_of_signal
    posterior = (prior * lr) / (prior * lr + (1 - prior) * 1.0)
    return posterior

# ============================================================
# 3. SIMULATION ENGINE
# ============================================================

def simulate_signal_dynamics():
    """Simulate cost, credibility, and belief dynamics over time."""
    years = np.arange(N_YEARS + 1)

    # Costs
    p_costs = [type_p_cumulative_cost(y) for y in years]
    s_costs = [type_s_cumulative_cost(y) for y in years]

    # Annual marginal costs
    p_marginal = [TYPE_P_ANNUAL_COST] * len(years)
    s_marginal = [TYPE_S_ANNUAL_COST * (1 + TYPE_S_COST_GROWTH) ** y for y in years]

    # Credibility
    credibility = [credibility_function(y, post_claim=(y >= PROPHETHOOD_YEAR)) for y in years]

    # Bayesian belief
    beliefs = [bayesian_belief_update(y) for y in years]

    # Deceiver's net expected payoff at each year (if he claims NOW)
    s_net_payoff = [type_s_expected_payoff(y) for y in years]

    # Separation measure: cost gap between types
    cost_gap = [s - p for s, p in zip(s_costs, p_costs)]

    return {
        'years': years,
        'p_costs': p_costs,
        's_costs': s_costs,
        'p_marginal': p_marginal,
        's_marginal': s_marginal,
        'credibility': credibility,
        'beliefs': beliefs,
        's_net_payoff': s_net_payoff,
        'cost_gap': cost_gap,
    }


def simulate_deceiver_population(n_sims=N_SIMULATIONS):
    """Simulate a population of potential deceivers to find when they quit."""
    quit_years = []

    for _ in range(n_sims):
        # Each deceiver has slightly different cost parameters
        base_cost = np.random.uniform(1.5, 3.0)
        growth = np.random.uniform(0.05, 0.12)
        discount = np.random.uniform(0.03, 0.10)
        patience = np.random.uniform(5, 20)  # Max years willing to invest

        cumulative_cost = 0
        quit_year = N_YEARS  # Default: never quits (but shouldn't happen)

        for y in range(N_YEARS):
            annual = base_cost * (1 + growth) ** y
            cumulative_cost += annual

            # Deceiver quits when cumulative cost exceeds expected payoff
            expected = DECEPTION_PAYOFF / (1 + discount) ** max(0, PROPHETHOOD_YEAR - y)
            if cumulative_cost > expected or y > patience:
                quit_year = y
                break

        quit_years.append(quit_year)

    return quit_years

# ============================================================
# 4. MAIN FUNCTION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 18: SIGNALING GAME — 40 YEARS OF AL-AMIN REPUTATION")
    print("Costly Separating Signal Analysis")
    print("=" * 70)

    print("\nRunning signal dynamics simulation...")
    dynamics = simulate_signal_dynamics()

    print("Running deceiver population simulation ({} agents)...".format(N_SIMULATIONS))
    quit_years = simulate_deceiver_population()

    # --- Results ---
    print("\n--- Signal Cost Comparison ---\n")
    print(f"  {'Year':<8} {'Type P Cost':<15} {'Type S Cost':<15} {'Cost Gap':<15} "
          f"{'Credibility':<15} {'Belief P(prophet)':<18}")
    print(f"  {'-'*85}")

    checkpoints = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    for y in checkpoints:
        if y <= N_YEARS:
            marker = " <-- CLAIM" if y == 40 else ""
            print(f"  {y:<8} {dynamics['p_costs'][y]:<15.1f} {dynamics['s_costs'][y]:<15.1f} "
                  f"{dynamics['cost_gap'][y]:<15.1f} {dynamics['credibility'][y]:<15.3f} "
                  f"{dynamics['beliefs'][y]:<18.6f}{marker}")

    print(f"\n--- Deceiver Dropout Analysis ({N_SIMULATIONS} simulated deceivers) ---\n")
    quit_arr = np.array(quit_years)
    print(f"  Mean dropout year:    {np.mean(quit_arr):.1f}")
    print(f"  Median dropout year:  {np.median(quit_arr):.1f}")
    print(f"  Max dropout year:     {np.max(quit_arr)}")
    print(f"  % who quit by year 10: {np.mean(quit_arr <= 10):.1%}")
    print(f"  % who quit by year 20: {np.mean(quit_arr <= 20):.1%}")
    print(f"  % who quit by year 30: {np.mean(quit_arr <= 30):.1%}")
    print(f"  % who survive to 40:   {np.mean(quit_arr >= 40):.1%}")

    print("\n--- Separation Theorem ---")
    print(f"  At year 40 (prophethood claim):")
    print(f"    Type P cumulative cost:  {dynamics['p_costs'][40]:.1f}")
    print(f"    Type S cumulative cost:  {dynamics['s_costs'][40]:.1f}")
    print(f"    Cost ratio (S/P):        {dynamics['s_costs'][40] / dynamics['p_costs'][40]:.1f}x")
    print(f"    Credibility:             {dynamics['credibility'][40]:.3f}")
    print(f"    Bayesian belief:         {dynamics['beliefs'][40]:.6f}")
    print(f"    Deceivers surviving:     {np.mean(quit_arr >= 40):.1%}")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Cumulative costs
    ax = axes[0, 0]
    ax.plot(dynamics['years'], dynamics['p_costs'], 'g-', linewidth=2.5, label='Type P (Genuine Prophet)')
    ax.plot(dynamics['years'], dynamics['s_costs'], 'r-', linewidth=2.5, label='Type S (Strategic Deceiver)')
    ax.axvline(x=40, color='gold', linewidth=2, linestyle='--', label='Prophethood Claim')
    ax.fill_between(dynamics['years'], dynamics['p_costs'], dynamics['s_costs'],
                     alpha=0.15, color='orange', label='Cost Gap')
    ax.set_xlabel('Years of Consistent Honesty')
    ax.set_ylabel('Cumulative Signal Cost')
    ax.set_title('Cumulative Cost of Honesty Signal')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Plot 2: Marginal costs
    ax = axes[0, 1]
    ax.plot(dynamics['years'], dynamics['p_marginal'], 'g-', linewidth=2.5, label='Type P (constant)')
    ax.plot(dynamics['years'], dynamics['s_marginal'], 'r-', linewidth=2.5, label='Type S (growing)')
    ax.axvline(x=40, color='gold', linewidth=2, linestyle='--', label='Prophethood Claim')
    ax.set_xlabel('Year')
    ax.set_ylabel('Annual Marginal Cost')
    ax.set_title('Annual Cost of Maintaining Signal')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Plot 3: Credibility over time
    ax = axes[0, 2]
    ax.plot(dynamics['years'], dynamics['credibility'], 'b-', linewidth=2.5)
    ax.axvline(x=40, color='gold', linewidth=2, linestyle='--', label='Prophethood Claim')
    ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, label='50% credibility')
    ax.set_xlabel('Years of Signal')
    ax.set_ylabel('Credibility')
    ax.set_title('Credibility vs. Signal Duration')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Plot 4: Deceiver dropout histogram
    ax = axes[1, 0]
    ax.hist(quit_years, bins=40, color='red', alpha=0.7, edgecolor='darkred')
    ax.axvline(x=40, color='gold', linewidth=2, linestyle='--', label='Year 40 (Claim)')
    ax.set_xlabel('Year of Dropout')
    ax.set_ylabel('Number of Deceivers')
    ax.set_title(f'Deceiver Dropout Distribution (n={N_SIMULATIONS})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 5: Deceiver net payoff
    ax = axes[1, 1]
    ax.plot(dynamics['years'], dynamics['s_net_payoff'], 'r-', linewidth=2.5)
    ax.axhline(y=0, color='black', linewidth=1, linestyle='-')
    ax.axvline(x=40, color='gold', linewidth=2, linestyle='--', label='Prophethood Claim')
    ax.fill_between(dynamics['years'], dynamics['s_net_payoff'], 0,
                     where=[p < 0 for p in dynamics['s_net_payoff']],
                     alpha=0.2, color='red', label='Net loss region')
    ax.set_xlabel('Years Invested')
    ax.set_ylabel('Deceiver Net Expected Payoff')
    ax.set_title('Deceiver Profitability Over Time')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Plot 6: Bayesian belief evolution
    ax = axes[1, 2]
    ax.plot(dynamics['years'], dynamics['beliefs'], 'b-', linewidth=2.5)
    ax.axvline(x=40, color='gold', linewidth=2, linestyle='--', label='Prophethood Claim')
    ax.set_xlabel('Years of Observed Honesty')
    ax.set_ylabel('P(Genuine Prophet | Signal)')
    ax.set_title('Bayesian Belief Update')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

    plt.suptitle("Signaling Game: 40 Years of Al-Amin Reputation\nCostly Separating Signal Analysis",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_18_signaling_alamin.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\nFigure saved: islamic_gt_codes/fig_18_signaling_alamin.png")

    print("\n--- CONCLUSION ---")
    print("The 40-year Al-Amin signal creates a perfect separating equilibrium:")
    print("  1. Type P (genuine) cost grows linearly — sustainable indefinitely")
    print("  2. Type S (deceiver) cost grows exponentially — unsustainable past ~10-15 years")
    print(f"  3. By year 40, {np.mean(quit_arr >= 40):.1%} of simulated deceivers survive")
    print("  4. The signal is UNFORGEABLE: no rational deceiver invests 40 years in a")
    print("     deception whose payoff date is unknown and whose cost grows exponentially")
    print("  5. This explains why even Quraysh, who rejected the message, never questioned")
    print("     Muhammad's personal honesty — the signal was too costly to fake")
    print("  6. Classical signaling theory (Spence) predicts exactly this separation")


if __name__ == "__main__":
    main()
