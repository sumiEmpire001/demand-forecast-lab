# Demand Forecast Lab

A Python standard-library CLI for forecasting daily demand using a recursive moving average. It also evaluates historical one-step predictions using mean absolute error (MAE). Validates nonnegative numeric demand and consecutive daily dates.

## Run

```bash
python forecast.py examples/demand.csv --window 3 --days 7
python forecast.py examples/demand.csv --window 5 --days 14 --output forecast.json
```

Input CSV columns: `date,units`, with one row per consecutive calendar day. A forecast horizon of 1–365 days is supported.

## Tests

```bash
python -m unittest discover -s tests -v
```

Eight tests run on Python 3.10, 3.12 and 3.13 through GitHub Actions.

## Limitations

This baseline is not a trained machine learning model. Recursive predictions may smooth away seasonality and trends. Backtest MAE measures historical error but does not provide a probabilistic prediction interval. Do not use forecasts alone for inventory purchasing decisions.
