from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load cleaned dataset
df = pd.read_csv("retail_store_inventory.csv")


@app.route("/", methods=["GET", "POST"])
def home():

    products = sorted(df["Product ID"].unique())

    recommendation = None
    current_stock = None
    forecast_demand = None
    stock_status = None

    if request.method == "POST":

        product_id = request.form["product"]

        # Get the latest record for the selected product
        product_data = df[df["Product ID"] == product_id].sort_values("Date").iloc[-1]

        current_stock = product_data["Inventory Level"]
        forecast_demand = product_data["Demand Forecast"]

        # Recommendation logic
        if current_stock < forecast_demand:
            stock_status = "Low Stock"
            reorder_quantity = round(forecast_demand - current_stock)
            recommendation = f"REORDER {reorder_quantity} UNITS"

        elif current_stock > forecast_demand * 1.5:
            stock_status = "Overstock"
            recommendation = "DO NOT REORDER"

        else:
            stock_status = "Healthy Stock"
            recommendation = "NO REORDER NEEDED"

    return render_template(
        "index.html",
        products=products,
        current_stock=current_stock,
        forecast_demand=forecast_demand,
        stock_status=stock_status,
        recommendation=recommendation
    )


if __name__ == "__main__":
    app.run(debug=True)