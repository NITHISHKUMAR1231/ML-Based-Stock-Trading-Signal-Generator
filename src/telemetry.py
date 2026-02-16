def calculate_telemetry(df):
    df["pnl_percent"] = (
        (df["current_price"] - df["avg_price"]) / df["avg_price"]
    ) * 100

    df["price_vs_avg"] = df["current_price"] - df["avg_price"]

    df["volatility"] = df["current_price"].pct_change().rolling(2).std()

    return df

print("done")