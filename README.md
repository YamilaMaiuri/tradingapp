# Trading Agent API - ICBC Demo

API REST con 4 herramientas (tools) para agente de trading con watsonx.orchestrate.

## 🔧 Tools Disponibles

### 1. **execute_order** - Ejecutar Órdenes
Ejecuta órdenes de compra/venta y modifica el portfolio real.
- **Endpoint:** `POST /api/execute_order`
- **Persiste datos en:** `data/portfolio.json` y `data/orders.json`

### 2. **get_portfolio_state** - Estado de Cartera
Obtiene el estado actual del portfolio.
- **Endpoint:** `GET /api/get_portfolio_state`
- **Lee desde:** `data/portfolio.json`

### 3. **get_business_rules** - Reglas de Negocio
Obtiene las reglas de negocio activas.
- **Endpoint:** `GET /api/get_business_rules`
- **Lee desde:** `data/business_rules.json`

### 4. **get_market_prices** - Precios de Mercado
Obtiene precios de activos en BYMA y A3.
- **Endpoint:** `POST /api/get_market_prices`
- **Activos:** YPF, AL30, GGAL, USD

## 📊 Activos Soportados

```python
YPF:  $1284.50 (variación: +2.3%)
AL30: $62.15   (variación: -1.1%)
GGAL: $935.00  (variación: +0.8%)
USD:  $1042.00 (variación: 0.0%)
```

## 🚀 Deployment en Code Engine

### Archivos necesarios:
- `api_server.py` - Servidor Flask con las 4 tools
- `requirements_api.txt` - Dependencias Python
- `Dockerfile` - Configuración para Code Engine
- `openapi.yaml` - Especificación para watsonx.orchestrate

### Pasos:
1. Code Engine construye la imagen desde el Dockerfile
2. Expone la API en puerto 8080
3. Importar `openapi.yaml` en watsonx.orchestrate como Custom API

## 📁 Estructura

```
trading-demo/
├── api_server.py          # Servidor Flask con las 4 tools
├── requirements_api.txt   # Dependencias
├── Dockerfile            # Config para Code Engine
├── openapi.yaml          # Spec para watsonx.orchestrate
├── data/                 # Datos persistentes (JSON)
│   ├── portfolio.json
│   ├── orders.json
│   └── business_rules.json
└── README.md
```

## 🔗 Conexión con watsonx.orchestrate

1. Despliega en Code Engine
2. Obtén la URL pública
3. Actualiza `openapi.yaml` línea 11 con la URL
4. Importa en watsonx.orchestrate: Skills → Add skills → Custom API

## 💾 Persistencia de Datos

Las tools modifican archivos JSON reales en `data/`:
- Cada orden ejecutada modifica el portfolio
- Los cambios persisten entre llamadas
- Historial completo de órdenes

## 🧪 Prueba Local

```bash
pip install -r requirements_api.txt
python api_server.py
```

Luego:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/get_portfolio_state