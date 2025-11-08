from flask import Flask, jsonify
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

app = Flask(__name__)

pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "EURGBP=X", "USDCAD=X"]

def get_features(pair):
    df = yf.download(pair, period="1mo", interval="1h")
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean()))
    df.dropna(inplace=True)
    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    X = df[['MA5', 'MA20', 'RSI']]
    y = df['Target']
    return X, y, df

def get_signal(pair):
    X, y, df = get_features(pair)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X_train)
    model = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
    model.fit(Xs, y_train)
    last = scaler.transform([X.iloc[-1]])
    prob = model.predict_proba(last)[0][1]
    if prob > 0.6:
        signal = "BUY"
    elif prob < 0.4:
        signal = "SELL"
    else:
        signal = "HOLD"
    return {"pair": pair, "signal": signal, "confidence": round(prob*100, 2)}

@app.route('/')
def home():
    return jsonify({"status": "TopSecret AI running", "pairs": pairs})

@app.route('/signals')
def signals():
    results = [get_signal(pair) for pair in pairs]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
