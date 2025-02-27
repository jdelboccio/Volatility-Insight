from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Volatility Insight API!"})

@app.route('/analyze', methods=['GET'])
def analyze_stock():
    ticker = request.args.get('ticker', 'AAPL')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        stock_data = yf.download(ticker, start=start_date)
        stock_data['Returns'] = stock_data['Adj Close'].pct_change()
        volatility = stock_data['Returns'].std() * np.sqrt(252)  # Annualized volatility

        return jsonify({
            "ticker": ticker,
            "volatility": round(volatility, 4),
            "message": "Analysis complete!"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
