var outputCollection = "stock_exchange_data_processed";

db[outputCollection].drop();
db.createCollection(outputCollection, {
    // timeseries: {
    //     timeField: "ts",
    //     metaField: "source",
    //     granularity: "hours"
    // }
});

var rolling = {
    $setWindowFields: {
        partitionBy: "$source",
        sortBy: { ts: 1 },
        output: {
            "window.rollingCloseUSD": {
                $avg: "$closeUSD",
                window: {
                    documents: [-5, 0]
                }
            },
            "window.dailyDifference": {
                $derivative: {
                    input: "$closeUSD",
                    unit: "day"
                },
                window: {
                    documents: [-1, 0]
                }
            },
        }
    }
};

var rollingDiff = {
    "$setWindowFields": {
        partitionBy: "$source",
        sortBy: { ts: 1 },
        output: {
            "window.dailyDifferenceRolling": {
                $avg: "$window.dailyDifference",
                window: {
                    documents: [-10, 0]
                }
            }
        }
    }
}

var merge = {
    $merge: {
        //on: "_id",
        whenMatched: "replace"
    }
};
merge["$merge"]["into"] = outputCollection;

var out = {};
out["$out"] = outputCollection;

var pipeline = [rolling, rollingDiff, merge];

console.log(pipeline);

db.stock_exchange_data.aggregate(pipeline, { allowDiskUse: true });