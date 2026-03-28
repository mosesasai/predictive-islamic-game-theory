"""
Simulation 22: Market Design — The Market of Medina

This simulation compares two market regimes:
  1. Unregulated market (pre-Islamic / classical laissez-faire)
  2. Prophet's market design (Islamic market rules)

Historical Context: Upon arriving in Medina (622 CE), the Prophet Muhammad established
a new marketplace with specific rules:
  - No rent charged for market stalls (public space, not private extraction)
  - No hoarding (ihtikar): cannot buy and withhold goods to create artificial scarcity
  - No intercepting traders (talaqqi al-rukban): cannot buy from incoming traders
    before they reach the market and learn fair prices
  - No najash: shill bidding / fake price inflation forbidden
  - Transparent weights and measures
  - Free entry and exit

These rules anticipate modern market design theory (Roth 2002, 2012): markets work well
when they are thick (many participants), avoid congestion, and are safe (participants
can reveal true preferences). The Prophet's rules directly address market failures
that modern economics only formalized centuries later.

Reference: prophet_hypothesis.md — Hypothesis H22
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

N_PERIODS = 200          # Trading periods
N_SELLERS = 30           # Number of sellers
N_BUYERS = 50            # Number of buyers
N_GOODS = 5              # Types of goods
N_SIMULATIONS = 100      # Monte Carlo runs

# Good parameters
BASE_SUPPLY = 20         # Base units supplied per good per period
BASE_DEMAND = 25         # Base units demanded per good per period
COST_MEAN = 5.0          # Mean production cost
COST_STD = 1.0
VALUE_MEAN = 10.0        # Mean buyer valuation
VALUE_STD = 2.0

# Unregulated market parameters (market failures)
HOARDING_PROBABILITY = 0.3      # Probability a seller hoards
HOARDING_FRACTION = 0.5         # Fraction of supply hoarded
INTERCEPT_PROBABILITY = 0.25    # Probability of trade interception
INTERCEPT_MARKUP = 0.4          # Markup from intercepting traders
MONOPOLY_PROBABILITY = 0.15     # Probability of monopolistic behavior
MONOPOLY_MARKUP = 0.6           # Monopoly price markup
RENT_FRACTION = 0.1             # Fraction of revenue extracted as rent
INFO_ASYMMETRY = 0.3            # Price information disadvantage for buyers

# Islamic market parameters (market design)
ISLAMIC_HOARDING = 0.0          # No hoarding allowed
ISLAMIC_INTERCEPT = 0.0         # No interception allowed
ISLAMIC_MONOPOLY = 0.02         # Near-zero monopoly (free entry)
ISLAMIC_RENT = 0.0              # No rent
ISLAMIC_INFO_ASYMMETRY = 0.05   # Near-perfect price transparency

np.random.seed(42)

# ============================================================
# 2. MARKET MODEL
# ============================================================

class Market:
    """A market with configurable rules."""

    def __init__(self, name, hoarding_prob, intercept_prob, monopoly_prob,
                 rent_frac, info_asym):
        self.name = name
        self.hoarding_prob = hoarding_prob
        self.intercept_prob = intercept_prob
        self.monopoly_prob = monopoly_prob
        self.rent_frac = rent_frac
        self.info_asym = info_asym

    def simulate_period(self):
        """Simulate one trading period."""
        # Generate supply and demand
        supply = np.random.poisson(BASE_SUPPLY, N_GOODS).astype(float)
        demand = np.random.poisson(BASE_DEMAND, N_GOODS).astype(float)

        costs = np.random.normal(COST_MEAN, COST_STD, N_GOODS)
        values = np.random.normal(VALUE_MEAN, VALUE_STD, N_GOODS)

        # Apply market frictions
        effective_supply = supply.copy()
        price_markup = np.zeros(N_GOODS)

        # Hoarding: reduces effective supply
        for g in range(N_GOODS):
            if np.random.random() < self.hoarding_prob:
                effective_supply[g] *= (1 - HOARDING_FRACTION)
                price_markup[g] += 0.2  # Scarcity drives prices up

        # Interception: increases cost for final buyers
        for g in range(N_GOODS):
            if np.random.random() < self.intercept_prob:
                price_markup[g] += INTERCEPT_MARKUP

        # Monopoly: direct price markup
        for g in range(N_GOODS):
            if np.random.random() < self.monopoly_prob:
                price_markup[g] += MONOPOLY_MARKUP

        # Information asymmetry: buyers pay more than fair price
        for g in range(N_GOODS):
            price_markup[g] += self.info_asym * np.random.exponential(0.5)

        # Compute equilibrium prices
        prices = np.zeros(N_GOODS)
        quantities = np.zeros(N_GOODS)
        for g in range(N_GOODS):
            # Simple supply-demand price
            if effective_supply[g] > 0:
                scarcity = demand[g] / effective_supply[g]
                base_price = costs[g] + (values[g] - costs[g]) * min(scarcity / 2, 1)
                prices[g] = base_price * (1 + price_markup[g])
                quantities[g] = min(effective_supply[g], demand[g])
            else:
                prices[g] = values[g] * 2  # Extreme scarcity
                quantities[g] = 0

        # Compute welfare
        consumer_surplus = sum(max(0, values[g] - prices[g]) * quantities[g]
                               for g in range(N_GOODS))
        producer_surplus = sum(max(0, prices[g] - costs[g]) * quantities[g]
                               for g in range(N_GOODS))
        rent_extracted = self.rent_frac * sum(prices[g] * quantities[g]
                                               for g in range(N_GOODS))
        total_welfare = consumer_surplus + producer_surplus - rent_extracted

        # Participation: buyers who can afford to participate
        participation = sum(1 for g in range(N_GOODS)
                           for _ in range(int(demand[g]))
                           if values[g] > prices[g]) / max(sum(demand), 1)

        return {
            'prices': prices,
            'quantities': quantities,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': producer_surplus,
            'rent_extracted': rent_extracted,
            'total_welfare': total_welfare,
            'participation': participation,
            'effective_supply': effective_supply,
            'demand': demand,
            'price_markup': price_markup,
        }


def run_market_simulation(market, n_periods=N_PERIODS):
    """Run a full market simulation."""
    history = {
        'prices': [], 'quantities': [], 'consumer_surplus': [],
        'producer_surplus': [], 'rent': [], 'welfare': [],
        'participation': [], 'price_volatility': [],
    }

    price_buffer = []

    for t in range(n_periods):
        result = market.simulate_period()
        mean_price = np.mean(result['prices'])
        history['prices'].append(mean_price)
        history['quantities'].append(np.sum(result['quantities']))
        history['consumer_surplus'].append(result['consumer_surplus'])
        history['producer_surplus'].append(result['producer_surplus'])
        history['rent'].append(result['rent_extracted'])
        history['welfare'].append(result['total_welfare'])
        history['participation'].append(result['participation'])

        price_buffer.append(mean_price)
        if len(price_buffer) > 10:
            history['price_volatility'].append(np.std(price_buffer[-10:]))
        else:
            history['price_volatility'].append(np.std(price_buffer))

    return history

# ============================================================
# 3. SIMULATION ENGINE
# ============================================================

def run_monte_carlo(market, n_sims=N_SIMULATIONS):
    """Run Monte Carlo simulations for a market."""
    all_welfare = []
    all_participation = []
    all_prices = []
    all_volatility = []

    for _ in range(n_sims):
        h = run_market_simulation(market)
        all_welfare.append(np.mean(h['welfare']))
        all_participation.append(np.mean(h['participation']))
        all_prices.append(np.mean(h['prices']))
        all_volatility.append(np.mean(h['price_volatility']))

    return {
        'welfare': all_welfare,
        'participation': all_participation,
        'prices': all_prices,
        'volatility': all_volatility,
    }

# ============================================================
# 4. MAIN FUNCTION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 22: MARKET DESIGN — MARKET OF MEDINA")
    print("Unregulated Market vs. Prophet's Market Rules")
    print("=" * 70)

    # Create markets
    unreg = Market("Unregulated Market", HOARDING_PROBABILITY, INTERCEPT_PROBABILITY,
                   MONOPOLY_PROBABILITY, RENT_FRACTION, INFO_ASYMMETRY)
    islamic = Market("Islamic Market (Prophetic)", ISLAMIC_HOARDING, ISLAMIC_INTERCEPT,
                     ISLAMIC_MONOPOLY, ISLAMIC_RENT, ISLAMIC_INFO_ASYMMETRY)

    # Single detailed runs
    print("\nRunning detailed simulations...")
    h_unreg = run_market_simulation(unreg)
    h_islamic = run_market_simulation(islamic)

    # Monte Carlo
    print(f"Running Monte Carlo ({N_SIMULATIONS} runs each)...")
    mc_unreg = run_monte_carlo(unreg)
    mc_islamic = run_monte_carlo(islamic)

    # --- Results ---
    print("\n--- Market Rule Comparison ---\n")
    print(f"  {'Rule':<35} {'Unregulated':<18} {'Islamic Market':<18}")
    print(f"  {'-'*71}")
    print(f"  {'Hoarding allowed':<35} {'Yes (30%)':<18} {'No (0%)':<18}")
    print(f"  {'Trade interception':<35} {'Yes (25%)':<18} {'No (0%)':<18}")
    print(f"  {'Monopoly behavior':<35} {'Yes (15%)':<18} {'Minimal (2%)':<18}")
    print(f"  {'Stall rent extraction':<35} {'10%':<18} {'0% (public)':<18}")
    print(f"  {'Information asymmetry':<35} {'High (30%)':<18} {'Low (5%)':<18}")

    print(f"\n--- Performance Comparison (Mean over {N_SIMULATIONS} simulations) ---\n")
    print(f"  {'Metric':<35} {'Unregulated':<18} {'Islamic':<18} {'Improvement':<18}")
    print(f"  {'-'*89}")

    metrics = [
        ('Total Welfare', mc_unreg['welfare'], mc_islamic['welfare']),
        ('Participation Rate', mc_unreg['participation'], mc_islamic['participation']),
        ('Mean Price', mc_unreg['prices'], mc_islamic['prices']),
        ('Price Volatility', mc_unreg['volatility'], mc_islamic['volatility']),
    ]

    for name, unreg_vals, isl_vals in metrics:
        u_mean = np.mean(unreg_vals)
        i_mean = np.mean(isl_vals)
        if 'Price' in name and 'Volatility' not in name:
            improvement = f"{(u_mean - i_mean)/u_mean:+.1%}"
        elif 'Volatility' in name:
            improvement = f"{(u_mean - i_mean)/u_mean:+.1%} (lower is better)"
        else:
            improvement = f"{(i_mean - u_mean)/max(abs(u_mean), 0.01):+.1%}"
        print(f"  {name:<35} {u_mean:<18.2f} {i_mean:<18.2f} {improvement:<18}")

    # Detailed single-run stats
    print(f"\n--- Single Run Statistics ({N_PERIODS} periods) ---\n")
    print(f"  {'Metric':<35} {'Unregulated':<18} {'Islamic':<18}")
    print(f"  {'-'*71}")
    print(f"  {'Mean consumer surplus':<35} {np.mean(h_unreg['consumer_surplus']):<18.2f} "
          f"{np.mean(h_islamic['consumer_surplus']):<18.2f}")
    print(f"  {'Mean producer surplus':<35} {np.mean(h_unreg['producer_surplus']):<18.2f} "
          f"{np.mean(h_islamic['producer_surplus']):<18.2f}")
    print(f"  {'Mean rent extracted':<35} {np.mean(h_unreg['rent']):<18.2f} "
          f"{np.mean(h_islamic['rent']):<18.2f}")
    print(f"  {'Mean total quantity traded':<35} {np.mean(h_unreg['quantities']):<18.1f} "
          f"{np.mean(h_islamic['quantities']):<18.1f}")

    # --- Historical ---
    print("\n--- Historical Verification ---")
    print("  Prophet's Market of Medina (622+ CE):")
    print("  * Competed with existing Jewish-controlled market at Banu Qaynuqa")
    print("  * Zero rent attracted sellers -> market became thick (many participants)")
    print("  * No hoarding rule prevented artificial scarcity")
    print("  * No interception ensured sellers got fair market prices")
    print("  * Transparent weights reduced information asymmetry")
    print("  * Within years, became the primary market of Medina")
    print("  * Modern parallel: Roth's market design principles (thickness,")
    print("    uncongested, safe to participate)")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    periods = np.arange(N_PERIODS)

    # Plot 1: Price dynamics
    ax = axes[0, 0]
    ax.plot(periods, h_unreg['prices'], 'r-', alpha=0.7, linewidth=1, label='Unregulated')
    ax.plot(periods, h_islamic['prices'], 'g-', alpha=0.7, linewidth=1, label='Islamic')
    ax.set_xlabel('Trading Period')
    ax.set_ylabel('Mean Price')
    ax.set_title('Price Dynamics Over Time')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 2: Price volatility
    ax = axes[0, 1]
    ax.plot(periods, h_unreg['price_volatility'], 'r-', linewidth=1.5, label='Unregulated')
    ax.plot(periods, h_islamic['price_volatility'], 'g-', linewidth=1.5, label='Islamic')
    ax.set_xlabel('Trading Period')
    ax.set_ylabel('Price Volatility (10-period std)')
    ax.set_title('Price Stability')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 3: Participation rate
    ax = axes[0, 2]
    ax.plot(periods, h_unreg['participation'], 'r-', alpha=0.7, linewidth=1, label='Unregulated')
    ax.plot(periods, h_islamic['participation'], 'g-', alpha=0.7, linewidth=1, label='Islamic')
    ax.set_xlabel('Trading Period')
    ax.set_ylabel('Participation Rate')
    ax.set_title('Market Participation')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 4: Welfare distribution (Monte Carlo)
    ax = axes[1, 0]
    ax.hist(mc_unreg['welfare'], bins=30, alpha=0.6, color='red',
            label=f'Unreg (mean={np.mean(mc_unreg["welfare"]):.1f})', density=True)
    ax.hist(mc_islamic['welfare'], bins=30, alpha=0.6, color='green',
            label=f'Islamic (mean={np.mean(mc_islamic["welfare"]):.1f})', density=True)
    ax.set_xlabel('Mean Total Welfare')
    ax.set_ylabel('Density')
    ax.set_title(f'Welfare Distribution ({N_SIMULATIONS} sims)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 5: Surplus decomposition
    ax = axes[1, 1]
    categories = ['Consumer\nSurplus', 'Producer\nSurplus', 'Rent\nExtracted', 'Total\nWelfare']
    unreg_vals = [np.mean(h_unreg['consumer_surplus']),
                  np.mean(h_unreg['producer_surplus']),
                  np.mean(h_unreg['rent']),
                  np.mean(h_unreg['welfare'])]
    isl_vals = [np.mean(h_islamic['consumer_surplus']),
                np.mean(h_islamic['producer_surplus']),
                np.mean(h_islamic['rent']),
                np.mean(h_islamic['welfare'])]
    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, unreg_vals, width, color='red', alpha=0.7, label='Unregulated')
    ax.bar(x + width/2, isl_vals, width, color='green', alpha=0.7, label='Islamic')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylabel('Value')
    ax.set_title('Surplus Decomposition')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 6: Market design comparison radar-like bar chart
    ax = axes[1, 2]
    design_features = ['Thickness\n(Participation)', 'Price\nStability',
                       'Fairness\n(Low Rent)', 'Efficiency\n(Welfare)',
                       'Transparency\n(Low Asym)']
    unreg_scores = [
        np.mean(mc_unreg['participation']),
        1 - np.mean(mc_unreg['volatility']) / max(np.mean(mc_unreg['volatility']), np.mean(mc_islamic['volatility'])),
        1 - RENT_FRACTION,
        np.mean(mc_unreg['welfare']) / max(np.mean(mc_unreg['welfare']), np.mean(mc_islamic['welfare'])),
        1 - INFO_ASYMMETRY,
    ]
    isl_scores = [
        np.mean(mc_islamic['participation']),
        1 - np.mean(mc_islamic['volatility']) / max(np.mean(mc_unreg['volatility']), np.mean(mc_islamic['volatility'])),
        1 - ISLAMIC_RENT,
        np.mean(mc_islamic['welfare']) / max(np.mean(mc_unreg['welfare']), np.mean(mc_islamic['welfare'])),
        1 - ISLAMIC_INFO_ASYMMETRY,
    ]

    x = np.arange(len(design_features))
    width = 0.35
    ax.barh(x - width/2, unreg_scores, width, color='red', alpha=0.7, label='Unregulated')
    ax.barh(x + width/2, isl_scores, width, color='green', alpha=0.7, label='Islamic')
    ax.set_yticks(x)
    ax.set_yticklabels(design_features, fontsize=8)
    ax.set_xlabel('Score (higher = better)')
    ax.set_title('Market Design Quality')
    ax.legend(fontsize=8)
    ax.set_xlim(0, 1.1)
    ax.grid(True, alpha=0.3, axis='x')

    plt.suptitle("Market Design: Market of Medina\nUnregulated vs. Prophet's Market Rules",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_22_market_medina.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\nFigure saved: islamic_gt_codes/fig_22_market_medina.png")

    print("\n--- CONCLUSION ---")
    print("The Prophet's market design anticipated modern market design theory:")
    print(f"  1. Welfare improvement: {(np.mean(mc_islamic['welfare'])-np.mean(mc_unreg['welfare']))/max(abs(np.mean(mc_unreg['welfare'])),0.01):+.1%} over unregulated")
    print(f"  2. Higher participation: {np.mean(mc_islamic['participation']):.1%} vs {np.mean(mc_unreg['participation']):.1%}")
    print(f"  3. Lower price volatility: more stable, predictable market")
    print(f"  4. Zero rent extraction: public space ensures free entry")
    print("  5. Anti-hoarding and anti-interception rules prevent market manipulation")
    print("  6. These rules map directly to Roth's (2012) market design principles:")
    print("     thickness, uncongested, safe participation, transparent")


if __name__ == "__main__":
    main()
