#!/bin/bash

touch D_data.csv
touch G_data.csv

echo "[starter]
ID = 813286
[credentials]
bearer_token1 = AAAAAAAAAAAAAAAAAAAAA
bearer_token2 = AAAAAAAAAAAAAAAAAAAAA
bearer_token3 = AAAAAAAAAAAAAAAAAAAAA
bearer_token4 = AAAAAAAAAAAAAAAAAAAAA" > numbers.ini

python3 followingScrape.py

