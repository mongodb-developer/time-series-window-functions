db.stock_exchange_data.drop();

db.createCollection("stock_exchange_data", {
    timeseries: {
        timeField: "ts",
        metaField: "source",
        granularity: "hours"
    }
});

db.stock_exchange_data.createIndex({ "source": 1, "ts": 1 });