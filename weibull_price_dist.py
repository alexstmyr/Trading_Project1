import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min

lambda_param = 50
k_param = 10

np.random.seed(42)
weibull_prices = weibull_min.rvs(k_param, scale=lambda_param, size=10000)

# Plot the Weibull price distribution
plt.figure(figsize=(8, 5))
plt.hist(weibull_prices, bins=50, density=True, alpha=0.6, color='blue', edgecolor='black')
plt.title("Weibull Price Distribution (λ=50, K=10)")
plt.xlabel("Price")
plt.ylabel("Density")
plt.grid(True)
plt.show()
