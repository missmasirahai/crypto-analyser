# ₿ CryptoAI — AI Cryptocurrency Market Analyser

An AI-powered cryptocurrency analysis dashboard that fetches live market data, calculates technical indicators, and provides Gemini AI-generated market commentary with Bull/Bear signals.

## 🌐 Live Demo
👉 [crypto-analyser-nine.vercel.app](https://crypto-analyser-nine.vercel.app)

---

## ✨ Features

- **📊 Live Market Overview** — Real-time prices for top 10 cryptocurrencies
- **🤖 AI Market Sentiment** — Gemini AI analyses overall market mood
- **📈 AI Signal** — Bullish / Bearish / Neutral with confidence level
- **💪 Signal Strength** — Score out of 100
- **📉 Interactive Price Chart** — 7D and 30D toggle with Chart.js
- **📊 Technical Indicators** — MA7, MA14, MA30, RSI, trend direction
- **🎯 Key Levels** — AI-identified support and resistance levels
- **⚠️ Risk Factors** — What could go wrong
- **💡 Opportunities** — What to watch for
- **🔮 Short Term Outlook** — Next 7 days prediction
- **Real Coin Logos** — Live images from CoinGecko

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Backend web server |
| Flask-CORS | Cross-origin request handling |
| Google Gemini API | AI market analysis and sentiment |
| CoinGecko API | Live cryptocurrency market data |
| Chart.js | Interactive price charts |
| HTML/CSS/JavaScript | Dark professional frontend |
| Render | Backend deployment |
| Vercel | Frontend deployment |

---

## 📁 Project Structure

```
crypto-analyser/
├── backend/
│   ├── app.py          # Flask server with API routes
│   ├── crypto.py       # CoinGecko API integration + indicators
│   ├── analyst.py      # Gemini AI market analysis
│   └── .env            # Secret API keys (not on GitHub)
├── frontend/
│   ├── index.html      # Main dashboard interface
│   └── style.css       # Dark crypto-themed design
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes .env and cache
└── README.md           # Project documentation
```

---

## 🚀 How to Run Locally

### Step 1 — Clone the repository
```bash
git clone https://github.com/missmasirahai/crypto-analyser.git
cd crypto-analyser
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Add your API keys
Create a `.env` file inside the `backend` folder:
```
GEMINI_API_KEY=your-gemini-api-key-here
COINGECKO_API_KEY=your-coingecko-api-key-here
```

Get free keys at:
- Gemini: https://aistudio.google.com/apikey
- CoinGecko: https://www.coingecko.com/en/api

### Step 4 — Run the Flask server
```bash
cd backend
python app.py
```

### Step 5 — Open the frontend
Open `frontend/index.html` in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/top-coins` | Get top 10 coins with market sentiment |
| GET | `/analyse/<coin_id>` | Full AI analysis for a specific coin |
| GET | `/price-history/<coin_id>` | Price history for charting |

---

## 📊 Technical Indicators Explained

| Indicator | What it means |
|---|---|
| MA7 | Average price of last 7 days |
| MA14 | Average price of last 14 days |
| MA30 | Average price of last 30 days |
| RSI > 70 | Overbought — price may drop |
| RSI < 30 | Oversold — price may rise |
| RSI 30-70 | Neutral zone |
| MA7 > MA14 | Uptrend signal |
| MA7 < MA14 | Downtrend signal |

---

## ⚠️ Disclaimer

This app is for educational purposes only. Nothing here is financial advice. Always do your own research before making any investment decisions.

---

## 🌍 Deployment

- **Backend:** Render free tier — `https://crypto-analyser-dwjd.onrender.com`
- **Frontend:** Vercel free tier — `https://crypto-analyser-nine.vercel.app`

---

## 👩‍💻 Author

**Masirah Saudagar**
- GitHub: [@missmasirahai](https://github.com/missmasirahai)
- LinkedIn: [masirah-saudagar](https://linkedin.com/in/masirah-saudagar-2980a93a1)
- B.Sc. Information Technology — University of Mumbai (CDOE)

---

## 📌 Part of LLM Project Hub

1. ✅ Movie Recommendation System
2. ✅ Podcast Summarization App
3. ✅ Contract & Legal Document Analyser
4. ✅ EDA using LLMs
5. ✅ Fake News Detection
6. ✅ Cryptocurrency Analysis ← This project
7. Stock Market Trend Prediction
