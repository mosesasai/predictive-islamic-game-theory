"""
Simulation 19: Screening Game — Abyssinian Migration (615 CE)

In screening games, the uninformed party designs a mechanism that induces the informed
party to reveal their type through self-selection. This is the reverse of signaling:
the RECEIVER designs the test, not the sender.

Historical Context: When the Prophet sent the first Muslim emigrants to Abyssinia (615 CE),
he selected:
  1. Ja'far ibn Abi Talib as spokesperson (eloquent, dignified, cousin of the Prophet)
  2. Surah Maryam (Chapter 19) as the content to present — a chapter about Jesus and
     Mary that would resonate with a Christian king

The Quraysh counter-delegation (led by Amr ibn al-As) brought expensive gifts and tried
to frame Muslims as heretics who insult Jesus — a pooling strategy that treats all rulers
as bribable.

The Prophet's strategy was a SCREENING mechanism: the content of Surah Maryam would
separate a just ruler (Negus's true type) from a corrupt one. A just ruler would
recognize theological affinity; a corrupt ruler would take the gifts.

Reference: prophet_hypothesis.md — Hypothesis H19
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

N_SIMULATIONS = 5000     # Monte Carlo runs
N_RULER_TYPES = 2        # Just ruler, Corrupt ruler

# Prior probability of ruler types
P_JUST = 0.3            # Prior: 30% of rulers are genuinely just
P_CORRUPT = 0.7         # Prior: 70% are primarily self-interested

# Ruler utility functions
# Just ruler: values theological truth, justice, reputation, somewhat values gifts
JUST_WEIGHT_TRUTH = 0.6
JUST_WEIGHT_JUSTICE = 0.3
JUST_WEIGHT_GIFTS = 0.1

# Corrupt ruler: values gifts, political expedience, somewhat values reputation
CORRUPT_WEIGHT_TRUTH = 0.05
CORRUPT_WEIGHT_JUSTICE = 0.15
CORRUPT_WEIGHT_GIFTS = 0.8

# Content-based approach (Prophet's Surah Maryam strategy)
CONTENT_TRUTH_SIGNAL = 0.9      # High theological content quality
CONTENT_JUSTICE_APPEAL = 0.85   # Appeals to sense of justice
CONTENT_GIFT_VALUE = 0.0        # No material gifts

# Gift-based approach (Quraysh strategy)
GIFT_TRUTH_SIGNAL = 0.1         # No theological content
GIFT_JUSTICE_APPEAL = 0.1       # Frames opponents as heretics (low justice appeal)
GIFT_GIFT_VALUE = 0.95          # Very expensive gifts

# Decision thresholds
PROTECT_THRESHOLD = 0.5         # Ruler protects if utility > threshold

np.random.seed(42)

# ============================================================
# 2. SCREENING MODEL
# ============================================================

class Ruler:
    """A ruler with a hidden type (just or corrupt)."""

    def __init__(self, ruler_type):
        self.type = ruler_type
        if ruler_type == "just":
            self.w_truth = JUST_WEIGHT_TRUTH + np.random.normal(0, 0.05)
            self.w_justice = JUST_WEIGHT_JUSTICE + np.random.normal(0, 0.05)
            self.w_gifts = JUST_WEIGHT_GIFTS + np.random.normal(0, 0.02)
        else:
            self.w_truth = CORRUPT_WEIGHT_TRUTH + np.random.normal(0, 0.03)
            self.w_justice = CORRUPT_WEIGHT_JUSTICE + np.random.normal(0, 0.05)
            self.w_gifts = CORRUPT_WEIGHT_GIFTS + np.random.normal(0, 0.05)

        # Normalize weights
        total = abs(self.w_truth) + abs(self.w_justice) + abs(self.w_gifts)
        self.w_truth = max(0, self.w_truth) / total
        self.w_justice = max(0, self.w_justice) / total
        self.w_gifts = max(0, self.w_gifts) / total

    def evaluate(self, truth_signal, justice_appeal, gift_value):
        """Evaluate a delegation's approach."""
        utility = (self.w_truth * truth_signal +
                   self.w_justice * justice_appeal +
                   self.w_gifts * gift_value)
        # Add noise for uncertainty
        utility += np.random.normal(0, 0.05)
        return utility

    def decide(self, utility_content, utility_gifts):
        """Decide whether to protect Muslims or extradite them."""
        # Ruler compares the two approaches and decides
        if utility_content > utility_gifts:
            return "protect"
        else:
            return "extradite"


def run_screening_game(ruler, approach="content"):
    """Run a single screening interaction."""
    if approach == "content":
        u = ruler.evaluate(CONTENT_TRUTH_SIGNAL, CONTENT_JUSTICE_APPEAL, CONTENT_GIFT_VALUE)
    else:
        u = ruler.evaluate(GIFT_TRUTH_SIGNAL, GIFT_JUSTICE_APPEAL, GIFT_GIFT_VALUE)
    return u

# ============================================================
# 3. SIMULATION ENGINE
# ============================================================

def run_monte_carlo():
    """Run Monte Carlo simulation of the screening game."""
    results = {
        'just_content_utility': [], 'just_gift_utility': [],
        'corrupt_content_utility': [], 'corrupt_gift_utility': [],
        'just_protect_content': 0, 'just_protect_gift': 0,
        'corrupt_protect_content': 0, 'corrupt_protect_gift': 0,
        'n_just': 0, 'n_corrupt': 0,
        'content_separates': 0, 'gift_separates': 0,
    }

    for _ in range(N_SIMULATIONS):
        # Draw ruler type
        is_just = np.random.random() < P_JUST
        ruler_type = "just" if is_just else "corrupt"
        ruler = Ruler(ruler_type)

        # Both delegations present
        u_content = run_screening_game(ruler, "content")
        u_gift = run_screening_game(ruler, "gift")

        decision = ruler.decide(u_content, u_gift)

        if ruler_type == "just":
            results['n_just'] += 1
            results['just_content_utility'].append(u_content)
            results['just_gift_utility'].append(u_gift)
            if decision == "protect":
                results['just_protect_content'] += 1
        else:
            results['n_corrupt'] += 1
            results['corrupt_content_utility'].append(u_content)
            results['corrupt_gift_utility'].append(u_gift)
            if decision == "protect":
                results['corrupt_protect_content'] += 1

        # Check separation: content approach separates if just rulers protect
        # and corrupt rulers don't (or vice versa for gift approach)
        if is_just and decision == "protect":
            results['content_separates'] += 1
        elif not is_just and decision == "extradite":
            results['content_separates'] += 1

    return results


def analyze_screening_power(results):
    """Analyze the screening (type-separation) power of each approach."""
    n_just = max(results['n_just'], 1)
    n_corrupt = max(results['n_corrupt'], 1)

    # Content approach: just rulers prefer content, corrupt prefer gifts
    just_prefers_content = sum(1 for uc, ug in zip(results['just_content_utility'],
                                                     results['just_gift_utility'])
                               if uc > ug)
    corrupt_prefers_gifts = sum(1 for uc, ug in zip(results['corrupt_content_utility'],
                                                      results['corrupt_gift_utility'])
                                if ug > uc)

    content_separation = (just_prefers_content / n_just + corrupt_prefers_gifts / n_corrupt) / 2
    gift_separation = 1 - content_separation  # Gift approach pools — no separation

    return {
        'just_prefers_content_rate': just_prefers_content / n_just,
        'corrupt_prefers_gifts_rate': corrupt_prefers_gifts / n_corrupt,
        'content_separation_power': content_separation,
        'gift_pooling_weakness': gift_separation,
        'just_protect_rate': results['just_protect_content'] / n_just,
        'corrupt_extradite_rate': 1 - (results['corrupt_protect_content'] / n_corrupt) if n_corrupt > 0 else 0,
    }

# ============================================================
# 4. MAIN FUNCTION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 19: SCREENING GAME — ABYSSINIAN MIGRATION (615 CE)")
    print("Content-Based Screening vs. Gift-Based Pooling")
    print("=" * 70)

    print(f"\nRunning Monte Carlo simulation ({N_SIMULATIONS} rulers)...")
    results = run_monte_carlo()
    analysis = analyze_screening_power(results)

    # --- Results ---
    print("\n--- Screening Game Results ---\n")
    print(f"  {'Metric':<45} {'Value':<15}")
    print(f"  {'-'*60}")
    print(f"  {'Rulers simulated':<45} {N_SIMULATIONS:<15}")
    print(f"  {'Just rulers drawn':<45} {results['n_just']:<15} ({results['n_just']/N_SIMULATIONS:.1%})")
    print(f"  {'Corrupt rulers drawn':<45} {results['n_corrupt']:<15} ({results['n_corrupt']/N_SIMULATIONS:.1%})")

    print(f"\n--- Type Separation Analysis ---\n")
    print(f"  {'Just rulers prefer content (Surah Maryam)':<45} {analysis['just_prefers_content_rate']:.1%}")
    print(f"  {'Corrupt rulers prefer gifts (Quraysh)':<45} {analysis['corrupt_prefers_gifts_rate']:.1%}")
    print(f"  {'Content approach separation power':<45} {analysis['content_separation_power']:.1%}")
    print(f"  {'Gift approach (pooling failure)':<45} {analysis['gift_pooling_weakness']:.1%}")

    print(f"\n--- Decision Outcomes ---\n")
    print(f"  {'Just rulers protect Muslims (content wins)':<45} {analysis['just_protect_rate']:.1%}")
    print(f"  {'Corrupt rulers extradite (gifts win)':<45} {analysis['corrupt_extradite_rate']:.1%}")
    print(f"  {'Overall correct screening rate':<45} "
          f"{results['content_separates']/N_SIMULATIONS:.1%}")

    print(f"\n--- Strategy Comparison ---\n")
    print(f"  {'Approach':<25} {'Mechanism':<15} {'Separates Types?':<20} {'Outcome for Muslims':<20}")
    print(f"  {'-'*80}")
    print(f"  {'Surah Maryam (Prophet)':<25} {'Screening':<15} {'YES (strong)':<20} {'Protected by just ruler':<20}")
    print(f"  {'Gifts (Quraysh)':<25} {'Pooling':<15} {'NO (weak)':<20} {'Only works if corrupt':<20}")

    # --- Historical Verification ---
    print("\n--- Historical Verification ---")
    print("  Actual outcome in Abyssinia (615 CE):")
    print("  * Negus (Najashi) wept upon hearing Surah Maryam recited by Ja'far")
    print("  * Said: 'This and what Jesus brought come from the same source'")
    print("  * Refused Quraysh gifts and protected the Muslims")
    print("  * Later secretly accepted Islam — confirming his 'just ruler' type")
    print("  * Quraysh delegation returned empty-handed despite expensive gifts")
    print("  * The content SCREENED Negus's type perfectly")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Utility distributions for just rulers
    ax = axes[0, 0]
    ax.hist(results['just_content_utility'], bins=40, alpha=0.6, color='green',
            label='Content (Surah Maryam)', density=True)
    ax.hist(results['just_gift_utility'], bins=40, alpha=0.6, color='red',
            label='Gifts (Quraysh)', density=True)
    ax.set_xlabel('Utility')
    ax.set_ylabel('Density')
    ax.set_title('Just Ruler Utility: Content vs Gifts')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 2: Utility distributions for corrupt rulers
    ax = axes[0, 1]
    ax.hist(results['corrupt_content_utility'], bins=40, alpha=0.6, color='green',
            label='Content (Surah Maryam)', density=True)
    ax.hist(results['corrupt_gift_utility'], bins=40, alpha=0.6, color='red',
            label='Gifts (Quraysh)', density=True)
    ax.set_xlabel('Utility')
    ax.set_ylabel('Density')
    ax.set_title('Corrupt Ruler Utility: Content vs Gifts')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 3: Separation power comparison
    ax = axes[0, 2]
    approaches = ['Content\n(Prophet)', 'Gifts\n(Quraysh)']
    sep_power = [analysis['content_separation_power'], analysis['gift_pooling_weakness']]
    colors = ['green', 'red']
    bars = ax.bar(approaches, sep_power, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Separation Power')
    ax.set_title('Type Separation Power')
    ax.set_ylim(0, 1)
    for bar, val in zip(bars, sep_power):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.1%}', ha='center', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 4: 2D scatter of content vs gift utility by type
    ax = axes[1, 0]
    ax.scatter(results['just_content_utility'], results['just_gift_utility'],
               alpha=0.2, color='blue', s=8, label='Just Rulers')
    ax.scatter(results['corrupt_content_utility'], results['corrupt_gift_utility'],
               alpha=0.2, color='red', s=8, label='Corrupt Rulers')
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Indifference line')
    ax.set_xlabel('Content Utility (Surah Maryam)')
    ax.set_ylabel('Gift Utility (Quraysh)')
    ax.set_title('Ruler Type Separation in Utility Space')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 5: Outcome probabilities by ruler type
    ax = axes[1, 1]
    categories = ['Just\nProtects', 'Just\nExtradites', 'Corrupt\nProtects', 'Corrupt\nExtradites']
    n_j = max(results['n_just'], 1)
    n_c = max(results['n_corrupt'], 1)
    probs = [
        results['just_protect_content'] / n_j,
        1 - results['just_protect_content'] / n_j,
        results['corrupt_protect_content'] / n_c,
        1 - results['corrupt_protect_content'] / n_c,
    ]
    bar_colors = ['green', 'lightcoral', 'lightgreen', 'red']
    bars = ax.bar(categories, probs, color=bar_colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('Probability')
    ax.set_title('Decision Outcomes by Ruler Type')
    for bar, val in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.0%}', ha='center', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 6: Screening mechanism diagram
    ax = axes[1, 2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Draw mechanism flow
    ax.text(5, 9.2, 'SCREENING MECHANISM', ha='center', fontsize=12, fontweight='bold')

    # Content path
    ax.annotate('', xy=(3, 7.5), xytext=(5, 8.5),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(2, 7.2, 'Surah Maryam\n(Content)', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # Gift path
    ax.annotate('', xy=(7, 7.5), xytext=(5, 8.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(8, 7.2, 'Expensive\nGifts', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Ruler types
    ax.text(5, 8.5, 'Unknown\nRuler Type', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Just ruler outcome
    ax.text(2, 5.0, 'Just Ruler\nChooses Content', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
    ax.annotate('', xy=(2, 5.5), xytext=(2, 6.5),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax.text(2, 3.5, 'PROTECTS\nMuslims', ha='center', fontsize=10, fontweight='bold', color='green')

    # Corrupt ruler outcome
    ax.text(8, 5.0, 'Corrupt Ruler\nChooses Gifts', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
    ax.annotate('', xy=(8, 5.5), xytext=(8, 6.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax.text(8, 3.5, 'EXTRADITES\nMuslims', ha='center', fontsize=10, fontweight='bold', color='red')

    ax.text(5, 1.5, 'Content screening SEPARATES types\nGift pooling does NOT',
            ha='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax.set_title('Screening Mechanism Flow')
    ax.axis('off')

    plt.suptitle("Screening Game: Abyssinian Migration (615 CE)\nContent-Based Screening vs Gift-Based Pooling",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_19_abyssinia_screening.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\nFigure saved: islamic_gt_codes/fig_19_abyssinia_screening.png")

    print("\n--- CONCLUSION ---")
    print("The Prophet's Abyssinian migration strategy was a sophisticated screening mechanism:")
    print("  1. Surah Maryam CONTENT separated just rulers from corrupt ones")
    print("  2. Quraysh GIFTS created a pooling equilibrium — only works on corrupt rulers")
    print(f"  3. Content separation power: {analysis['content_separation_power']:.1%}")
    print(f"  4. Just rulers chose content over gifts: {analysis['just_prefers_content_rate']:.1%}")
    print("  5. The Prophet correctly predicted Negus was type 'just' and designed")
    print("     the screening mechanism accordingly — a masterclass in mechanism design")
    print("  6. Key insight: WHAT you present reveals WHO they are")


if __name__ == "__main__":
    main()
