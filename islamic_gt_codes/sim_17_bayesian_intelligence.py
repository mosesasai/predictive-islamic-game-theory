"""
Simulation 17: Bayesian Intelligence — Dar al-Arqam Network

This simulation models information asymmetry between the Prophet Muhammad's intelligence
network and Quraysh surveillance during the early Meccan period (613-622 CE).

Historical Context: The Prophet operated from Dar al-Arqam (the House of Arqam), using
an unconventional intelligence network composed of individuals Quraysh systematically
overlooked: women (Umm Salama, Ruqayyah), freed slaves (Bilal, Ammar), youth (Ali ibn
Abi Talib, age 10), and lower-class individuals. This violated Quraysh's implicit
assumption that strategic actors must be tribal elites.

Game-Theoretic Model: Both sides are Bayesian updaters about the other's intentions,
capabilities, and plans. The key asymmetry:
  - Prophet's network: diverse, unconventional sources -> low-variance posterior beliefs
  - Quraysh network: elite-focused, conventional -> high-variance, systematically biased

When both sides make strategic decisions based on their beliefs, the side with lower
posterior variance consistently achieves superior outcomes — even if their prior
information is initially worse.

Reference: prophet_hypothesis.md — Hypothesis H17
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

N_PERIODS = 120          # Months (roughly 10 years of Meccan period)
N_SIMULATIONS = 500      # Monte Carlo runs
N_DECISIONS = 50         # Strategic decisions over the period

# True state: hidden variable representing actual conditions (movements, plans, etc.)
# Modeled as a random walk
STATE_VOLATILITY = 0.3

# Prophet's intelligence network (Dar al-Arqam)
PROPHET_N_SOURCES = 8             # Number of independent sources
PROPHET_SOURCE_NOISE = [0.4, 0.5, 0.3, 0.6, 0.35, 0.45, 0.55, 0.5]  # Varied quality
PROPHET_SOURCE_BIAS = [0.0, 0.05, -0.02, 0.03, 0.0, -0.01, 0.02, 0.01]  # Low bias
PROPHET_PRIOR_PRECISION = 0.5     # Initial prior precision

# Quraysh surveillance network
QURAYSH_N_SOURCES = 5             # Fewer effective sources (elite-only)
QURAYSH_SOURCE_NOISE = [0.3, 0.4, 0.7, 0.8, 0.9]  # Top sources good, rest poor
QURAYSH_SOURCE_BIAS = [0.15, 0.2, 0.25, 0.3, 0.1]  # Systematic bias (confirmation)
QURAYSH_PRIOR_PRECISION = 0.8     # Overconfident prior

# Strategic decision payoffs
CORRECT_DECISION_PAYOFF = 10.0
WRONG_DECISION_COST = -8.0

np.random.seed(42)

# ============================================================
# 2. BAYESIAN INTELLIGENCE MODEL
# ============================================================

class IntelligenceNetwork:
    """A Bayesian intelligence network that updates beliefs from multiple sources."""

    def __init__(self, name, n_sources, source_noise, source_bias, prior_precision):
        self.name = name
        self.n_sources = n_sources
        self.source_noise = source_noise
        self.source_bias = source_bias
        self.prior_mean = 0.0
        self.prior_precision = prior_precision
        self.belief_history = []
        self.variance_history = []

    def observe_and_update(self, true_state):
        """Receive signals from sources and perform Bayesian update."""
        # Each source provides a noisy, possibly biased signal
        signals = []
        precisions = []

        for i in range(self.n_sources):
            noise = self.source_noise[i]
            bias = self.source_bias[i]
            signal = true_state + bias + np.random.normal(0, noise)
            signals.append(signal)
            precisions.append(1.0 / (noise ** 2))

        # Bayesian update with Gaussian conjugate prior
        total_precision = self.prior_precision + sum(precisions)
        posterior_mean = (self.prior_precision * self.prior_mean +
                          sum(p * s for p, s in zip(precisions, signals))) / total_precision
        posterior_variance = 1.0 / total_precision

        # Update prior for next period
        self.prior_mean = posterior_mean
        self.prior_precision = min(total_precision * 0.7, 20.0)  # Decay + cap

        self.belief_history.append(posterior_mean)
        self.variance_history.append(posterior_variance)

        return posterior_mean, posterior_variance

    def make_decision(self, true_state, threshold=0.0):
        """Make a binary strategic decision based on beliefs."""
        belief, variance = self.observe_and_update(true_state)
        # Decision: act if belief > threshold
        # Better intelligence -> belief closer to true state -> better decisions
        decision = 1 if belief > threshold else 0
        correct = 1 if (true_state > threshold) == (decision == 1) else 0
        return decision, correct, abs(belief - true_state), variance


def generate_true_states(n_periods):
    """Generate hidden true states as random walk with drift."""
    states = [0.0]
    for _ in range(n_periods - 1):
        states.append(states[-1] + np.random.normal(0, STATE_VOLATILITY))
    return np.array(states)

# ============================================================
# 3. SIMULATION ENGINE
# ============================================================

def run_single_simulation():
    """Run one simulation comparing both networks."""
    true_states = generate_true_states(N_DECISIONS)

    prophet_net = IntelligenceNetwork(
        "Prophet (Dar al-Arqam)", PROPHET_N_SOURCES,
        PROPHET_SOURCE_NOISE, PROPHET_SOURCE_BIAS, PROPHET_PRIOR_PRECISION
    )
    quraysh_net = IntelligenceNetwork(
        "Quraysh Surveillance", QURAYSH_N_SOURCES,
        QURAYSH_SOURCE_NOISE, QURAYSH_SOURCE_BIAS, QURAYSH_PRIOR_PRECISION
    )

    prophet_correct = 0
    quraysh_correct = 0
    prophet_errors = []
    quraysh_errors = []
    prophet_vars = []
    quraysh_vars = []

    for t in range(N_DECISIONS):
        _, pc, pe, pv = prophet_net.make_decision(true_states[t])
        _, qc, qe, qv = quraysh_net.make_decision(true_states[t])
        prophet_correct += pc
        quraysh_correct += qc
        prophet_errors.append(pe)
        quraysh_errors.append(qe)
        prophet_vars.append(pv)
        quraysh_vars.append(qv)

    return {
        'prophet_accuracy': prophet_correct / N_DECISIONS,
        'quraysh_accuracy': quraysh_correct / N_DECISIONS,
        'prophet_mean_error': np.mean(prophet_errors),
        'quraysh_mean_error': np.mean(quraysh_errors),
        'prophet_mean_var': np.mean(prophet_vars),
        'quraysh_mean_var': np.mean(quraysh_vars),
        'prophet_errors': prophet_errors,
        'quraysh_errors': quraysh_errors,
        'prophet_vars': prophet_vars,
        'quraysh_vars': quraysh_vars,
        'prophet_beliefs': prophet_net.belief_history,
        'quraysh_beliefs': quraysh_net.belief_history,
        'true_states': true_states,
    }


def run_monte_carlo():
    """Run Monte Carlo simulations."""
    results = {
        'prophet_accuracies': [],
        'quraysh_accuracies': [],
        'prophet_errors': [],
        'quraysh_errors': [],
        'prophet_vars': [],
        'quraysh_vars': [],
    }

    for _ in range(N_SIMULATIONS):
        r = run_single_simulation()
        results['prophet_accuracies'].append(r['prophet_accuracy'])
        results['quraysh_accuracies'].append(r['quraysh_accuracy'])
        results['prophet_errors'].append(r['prophet_mean_error'])
        results['quraysh_errors'].append(r['quraysh_mean_error'])
        results['prophet_vars'].append(r['prophet_mean_var'])
        results['quraysh_vars'].append(r['quraysh_mean_var'])

    return results

# ============================================================
# 4. MAIN FUNCTION
# ============================================================

def main():
    print("=" * 70)
    print("SIMULATION 17: BAYESIAN INTELLIGENCE — DAR AL-ARQAM NETWORK")
    print("Information Asymmetry and Variance Reduction")
    print("=" * 70)

    print("\nRunning Monte Carlo simulation ({} runs)...".format(N_SIMULATIONS))
    mc_results = run_monte_carlo()

    # Single detailed run for plotting
    print("Running detailed single simulation for visualization...")
    detail = run_single_simulation()

    # --- Results ---
    print("\n--- Intelligence Network Comparison ---\n")
    print(f"  {'Metric':<40} {'Prophet Network':<20} {'Quraysh Network':<20}")
    print(f"  {'-'*80}")

    pa = mc_results['prophet_accuracies']
    qa = mc_results['quraysh_accuracies']
    pe = mc_results['prophet_errors']
    qe = mc_results['quraysh_errors']
    pv = mc_results['prophet_vars']
    qv = mc_results['quraysh_vars']

    print(f"  {'Decision Accuracy (mean)':<40} {np.mean(pa):<20.1%} {np.mean(qa):<20.1%}")
    print(f"  {'Decision Accuracy (std)':<40} {np.std(pa):<20.4f} {np.std(qa):<20.4f}")
    print(f"  {'Mean Belief Error':<40} {np.mean(pe):<20.4f} {np.mean(qe):<20.4f}")
    print(f"  {'Mean Posterior Variance':<40} {np.mean(pv):<20.4f} {np.mean(qv):<20.4f}")
    print(f"  {'Number of Sources':<40} {PROPHET_N_SOURCES:<20} {QURAYSH_N_SOURCES:<20}")
    print(f"  {'Mean Source Bias':<40} {np.mean(np.abs(PROPHET_SOURCE_BIAS)):<20.4f} "
          f"{np.mean(np.abs(QURAYSH_SOURCE_BIAS)):<20.4f}")

    # Strategic payoff comparison
    prophet_payoff = np.mean(pa) * CORRECT_DECISION_PAYOFF + (1 - np.mean(pa)) * WRONG_DECISION_COST
    quraysh_payoff = np.mean(qa) * CORRECT_DECISION_PAYOFF + (1 - np.mean(qa)) * WRONG_DECISION_COST
    print(f"\n  {'Expected Strategic Payoff':<40} {prophet_payoff:<20.2f} {quraysh_payoff:<20.2f}")
    print(f"  {'Payoff Advantage':<40} {prophet_payoff - quraysh_payoff:<20.2f} {'(baseline)':<20}")

    # --- Historical Examples ---
    print("\n--- Historical Verification ---")
    print("  Prophet's intelligence advantages (documented):")
    print("  * Knew of Quraysh assassination plot -> timed Hijra perfectly (622 CE)")
    print("  * Knew Quraysh caravan routes -> Battle of Badr positioning (624 CE)")
    print("  * Knew of Banu Qurayza negotiations with Quraysh (Battle of Trench)")
    print("  * Unconventional sources: Quraysh never suspected women/slaves/youth")
    print("  * Quraysh repeatedly surprised by Prophet's foreknowledge")

    # --- Plot ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Beliefs vs True State (single run)
    ax = axes[0, 0]
    t = np.arange(N_DECISIONS)
    ax.plot(t, detail['true_states'], 'k-', linewidth=2, label='True State', alpha=0.7)
    ax.plot(t, detail['prophet_beliefs'], 'g-', linewidth=1.5, label='Prophet Belief')
    ax.plot(t, detail['quraysh_beliefs'], 'r--', linewidth=1.5, label='Quraysh Belief')
    ax.set_xlabel('Strategic Decision Period')
    ax.set_ylabel('State / Belief')
    ax.set_title('Belief Tracking of True State')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 2: Belief Error Over Time
    ax = axes[0, 1]
    window = 5
    pe_smooth = np.convolve(detail['prophet_errors'], np.ones(window)/window, mode='valid')
    qe_smooth = np.convolve(detail['quraysh_errors'], np.ones(window)/window, mode='valid')
    ax.plot(pe_smooth, 'g-', linewidth=2, label='Prophet Error')
    ax.plot(qe_smooth, 'r--', linewidth=2, label='Quraysh Error')
    ax.set_xlabel('Decision Period')
    ax.set_ylabel('Absolute Belief Error')
    ax.set_title('Belief Error (Smoothed)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 3: Posterior Variance Over Time
    ax = axes[0, 2]
    ax.plot(detail['prophet_vars'], 'g-', linewidth=2, label='Prophet Variance')
    ax.plot(detail['quraysh_vars'], 'r--', linewidth=2, label='Quraysh Variance')
    ax.set_xlabel('Decision Period')
    ax.set_ylabel('Posterior Variance')
    ax.set_title('Belief Uncertainty Over Time')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 4: Accuracy Distribution (Monte Carlo)
    ax = axes[1, 0]
    ax.hist(mc_results['prophet_accuracies'], bins=30, alpha=0.6, color='green',
            label=f'Prophet (mean={np.mean(pa):.1%})', density=True)
    ax.hist(mc_results['quraysh_accuracies'], bins=30, alpha=0.6, color='red',
            label=f'Quraysh (mean={np.mean(qa):.1%})', density=True)
    ax.set_xlabel('Decision Accuracy')
    ax.set_ylabel('Density')
    ax.set_title(f'Accuracy Distribution ({N_SIMULATIONS} simulations)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 5: Variance vs Accuracy scatter
    ax = axes[1, 1]
    ax.scatter(mc_results['prophet_vars'], mc_results['prophet_accuracies'],
               alpha=0.3, color='green', s=10, label='Prophet')
    ax.scatter(mc_results['quraysh_vars'], mc_results['quraysh_accuracies'],
               alpha=0.3, color='red', s=10, label='Quraysh')
    ax.set_xlabel('Mean Posterior Variance')
    ax.set_ylabel('Decision Accuracy')
    ax.set_title('Variance Reduction -> Better Decisions')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 6: Source comparison diagram
    ax = axes[1, 2]
    categories = ['Sources', 'Avg Noise', 'Avg |Bias|', 'Accuracy', 'Avg Variance']
    prophet_vals = [PROPHET_N_SOURCES / 10, np.mean(PROPHET_SOURCE_NOISE),
                    np.mean(np.abs(PROPHET_SOURCE_BIAS)) * 5,
                    np.mean(pa), np.mean(pv) * 5]
    quraysh_vals = [QURAYSH_N_SOURCES / 10, np.mean(QURAYSH_SOURCE_NOISE),
                    np.mean(np.abs(QURAYSH_SOURCE_BIAS)) * 5,
                    np.mean(qa), np.mean(qv) * 5]

    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, prophet_vals, width, color='green', alpha=0.7, label='Prophet')
    ax.bar(x + width/2, quraysh_vals, width, color='red', alpha=0.7, label='Quraysh')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8, rotation=15)
    ax.set_title('Network Comparison (Normalized)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

    plt.suptitle("Bayesian Intelligence: Dar al-Arqam Network\nVariance Reduction Through Unconventional Sources",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('islamic_gt_codes/fig_17_bayesian_intelligence.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\nFigure saved: islamic_gt_codes/fig_17_bayesian_intelligence.png")

    print("\n--- CONCLUSION ---")
    print("The Prophet's Dar al-Arqam intelligence network achieved superior strategic")
    print("outcomes through Bayesian variance reduction:")
    print("  1. MORE independent sources (8 vs 5) from unconventional demographics")
    print("  2. LOWER systematic bias (sources not captured by elite groupthink)")
    print("  3. LOWER posterior variance -> consistently better strategic decisions")
    print("  4. Quraysh's 'blind spots' (ignoring women, slaves, youth) were exploited")
    print("  5. The accuracy advantage compounds over multiple decisions, explaining")
    print("     the Prophet's seemingly 'miraculous' strategic foresight")


if __name__ == "__main__":
    main()
