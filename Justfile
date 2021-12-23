all: convert init import

convert:
    ./scripts/convert.py data/indexProcessed.csv indexProcessed.json

init:
    mongosh $MDB_URI scripts/init_database.js

import:
    mongoimport --uri $MDB_URI indexProcessed.json --collection stock_exchange_data

process:
    mongosh $MDB_URI scripts/window_functions.js

connect:
    mongosh $MDB_URI

clean:
    rm -f indexProcessed.json