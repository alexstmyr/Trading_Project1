from market_maker import MarketMaker, plot_price_distribution, plot_expected_revenue

def main():
    market_maker = MarketMaker()
    #plot_price_distribution(market_maker)
    #plot_expected_revenue(market_maker)
    optimal_bid, optimal_ask = market_maker.compute_optimal_bid_ask()

    if optimal_bid is not None and optimal_ask is not None:
        print(f"Optimal Bid: {optimal_bid:.2f}, Optimal Ask: {optimal_ask:.2f}")
    else:
        print("No valid bid/ask prices found satisfying the constraint.")

if __name__ == "__main__":
    main()