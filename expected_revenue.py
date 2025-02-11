import numpy as np
import matplotlib.pyplot as plt


# Define parameters
P_0 = 51  # Initial price
Pi_I = 0.4  # Probability of informed trade
S_values = np.linspace(0, 10, 100)  # Spread values

# Compute probability functions
Pi_LB_S = 0.5 - 0.08 * S_values
Pi_LS_S = 0.5 - 0.08 * S_values

# Ensure probabilities remain within [0,0.5] range
Pi_LB_S = np.clip(Pi_LB_S, 0, 0.5)
Pi_LS_S = np.clip(Pi_LS_S, 0, 0.5)

# Expected revenue calculations
# 1. All trades are liquidity-motivated
expected_revenue_liq = (Pi_LB_S + Pi_LS_S) * S_values

# 2. 40% chance of informed trade
expected_revenue_informed = ((1 - Pi_I) * (Pi_LB_S + Pi_LS_S) * S_values)

# 3. Considering the given probabilities
expected_revenue_considering = (1 - Pi_I) * (Pi_LB_S + Pi_LS_S) * S_values

# Plot expected revenue under different conditions
plt.figure(figsize=(8, 5))
plt.plot(S_values, expected_revenue_liq, label="Liquidity Motivated Trades", linestyle="dashed")
plt.plot(S_values, expected_revenue_informed, label="40% Informed Trades")
plt.plot(S_values, expected_revenue_considering, label="Considering Given Probabilities", linestyle="dotted")

plt.xlabel("Spread (S)")
plt.ylabel("Expected Revenue")
plt.title("Expected Revenue under Different Conditions")
plt.legend()
plt.grid(True)
plt.show()
