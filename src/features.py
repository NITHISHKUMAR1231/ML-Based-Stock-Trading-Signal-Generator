def generate_labels(df):
    def classify(pnl):
        if pnl >= 20:
            return 2  # SELL
        elif pnl >= 5:
            return 1  # HOLD_PROFIT
        elif pnl >= -5:
            return 0  # HOLD
        else:
            return -1  # STOP_LOSS

    df["label"] = df["pnl_percent"].apply(classify)
    return df


def get_features_and_labels(df):
    X = df[["pnl_percent", "volatility", "price_vs_avg"]].dropna()
    y = df.loc[X.index, "label"]
    return X, y

print("done features.py")