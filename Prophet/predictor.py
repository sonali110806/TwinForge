import pandas as pd

def simple_prediction(df):
    # Simple fallback prediction (no ML dependency issues)
    last_value = df['y'].iloc[-1]
    predictions = []

    for i in range(5):
        last_value += 5  # simulate increase
        predictions.append(last_value)

    return predictions


def run_prediction(file_path="data.csv"):
    # Load data
    df = pd.read_csv(file_path)

    # Fix datetime
    df['ds'] = pd.to_datetime(df['ds'])

    try:
        # Try Prophet
        from prophet import Prophet

        model = Prophet()
        model.fit(df)

        future = model.make_future_dataframe(periods=5, freq='min')
        forecast = model.predict(future)

        result = forecast[['ds', 'yhat']].tail(5)

        values = result['yhat'].tolist()

    except Exception as e:
        # Fallback if Prophet fails
        print("⚠️ Prophet failed, using simple prediction")
        values = simple_prediction(df)

        future_times = pd.date_range(start=df['ds'].iloc[-1], periods=5, freq='min')
        result = pd.DataFrame({
            'ds': future_times,
            'yhat': values
        })

    # Risk detection
    threshold = 85
    risk = any(v > threshold for v in values)

    output = {
        "prediction": result.to_dict(orient="records"),
        "risk": "HIGH CPU SPIKE LIKELY" if risk else "SYSTEM STABLE"
    }

    return output


if __name__ == "__main__":
    result = run_prediction()

    print("\nPredictions:")
    for row in result["prediction"]:
        print(row)

    print("\nStatus:", result["risk"])
