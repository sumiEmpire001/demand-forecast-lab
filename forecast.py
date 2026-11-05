"""Simple moving-average demand forecasts and backtesting."""
import argparse
import csv
import datetime as dt
import json
import math


def load(path):
    with open(path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    result = []
    for row in rows:
        date = dt.date.fromisoformat(row["date"])
        units = float(row["units"])
        if not math.isfinite(units) or units < 0:
            raise ValueError("units must be finite and nonnegative")
        result.append((date, units))
    if len(set(day for day, _ in result)) != len(result):
        raise ValueError("duplicate date")
    result.sort()
    if any((b[0]-a[0]).days != 1 for a,b in zip(result,result[1:])):
        raise ValueError("daily data must have no gaps")
    return result


def moving_average(values, window):
    if not isinstance(window,int) or window<1:
        raise ValueError("window must be positive")
    if len(values)<window:
        raise ValueError("insufficient history")
    return sum(values[-window:])/window


def backtest(values, window):
    if len(values)<=window:
        raise ValueError("need more observations than window")
    predictions=[moving_average(values[:i],window) for i in range(window,len(values))]
    actual=values[window:]
    mae=sum(abs(a-p) for a,p in zip(actual,predictions))/len(actual)
    return {"evaluated_days":len(actual),"mae":round(mae,4)}


def forecast(series, window, days):
    if not isinstance(days,int) or days<1 or days>365:
        raise ValueError("days must be 1-365")
    values=[value for _,value in series]
    if not series:
        raise ValueError("empty series")
    future=[]
    for offset in range(1,days+1):
        prediction=moving_average(values,window)
        future.append({"date":(series[-1][0]+dt.timedelta(days=offset)).isoformat(),"units":round(prediction,3)})
        values.append(prediction)
    return {"window":window,"backtest":backtest([value for _,value in series],window) if len(series)>window else None,"forecast":future}


def main():
    parser=argparse.ArgumentParser(description="Forecast daily demand")
    parser.add_argument("csv_file")
    parser.add_argument("--window",type=int,default=3)
    parser.add_argument("--days",type=int,default=7)
    parser.add_argument("--output")
    args=parser.parse_args()
    report=json.dumps(forecast(load(args.csv_file),args.window,args.days),indent=2)
    if args.output:
        with open(args.output,"w",encoding="utf-8") as file:
            file.write(report+"\n")
    else:
        print(report)


if __name__=="__main__":
    main()
