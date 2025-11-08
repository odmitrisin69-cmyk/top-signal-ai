from flask import Flask, jsonify, render_template
import random
import datetime

app = Flask(__name__)

# --- Валютні пари для аналізу ---
pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "EURJPY"]

# --- Генератор випадкових сигналів (імітація роботи AI) ---
def generate_signals():
    signals = []
    for pair in pairs:
        signal_type = random.choice(["BUY", "SELL", "HOLD"])
        confidence = round(random.uniform(52, 80), 1)
        signals.append({
            "pair": pair,
            "signal": signal_type,
            "confidence": confidence,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
    return signals


# --- Головна сторінка (інтерфейс) ---
@app.route('/')
def home():
    return render_template('index.html')


# --- API для отримання сигналів ---
@app.route('/signals')
def get_signals():
    data = generate_signals()
    return jsonify(data)


# --- Запуск Flask сервера ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
