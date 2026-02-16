from flask import Flask, request, render_template_string
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
model = joblib.load(MODEL_PATH)

# Load stock data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "stocks.csv")
df = pd.read_csv(DATA_PATH)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Predictor</title>
</head>
<body>
    <h2>Stock ML Predictor</h2>
    <form method="POST">
        <label>Enter Stock Name:</label><br>
        <input type="text" name="stock_name"><br><br>
        <input type="submit" value="Predict">
    </form>

    {% if result %}
        <h3>Stock: {{ stock }}</h3>
        <p>Average Price: {{ avg }}</p>
        <p>Closing Price: {{ close }}</p>
        <p>PnL %: {{ pnl }}</p>
        <p>Volatility: {{ vol }}</p>
        <h3>Prediction: {{ result }}</h3>
    {% endif %}

    {% if error %}
        <p style="color:red;">Error: {{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    stock = None
    avg = None
    close = None
    pnl = None
    vol = None

    if request.method == "POST":
        try:
            stock = request.form["stock_name"].upper()

            stock_row = df[df["name"] == stock]

            if stock_row.empty:
                raise ValueError("Stock not found!")

            avg = float(stock_row["average_price"].values[0])
            close = float(stock_row["closing_price"].values[0])

            # Calculate telemetry
            pnl = ((close - avg) / avg) * 100
            price_vs_avg = close - avg

            # Simple volatility using full dataset
            df["volatility"] = df["closing_price"].pct_change().rolling(2).std()
            vol = float(df["volatility"].iloc[-1])

            input_data = [[pnl, vol, price_vs_avg]]
            prediction = int(model.predict(input_data)[0])

            label_map = {
                2: "SELL",
                1: "HOLD (PROFIT)",
                0: "HOLD",
                -1: "STOP LOSS"
            }

            result = label_map.get(prediction, "UNKNOWN")

        except Exception as e:
            error = str(e)

    return render_template_string(
        HTML_PAGE,
        result=result,
        error=error,
        stock=stock,
        avg=avg,
        close=close,
        pnl=round(pnl, 2) if pnl else None,
        vol=round(vol, 5) if vol else None,
    )


if __name__ == "__main__":
    app.run(debug=True)
