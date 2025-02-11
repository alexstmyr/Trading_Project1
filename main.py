from market_maker import MarketMaker, plot_price_distribution, plot_expected_revenue

def main():
    market_maker = MarketMaker()
    
    plot_price_distribution(market_maker)
    
    plot_expected_revenue(market_maker)
    
    optimal_bid, optimal_ask = market_maker.compute_optimal_bid_ask()
    print(f"Optimal Bid: {optimal_bid:.2f}, Optimal Ask: {optimal_ask:.2f}")

if __name__ == "__main__":
    main()
