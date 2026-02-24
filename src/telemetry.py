def calculate_telemetry(df):
    try:
        # Calculate PnL percent
        df["pnl_percent"] = (
            (df["current_price"] - df["avg_price"]) / df["avg_price"]
        ) * 100

        # Calculate price difference vs average
        df["price_vs_avg"] = df["current_price"] - df["avg_price"]

        # Calculate volatility
        df["volatility"] = df["current_price"].pct_change().rolling(2).std()

        return df
    except KeyError as e:
        print(f"Error: Missing column in DataFrame - {e}")
        return df
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return df

print("done")
