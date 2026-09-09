import os
from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP

app = Flask(__name__)

# Recuperació de claus des de les variables d'entorn de Render
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Client unificat de Bybit (entorn Demo / Testnet)
session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Validació del token de seguretat
    if not data or data.get('secret') != WEBHOOK_SECRET:
        return jsonify({"status": "error", "message": "No autoritzat"}), 401

    try:
        symbol = data.get('symbol', 'BTCUSDT')
        side = data.get('side', 'Buy')
        qty = data.get('qty', '0.002')
        tp = data.get('tp')
        sl = data.get('sl')

        # Execució de l'ordre a mercat
        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(qty),
            takeProfit=str(tp) if tp else None,
            stopLoss=str(sl) if sl else None,
            timeInForce="GTC"
        )
        return jsonify({"status": "success", "response": response}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)