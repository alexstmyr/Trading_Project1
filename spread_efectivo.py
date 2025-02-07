#Effective spread
import pandas as pd
import numpy as np


def effective_spead(data, window_size=10):

    df_copy = data.copy()
    df_copy.dropna(inplace=True)

    if 'timestamp' in df_copy.columns:
        df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'])
        df_copy.sort_values(by='timestamp', inplace=True)

    df_copy['price_change'] = df_copy['Close'].diff()
    df_copy = df_copy.dropna(subset=["price_change"])

    df_copy['cov_price_change'] = np.abs(df_copy['price_change'].rolling(window=window_size).cov(df_copy['price_change'].shift(1)))

    df_copy['effective_spread'] = 2 * np.sqrt(df_copy['cov_price_change'])

    df_copy["posicion"] = np.where(df_copy["Close"] > df_copy["Close"].shift(),"ask","bid")

    df_copy["valor_original"] = df_copy["Close"]

    for i in range(window_size, len(df_copy) - window_size):
        if df_copy["posicion"].iloc[i] == "ask":
            df_copy.loc[df_copy.index[i], "valor_original"] = (df_copy["Close"].iloc[i] - df_copy["effective_spread"].iloc[i])
        else:
            df_copy.loc[df_copy.index[i], "valor_original"] = (df_copy["Close"].iloc[i] + df_copy["effective_spread"].iloc[i])

    df_copy = df_copy.dropna(subset=["cov_price_change"])

    return df_copy


data = pd.read_csv('aapl_5m_train.csv')
file = effective_spead(data)
output_file_path = "/Users/alexsotomayor/code/trading/activities/aapl_5m_with_spread2.csv"
file.to_csv(output_file_path, index=False)

