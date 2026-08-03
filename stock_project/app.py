from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

# -------------------------------
# YOUR FUNCTIONS (unchanged logic)
# -------------------------------

def linear_regression(prices):
    n = len(prices)
    xs = np.arange(n, dtype=float)
    ys = np.array(prices, dtype=float)

    m = (n * np.sum(xs * ys) - np.sum(xs) * np.sum(ys)) / \
        (n * np.sum(xs**2) - np.sum(xs)**2)
    b = (np.sum(ys) - m * np.sum(xs)) / n

    y_pred = m * xs + b
    ss_res = np.sum((ys - y_pred) ** 2)
    ss_tot = np.sum((ys - np.mean(ys)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

    return m, b, r2


def predict_next_price(prices, m, b):
    return m * len(prices) + b


def make_decision(current, predicted, slope, r2):
    change = predicted - current
    change_pct = (change / current) * 100
    confidence = min(100, round(r2 * 100))
    trend = "Increasing 📈" if slope > 0 else "Decreasing 📉"

    if slope > 0 and change > 0:
        decision = "INVEST"
        reason = f"Upward trend (confidence {confidence}%)"
    else:
        decision = "DO NOT INVEST"
        reason = f"Weak or downward trend (confidence {confidence}%)"

    return decision, reason, change, change_pct, trend, confidence


# -------------------------------
# FLASK ROUTES
# -------------------------------

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    # Get input from HTML
    prices = [float(x) for x in request.form['prices'].split(",")]

    # Use YOUR logic
    m, b, r2 = linear_regression(prices)
    predicted = predict_next_price(prices, m, b)

    current = prices[-1]

    decision, reason, change, change_pct, trend, confidence = \
        make_decision(current, predicted, m, r2)

    # Send results to HTML
    return render_template(
        "index.html",
        prices=prices,
        prediction=round(predicted, 2),
        current=current,
        change=round(change, 2),
        change_pct=round(change_pct, 2),
        trend=trend,
        confidence=confidence,
        decision=decision,
        reason=reason
    )


# -------------------------------
# RUN APP
# -------------------------------
import webbrowser
import threading

if __name__ == "__main__":
    threading.Timer (1, lambda:webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(debug=True, use_reloader=False)