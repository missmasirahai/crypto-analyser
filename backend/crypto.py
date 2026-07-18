import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings()

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

session = requests.Session()
session.verify = False
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "accept": "application/json"
})

SUPPORTED_COINS = {
    "bitcoin": {"name": "Bitcoin", "symbol": "BTC"},
    "ethereum": {"name": "Ethereum", "symbol": "ETH"},
    "binancecoin": {"name": "BNB", "symbol": "BNB"},
    "solana": {"name": "Solana", "symbol": "SOL"},
    "ripple": {"name": "XRP", "symbol": "XRP"},
    "cardano": {"name": "Cardano", "symbol": "ADA"},
    "dogecoin": {"name": "Dogecoin", "symbol": "DOGE"},
    "polkadot": {"name": "Polkadot", "symbol": "DOT"},
    "litecoin": {"name": "Litecoin", "symbol": "LTC"},
    "chainlink": {"name": "Chainlink", "symbol": "LINK"}
}


def get_coin_price(coin_id):
    try:
        url = f"{COINGECKO_BASE}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        response = session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                coin = data[coin_id]
                return {
                    "price": coin.get("usd", 0),
                    "change_24h": round(coin.get("usd_24h_change", 0), 2),
                    "volume_24h": coin.get("usd_24h_vol", 0),
                    "market_cap": coin.get("usd_market_cap", 0)
                }
    except Exception as e:
        print(f"Price fetch error: {e}")
    return None


def get_price_history(coin_id, days=30):
    try:
        url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        response = session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            prices = data.get("prices", [])

            formatted = []
            for p in prices:
                timestamp = p[0]
                price = p[1]
                date = datetime.fromtimestamp(
                    timestamp / 1000).strftime("%Y-%m-%d")
                formatted.append({"date": date, "price": round(price, 2)})

            return formatted
    except Exception as e:
        print(f"History fetch error: {e}")
    return []


def calculate_indicators(price_history):
    if len(price_history) < 14:
        return {}

    prices = [p["price"] for p in price_history]

    # Moving averages
    ma7 = round(sum(prices[-7:]) / 7, 2) if len(prices) >= 7 else None
    ma14 = round(sum(prices[-14:]) / 14, 2) if len(prices) >= 14 else None
    ma30 = round(sum(prices[-30:]) / 30, 2) if len(prices) >= 30 else None

    # Price change %
    if len(prices) >= 2:
        change_7d = round(((prices[-1] - prices[-7]) / prices[-7]) * 100, 2) if len(prices) >= 7 else None
        change_30d = round(((prices[-1] - prices[-30]) / prices[-30]) * 100, 2) if len(prices) >= 30 else None
    else:
        change_7d = None
        change_30d = None

    # RSI calculation
    rsi = calculate_rsi(prices)

    # Trend direction
    if ma7 and ma14:
        trend = "Uptrend" if ma7 > ma14 else "Downtrend"
    else:
        trend = "Unknown"

    return {
        "ma7": ma7,
        "ma14": ma14,
        "ma30": ma30,
        "change_7d": change_7d,
        "change_30d": change_30d,
        "rsi": rsi,
        "trend": trend,
        "current_price": prices[-1] if prices else None,
        "highest_30d": round(max(prices[-30:]), 2) if len(prices) >= 30 else None,
        "lowest_30d": round(min(prices[-30:]), 2) if len(prices) >= 30 else None
    }


def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, period + 1):
        change = prices[-period + i] - prices[-period + i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = round(100 - (100 / (1 + rs)), 2)
    return rsi


def get_top_coins():
    try:
        url = f"{COINGECKO_BASE}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "24h"
        }
        response = session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            coins = response.json()
            result = []
            for c in coins:
                result.append({
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "symbol": c.get("symbol", "").upper(),
                    "price": c.get("current_price", 0),
                    "change_24h": round(c.get("price_change_percentage_24h", 0) or 0, 2),
                    "market_cap": c.get("market_cap", 0),
                    "image": c.get("image", "")
                })
            return result
    except Exception as e:
        print(f"Top coins error: {e}")
    return []