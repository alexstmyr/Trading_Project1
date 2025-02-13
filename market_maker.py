import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
from scipy.integrate import quad
from scipy.optimize import minimize

class MarketMaker:
    def __init__(self, lambda_param=50, k_param=10, P_0=51, Pi_I=0.4):
        self.lambda_param = lambda_param
        self.k_param = k_param
        self.P_0 = P_0
        self.Pi_I = Pi_I
        self.S_values = np.linspace(0, 100, 1000)
        self.price_distribution = self.generate_price_distribution()

    def generate_price_distribution(self, size=10000):
        np.random.seed(42)
        return weibull_min.rvs(self.k_param, scale=self.lambda_param, size=size)

    def weibull_pdf(self, S):
        return weibull_min.pdf(S, self.k_param, scale=self.lambda_param)

    def pi_LB(self, K_A):
        return max(0, min(0.5, 0.5 - 0.08 * (K_A - self.P_0)))

    def pi_LS(self, K_B):
        return max(0, min(0.5, 0.5 - 0.08 * (self.P_0 - K_B)))

    def profit_function(self, K):
        K_A, K_B = K
        
        income = (1 - self.Pi_I) * (self.pi_LB(K_A) * (K_A - self.P_0) + self.pi_LS(K_B) * (self.P_0 - K_B))
        
        integral_above_K_A, _ = quad(lambda S: (S - K_A) * self.weibull_pdf(S), K_A, np.inf)
        integral_below_K_B, _ = quad(lambda S: (K_B - S) * self.weibull_pdf(S), 0, K_B)
        
        cost = self.Pi_I * (integral_above_K_A + integral_below_K_B)
        
        return -(income - cost)

    def compute_optimal_bid_ask(self):
        initial_guess = [self.P_0 + 2, self.P_0 - 2]
        bounds = [(self.P_0, None), (self.P_0 - 10 * self.k_param, self.P_0)]
        result = minimize(self.profit_function, initial_guess, bounds=bounds)

        if result.success:
            return result.x[1], result.x[0] 
        else:
            return None, None

def plot_price_distribution(market_maker):
    prices = market_maker.generate_price_distribution()
    plt.figure(figsize=(8, 5))
    plt.hist(prices, bins=50, density=True, alpha=0.6, color='blue', edgecolor='black')
    plt.title("Weibull Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Density")
    plt.grid(True)
    plt.show()

def plot_expected_revenue(market_maker):
    expected_revenue, expected_revenue_liquidity, expected_revenue_informed = market_maker.compute_expected_revenue()
    
    plt.figure(figsize=(8, 5))
    plt.plot(market_maker.S_values, expected_revenue, label="Expected Revenue")
    plt.plot(market_maker.S_values, expected_revenue_liquidity, label="Only Liquidity Motivated Trades", linestyle="dashdot")
    plt.plot(market_maker.S_values, expected_revenue_informed, label="40% Informed Trades", linestyle="dashed")
    
    plt.xlabel("Spread (S)")
    plt.ylabel("Expected Revenue")
    plt.title("Expected Revenue under Different Conditions")
    plt.legend()
    plt.grid(True)
    plt.show()