import os
import json
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found!")
else:
    print("✅ Gemini API key loaded!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def analyse_coin(coin_id, coin_name, price_data, indicators):
    prompt = f"""
You are a professional cryptocurrency market analyst with 10 years of experience.

Analyse the following market data for {coin_name} and provide a structured analysis.

Market Data:
- Current Price: ${price_data.get('price', 0):,.2f}
- 24h Change: {price_data.get('change_24h', 0)}%
- 24h Volume: ${price_data.get('volume_24h', 0):,.0f}
- Market Cap: ${price_data.get('market_cap', 0):,.0f}

Technical Indicators:
- 7-Day Moving Average: ${indicators.get('ma7', 'N/A')}
- 14-Day Moving Average: ${indicators.get('ma14', 'N/A')}
- 30-Day Moving Average: ${indicators.get('ma30', 'N/A')}
- RSI (14): {indicators.get('rsi', 'N/A')}
- 7-Day Change: {indicators.get('change_7d', 'N/A')}%
- 30-Day Change: {indicators.get('change_30d', 'N/A')}%
- Current Trend: {indicators.get('trend', 'N/A')}
- 30-Day High: ${indicators.get('highest_30d', 'N/A')}
- 30-Day Low: ${indicators.get('lowest_30d', 'N/A')}

Return ONLY this JSON format. No markdown. No backticks. No explanation.

{{
  "signal": "Bullish / Bearish / Neutral",
  "confidence": "High / Medium / Low",
  "signal_strength": 75,
  "summary": "2-3 sentence plain English market summary",
  "price_analysis": "2-3 sentences about current price action",
  "rsi_analysis": "1-2 sentences interpreting the RSI value",
  "trend_analysis": "1-2 sentences about the trend",
  "key_levels": {{
    "support": "Key support price level",
    "resistance": "Key resistance price level"
  }},
  "short_term_outlook": "1-2 sentences about next 7 days",
  "risk_factors": [
    "Risk factor 1",
    "Risk factor 2",
    "Risk factor 3"
  ],
  "opportunities": [
    "Opportunity 1",
    "Opportunity 2"
  ],
  "disclaimer": "This is not financial advice. Always do your own research."
}}

Important: RSI above 70 means overbought, below 30 means oversold.
Be honest and balanced. This is educational only, not financial advice.
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw = "\n".join(lines).strip()

    return json.loads(raw)


def get_market_sentiment(top_coins):
    gainers = [c for c in top_coins if c.get("change_24h", 0) > 0]
    losers = [c for c in top_coins if c.get("change_24h", 0) < 0]

    avg_change = sum(c.get("change_24h", 0)
                     for c in top_coins) / len(top_coins) if top_coins else 0

    prompt = f"""
You are a crypto market analyst. Based on this market data give a brief sentiment analysis.

Top 10 coins summary:
- Gainers: {len(gainers)} out of {len(top_coins)}
- Losers: {len(losers)} out of {len(top_coins)}
- Average 24h change: {round(avg_change, 2)}%
- Top gainer: {max(top_coins, key=lambda x: x.get('change_24h', 0)).get('name', 'N/A') if top_coins else 'N/A'}
- Top loser: {min(top_coins, key=lambda x: x.get('change_24h', 0)).get('name', 'N/A') if top_coins else 'N/A'}

Return ONLY this JSON. No markdown. No backticks.

{{
  "overall_sentiment": "Bullish / Bearish / Neutral / Mixed",
  "market_mood": "Greedy / Fearful / Neutral / Excited",
  "summary": "2 sentences describing today market in plain English",
  "advice": "1 sentence general market advice"
}}
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw = "\n".join(lines).strip()

    return json.loads(raw)