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
        self.S_values = np.linspace(0, 10, 100)

    def generate_price_distribution(self, size=10000):
        np.random.seed(42)
        return weibull_min.rvs(self.k_param, scale=self.lambda_param, size=size)

    def weibull_pdf(self, S):
        return weibull_min.pdf(S, self.k_param, scale=self.lambda_param)

    def compute_expected_revenue(self):
        Pi_LB_S = np.clip(0.5 - 0.08 * self.S_values, 0, 0.5)
        Pi_LS_S = np.clip(0.5 - 0.08 * self.S_values, 0, 0.5)
        expected_revenue = (1 - self.Pi_I) * ((Pi_LB_S * self.S_values) + (Pi_LS_S * self.S_values))
        
        Pi_LB_S_fixed = np.full_like(self.S_values, 0.5)
        Pi_LS_S_fixed = np.full_like(self.S_values, 0.5)
        expected_revenue_liquidity = (Pi_LB_S_fixed * self.S_values) + (Pi_LS_S_fixed * self.S_values)
        expected_revenue_informed = (1 - self.Pi_I) * ((Pi_LB_S_fixed * self.S_values) + (Pi_LS_S_fixed * self.S_values))
        
        return expected_revenue, expected_revenue_liquidity, expected_revenue_informed

    def profit_function(self, prices):
        K_A, K_B = prices
        S_0 = self.P_0

        term1 = (1 - self.Pi_I) * ((0.5 * (K_A - S_0)) + (0.5 * (S_0 - K_B)))
        
        term2, _ = quad(lambda S: (S - K_A) * self.weibull_pdf(S), K_A, np.inf)
        term3, _ = quad(lambda S: (K_B - S) * self.weibull_pdf(S), 0, K_B)
        
        expected_profit = term1 - self.Pi_I * (term2 + term3)
        
        return -expected_profit if expected_profit >= 0 else np.inf  

    def compute_optimal_bid_ask(self):
        #bounds = [(self.P_0 - 5, self.P_0 + 5), (self.P_0 - 5, self.P_0 + 5)] 
        result = minimize(self.profit_function, [self.P_0 + 1, self.P_0 - 1], method='Nelder-Mead')
        return result.x[1], result.x[0]

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

