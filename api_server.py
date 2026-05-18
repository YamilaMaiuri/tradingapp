from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Precios mock de activos argentinos
PRECIOS_MOCK = {
    "YPF":  {"base": 1284.50, "variacion_pct": 2.3},
    "AL30": {"base": 62.15,   "variacion_pct": -1.1},
    "GGAL": {"base": 935.00,  "variacion_pct": 0.8},
    "USD":  {"base": 1042.00, "variacion_pct": 0.0},
}

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
ORDERS_FILE = DATA_DIR / "orders.json"
RULES_FILE = DATA_DIR / "business_rules.json"

def init_data_files():
    if not PORTFOLIO_FILE.exists():
        default_portfolio = {
            "cash_ars": 150000.00,
            "cash_usd": 10000.00,
            "posiciones": [
                {"activo": "YPF", "cantidad": 100, "precio_promedio": 1284.50, "mercado": "BYMA"},
                {"activo": "AL30", "cantidad": 200, "precio_promedio": 62.15, "mercado": "BYMA"}
            ],
            "last_updated": datetime.now().isoformat()
        }
        with open(PORTFOLIO_FILE, 'w') as f:
            json.dump(default_portfolio, f, indent=2)
    
    if not ORDERS_FILE.exists():
        with open(ORDERS_FILE, 'w') as f:
            json.dump({"orders": []}, f, indent=2)
    
    if not RULES_FILE.exists():
        default_rules = {
            "reglas": [
                {"id": "R001", "nombre": "Arbitraje BYMA-A3", "activa": True, "ejecuciones": 0},
                {"id": "R002", "nombre": "Stop Loss", "activa": True, "ejecuciones": 0}
            ]
        }
        with open(RULES_FILE, 'w') as f:
            json.dump(default_rules, f, indent=2)

init_data_files()

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/execute_order', methods=['POST'])
def execute_order():
    data = request.get_json()
    portfolio = load_json(PORTFOLIO_FILE)
    orders_data = load_json(ORDERS_FILE)
    
    activo = data['activo']
    if activo in PRECIOS_MOCK:
        precio = PRECIOS_MOCK[activo]["base"]
    else:
        precio = 100.0
    
    order_id = f"ORD-{len(orders_data['orders']) + 1:05d}"
    
    if data['tipo'] == 'compra':
        costo = precio * data['cantidad']
        if portfolio['cash_ars'] >= costo:
            portfolio['cash_ars'] -= costo
            portfolio['posiciones'].append({
                'activo': data['activo'],
                'cantidad': data['cantidad'],
                'precio_promedio': precio,
                'mercado': data['mercado']
            })
        else:
            return jsonify({'error': 'Fondos insuficientes'}), 400
    
    portfolio['last_updated'] = datetime.now().isoformat()
    save_json(PORTFOLIO_FILE, portfolio)
    
    order_record = {
        'order_id': order_id,
        'activo': data['activo'],
        'tipo': data['tipo'],
        'cantidad': data['cantidad'],
        'precio_ejecutado': precio,
        'timestamp': datetime.now().isoformat()
    }
    orders_data['orders'].append(order_record)
    save_json(ORDERS_FILE, orders_data)
    
    return jsonify({'success': True, **order_record})

@app.route('/api/get_portfolio_state', methods=['GET'])
def get_portfolio_state():
    portfolio = load_json(PORTFOLIO_FILE)
    return jsonify(portfolio)

@app.route('/api/get_business_rules', methods=['GET'])
def get_business_rules():
    rules_data = load_json(RULES_FILE)
    return jsonify(rules_data)

@app.route('/api/get_market_prices', methods=['POST'])
def get_market_prices():
    data = request.get_json()
    activos = data.get('activos', list(PRECIOS_MOCK.keys()))
    precios = {}
    for activo in activos:
        if activo in PRECIOS_MOCK:
            base = PRECIOS_MOCK[activo]["base"]
            var  = PRECIOS_MOCK[activo]["variacion_pct"]
            precios[activo] = {
                "BYMA": {"bid": base, "ask": round(base * 1.001, 2), "last": base},
                "A3":   {"bid": round(base * 1.005, 2), "ask": round(base * 1.006, 2), "last": round(base * 1.005, 2)},
                "variacion_pct": var
            }
    return jsonify({"precios": precios, "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Trading API Started")
    print(f"📊 Activos disponibles: {', '.join(PRECIOS_MOCK.keys())}")
    app.run(host='0.0.0.0', port=8080, debug=False)
