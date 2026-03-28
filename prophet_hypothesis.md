# Prophet's Hypothesis: Mapping the Strategic Actions of Prophet Muhammad ﷺ to Classical Game Theory Problems

---

> *"For every classical game theory problem that predicts collective disaster through rational self-interest, the Prophet Muhammad ﷺ demonstrated a historical solution that achieved collective optimality through moral architecture."*

---

## Methodology

For each classical game theory problem listed in `classic_gt_contents.md`, we identify:
1. **The classical problem** and its Nash Equilibrium prediction
2. **The historical episode** from the Prophet's life that addresses this problem
3. **The hypothesis** — how the Prophet's strategy resolves the classical failure
4. **Testable prediction** — what the IGT model predicts vs. what classical GT predicts
5. **Simulation reference** — pointer to the Python code in `islamic_gt_codes/`

---

## Part 1: The Basics — Foundational Game Structures

### H1: The Prisoner's Dilemma and Strict Dominance → The Muwakhat (Brotherhood)

**Classical Problem:** Two players each have a strictly dominant strategy to defect, producing outcome (D,D) with payoffs (1,1) despite (C,C) yielding (3,3). Individual rationality destroys collective welfare.

**Historical Episode:** Upon arrival in Medina (622 CE), the Prophet ﷺ paired each Muhajir (Meccan emigrant with zero assets) with an Ansar (Medinan host). The Ansar voluntarily shared half their wealth, homes, and land — an act of cooperation with no external enforcement.

**Hypothesis H1:** When players internalize altruistic preferences ($\alpha > 0$) and transcendental accountability ($\lambda > 0$), cooperation becomes the dominant strategy even in one-shot Prisoner's Dilemma. The Muwakhat demonstrates that cultivating these parameters through community-building and moral education transforms the payoff structure so that $U_i(C) > U_i(D)$ regardless of the other player's action.

**Testable Prediction:** In a population with sufficiently high $\alpha$ and $\lambda$, mutual cooperation emerges as the unique equilibrium. Historically confirmed: zero Ansar defected from the Muwakhat arrangement, and the Muhajirun (notably Abdur-Rahman ibn Awf) refused full transfers, requesting only market access — demonstrating bilateral cooperation.

**Simulation:** `islamic_gt_codes/sim_01_prisoners_dilemma_muwakhat.py`

---

### H2: Iterated Elimination of Strictly Dominated Strategies → Pre-Islamic Pact of the Virtuous (Hilf al-Fudul)

**Classical Problem:** In multi-player games, iterated elimination removes dominated strategies, but the remaining strategies may still produce suboptimal outcomes due to coordination failures and free-riding.

**Historical Episode:** Before prophethood (~595 CE), young Muhammad participated in the Hilf al-Fudul — a voluntary pact where Qurayshi clans agreed to protect oppressed merchants regardless of tribal affiliation. Free-riding (not joining but benefiting from others' enforcement) was the dominant strategy.

**Hypothesis H2:** Moral reputation effects and social accountability create additional payoff dimensions that make free-riding a dominated strategy. When the reputational cost of non-participation exceeds the enforcement cost of joining, joining becomes strictly dominant. The Prophet's later endorsement of this pact (even after revelation) shows that pre-Islamic moral mechanisms already contained seeds of IGT logic.

**Testable Prediction:** Voluntary enforcement coalitions form and sustain when moral accountability ($\Omega$) penalizes non-participation. Historically confirmed: the pact held for decades and protected multiple merchants.

**Simulation:** `islamic_gt_codes/sim_02_hilf_al_fudul.py`

---

### H3: Pure Strategy Nash Equilibrium and the Stag Hunt → The Aqaba Pledges

**Classical Problem:** In the Stag Hunt, two equilibria exist: (Stag, Stag) with high payoff requiring mutual trust, and (Hare, Hare) with low payoff but no risk. Players often converge on the safe but suboptimal (Hare, Hare) equilibrium due to trust deficit.

**Historical Episode:** The First Pledge of Aqaba (621 CE) and Second Pledge of Aqaba (622 CE). Seventy-three Medinan converts secretly pledged to protect the Prophet ﷺ at the cost of their lives — choosing "Stag" (full commitment) over "Hare" (nominal faith with no risk). The Prophet organized 12 Naqibs (leaders) to coordinate the pledge.

**Hypothesis H3:** The Naqib system solved the Stag Hunt coordination problem by creating observable intermediate commitments. Each Naqib served as a credible signal that others were choosing "Stag," reducing uncertainty about collective action. The akhirah payoff ($\lambda \cdot \Omega$) made the risk of choosing "Stag" acceptable even under uncertainty, because the divine reward for commitment exceeded the material risk of betrayal.

**Testable Prediction:** With intermediate leadership coordination and transcendental payoffs, groups converge on the Pareto-dominant (Stag, Stag) equilibrium. Historically confirmed: all 73 pledgers honored their commitment, and the Hijra succeeded.

**Simulation:** `islamic_gt_codes/sim_03_stag_hunt_aqaba.py`

---

### H4: Best Responses and Mixed Strategy Nash Equilibrium → The Battle of Badr

**Classical Problem:** In mixed strategy equilibria, players randomize to make opponents indifferent. This creates unpredictability but no stable cooperative outcome.

**Historical Episode:** At the Battle of Badr (624 CE), the Muslim force of 313 faced a Meccan army of approximately 1,000. Classical military calculus (a mixed strategy game) would predict retreat or guerrilla avoidance. Instead, the Prophet ﷺ chose decisive engagement after consultation (shura), trusting divine guidance over probabilistic calculation.

**Hypothesis H4:** When one player has access to information beyond the standard Bayesian framework (divine revelation as a "type" signal), mixed strategy calculation becomes irrelevant. The Prophet's "pure strategy" of engagement was supported by $\lambda \cdot \Omega(\text{obey revelation}) \gg$ any material expected loss. This is not irrationality — it is rationality under an expanded utility function that includes certainty from divine command.

**Testable Prediction:** Players with high $\lambda$ will choose pure strategies (obedience to moral/divine command) even when mixed strategies are "optimal" under material payoffs alone. The outcome at Badr — decisive victory by a 3:1 outnumbered force — is consistent with the hypothesis that moral certainty generates commitment advantages that probabilistic models cannot capture.

**Simulation:** `islamic_gt_codes/sim_04_battle_of_badr.py`

---

### H5: Battle of the Sexes → The Aws-Khazraj Reconciliation (Constitution of Medina)

**Classical Problem:** Two players prefer coordination but disagree on which outcome to coordinate on. Multiple Nash equilibria exist, and without a focal point, coordination fails.

**Historical Episode:** The Aws and Khazraj tribes of Medina had been locked in decades of devastating civil war (culminating in the Battle of Bu'ath, 617 CE). Each tribe preferred peace coordinated on their terms. The Prophet ﷺ arrived as an external arbiter and established the Constitution of Medina (Sahifa), creating a new focal point: shared identity as one Ummah with tribal autonomy preserved.

**Hypothesis H5:** An external moral authority with credibility among all parties can create a new focal point (Schelling point) that resolves the Battle of the Sexes coordination failure. The Constitution of Medina achieved what neither tribe could achieve alone: coordination on a mutually beneficial outcome that preserved each tribe's preferences while creating a higher-order identity.

**Testable Prediction:** Multi-party coordination games with historical grievances are resolved when a trusted arbiter establishes a new focal point that doesn't require either side to "lose." Historically confirmed: Aws and Khazraj united under the Constitution, ending decades of war.

**Simulation:** `islamic_gt_codes/sim_05_aws_khazraj_coordination.py`

---

## Part 2: Extensive Form Games

### H6: Subgame Perfect Equilibrium and Backward Induction → The Treaty of Hudaybiyyah

**Classical Problem:** In finite sequential games, backward induction produces subgame perfect equilibria that often require harsh punishment in early stages to deter deviation. The logic unravels cooperation in finite games.

**Historical Episode:** At Hudaybiyyah (628 CE), the Prophet ﷺ accepted seemingly humiliating treaty terms: no Umrah that year, asymmetric extradition clause, removal of "Messenger of God" from the document. Backward induction from a finite game perspective would predict these as losses.

**Hypothesis H6:** The Prophet was not playing a finite game. By treating the interaction as an infinite game with akhirah horizon, backward induction does not apply. The "humiliating" terms were optimal in the infinite game because peace enabled dakwah (propagation), which was worth more than any single-period military advantage. The Quran's designation of Hudaybiyyah as "a clear victory" (48:1) is the IGT prediction: short-term material loss for long-term systemic gain.

**Testable Prediction:** In infinite-horizon games with dakwah externalities, accepting unfavorable short-term terms is optimal when the peace dividend exceeds the material concession. Historically confirmed: within 22 months, Khalid ibn al-Walid, Amr ibn al-As, and thousands of others converted during the peace period.

**Simulation:** `islamic_gt_codes/sim_06_hudaybiyyah_treaty.py`

---

### H7: Punishment Strategies and Tying Hands → The Meccan Period Patience (13 Years)

**Classical Problem:** In repeated games, cooperation is sustained through punishment strategies (Grim Trigger, Tit-for-Tat). But punishment requires the ability to credibly retaliate.

**Historical Episode:** For 13 years in Mecca (610–622 CE), the Prophet ﷺ and his followers endured torture, boycott, assassination attempts, and economic sanctions without retaliating. God explicitly commanded patience over retaliation. The Prophet "tied his hands" by committing to non-violence even when retaliation was physically possible.

**Hypothesis H7:** Strategic patience is a dominant strategy in asymmetric repeated games when (a) the weaker player's time horizon is infinite (akhirah), (b) retaliation would trigger escalation spirals that destroy the movement, and (c) patience builds moral capital that converts future adversaries. The Prophet's "tied hands" commitment was credible precisely because it was costly — making it a separating signal that distinguished him from tribal power-seekers.

**Testable Prediction:** In asymmetric conflicts, the patient player with infinite time horizon outperforms the retaliatory player in the long run. Historically confirmed: the patient Meccan strategy preserved the movement for explosive growth in Medina.

**Simulation:** `islamic_gt_codes/sim_07_meccan_patience.py`

---

### H8: The Centipede Game → Generosity of Abdur-Rahman ibn Awf

**Classical Problem:** In the Centipede Game, backward induction predicts immediate defection at the first node, despite the possibility of large mutual gains from continued play. Trust unravels from the end.

**Historical Episode:** When Sa'd ibn al-Rabi' offered Abdur-Rahman ibn Awf half his wealth and one of his wives through Muwakhat, Abdur-Rahman declined, asking only: "Show me the way to the market." He then built his fortune through trade and later donated massive wealth to the Islamic community. Instead of "defecting" (taking the maximum offer), he chose to "continue the game" through independent effort, generating far more value for both parties.

**Hypothesis H8:** The Centipede Game unravels because players fear being exploited at later nodes. When both players have akhirah preferences ($\lambda > 0$), continuing the game becomes dominant because exploitation at later nodes is penalized by $\Omega$. The result is that the game reaches its maximum cooperative payoff node. Abdur-Rahman's behavior demonstrates this: he trusted the system, continued playing, and generated wealth that exceeded Sa'd's original offer by orders of magnitude.

**Testable Prediction:** Under IGT preferences, Centipede Games reach deeper nodes (more cooperation) as $\lambda$ increases. The historical record shows extraordinary depth of cooperative exchange in the early Muslim community.

**Simulation:** `islamic_gt_codes/sim_08_centipede_muwakhat.py`

---

## Part 3: Advanced Strategic Form Games

### H9: Rock-Paper-Scissors and Symmetric Games → Multi-Front Diplomacy (Letters to Kings)

**Classical Problem:** In symmetric zero-sum games, no pure strategy equilibrium exists. Players must randomize, producing unpredictable outcomes.

**Historical Episode:** After Hudaybiyyah, the Prophet ﷺ sent letters simultaneously to the Byzantine Emperor, Persian Emperor, Negus of Abyssinia, Muqawqis of Egypt, and rulers of Bahrain, Oman, and Yemen. This multi-front diplomatic engagement ensured no single rejection could constitute total failure.

**Hypothesis H9:** In multi-player zero-sum diplomatic games, the Prophet converted the game from zero-sum to positive-sum by offering each ruler a unique value proposition (spiritual and political). The simultaneous multi-front approach created a portfolio strategy where success with any subset of rulers generated positive returns, eliminating the need for mixed-strategy randomization.

**Testable Prediction:** Multi-front simultaneous engagement dominates sequential single-front diplomacy when partial success is valuable. Historically confirmed: Negus and the rulers of Bahrain and Oman accepted, while Persia and Byzantium rejected — but the portfolio returned positive net value.

**Simulation:** `islamic_gt_codes/sim_09_diplomatic_portfolio.py`

---

### H10: Comparative Statics and the Support of Mixed Strategies → Evolution of Islamic Community Strategy

**Classical Problem:** Comparative statics analyze how equilibrium changes when parameters shift. In mixed strategies, changing one player's payoff can paradoxically affect the other player's mixing probability.

**Historical Episode:** The Prophet ﷺ systematically adjusted community strategy as conditions changed: secret worship in Mecca (Dar al-Arqam period) → semi-public preaching → Abyssinian migration → Medinan military capability → Hudaybiyyah diplomacy → Conquest mercy. Each strategic shift was calibrated to changing parameter conditions.

**Hypothesis H10:** The Prophet's strategic evolution is explained by comparative statics in the IGT model. As the community's strength parameter ($n$, number of believers), material resources ($w$), and external threat level ($\theta$) changed, the optimal strategy profile shifted predictably. The transition from patience to engagement to diplomacy to mercy follows the comparative statics of the IGT equilibrium as these parameters evolved.

**Testable Prediction:** The IGT model predicts specific strategy transitions at identifiable parameter thresholds. The historical sequence matches these predictions.

**Simulation:** `islamic_gt_codes/sim_10_strategy_evolution.py`

---

## Part 4: Games with Infinite Strategy Spaces

### H11: Hotelling's Game and the Median Voter Theorem → The Prophet's Universal Message

**Classical Problem:** In Hotelling's spatial competition model, two parties converge to the median voter position, producing minimal differentiation.

**Historical Episode:** The Prophet ﷺ did not position his message at the "median" of Meccan religious opinion (which would have been a moderate polytheism). Instead, he positioned at the extreme of pure monotheism (tawhid) — the furthest possible point from the Qurayshi consensus.

**Hypothesis H11:** The Hotelling convergence-to-center prediction assumes voters/followers are uniformly distributed and switch based on proximity. The Prophet's strategy exploited a different dynamic: his extreme position created a new dimension of competition (moral authority, afterlife accountability) that attracted supporters from across the existing spectrum. By creating a new axis of competition rather than competing on the existing axis, he escaped the Hotelling trap.

**Testable Prediction:** Movements that create new dimensions of competition (rather than competing on existing dimensions) can achieve dominance from initially extreme positions. Historically confirmed: the "extreme" monotheist position attracted followers from all tribal and economic backgrounds within two decades.

**Simulation:** `islamic_gt_codes/sim_11_hotelling_tawhid.py`

---

### H12: Second Price Auctions (Vickrey) → Sadaqah (Voluntary Charity) Mechanism

**Classical Problem:** In Vickrey auctions, the optimal strategy is truthful bidding because you pay the second price, not your bid. This achieves efficient allocation through incentive-compatible mechanism design.

**Historical Episode:** The Prophet ﷺ encouraged sadaqah (voluntary charity) through a mechanism where the reward was proportional to sincerity, not the amount. The akhirah payoff function $\Omega_i(\text{sadaqah})$ was calibrated to intention (niyyah) rather than observable amount. A poor widow's single date was declared more valuable than a wealthy man's large donation if her sincerity was greater.

**Hypothesis H12:** Sadaqah operates as a divine mechanism where "truthful bidding" (sincere giving) is the dominant strategy because the "price" paid (material loss) is always less than the "reward" received (akhirah gain). This is structurally identical to the Vickrey auction's incentive compatibility: truthful revelation of capacity is optimal because the payoff mechanism rewards sincerity, not strategic misrepresentation.

**Testable Prediction:** Under sadaqah mechanism design, voluntary charitable giving exceeds coerced taxation in both participation rates and total redistribution when $\lambda$ is sufficiently high. The early Muslim community's extraordinary voluntary giving confirms this.

**Simulation:** `islamic_gt_codes/sim_12_sadaqah_mechanism.py`

---

## Part 5: Expected Utility Theory

### H13: The Allais Paradox and Risk Preferences → Abu Bakr's Total Sacrifice

**Classical Problem:** The Allais Paradox shows that humans violate expected utility axioms through certainty bias: preferring a sure gain over a probabilistic higher expected value. This challenges the rationality assumption.

**Historical Episode:** Abu Bakr al-Siddiq donated his entire wealth — 100% of his assets — to the Muslim cause at multiple critical junctures. Under classical expected utility with risk aversion, no rational agent donates everything because the marginal utility of zero wealth is infinitely negative.

**Hypothesis H13:** Abu Bakr's behavior is perfectly rational under IGT. His utility function includes $\lambda \cdot \Omega(\text{total sacrifice})$, which makes the akhirah return on total donation overwhelm the material utility loss. The "Allais Paradox" of preferring certainty disappears because the akhirah payoff is certain (from the believer's perspective) and infinite in magnitude. Abu Bakr was not risk-seeking in material terms — he was risk-averse in akhirah terms: the "risky" option was not donating and facing divine accountability.

**Testable Prediction:** Agents with high $\lambda$ exhibit risk-seeking behavior in material domains and risk-averse behavior in akhirah domains. This reversal of risk preferences is observed systematically in the companions' behavior.

**Simulation:** `islamic_gt_codes/sim_13_abu_bakr_utility.py`

---

### H14: Pareto Efficiency → The Zakat System as Pareto Improvement

**Classical Problem:** Pareto efficiency states that no reallocation can make someone better off without making someone worse off. Wealth redistribution under classical assumptions is not Pareto-improving because the rich lose.

**Historical Episode:** The Zakat system (2.5% annual wealth levy) was experienced by the rich as a Pareto improvement — not merely tolerated but actively embraced. The wealthy companions competed in Zakat payment and voluntary sadaqah beyond the minimum.

**Hypothesis H14:** Under IGT, Zakat is a genuine Pareto improvement because the payer's total utility increases: the material loss ($\Delta w$) is outweighed by the altruistic payoff ($\alpha \cdot u_{\text{recipient}}$) and akhirah payoff ($\lambda \cdot \Omega(\text{Zakat})$). Every party is strictly better off under Zakat when $\alpha$ and $\lambda$ are above threshold. This resolves the classical impossibility of voluntary redistribution.

**Testable Prediction:** In communities with high $\alpha$ and $\lambda$, wealth redistribution mechanisms achieve near-universal voluntary compliance. Historically confirmed: Zakat compliance in the early Muslim community was virtually complete, and Caliph Umar ibn Abd al-Aziz reportedly could not find eligible Zakat recipients because poverty had been eliminated.

**Simulation:** `islamic_gt_codes/sim_14_zakat_pareto.py`

---

## Part 6: Repeated Games

### H15: Grim Trigger and Tit-for-Tat → The Conquest of Mecca Amnesty

**Classical Problem:** In repeated Prisoner's Dilemma, cooperation is sustained by punishment strategies like Grim Trigger (permanent retaliation) or Tit-for-Tat (mirror opponent). Both require punishment to maintain cooperation.

**Historical Episode:** The Conquest of Mecca (630 CE). The Quraysh had defected from the Treaty of Hudaybiyyah by aiding an attack on the Prophet's allies. Classical Grim Trigger prescribes permanent punishment. Tit-for-Tat prescribes retaliation. Instead, the Prophet declared: "Go, for you are free" — universal amnesty for all previous offenses.

**Hypothesis H15:** The Prophet's amnesty strategy dominates both Grim Trigger and Tit-for-Tat in the post-conquest continuation game. Grim Trigger creates a permanent adversary (guerrilla resistance). Tit-for-Tat creates a cycle of retaliation. Amnesty eliminates the motivation for future defection by removing the fear that drives it. The rebellion probability after amnesty ($p_R^{\text{amnesty}} \approx 0$) is lower than after punishment ($p_R^{\text{punishment}} > 0$) because amnesty destroys the oppressor-liberator framing that sustains resistance movements.

**Testable Prediction:** In post-conflict games, unconditional amnesty produces lower rebellion rates and faster reconciliation than punishment strategies when accompanied by credible moral authority. Historically confirmed: zero organized resistance after the Conquest, and the entire Arabian Peninsula unified within two years.

**Simulation:** `islamic_gt_codes/sim_15_conquest_amnesty.py`

---

### H16: The Folk Theorem → The Prophet's 23-Year Parameter Cultivation

**Classical Problem:** The Folk Theorem proves that in infinitely repeated games with sufficient patience ($\delta$ high enough), any feasible individually rational payoff can be sustained as equilibrium. The problem: too many equilibria, no guidance on which one emerges.

**Historical Episode:** The Prophet's 23-year mission was a systematic equilibrium selection project. Through revelation, community-building, institutional design (Dar al-Arqam, Constitution of Medina, Muwakhat, Zakat), and personal example, he cultivated specific parameters ($\alpha$, $\lambda$) that selected the cooperative equilibrium from the infinite set predicted by the Folk Theorem.

**Hypothesis H16:** The Folk Theorem's multiplicity problem is solved by moral parameter cultivation. When a community's $\alpha$ and $\lambda$ are raised above specific thresholds, the Muhammad Equilibrium becomes the unique stable equilibrium from the Folk Theorem's feasible set. The Prophet's mission was precisely this: engineering the $(\alpha, \lambda)$ parameter values that select the Pareto-dominant equilibrium.

**Testable Prediction:** Communities with systematically cultivated moral parameters ($\alpha, \lambda$) converge on cooperative equilibria, while communities relying only on material incentives cycle among Folk Theorem equilibria unpredictably. The contrast between pre-Islamic Arabia (chaotic multi-equilibrium) and post-prophetic Arabia (stable cooperative equilibrium) confirms this.

**Simulation:** `islamic_gt_codes/sim_16_folk_theorem_selection.py`

---

## Part 7: Bayesian-Nash Equilibrium

### H17: Incomplete Information and Bayesian Updating → The Dar al-Arqam Intelligence Network

**Classical Problem:** In games of incomplete information, players form beliefs about others' types and update via Bayes' Rule. Players with better information have strategic advantage.

**Historical Episode:** The Prophet ﷺ established the Dar al-Arqam as an organizational hub hidden in plain sight — in Abu Jahl's own neighborhood. He deployed women, children, and slaves as information carriers whom the Quraysh surveillance dismissed as non-strategic actors. He maintained systematically lower uncertainty about Qurayshi types than they had about his network.

**Hypothesis H17:** The Prophet achieved Bayesian superiority through two mechanisms: (a) unconventional intelligence assets (demographics the enemy considered non-strategic), and (b) the "eyebrow principle" — positioning operational nodes in locations adversaries would never suspect precisely because of their proximity to threat. This reduced $\text{Var}[\hat{t}_Q | \text{Prophet's info}]$ while maximizing $\text{Var}[\hat{t}_M | \text{Quraysh info}]$.

**Testable Prediction:** Players who exploit informational blind spots in adversary surveillance (by using agents the adversary considers non-strategic) achieve persistent Bayesian advantage. Historically confirmed: the Dar al-Arqam operated undetected for approximately 4 years despite Abu Jahl's active surveillance.

**Simulation:** `islamic_gt_codes/sim_17_bayesian_intelligence.py`

---

### H18: Signaling Games and Separating Equilibrium → The Prophet's Pre-Prophethood Reputation

**Classical Problem:** In signaling games, informed types send costly signals to separate from imitation types. Credible signals must be sufficiently costly that low types cannot imitate.

**Historical Episode:** The Prophet ﷺ earned the title "Al-Amin" (The Trustworthy) and "Al-Sadiq" (The Truthful) decades before claiming prophethood. This 40-year record of perfect honesty was a costly signal: maintaining perfect truthfulness requires forgoing profitable deception opportunities over an entire lifetime.

**Hypothesis H18:** The Prophet's pre-prophethood reputation constitutes a separating equilibrium signal. The cost of maintaining perfect honesty for 40 years is so high that no strategic deceiver would undertake it as a preparatory deception strategy. This signal perfectly separated the "prophetic type" from the "power-seeker type." When the Quraysh later accused him of lying, their own prior assessment ("He has never told a lie") contradicted the accusation — the signal had already established type separation.

**Testable Prediction:** Long-duration costly signals (decades of consistent behavior) achieve more credible type separation than short-duration signals. The historical record confirms that the "Al-Amin" signal was the Prophet's most powerful asset in early conversions.

**Simulation:** `islamic_gt_codes/sim_18_signaling_alamin.py`

---

## Part 8: Perfect Bayesian Equilibrium

### H19: Screening Games and Adverse Selection → The Abyssinian Migration Screening

**Classical Problem:** In screening games, the uninformed party designs a menu of contracts to separate agent types. Adverse selection occurs when low types mimic high types.

**Historical Episode:** The migration to Abyssinia (615 CE) served as a screening mechanism. The Prophet ﷺ selected specific companions to present Islam to the Negus — choosing Ja'far ibn Abi Talib for his eloquence and selecting Surah Maryam (about Jesus and Mary) as the presentation content. This was a screening mechanism targeting the Negus's type (Christian king) with content designed to elicit truthful type-revelation.

**Hypothesis H19:** The Prophet designed the Abyssinian presentation as a screening mechanism: if the Negus was type "just ruler open to truth," Surah Maryam would produce acceptance; if type "tribal partisan," the same content would produce rejection. The content was chosen to maximize the diagnostic separation between these types. The Quraysh counter-emissaries offered gifts (pooling signal — any type accepts gifts), while the Muslims offered theological content (separating signal — only the truth-seeking type responds positively).

**Testable Prediction:** Content-based appeals separate types more effectively than material-based appeals in diplomatic screening games. Historically confirmed: the Negus wept upon hearing Surah Maryam and granted protection, rejecting the Quraysh's material gifts.

**Simulation:** `islamic_gt_codes/sim_19_abyssinia_screening.py`

---

### H20: The Beer-Quiche Game → Abu Sufyan's Type Revelation at Conquest

**Classical Problem:** In the Beer-Quiche game, a strong type and weak type send signals about their strength. Pooling equilibria exist where both types send the same signal, making type identification impossible.

**Historical Episode:** Before the Conquest of Mecca, the Prophet ﷺ arranged for his uncle Abbas to meet Abu Sufyan (the Quraysh leader) outside Mecca and bring him to the Muslim camp. There, Abu Sufyan witnessed 10,000 campfires — an overwhelming display of force. Abbas then facilitated Abu Sufyan's conversion, offering him a face-saving formula: "Whoever enters Abu Sufyan's house is safe."

**Hypothesis H20:** The Prophet created a separating equilibrium through asymmetric information revelation. Abu Sufyan was forced to observe the Muslim army's true strength (10,000 strong), which separated the game's types: resistance (subgame payoff = certain defeat) vs. submission (subgame payoff = survival + honor). The "Abu Sufyan's house is safe" formula was a mechanism design element that made submission incentive-compatible for a pride-driven leader. It solved the "quiche problem" — allowing the weak type (defeated leader) to adopt the cooperative action without the stigma of weakness.

**Testable Prediction:** Face-saving mechanisms that allow defeated players to cooperate without public humiliation produce higher cooperation rates than demands for unconditional surrender. Historically confirmed: Abu Sufyan cooperated fully, and his public conversion triggered a cascade.

**Simulation:** `islamic_gt_codes/sim_20_abu_sufyan_signaling.py`

---

## Part 9: Bargaining Theory

### H21: Nash Bargaining and the Outside Option → The Kaaba Stone Arbitration

**Classical Problem:** In bargaining games, the Nash Bargaining Solution splits surplus proportional to disagreement payoffs. Players with better outside options get better deals.

**Historical Episode:** When the Quraysh clans deadlocked over placing the Black Stone during the Kaaba renovation (~605 CE), tribal violence was imminent. Young Muhammad was selected as arbiter (being "the first to enter the gate"). He placed the stone on a cloth and had representatives of each tribe hold a corner, lifting it together.

**Hypothesis H21:** The Prophet's solution transcended the Nash Bargaining framework by redefining the game from zero-sum (one tribe's honor vs. another's) to positive-sum (shared honor for all). The cloth mechanism was a brilliant mechanism design that distributed the action (lifting) symmetrically while concentrating the symbolic act (final placement) with the arbiter. This eliminated the disagreement payoff differential that drives unequal bargaining outcomes.

**Testable Prediction:** Third-party mechanisms that convert zero-sum honor disputes into positive-sum shared actions produce agreements that bilateral negotiation cannot reach. The historical outcome — all tribes satisfied, violence averted — confirms this.

**Simulation:** `islamic_gt_codes/sim_21_kaaba_stone_bargaining.py`

---

## Part 10: Mechanism Design and Market Games

### H22: Market of Medina → Fair Market Design

**Classical Problem:** Markets under classical GT tend toward monopoly, information asymmetry, and exploitation of weaker participants.

**Historical Episode:** The Prophet ﷺ established the Market of Medina with specific rules: no middleman exploitation (no intercepting goods before they reach market), no hoarding to create artificial scarcity, no deceptive practices. The market had no rent — it was public space, preventing monopolistic extraction.

**Hypothesis H22:** The Market of Medina was a mechanism design solution that eliminated the Nash equilibria of manipulation, hoarding, and monopoly. By prohibiting specific strategies (hoarding, intercepting caravans, deceptive pricing) and making the market rent-free public space, the Prophet constrained the strategy space to eliminate exploitative equilibria. The remaining equilibrium was competitive and fair — achieving what modern antitrust regulation attempts but with lower enforcement cost.

**Testable Prediction:** Markets with prohibited manipulation strategies and zero-rent public access achieve fairer price discovery and broader participation than unregulated markets. Historical evidence from early Islamic markets confirms this.

**Simulation:** `islamic_gt_codes/sim_22_market_medina.py`

---

### H23: Riba Prohibition → Restructuring the Financial Game

**Classical Problem:** Interest-bearing debt creates a moral hazard game where lenders profit regardless of borrower success, incentivizing excessive risk-taking and creating systemic fragility (2008 financial crisis as Nash equilibrium).

**Historical Episode:** The Prophet ﷺ prohibited Riba (usury/interest), mandating risk-sharing contracts (mudaraba, musharaka) where lender and borrower share both profits and losses.

**Hypothesis H23:** Riba prohibition is a mechanism design intervention that aligns lender-borrower incentives. Under risk-sharing, the bank profits only when the entrepreneur succeeds — eliminating the moral hazard that produces the Nash equilibrium of excessive leverage and systemic collapse. This achieves what decades of financial regulation have failed to achieve: intrinsic incentive alignment in financial markets.

**Testable Prediction:** Risk-sharing financial systems produce lower systemic risk and more equitable wealth distribution than interest-based systems. This hypothesis is testable through simulation comparing Islamic finance vs. conventional finance under stress scenarios.

**Simulation:** `islamic_gt_codes/sim_23_riba_prohibition.py`

---

## Part 11: Coalition Games and Cooperative Theory

### H24: The Core of Cooperative Games → The Constitution of Medina as Core Allocation

**Classical Problem:** The Core of a cooperative game is the set of payoff allocations that no coalition can improve upon. In many games, the Core is empty — no stable allocation exists.

**Historical Episode:** The Constitution of Medina created a multi-party agreement among Muslims, Jews, and pagan Arabs that held as the governing framework for several years — despite the extraordinary heterogeneity of participants.

**Hypothesis H24:** The Constitution of Medina implemented a Core allocation in a cooperative game with heterogeneous players. Each provision was designed so that no sub-coalition (tribal group, religious community) could improve its payoff by breaking the agreement. The collective defense clause made defection costly (loss of security), while tribal autonomy made participation low-cost (no cultural erasure). The resulting allocation was in the Core — coalitionally stable.

**Testable Prediction:** Multi-party constitutions that provide collective security, dispute resolution, and preference heterogeneity accommodation produce Core-stable allocations. The Constitution of Medina held until external parties (Banu Qaynuqa, Banu Nadir) violated its terms by coordinating with Meccan enemies — confirming that the mechanism was stable as long as commitments were honored.

**Simulation:** `islamic_gt_codes/sim_24_medina_constitution_core.py`

---

## Summary Table: Hypothesis Mapping

| # | Classical GT Problem | Prophet's Historical Episode | Key IGT Parameter |
|---|---|---|---|
| H1 | Prisoner's Dilemma | Muwakhat Brotherhood | $\alpha > 0, \lambda > 0$ |
| H2 | Iterated Elimination | Hilf al-Fudul Pact | $\Omega$(reputation) |
| H3 | Stag Hunt | Aqaba Pledges + Naqibs | $\lambda$(commitment) |
| H4 | Mixed Strategy NE | Battle of Badr | $\lambda \cdot \Omega$(revelation obedience) |
| H5 | Battle of the Sexes | Aws-Khazraj / Constitution of Medina | Focal point authority |
| H6 | Subgame Perfect Eq. | Treaty of Hudaybiyyah | Infinite horizon ($\delta_{\text{akhirah}} = 1$) |
| H7 | Punishment Strategies | 13 Years Meccan Patience | Strategic patience as separating signal |
| H8 | Centipede Game | Abdur-Rahman ibn Awf | Trust under $\lambda$ reduces exploitation |
| H9 | Zero-Sum Games | Letters to Kings (Diplomacy) | Portfolio / positive-sum conversion |
| H10 | Comparative Statics | Strategy Evolution (Mecca→Medina) | Parameter-dependent transitions |
| H11 | Hotelling's Game | Tawhid as New Dimension | Dimension creation vs. convergence |
| H12 | Vickrey Auction | Sadaqah Mechanism | $\Omega$(sincerity) as truthful-bidding incentive |
| H13 | Allais Paradox | Abu Bakr's Total Sacrifice | $\lambda$-driven risk reversal |
| H14 | Pareto Efficiency | Zakat System | Genuine Pareto improvement under IGT |
| H15 | Grim Trigger / TfT | Conquest of Mecca Amnesty | Amnesty > Punishment in continuation game |
| H16 | Folk Theorem | 23-Year Mission | Equilibrium selection via $(\alpha, \lambda)$ |
| H17 | Bayesian-Nash | Dar al-Arqam Intelligence | Unconventional info assets |
| H18 | Signaling / Separating | Al-Amin Reputation (40 years) | Long-duration costly signal |
| H19 | Screening / Adverse Selection | Abyssinian Migration | Content-based type separation |
| H20 | Beer-Quiche Game | Abu Sufyan at Conquest | Face-saving mechanism design |
| H21 | Nash Bargaining | Kaaba Stone Arbitration | Zero-sum → positive-sum conversion |
| H22 | Market Design | Market of Medina | Strategy space restriction |
| H23 | Financial Games / Moral Hazard | Riba Prohibition | Risk-sharing alignment |
| H24 | Core of Cooperative Games | Constitution of Medina | Multi-party Core allocation |

---

*Each hypothesis is supported by a Python simulation in the `islamic_gt_codes/` directory.
