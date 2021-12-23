#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import os, sys, csv, json

{
    "Index": "HSI",
    "Date": "1986-12-31",
    "Open": "2568.300049",
    "High": "2568.300049",
    "Low": "2568.300049",
    "Close": "2568.300049",
    "Adj Close": "2568.300049",
    "Volume": "0.0",
    "CloseUSD": "333.87900637",
}


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args(argv)

    index_data = {}

    with open("data/indexInfo.csv", "r", encoding="utf-8-sig") as input:
        csv_input = csv.DictReader(input)
        for row in csv_input:
            index_data[row["Index"]] = row

    with open(args.input, "r") as input, open(args.output, "w") as output:
        csv_input = csv.DictReader(input)
        for i in csv_input:
            dt = datetime.fromisoformat(i["Date"]).astimezone(timezone.utc)

            reshaped = {
                "source": index_data[i["Index"]],
                "ts": {
                    "$date": dt.isoformat(),
                },
                "open": {"$numberDecimal": i["Open"]},
                "high": {"$numberDecimal": i["High"]},
                "low": {"$numberDecimal": i["Low"]},
                "close": {"$numberDecimal": i["Close"]},
                "adjustedClose": {"$numberDecimal": i["Adj Close"]},
                "volume": {"$numberDecimal": i["Volume"]},
                "closeUSD": {"$numberDecimal": i["CloseUSD"]},
            }

            json.dump(reshaped, output)
            output.write("\n")


if __name__ == "__main__":
    main()