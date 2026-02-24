from flask import Flask, request, render_template_string
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load model and stock data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_FOLDER = os.path.join(BASE_DIR, "..", "models")
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "stocks.csv")
# load stock data
df=pd.read_csv(DATA_PATH)

def get_available_models():
    return [f for f in os.listdir(MODEL_FOLDER) if f.endswith(".pkl")]

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Predictor</title>
</head>
<body>
    <h2>Stock ML Predictor</h2>
    <form method="POST">
        <label>Select Model:</label><br>
        <select name="model_name" required>
            <option value="">-- Select Model --</option>
            {% for model in models %}
                <option value="{{ model }}">{{ model }}</option>
            {% endfor %}
        </select><br><br>

        <label>Enter Stock Name:</label><br>
        <input type="text" name="stock_name" required><br><br>

        <input type="submit" value="Predict">
    </form>

    {% if result %}
        <h3>Using Model: {{ selected_model }}</h3>
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
    selected_model=None

    models=get_available_models()

    if request.method == "POST":
        try:
            selected_model = request.form["model_name"]
            stock = request.form["stock_name"].upper()
             
            model_path = os.path.join(MODEL_FOLDER, selected_model)
            model = joblib.load(model_path)

            stock_row = df[df["name"] == stock]

            if stock_row.empty:
                raise ValueError("Stock not found!")

            avg = float(stock_row["avg_price"].values[0])
            close = float(stock_row["current_price"].values[0])

            # Calculate telemetry
            pnl = ((close - avg) / avg) * 100
            price_vs_avg = close - avg

            # Simple volatility using full dataset
            df["volatility"] = df["current_price"].pct_change().rolling(2).std()
            vol = float(df["volatility"].iloc[-1])

            input_data = [[pnl, vol, price_vs_avg,avg,close]]
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
        models=models,
        result=result,
        error=error,
        stock=stock,
        avg=avg,
        close=close,
        pnl=round(pnl, 2) if pnl else None,
        vol=round(vol, 5) if vol else None,
        selected_model=selected_model
    )


if __name__ == "__main__":
    app.run(debug=True)
