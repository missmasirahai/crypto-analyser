import os
import json
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from crypto import get_coin_price, get_price_history, calculate_indicators, get_top_coins
from analyst import analyse_coin, get_market_sentiment

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)
CORS(app)

COIN_NAMES = {
    "bitcoin": "Bitcoin", "ethereum": "Ethereum",
    "binancecoin": "BNB", "solana": "Solana",
    "ripple": "XRP", "cardano": "Cardano",
    "dogecoin": "Dogecoin", "polkadot": "Polkadot",
    "litecoin": "Litecoin", "chainlink": "Chainlink"
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Crypto Analyser API is running!"})


@app.route("/top-coins", methods=["GET"])
def top_coins():
    try:
        coins = get_top_coins()
        sentiment = {}
        if coins:
            try:
                sentiment = get_market_sentiment(coins)
            except Exception as se:
                print(f"Sentiment error: {se}")
                sentiment = {
                    "overall_sentiment": "Neutral",
                    "market_mood": "Neutral",
                    "summary": "Market data loaded successfully.",
                    "advice": "Always do your own research."
                }
        return jsonify({"success": True, "coins": coins, "sentiment": sentiment})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyse/<coin_id>", methods=["GET"])
def analyse(coin_id):
    try:
        coin_name = COIN_NAMES.get(coin_id, coin_id.title())
        price_data = get_coin_price(coin_id)
        if not price_data:
            return jsonify({"error": "Could not fetch price data. Try again."}), 404

        history = get_price_history(coin_id, days=30)
        indicators = calculate_indicators(history) if history else {}
        analysis = analyse_coin(coin_id, coin_name, price_data, indicators)

        return jsonify({
            "success": True,
            "coin_id": coin_id,
            "coin_name": coin_name,
            "price_data": price_data,
            "indicators": indicators,
            "history": history,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/price-history/<coin_id>", methods=["GET"])
def price_history(coin_id):
    try:
        days = request.args.get("days", 30, type=int)
        history = get_price_history(coin_id, days=days)
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)