import requests
import pandas as pd
import time

headers = {"x-cg-demo-api-key": "CG-fJHx5DKnMSNeyBfFWPGbQgHD"}


url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1
}
response = requests.get(url, params=params, headers=headers)
markets = response.json()

coins = [coin["id"] for coin in markets]
print("Монет найдено:", len(coins))


all_data = []

for coin in coins:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 120,
        "interval": "daily"
    }
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["coin"] = coin
        df = df[["date", "coin", "price"]]
        all_data.append(df)
        print(f"OK: {coin}")
    else:
        print(f"SKIP: {coin} — статус {response.status_code}")
    
    time.sleep(1.5)

final_df = pd.concat(all_data)
final_df.to_csv("crypto_top50.csv", index=False)
print("Готово! Строк:", len(final_df))
