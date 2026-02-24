def get_features_and_labels(df):
    X = df[["avg_price","current_price","pnl_percent", "volatility", "price_vs_avg"]].dropna()
    y = df.loc[X.index, "label"]
    return X, y

print("done features.py")