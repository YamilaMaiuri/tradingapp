from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

PRECIOS_MOCK = {
    "YPF":  {"base": 1284.50, "variacion_pct": 2.3},
    "AL30": {"base": 62.15,   "variacion_pct": -1.1},
    "GGAL": {"base": 935.00,  "variacion_pct": 0.8},
    "USD":  {"base": 1042.00, "variacion_pct": 0.0},
}

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
ORDERS_FILE    = DATA_DIR / "orders.json"
RULES_FILE     = DATA_DIR / "business_rules.json"


def init_data_files():
    if not PORTFOLIO_FILE.exists():
        default_portfolio = {
            "cash_ars": 5000000.00,
            "cash_usd": 10000.00,
            "posiciones": [
                {"activo": "YPF",  "cantidad": 10000, "precio_promedio": 1250.00, "mercado": "BYMA"},
                {"activo": "AL30", "cantidad": 50000, "precio_promedio": 63.50,   "mercado": "BYMA"},
                {"activo": "GGAL", "cantidad": 5000,  "precio_promedio": 910.00,  "mercado": "BYMA"}
            ],
            "limite_perdida_diaria": 2000000,
            "perdida_acumulada_hoy": 87500,
            "last_updated": datetime.now().isoformat()
        }
        with open(PORTFOLIO_FILE, 'w') as f:
            json.dump(default_portfolio, f, indent=2)

    if not ORDERS_FILE.exists():
        with open(ORDERS_FILE, 'w') as f:
            json.dump({"orders": []}, f, indent=2)

    if not RULES_FILE.exists():
        _write_default_rules()


def _write_default_rules():
    default_rules = {
        "reglas": [
            {
                "id": "R001",
                "nombre": "Arbitraje BYMA-A3",
                "condicion": "Spread entre BYMA y A3 supera 0.5% en cualquier activo",
                "accion": "Comprar en el mercado más barato y vender en el más caro",
                "parametros": {
                    "umbral_spread_pct": 0.5,
                    "activo": "GGAL"
                },
                "activa": True,
                "prioridad": 1,
                "ejecuciones": 0
            },
            {
                "id": "R002",
                "nombre": "Stop Loss",
                "condicion": "Cualquier activo baja más del 1%",
                "accion": "Vender 30% de la posición en ese activo",
                "parametros": {
                    "umbral_pct": -1.0,
                    "porcentaje_venta": 30
                },
                "activa": True,
                "prioridad": 2,
                "ejecuciones": 0
            },
            {
                "id": "R003",
                "nombre": "Momentum alcista",
                "condicion": "Cualquier activo sube más del 2%",
                "accion": "Evaluar compra del activo correlacionado",
                "parametros": {
                    "umbral_pct": 2.0,
                    "activo_trigger": "YPF",
                    "activo_accion": "GGAL"
                },
                "activa": True,
                "prioridad": 3,
                "ejecuciones": 0
            }
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


# ──────────────────────────────────────────────
# SYSTEM
# ──────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Trading Agent API - ICBC',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/reset_rules', methods=['GET'])
def reset_rules():
    """Resetea las reglas de negocio al estado inicial. Útil para demo."""
    if RULES_FILE.exists():
        RULES_FILE.unlink()
    _write_default_rules()
    return jsonify({'success': True, 'message': 'Reglas reseteadas correctamente'})


@app.route('/api/reset_portfolio', methods=['GET'])
def reset_portfolio():
    """Resetea el portfolio al estado inicial. Útil para demo."""
    if PORTFOLIO_FILE.exists():
        PORTFOLIO_FILE.unlink()
    if ORDERS_FILE.exists():
        ORDERS_FILE.unlink()
    init_data_files()
    return jsonify({'success': True, 'message': 'Portfolio y órdenes reseteados correctamente'})


# ──────────────────────────────────────────────
# MARKET DATA
# ──────────────────────────────────────────────

@app.route('/api/get_market_prices', methods=['POST'])
def get_market_prices():
    data = request.get_json()
    activos = data.get('activos', list(PRECIOS_MOCK.keys()))
    precios = {}

    for activo in activos:
        if activo in PRECIOS_MOCK:
            base = PRECIOS_MOCK[activo]["base"]
            var  = PRECIOS_MOCK[activo]["variacion_pct"]
            precio_a3 = round(base * 1.005, 2)
            spread_pct = round((precio_a3 - base) / base * 100, 3)
            precios[activo] = {
                "precio": base,
                "variacion_pct": var,
                "mercado": "BYMA",
                "precio_a3": precio_a3,
                "spread_pct": spread_pct,
                "volumen": 1500000,
                "apertura": round(base * 0.98, 2),
                "maximo": round(base * 1.025, 2),
                "minimo": round(base * 0.975, 2),
                "BYMA": {"bid": base, "ask": round(base * 1.001, 2), "last": base},
                "A3":   {"bid": precio_a3, "ask": round(base * 1.006, 2), "last": precio_a3}
            }

    return jsonify({"precios": precios, "timestamp": datetime.now().isoformat()})


# ──────────────────────────────────────────────
# PORTFOLIO
# ──────────────────────────────────────────────

@app.route('/api/get_portfolio_state', methods=['GET'])
def get_portfolio_state():
    portfolio = load_json(PORTFOLIO_FILE)

    # Enriquecer con valores actuales
    valor_posiciones = 0
    for pos in portfolio.get("posiciones", []):
        activo = pos["activo"]
        precio_actual = PRECIOS_MOCK.get(activo, {}).get("base", pos["precio_promedio"])
        pos["precio_actual"]    = precio_actual
        pos["valor_actual"]     = round(precio_actual * pos["cantidad"], 2)
        pos["ganancia_perdida"] = round((precio_actual - pos["precio_promedio"]) * pos["cantidad"], 2)
        pos["ganancia_pct"]     = round((precio_actual - pos["precio_promedio"]) / pos["precio_promedio"] * 100, 2)
        valor_posiciones += pos["valor_actual"]

    valor_total = round(valor_posiciones + portfolio["cash_ars"], 2)
    portfolio["valor_total_posiciones"] = round(valor_posiciones, 2)
    portfolio["valor_total_portfolio"]  = valor_total
    portfolio["exposicion_pct"]         = round(valor_posiciones / valor_total * 100, 2) if valor_total > 0 else 0
    portfolio["timestamp"]              = datetime.now().isoformat()

    return jsonify(portfolio)


# ──────────────────────────────────────────────
# RULES
# ──────────────────────────────────────────────

@app.route('/api/get_business_rules', methods=['GET'])
def get_business_rules():
    rules_data = load_json(RULES_FILE)
    reglas_activas = sum(1 for r in rules_data["reglas"] if r.get("activa"))
    return jsonify({
        **rules_data,
        "total_reglas": len(rules_data["reglas"]),
        "reglas_activas": reglas_activas,
        "timestamp": datetime.now().isoformat()
    })


# ──────────────────────────────────────────────
# ORDERS
# ──────────────────────────────────────────────

@app.route('/api/execute_order', methods=['POST'])
def execute_order():
    data = request.get_json()

    required = ["activo", "tipo", "cantidad", "mercado", "regla_origen"]
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo requerido faltante: {field}'}), 400

    activo   = data["activo"]
    tipo     = data["tipo"].upper()
    cantidad = float(data["cantidad"])
    mercado  = data["mercado"]

    precio = PRECIOS_MOCK.get(activo, {}).get("base", 100.0)
    if mercado == "A3":
        precio = round(precio * 1.005, 2)

    portfolio   = load_json(PORTFOLIO_FILE)
    orders_data = load_json(ORDERS_FILE)
    order_id    = f"ORD-{len(orders_data['orders']) + 1:05d}"
    monto_total = round(precio * cantidad, 2)

    if tipo == "COMPRA":
        if portfolio["cash_ars"] < monto_total:
            return jsonify({'error': f'Fondos insuficientes. Requerido: ${monto_total:,.2f} | Disponible: ${portfolio["cash_ars"]:,.2f}'}), 400
        portfolio["cash_ars"] -= monto_total
        portfolio["posiciones"].append({
            "activo": activo,
            "cantidad": cantidad,
            "precio_promedio": precio,
            "mercado": mercado
        })

    elif tipo == "VENTA":
        posicion = next((p for p in portfolio["posiciones"] if p["activo"] == activo), None)
        if not posicion:
            return jsonify({'error': f'No se encontró posición en {activo}'}), 400
        if posicion["cantidad"] < cantidad:
            return jsonify({'error': f'Cantidad insuficiente. Disponible: {posicion["cantidad"]}'}), 400
        posicion["cantidad"] -= cantidad
        portfolio["cash_ars"] += monto_total
        if posicion["cantidad"] == 0:
            portfolio["posiciones"] = [p for p in portfolio["posiciones"] if p["activo"] != activo]

    portfolio["last_updated"] = datetime.now().isoformat()
    save_json(PORTFOLIO_FILE, portfolio)

    order_record = {
        "order_id":       order_id,
        "activo":         activo,
        "tipo":           tipo,
        "cantidad":       cantidad,
        "precio_ejecutado": precio,
        "monto_total":    monto_total,
        "mercado":        mercado,
        "regla_origen":   data.get("regla_origen", "MANUAL"),
        "estado":         "EJECUTADA",
        "timestamp":      datetime.now().isoformat()
    }
    orders_data["orders"].append(order_record)
    save_json(ORDERS_FILE, orders_data)

    return jsonify({'success': True, **order_record})


if __name__ == '__main__':
    print("🚀 Trading API Started — ICBC Demo")
    print(f"📊 Activos: {', '.join(PRECIOS_MOCK.keys())}")
    app.run(host='0.0.0.0', port=8080, debug=False)
